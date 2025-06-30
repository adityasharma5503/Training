import pulumi

from pulumi import Config

import pulumi_kubernetes.core.v1 as kube
import pulumi_kubernetes.apps.v1 as apps
import pulumi_kubernetes.meta.v1 as meta
from pulumi import ResourceOptions

from pulumi import ResourceOptions
from pulumi_kubernetes.apps.v1 import Deployment, DeploymentSpecArgs
from pulumi_kubernetes.core.v1 import Service
from pulumi_kubernetes.meta.v1 import ObjectMetaArgs, LabelSelectorArgs
from pulumi_kubernetes.core.v1 import (
    PodTemplateSpecArgs,
    PodSpecArgs,
    ContainerArgs,
    ContainerPortArgs,
    EnvVarArgs,
    VolumeMountArgs,
    VolumeArgs,
    PersistentVolumeClaimVolumeSourceArgs,
    ServiceSpecArgs,
    ServicePortArgs,
    EnvVarSourceArgs,
    EnvVarArgs,
    SecretKeySelectorArgs
)

from pulumi_kubernetes.networking.v1 import (
    Ingress,
    IngressSpecArgs,
    IngressRuleArgs,
    HTTPIngressRuleValueArgs,
    HTTPIngressPathArgs,
    IngressBackendArgs,
    IngressServiceBackendArgs,
    ServiceBackendPortArgs,
)

# namespace

ns = kube.Namespace("chat-ns",
    metadata={
        "name" : "pulumi"
    })

# secret for jwt

secret = kube.Secret("secret-jwt", 
    metadata = {
        "name" : "secret-jwt",
        "namespace" : "pulumi"
    },
    data = {
        "jwt_secret" : "c2VjcmV0X2FobHNqZGZobGFzZGpha2pkZmhrYWxqc2RsYWpmaGFzamRmaGxh"
    },
    opts=ResourceOptions(depends_on=[ns])
)

# pv-mongodb

pv_mongo = kube.PersistentVolume("pv-mongodb",
    metadata = {
        "name" : "pv-mongo",
        "namespace" : "pulumi"
    },
    spec = {
        "capacity" : {
            "storage" : "2Gi"
        },

        "access_modes" : ["ReadWriteOnce"],

        "persistent_volume_reclaim_policy" : "Retain",

        "storage_class_name" : "local-storage",

        "volume_mode" : "Filesystem",

        "host_path" : {
            "path" : "/data",
            "type" : "DirectoryOrCreate"
        }
    }
)

# pvc-mongodb

pvc_mongo = kube.PersistentVolumeClaim("pvc_mongodb",
    metadata = {
        "name": "pvc-mongodb",
        "namespace": "pulumi" 
    },
    spec = {
        "access_modes" : ["ReadWriteOnce"],
        "storage_class_name" : "local-storage",
        "resources" : {
            "requests" : {
                "storage" : "2Gi"
            }
        }
    },
    opts = ResourceOptions(depends_on=[pv_mongo])
)

# mongodb deploy

deployment = Deployment(
    "mongodb-deploy",
    metadata=ObjectMetaArgs(
        name="deploy-mongodb",
        namespace=ns.metadata["name"],
    ),
    spec=DeploymentSpecArgs(
        replicas=1,
        selector=LabelSelectorArgs(
            match_labels={"app": "mongodb"}
        ),
        template=PodTemplateSpecArgs(
            metadata=ObjectMetaArgs(
                labels={"app": "mongodb"}
            ),
            spec=PodSpecArgs(
                containers=[
                    ContainerArgs(
                        name="mongodb",
                        image="mongo:latest",
                        ports=[
                            ContainerPortArgs(container_port=27017)
                        ],
                        env=[
                            EnvVarArgs(
                                name="MONGO_INITDB_ROOT_USERNAME",
                                value="admin"
                            ),
                            EnvVarArgs(
                                name="MONGO_INITDB_ROOT_PASSWORD",
                                value="secretpassword"
                            ),
                        ],
                        volume_mounts=[
                            VolumeMountArgs(
                                name="mongodb-data",
                                mount_path="/data/db"
                            )
                        ]
                    )
                ],
                volumes=[
                    VolumeArgs(
                        name="mongodb-data",
                        persistent_volume_claim=PersistentVolumeClaimVolumeSourceArgs(
                            claim_name=pvc_mongo.metadata["name"]
                        )
                    )
                ]
            )
        )
    ),
    opts=ResourceOptions(depends_on=[pvc_mongo])
)

# mongodb service

mongodb_service = Service(
    "mongodb-service",
    metadata=ObjectMetaArgs(
        name="mongodb",
        namespace=ns.metadata["name"]
    ),
    spec=ServiceSpecArgs(
        selector={
            "app": "mongodb"
        },
        ports=[
            ServicePortArgs(
                port=27017,
                target_port=27017
            )
        ]
    ),
    opts=ResourceOptions(depends_on=[deployment])
)

# backend deploy

config = Config()
backend_env_list = config.get_object("backend_env") or []

backend_deployment = Deployment(
    "backend-deploy",
    metadata=ObjectMetaArgs(
        name="backend-deploy",
        namespace=ns.metadata["name"],
        labels={"test": "backend-deploy"},
    ),
    spec=DeploymentSpecArgs(
        replicas=1,
        selector=LabelSelectorArgs(
            match_labels={"test": "app-backend"}
        ),
        template=PodTemplateSpecArgs(
            metadata=ObjectMetaArgs(
                labels={"test": "app-backend"}
            ),
            spec=PodSpecArgs(
                containers=[
                    ContainerArgs(
                        name="app-backend",
                        image="adityasharmaap/chat-app-backend",
                        ports=[
                            ContainerPortArgs(container_port=5001)
                        ],
                        env=[
                            # Static secret env var from Kubernetes Secret
                            EnvVarArgs(
                                name="JWT_SECRET",
                                value_from=EnvVarSourceArgs(
                                    secret_key_ref=SecretKeySelectorArgs(
                                        name="secret-jwt",
                                        key="jwt_secret"
                                    )
                                )
                            ),
                            # Dynamic env vars from backend_env config
                            *[
                                EnvVarArgs(
                                    name=env["name"],
                                    value=env["value"]
                                ) for env in backend_env_list
                            ]
                        ]
                    )
                ]
            )
        )
    ),
    opts=ResourceOptions(depends_on=[ns, secret, mongodb_service])
)

# backend service

backend_service = Service(
    "backend-service",
    metadata=ObjectMetaArgs(
        name="backend",
        namespace=ns.metadata["name"]
    ),
    spec=ServiceSpecArgs(
        selector={
            "test": "app-backend"
        },
        ports=[
            ServicePortArgs(
                port=5001,
                target_port=5001
            )
        ],
        # Uncomment the following line if you want a LoadBalancer service
        # type="LoadBalancer"
    ),
    opts=ResourceOptions(depends_on=[backend_deployment])
)

# forntend deploy


frontend_deployment = Deployment(
    "frontend-deploy",
    metadata=ObjectMetaArgs(
        name="frontend-deploy",
        namespace=ns.metadata["name"],
    ),
    spec=DeploymentSpecArgs(
        replicas=1,
        selector=LabelSelectorArgs(
            match_labels={"app": "app-frontend"}
        ),
        template=PodTemplateSpecArgs(
            metadata=ObjectMetaArgs(
                namespace=ns.metadata["name"],  # Not always required in template, but included for parity
                labels={"app": "app-frontend"}
            ),
            spec=PodSpecArgs(
                containers=[
                    ContainerArgs(
                        name="frontend",
                        image="adityasharmaap/chat-app-frontend",
                        ports=[ContainerPortArgs(container_port=80)]
                    )
                ]
            )
        )
    ),
    opts=ResourceOptions(depends_on=[backend_service])
)

# frontend service

from pulumi import ResourceOptions

frontend_service = Service(
    "frontend-service",
    metadata=ObjectMetaArgs(
        name="frontend",
        namespace=ns.metadata["name"]
    ),
    spec=ServiceSpecArgs(
        selector={
            "app": "app-frontend"
        },
        ports=[
            ServicePortArgs(
                port=8080,
                target_port=80
            )
        ]
    ),
    opts=ResourceOptions(depends_on=[frontend_deployment])
)

# ingress

ingress_chatapp = Ingress(
    "ingress-chatapp",
    metadata=ObjectMetaArgs(
        name="ingress-chatapp",
        namespace=ns.metadata["name"],
        annotations={
            # "nginx.ingress.kubernetes.io/rewrite-target": "/",  # Uncomment if needed
            "nginx.ingress.kubernetes.io/ssl-redirect": "false"
        }
    ),
    spec=IngressSpecArgs(
        ingress_class_name="nginx",
        rules=[
            IngressRuleArgs(
                host="localhost",
                http=HTTPIngressRuleValueArgs(
                    paths=[
                        HTTPIngressPathArgs(
                            path="/",
                            path_type="Prefix",
                            backend=IngressBackendArgs(
                                service=IngressServiceBackendArgs(
                                    name=frontend_service.metadata["name"],
                                    port=ServiceBackendPortArgs(number=8080)
                                )
                            )
                        ),
                        HTTPIngressPathArgs(
                            path="/api",
                            path_type="Prefix",
                            backend=IngressBackendArgs(
                                service=IngressServiceBackendArgs(
                                    name=backend_service.metadata["name"],
                                    port=ServiceBackendPortArgs(number=5001)
                                )
                            )
                        )
                    ]
                )
            )
        ]
    ),
    opts=ResourceOptions(depends_on=[frontend_service, backend_service])
)

pulumi.export("frontend service :", frontend_service.metadata.name)
pulumi.export("backend service :", backend_service.metadata.name)
pulumi.export("mongodb service :", mongodb_service.metadata.name)
pulumi.export("ingress service :", ingress_chatapp.metadata.name)
