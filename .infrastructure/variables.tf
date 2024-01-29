variable "instance_name" {
  description = "Tag name of the EC2 instance"
  type        = string
  default     = "Dream"
}

# Hardcoded to a specific ami for now
# could be changed to take the id of the most recent AMI given a for the instance wanted
variable "ubunutu_ami" {
  description = "ami to use for EC2"
  type        = string
  default     = "ami-0c7217cdde317cfec"
}

# No need for a strong machine for this project
variable "instance_type" {
  description = "Type of EC2 instance"
  type        = string
  default     = "t2.micro"
}

variable "ecr_image_repo_url" {
  default = "905418012002.dkr.ecr.us-east-1.amazonaws.com/dream"
}

variable "image_tag" {
  default = "latest"
}