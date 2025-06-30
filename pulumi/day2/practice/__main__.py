import pulumi
import pulumi_kubernetes.core.v1.Namespace as Namespace     
import pulumi_kubernetes.core.v1.Pod as Pod     
from pulumi_kubernetes.meta.v1 import ObjectMetaArgs
from pulumi_kubernetes.core.v1 import(
    PodSpecArgs,
    ContainerArgs
)


# --------------- Importing and using resource --------------------
ns = Namespace.get("chat-app", id="chat-app")

pod = Pod("my-pod", 
    metadata=ObjectMetaArgs(
        namespace=ns.metadata.name
    ),
    spec=PodSpecArgs(
        containers=[ContainerArgs(
            name="nginx",
            image="nginx:latest"
        )]
    )
    )


# --------------Creating resources from function----------------
def podCreate(podName, podContainerImage):
    return Pod(podName, 
        metadata=ObjectMetaArgs(
        namespace=ns.metadata.name
        ),
        spec=PodSpecArgs(
            containers=[ContainerArgs(
                name=podName,
                image=podContainerImage
            )]
        )
    )



mongo_pod = podCreate("mongo-pod", "mongo:latest")
redis_pod = podCreate("redis-pod", "redis:latest")

# ------------Config and secret---------------------
config = pulumi.Config()

stack = config.get("stack")
secret_stack = config.get_secret("stack")



# ------------Importing custom Components---------------------
from components.k8s_app import K8sApp  # Assuming you save the class in mycomponents.py

app_nginx = K8sApp("nginx", image="nginx:latest", port=80, namespace="pulumi")

# -----------------Exports------------------------
pulumi.export("Stack: ", stack)
pulumi.export("SecretStack: ", secret_stack)
pulumi.export("Namespace: ", ns.metadata.name)




# -------------------------Update Plan

# pulumi preview --save-plan=plan.json

mysql = podCreate("mysql", "mysql:oraclelinux9")










