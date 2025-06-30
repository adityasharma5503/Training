module "full_deploy" {
  source = "./modules/full_deploy"

  name                = "nginx"
  namespace           = "my-nginx"
  app_image           = "nginx:latest"
  app_port            = 80
  service_port        = 80
  service_target_port = 80
}
