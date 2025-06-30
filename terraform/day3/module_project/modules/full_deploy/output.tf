output "namespace_id" {
  value = kubernetes_namespace_v1.namespace.id
}

output "pv_id" {
  value = kubernetes_persistent_volume_v1.pv.id
}

output "pvc_id" {
    value = kubernetes_persistent_volume_claim_v1.pvc.id
}

output "deployment_id" {
  value = kubernetes_deployment.deployment.id
}

output "service" {
  value = kubernetes_service_v1.service.id
}