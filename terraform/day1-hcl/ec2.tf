# key pair

resource "aws_key_pair" "my_key" {
    key_name = "terra-key-ec2"
    public_key = file("terra-key-ec2.pub")
}

resource "aws_default_vpc" "my_vpc" {

}

resource "aws_security_group" "my_sg" {
    name = "automate_sg"
    vpc_id = aws_default_vpc.my_vpc.id
    # key = aws_security_group.my_key.key_name

    #inbound rules
    ingress {
        from_port=22
        to_port=22
        protocol="tcp"
        cidr_blocks=["0.0.0.0/0"]
        description="SSH open"
    }

    ingress {
        from_port = 80
        to_port = 80
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
        description = "HTTP open"
    }

    #outbound rules
    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }

    #tags
    tags = {
        name = "automate_sg" 
    }
}

resource "aws_instance" "my_ec2" {

    depends_on = [ aws_security_group.my_sg, aws_key_pair.my_key ]

    # count = 5

    for_each = tomap({
        "k8s-worker-micro" = "t2.micro" 
        "k8s-control-medium" = "t2.medium"
    })

  key_name = aws_key_pair.my_key.key_name
  ami = var.ec2_ami_id
  instance_type = each.value
  security_groups = [aws_security_group.my_sg.name]

  user_data = file("install_nginx.sh")

  root_block_device {
    volume_size = var.ec2_env == "prod" ? var.ec2_default_root_storage_size : 10
    volume_type = "gp3"
  }

  tags = {
    Name = each.key
  }
}