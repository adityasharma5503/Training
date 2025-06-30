"""A Kubernetes Python Pulumi program"""

# import pulumi
# from pulumi_kubernetes.apps.v1 import Deployment

# app_labels = { "app": "nginx" }

# deployment = Deployment(
#     "nginx",
#     spec={
#         "selector": { "match_labels": app_labels },
#         "replicas": 1,
#         "template": {
#             "metadata": { "labels": app_labels },
#             "spec": { "containers": [{ "name": "nginx", "image": "nginx" }] }
#         },
#     })

# pulumi.export("name", deployment.metadata["name"])



# """
# Creating a Kubernetes Deployment
# """
# import pulumi
# from pulumi_kubernetes.apps.v1 import Deployment
# from pulumi_kubernetes.core.v1 import Service

# # Minikube does not implement services of type `LoadBalancer`; require the user to specify if we're
# # running on minikube, and if so, create only services of type ClusterIP.
# config = pulumi.Config()
# is_minikube = config.require_bool("isMinikube")

# app_name = "nginx"
# app_labels = { "app": app_name }

# deployment = Deployment(
#     app_name,
#     spec={
#         "selector": { "match_labels": app_labels },
#         "replicas": 1,
#         "template": {
#             "metadata": { "labels": app_labels },
#             "spec": { "containers": [{ "name": app_name, "image": "nginx" }] }
#         }
#     })

# # Allocate an IP to the Deployment.
# frontend = Service(
#     app_name,
#     metadata={
#         "labels": deployment.spec["template"]["metadata"]["labels"],
#     },
#     spec={
#         "type": "ClusterIP" if is_minikube else "LoadBalancer",
#         "ports": [{ "port": 80, "target_port": 80, "protocol": "TCP" }],
#         "selector": app_labels,
#     })

# # When "done", this will print the public IP.
# result = None
# if is_minikube:
#     result = frontend.spec.apply(lambda v: v["cluster_ip"] if "cluster_ip" in v else None)
# else:
#     ingress = frontend.status.load_balancer.apply(lambda v: v["ingress"][0] if "ingress" in v else "output<string>")
#     result = ingress.apply(lambda v: v["ip"] if v and "ip" in v else (v["hostname"] if v and "hostname" in v else "output<string>"))

# pulumi.export("ip", result)

#---------------------------------------------------------------------

import pulumi

#---------------------------------------------------------------------

import pulumi_kubernetes.core.v1.Namespace as ns
namespace = ns("pulumi", 
            metadata = {
                "name": "pulumi" 
            })

pulumi.export("namespace", namespace.metadata["name"])

#----------------------------------------------------------------------

import pulumi_kubernetes.core.v1.ConfigMap as cm

configMap = cm("my-cm", 
    metadata={
        "name": "my-cm",
        "namespace": "pulumi"
    },
    data={
        "url": "mongodb://username:password",
    })

#---------------------------------------------------------------------

import pulumi_kubernetes.core.v1.PersistentVolume as pv

myPvc = pv("my-pv",
    metadata={
        "name": "my-pv",
        # "namespace": "pulumi",
    },
    spec={
        "accessModes": ["ReadWriteOnce"],
        "volumeMode" : "Filesystem",
        "persistentVolumeReclaimPolicy" : "Delete",
        "storageClassName" : "local-storage",
        "hostPath" : {
            "path" : "/data",
            "type" : "DirectoryOrCreate"
        },
        "capacity" : {
            "storage" : "2Gi"
        }
    }
    )

#---------------------------------------------------------------------

import pulumi_kubernetes.core.v1.Pod as Pod

my_pod = Pod("my-pod", 
        metadata={
            "name" : "my-pod",
            "namespace" : "pulumi",
            "labels" : {
                "app" : "my-app"
            }
        },
        spec={
            "containers" : [{
                "name" : "nginx",
                "image" : "nginx:latest",
                "ports": [{
                    "container_port" : 80
                }]
            }] 
        })

#---------------------------------------------------------------------

