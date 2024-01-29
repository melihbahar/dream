terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "4.45.0"
    }
  }
}

# ECR Repo created manually

resource "aws_ecs_cluster" "ecs_cluster" {
  name = "dream-cluster"
}

resource "aws_security_group" "ecs_sg" {
    name        = "ecs-sg"
    vpc_id      = aws_vpc.vpc.id

    ingress {
        description = "SSH"
        from_port       = 22
        to_port         = 22
        protocol        = "tcp"
        cidr_blocks     = ["0.0.0.0/0"]
    }

    ingress {
        description = "HTTPS"
        from_port       = 443
        to_port         = 443
        protocol        = "tcp"
        cidr_blocks     = ["0.0.0.0/0"]
    }

    ingress {
          description = "HTTP"
          from_port       = 80
          to_port         = 80
          protocol        = "tcp"
          cidr_blocks     = ["0.0.0.0/0"]
      }

    egress {
        from_port       = 0
        to_port         = 65535
        protocol        = "tcp"
        cidr_blocks     = ["0.0.0.0/0"]
    }
}




resource "aws_instance" "dream" {
  ami           = var.ubunutu_ami
  instance_type = var.instance_type

  tags = {
    Name = var.instance_name
  }
}
