

# -------------  Using components ----------------------------------

# KubePrometheus stack creates prometheus and grafana deployment
# We are using loki-stack from grafana repository helm charts

import pulumi
import pulumi_kubernetes as k8s
from components.kube_prometheus import KubePrometheusStack
from components.loki_stack import LokiStack

# Create Namespace
ns = k8s.core.v1.Namespace("monitoring", metadata={"name": "monitoring"})

# Deploy Prometheus + Grafana
prom_stack = KubePrometheusStack(
    "monitoring",
    namespace=ns.metadata["name"],
    opts=pulumi.ResourceOptions(depends_on=[ns])
)

# Deploy Loki + Promtail
loki_stack = LokiStack(
    "monitoring",
    namespace=ns.metadata["name"],
    opts=pulumi.ResourceOptions(depends_on=[ns])
)


# -------------------- Helm Chart for kube-prometheus-stack ------------------------


# import pulumi_kubernetes as k8s
# import pulumi

# # Namespace
# ns = k8s.core.v1.Namespace("monitoring-ns", metadata={"name": "monitoring"})

# # Custom values file loaded into Python
# import yaml

# with open("./custom_kube_prometheus_stack.yml") as f:
#     custom_values = yaml.safe_load(f)

# # Helm Chart via Pulumi
# kube_stack = k8s.helm.v3.Chart(
#     "kube-prom-stack",
#     k8s.helm.v3.ChartOpts(
#         chart="kube-prometheus-stack",
#         version="58.5.2",  # optional
#         fetch_opts=k8s.helm.v3.FetchOpts(
#             repo="https://prometheus-community.github.io/helm-charts"
#         ),
#         namespace="monitoring",
#         values=custom_values
#     ),
#     opts=pulumi.ResourceOptions(depends_on=[ns])
# )


# --------------------------------------------




