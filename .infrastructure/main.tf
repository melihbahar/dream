#provider "aws" {
#  region  = "us-east-1"
#  access_key = "AKIA5FTY6OVRBLIY67LG"
#  secret_key = "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"
#}

provider "aws" {
  region = "us-east-1"
}


resource "aws_instance" "dream" {
  ami           = "ami-0c7217cdde317cfec"
  instance_type = "t2.micro"

  tags = {
    Name = "dream"
  }
}

