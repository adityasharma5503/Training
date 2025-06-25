variable "backend_env" {

  type = list(object({
    name = string
    value = string
  }))

  default = [ {
    name = "NODE_ENV"
    value = "production"
  },
  {
    name = "MONGODB_URI"
    value = "mongodb://root:example@mongodb:27017"
  },
  {
    name = "PORT"
    value = "5001"
  } ] 
}

variable "mongo_username" {
  type = object({
    name = string
    value = string
  })

  default = {
    name = "MONGO_INITDB_ROOT_USERNAME"
    value = "root"
  }
}

variable "mongo_password" {
  type = object({
    name = string
    value = string
  })

  default = {
    name = "MONGO_INITDB_ROOT_PASSWORD"
    value = "example"
  }
}