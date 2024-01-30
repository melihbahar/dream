variable "instance_name" {
  description = "Tag name of the EC2 instance"
  type        = string
  default     = "Dream"
}

# Hardcoded to a specific ami for now
# could be changed to take the id of the most recent AMI given a for the instance wanted
variable "ami" {
  description = "ami to use for EC2"
  type        = string
  default     = "ami-0a3c3a20c09d6f377"
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

variable "tag_name" {
  description = "The tag name for the EC2 instance"
  type        = string
}