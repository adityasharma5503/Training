variable "name" {
  type = string
  description = "Prefix name for all resources"
}

variable "namespace" {
  type = string
  description = "Namespace where resource will be created"
  default = "default"
}

variable "pv_capacity" {
  type = string
  description = "Capacity of Persistent volume"
  default = "2Gi"
}

variable "pv_local_path" {
  type = string
  description = "pv local path"
  default = "/data"
}

variable "pv_mount_path" {
  type = string
  description = "pv mount path in deployment"
  default = "/data"
}

variable "app_image" {
  type = string
  description = "Container image of the app"
}

variable "app_port" {
  type = number
  description = "Port on application"
}

variable "replicas" {
  type = number
  description = "Number of replicas for deployment"
  default = 1
}

variable "service_port" {
  type = number
  description = "Service port number"
}

variable "service_target_port" {
  type = number
  description = "Target port for service"
}