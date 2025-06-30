resource "kubernetes_namespace_v1" "namespace" {
  metadata {
    labels = {
      mylabel = "${var.namespace}"
    }

    name = "${var.namespace}"
  }
}

resource "kubernetes_persistent_volume_v1" "pv" {
  metadata {
    name = "${var.name}-pv"
  }
  spec {
    access_modes = ["ReadWriteOnce"]

    persistent_volume_reclaim_policy = "Retain"

    storage_class_name = "local-storage"

    volume_mode = "Filesystem"

    capacity = {
      storage = var.pv_capacity
    }

    persistent_volume_source {
      host_path {
        path = "${var.pv_local_path}"
        type = "DirectoryOrCreate"
      }
    }
  } 
}

resource "kubernetes_persistent_volume_claim_v1" "pvc" {

  depends_on = [ kubernetes_persistent_volume_v1.pv ]
  
  metadata {
    name = "${var.name}-pvc"
    namespace = "${var.namespace}"
  }
  spec {
    access_modes = ["ReadWriteOnce"]
    storage_class_name = "local-storage"
    resources {
      requests = {
        storage = "${var.pv_capacity}"
      }
    }
    # volume_name = "${var.name}-pv"
  }
}

resource "kubernetes_deployment" "deployment" {

  depends_on = [ kubernetes_persistent_volume_claim_v1.pvc ]

  metadata {
    name = "${var.name}-deploy"
    namespace = "${var.namespace}"
  }

  spec {
    replicas = var.replicas

    selector {
      match_labels = {
        app = "${var.name}"
      }
    }

    template {
      metadata {
        labels = {
          app = "${var.name}"
        }
      }

      spec {
        volume {
          name = "${var.name}-data"
          persistent_volume_claim {
            claim_name = "${var.name}-pvc"
          }
        }

        container {
          name = "${var.name}"
          image = "${var.app_image}"
          port {
            container_port = var.app_port
          }

          volume_mount {
            name = "${var.name}-data"
            mount_path = "${var.pv_mount_path}"
          }
        }
      }
    }
  }
}

resource "kubernetes_service_v1" "service" {
  
  depends_on = [ kubernetes_deployment.deployment ]
  
  metadata {
    name = "${var.name}-svc"
    namespace = var.namespace
  }
  spec {
    selector = {
      app = "${var.name}"
    }

    port {
      port        = var.service_port
      target_port = var.service_target_port
    }
  }
}