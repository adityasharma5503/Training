import pulumi
from pulumi import ComponentResource, ResourceOptions
from pulumi_kubernetes.apps.v1 import Deployment, DeploymentSpecArgs
from pulumi_kubernetes.core.v1 import Service, ServiceSpecArgs, ContainerArgs, ContainerPortArgs, PodSpecArgs, PodTemplateSpecArgs
from pulumi_kubernetes.meta.v1 import ObjectMetaArgs, LabelSelectorArgs

class K8sApp(pulumi.ComponentResource):
    def __init__(self, name: str, image: str, port: int, namespace: str, opts: ResourceOptions = None):
        super().__init__('pkg:index:K8sApp', name, None, opts)

        labels = { "app": name }

        self.deployment = Deployment(
            f"{name}-deploy",
            metadata=ObjectMetaArgs(
                name=f"{name}-deploy",
                namespace=namespace
            ),
            spec=DeploymentSpecArgs(
                replicas=1,
                selector=LabelSelectorArgs(match_labels=labels),
                template=PodTemplateSpecArgs(
                    metadata=ObjectMetaArgs(labels=labels),
                    spec=PodSpecArgs(
                        containers=[ContainerArgs(
                            name=name,
                            image=image,
                            ports=[ContainerPortArgs(container_port=port)]
                        )]
                    )
                )
            ),
            opts=ResourceOptions(parent=self)
        )

        self.service = Service(
            f"{name}-svc",
            metadata=ObjectMetaArgs(
                name=f"{name}-service",
                namespace=namespace
            ),
            spec=ServiceSpecArgs(
                selector=labels,
                ports=[{
                    "port": port,
                    "target_port": port
                }]
            ),
            opts=ResourceOptions(parent=self)
        )

        # Export the service name
        self.register_outputs({
            "deployment_name": self.deployment.metadata["name"],
            "service_name": self.service.metadata["name"]
        })
