output "backend_service_id" {
  value = kubernetes_service.backend-service.id
}

output "mongodb_service_id" {
  value = kubernetes_service.mongodb-service.id
}

output "frontend_service_id" {
  value = kubernetes_service.frontend-service.id
}

output "deploy_backend_id" {
  value = kubernetes_deployment.backend-deploy.id
}

output "deploy_mongodb_id" {
  value = kubernetes_deployment.mongodb_deploy.id
}

output "deploy_frontend_id" {
  value = kubernetes_deployment.frontend-deploy.id
}