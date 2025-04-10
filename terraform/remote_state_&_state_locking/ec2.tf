resource "aws_security_group" "ssh_access" {
  name        = "ssh_access"
  description = "Allow SSH traffic"
  vpc_id      = module.vpc.vpc_id

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "ssh_access"
  }
}

resource "aws_key_pair" "web_key" {
  key_name   = "web_key"
  public_key = file("~/.ssh/web_key.pub")
}

resource "aws_instance" "terraform_state_test" {
  ami           = "ami-01811d4912b4ccb26" # Amazon Linux 2 AMI ID
  instance_type = "t2.micro"

  key_name               = aws_key_pair.web_key.key_name
  subnet_id              = module.vpc.public_subnets[0]  # Using the first public subnet from the VPC module
  vpc_security_group_ids = [aws_security_group.ssh_access.id]
  associate_public_ip_address = true

  tags = {
    Name = "terraform_state_test"
  }
}