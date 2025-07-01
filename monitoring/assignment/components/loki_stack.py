import pulumi
import pulumi_kubernetes as k8s

class LokiStack(pulumi.ComponentResource):
    def __init__(self, name: str, namespace: str, values: dict = None, opts=None):
        super().__init__("custom:monitoring:LokiStack", name, None, opts)

        chart = k8s.helm.v3.Chart(
            f"{name}-loki-stack",
            k8s.helm.v3.ChartOpts(
                chart="loki-stack",
                version="2.10.2",
                fetch_opts=k8s.helm.v3.FetchOpts(
                    repo="https://grafana.github.io/helm-charts"
                ),
                namespace=namespace,
                values=values or {
                    "promtail": {"enabled": True},
                    "grafana": {"enabled": False},
                },
            ),
            opts=pulumi.ResourceOptions(parent=self)
        )

        self.register_outputs({})
