# -----------------------------------------------------------------------
# # Imported the pod :
# resource "kubernetes_pod_v1" "test" {
#     metadata {
#     name      = "nginx"
#     namespace = "default"
#     labels = {
#         run = "nginx"
#     }
#   }

#   spec {
#     automount_service_account_token = false
#     container {
#       name  = "nginx"
#       image = "nginx:latest"
#     }
#   }
# }
# -----------------------------------------------------------------------
