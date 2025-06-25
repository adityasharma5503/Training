resource "kubernetes_namespace" "terraform_ns" {
   metadata {
    labels = {
      name = "terraform-ns"
    }
    name = "terraform-ns"
  }
}

resource "kubernetes_secret" "secret_jwt" {
  
  depends_on = [ kubernetes_namespace.terraform_ns ]

  metadata {
    name = "secret-jwt"
    namespace = "terraform-ns"
  }

  data = {
    jwt_secret: "c2VjcmV0X2FobHNqZGZobGFzZGpha2pkZmhrYWxqc2RsYWpmaGFzamRmaGxh"
  }

  type = "Opaque"
}

resource "kubernetes_persistent_volume" "pv_mongodb" {

  metadata {
    name = "pv-mongodb"
  }

  spec {
    capacity = {
      storage = "3Gi"
    }

    access_modes = ["ReadWriteOnce"]

    persistent_volume_reclaim_policy = "Retain"

    storage_class_name = "local-storage"

    volume_mode = "Filesystem"

    persistent_volume_source {
      host_path {
        path = "/data"
        type = "DirectoryOrCreate"
      }
    }
  }
}

resource "kubernetes_persistent_volume_claim" "pvc_mongodb" {

  depends_on = [ kubernetes_persistent_volume.pv_mongodb, kubernetes_namespace.terraform_ns ]

  metadata {
    name = "pvc-mongodb"
    namespace = "terraform-ns"
  }

  spec {
    access_modes = [ "ReadWriteOnce" ]
    storage_class_name = "local-storage"
    resources {
      requests = {
        storage = "2Gi"
      }
    }
  }
}

resource "kubernetes_deployment" "mongodb_deploy" {
  depends_on = [ kubernetes_persistent_volume_claim.pvc_mongodb ]

  metadata {
    name = "deploy-mongodb"
    namespace = "terraform-ns"
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "mongodb"
      }
    }

    template {
      metadata {
        labels = {
          app = "mongodb"
        }
      }

      spec {
        volume {
          name = "mongodb-data"
          persistent_volume_claim {
            claim_name = "pvc-mongodb"
          }
        }

        container {
          name = "mongodb"
          image = "mongo:latest"
          port {
            container_port = 27017
          }

          env {
            name = var.mongo_username.name
            value = var.mongo_username.value 
          }

          env {
            name = var.mongo_password.name
            value = var.mongo_password.value
          }

          volume_mount {
            name = "mongodb-data"
            mount_path = "/data/db"
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "mongodb-service" {
  
  depends_on = [ kubernetes_deployment.mongodb_deploy ]

  metadata {
    name = "mongodb"
    namespace = "terraform-ns"
  }
  spec {
    selector = {
      app = "mongodb"
    }
    port {
      port        = 27017
      target_port = 27017
    }
  }
}

resource "kubernetes_deployment" "backend-deploy" {

  depends_on = [ kubernetes_namespace.terraform_ns, kubernetes_secret.secret_jwt, kubernetes_service.mongodb-service ]

  metadata {
    name = "backend-deploy"
    labels = {
      test = "backend-deploy"
    }
    namespace = "terraform-ns"
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        test = "app-backend"
      }
    }

    template {
      metadata {
        labels = {
          test = "app-backend"
        }
      }

      spec {
        container {
          image = "adityasharmaap/chat-app-backend"
          name  = "app-backend"
          port {
            container_port = 5001
          }

        #   env {
        #     name = NODE_ENV
        #     value = production
        #   }

          dynamic "env" {
            for_each = var.backend_env
            content {
              name  = env.value.name
              value = env.value.value
            }
          }

          env {
            name = "JWT_SECRET"
            value_from {
              secret_key_ref {
                name = "secret-jwt"
                key = "jwt_secret"
              }
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "backend-service" {
  
  depends_on = [ kubernetes_deployment.backend-deploy ]

  metadata {
    name = "backend"
    namespace = "terraform-ns"
  }
  spec {
    selector = {
      test = "app-backend"
    }
    port {
      port        = 5001
      target_port = 5001
    }

    # type = "LoadBalancer"
  }
}

resource "kubernetes_deployment" "frontend-deploy" {
  
  depends_on = [ kubernetes_service.backend-service ]

  metadata {
    name = "frontend-deploy"
    namespace = "terraform-ns"
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "app-frontend"
      }
    }

     template {
        metadata {
            namespace = "terraform-ns"
            labels = {
                app = "app-frontend"
            }
        }
        spec {
          container {
            name = "frontend"
            image = "adityasharmaap/chat-app-frontend"
            port {
              container_port = 80
            }
          }
        }
      }
  }
}

resource "kubernetes_service" "frontend-service" {

  depends_on = [ kubernetes_deployment.frontend-deploy ]

  metadata {
    name = "frontend"
    namespace = "terraform-ns"
  }

  spec {
    selector = {
        app = "app-frontend"
    }
    port {
      port = 8080
      target_port = 80
    }
  }
}

resource "kubernetes_ingress_v1" "ingress-chatapp" {

  depends_on = [ kubernetes_service.frontend-service, kubernetes_service.backend-service ]

  metadata {
    name = "ingress-chatapp"
    namespace = "terraform-ns"
    annotations = {
      "nginx.ingress.kubernetes.io/rewrite-target" = "/"
      "nginx.ingress.kubernetes.io/ssl-redirect" = "false"
    }
  }

  spec {

    ingress_class_name = "nginx"

    rule {
      host = "localhost"
      http {
        path {
          backend {
            # service_name = kubernetes_service.frontend-service.metadata[0].name
            # service_port = 8080

            service {
              name = kubernetes_service.frontend-service.metadata[0].name
              port {
                number = 8080
              }
            }

          }
          path = "/"
          path_type = "Prefix"
        }

        path {
          backend {
            # service_name = kubernetes_service.backend-service.metadata[0].name
            # service_port = 5001

            service {
              name = kubernetes_service.backend-service.metadata[0].name
              port {
                number = 5001
              }
            }
          }

          path = "/api"
          path_type = "Prefix"
        }
      }
    }
  }
}
