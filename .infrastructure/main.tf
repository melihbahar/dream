terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.34.0"
    }
  }
}

# ec2
resource "aws_instance" "dream" {
  ami           = var.ami
  instance_type = var.instance_type
  iam_instance_profile = aws_iam_instance_profile.profile.name
  key_name = aws_key_pair.default.key_name
  vpc_security_group_ids = [aws_security_group.sg.id]
  user_data = file("user_data.sh")

  tags = {
    Name = var.image_tag
  }
}
