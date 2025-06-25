provider "kubernetes" {
  config_path = "~/.kube/config"
  config_context = "kind-ingress-cluster"  # default is kind-kind
}
