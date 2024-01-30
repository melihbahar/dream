#! /bin/bash
set -e

# For Amazon Linux distributions
sudo yum install -y yum-utils

sudo yum install docker -y
sudo yum install awscli -y

sudo service docker start
# grant read, write, and execute permissions to docker.sock
sudo chmod 777 /var/run/docker.sock

# login to ecr
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 905418012002.dkr.ecr.us-east-1.amazonaws.com

# pull image from ecr
docker pull 905418012002.dkr.ecr.us-east-1.amazonaws.com/dream:d7fec2d99f95784d9a1bd7bb93e9741633e0a0b2

# Run application at start
docker run --restart=always -d -p 5000:5000  905418012002.dkr.ecr.us-east-1.amazonaws.com/dream:d7fec2d99f95784d9a1bd7bb93e9741633e0a0b2