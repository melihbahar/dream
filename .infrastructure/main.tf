terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.34.0"
    }
  }
}


#resource "null_resource" "null" {
#  provisioner "local-exec" {
#    command = "ssh to IP using key-pair that was created.. docker login docker pull
#    "
#  }
#}



# ECR Repo created manually

#resource "aws_ecs_cluster" "ecs_cluster" {
#  name = "dream-cluster"
#}
#
#resource "aws_ecs_task_definition" "task_definition" {
#  family                = "ecs_cluster"
#  container_definitions = data.template_file.task_definition_template.rendered
#}
#
#resource "aws_ecs_service" "worker" {
#  name            = "worker"
#  cluster         = aws_ecs_cluster.ecs_cluster.id
#  task_definition = aws_ecs_task_definition.task_definition.arn
#  desired_count   = 2
#}

# ec2
resource "aws_instance" "dream" {
  ami           = var.ami
  instance_type = var.instance_type
  iam_instance_profile = aws_iam_instance_profile.profile.name
  key_name = aws_key_pair.default.key_name
  vpc_security_group_ids = [aws_security_group.sg.id]
  user_data = file("user_data.sh")

  tags = {
    Name = var.instance_name
  }
}

#resource "aws_instance" "dream" {
#  ami           = var.ami
#  instance_type = var.instance_type
#
#  tags = {
#    Name = var.instance_name
#  }
#}



