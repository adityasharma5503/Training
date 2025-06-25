output "ec2_public_ip" {
#   value =  aws_instance.my_ec2.public_ip
  value = [ for key  in aws_instance.my_ec2: key.public_ip]
}

output "ec2_private_ip" {
#   value =  aws_instance.my_ec2.public_ip
  value = [ for key  in aws_instance.my_ec2: key.private_ip]
}

output "ec2_public_dns" {
#   value =  aws_instance.my_ec2.public_dns
  value = [ for key  in aws_instance.my_ec2: key.public_dns]
}