#resource "aws_vpc" "vpc" {
#  cidr_block = "10.0.0.0/16"
#}
#
#resource "aws_internet_gateway" "gateway" {
#    vpc_id = aws_vpc.vpc.id
#}

#resource "aws_route_table" "rt" {
#  vpc_id = aws_vpc.vpc.id
#
#    route {
#      cidr_block = "0.0.0.0/0"
#      gateway_id = aws_internet_gateway.gateway.id
#    }
#}
#
#resource "aws_subnet" "subnet" {
#  vpc_id = aws_vpc.vpc.id
#  cidr_block = "10.0.0.0/24"
#  availability_zone = "us-east-1a"
#}
#
#resource "aws_route_table_association" "assc" {
#  route_table_id = aws_route_table.rt.id
#    subnet_id = aws_subnet.subnet.id
#}