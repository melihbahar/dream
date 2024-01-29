#! /bin/bash
set -e

sudo yum install -y yum-utils

sudo yum install docker -y
sudo yum install awscli -y

sudo service docker start
sudo chmod 777 /var/run/docker.sock

# login to ecr
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 905418012002.dkr.ecr.us-east-1.amazonaws.com

# pull image from ecr
docker pull 905418012002.dkr.ecr.us-east-1.amazonaws.com/dream:45920721d26449b685d95ce75c1e00d0af830e95

# Run application at start
docker run --restart=always -d -p 5000:5000  905418012002.dkr.ecr.us-east-1.amazonaws.com/dream:45920721d26449b685d95ce75c1e00d0af830e95