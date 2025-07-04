variable "aws_instance_type" {
    default = "t2.micro"
    type = string
}

variable "ec2_default_root_storage_size" {
  default = 15
  type = number
}

variable "ec2_ami_id" {
  default = "ami-0fc5d935ebf8bc3bc"
  type = string
}

variable "ec2_env" {
    default = "test"
    type = string  
}