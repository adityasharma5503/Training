# import pulumi
# import pulumi_kubernetes as k8s

# class Grafana(pulumi.ComponentResource):
#     def __init__(self, name: str, namespace: str, opts=None):
#         super().__init__("custom:monitoring:Grafana", name, None, opts)

#         chart = k8s.helm.v3.Chart(
#             f"{name}-grafana",
#             k8s.helm.v3.ChartOpts(
#                 chart="grafana",
#                 version="7.3.11",
#                 fetch_opts=k8s.helm.v3.FetchOpts(
#                     repo="https://grafana.github.io/helm-charts"
#                 ),
#                 namespace=namespace,
#                 values={
#                     "adminPassword": "admin123",
#                     "service": {
#                         "type": "ClusterIP"
#                     }
#                 },
#             ),
#             opts=pulumi.ResourceOptions(parent=self)
#         )

#         self.register_outputs({})
