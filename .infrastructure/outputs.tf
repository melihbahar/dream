output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.dream.id
}

output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.dream.public_ip
}


