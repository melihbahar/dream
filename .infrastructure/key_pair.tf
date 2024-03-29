resource "tls_private_key" "key" {
  algorithm = "RSA"
  rsa_bits = 4096
}

resource "aws_key_pair" "default" {
  key_name = "default-key"
  public_key = tls_private_key.key.public_key_openssh
}