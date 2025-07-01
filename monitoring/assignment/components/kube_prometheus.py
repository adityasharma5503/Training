

import pulumi
import pulumi_kubernetes as k8s

class KubePrometheusStack(pulumi.ComponentResource):
    def __init__(self, name: str, namespace: str, values: dict = None, opts=None):
        super().__init__("custom:monitoring:KubePrometheus", name, None, opts)

        chart = k8s.helm.v3.Chart(
            f"{name}-kube-prometheus",
            k8s.helm.v3.ChartOpts(
                chart="kube-prometheus-stack",
                version="58.5.2",
                fetch_opts=k8s.helm.v3.FetchOpts(
                    repo="https://prometheus-community.github.io/helm-charts"
                ),
                namespace=namespace,
                values = values or {
                    "grafana": {
                        "additionalDataSources": [
                            {
                                "name": "Loki",
                                "type": "loki",
                                "access": "proxy",
                                "url": "http://monitoring-loki-stack.monitoring.svc.cluster.local:3100",
                                "isDefault": False,
                                "editable": True
                            }
                        ]
                    }
                },

            ),
            opts=pulumi.ResourceOptions(parent=self)
        )

        self.register_outputs({})





# ---------------------------------------------------------------------------------------------

# import pulumi_kubernetes as k8s
# import pulumi

# class Prometheus(pulumi.ComponentResource):
#     def __init__(self, namespace, opts=None):
#         super().__init__("custom:monitoring:Prometheus", "prometheus", None, opts)

#         self.chart = k8s.helm.v3.Chart(
#             "prometheus",
#             k8s.helm.v3.ChartOpts(
#                 chart="prometheus",
#                 version="25.21.0",
#                 fetch_opts=k8s.helm.v3.FetchOpts(
#                     repo="https://prometheus-community.github.io/helm-charts"
#                 ),
#                 namespace=namespace.metadata["name"],
#                 values={
#                     "alertmanager": {"enabled": False},
#                     "pushgateway": {"enabled": False},
#                     "server": {
#                         "service": {"type": "ClusterIP"},
#                         "retention": "6h"
#                     }
#                 }
#             ),
#             opts=pulumi.ResourceOptions(parent=self, depends_on=[namespace])
#         )
