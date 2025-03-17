terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0" # Use version 2.x of the local provider
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# Variables for instance types and AMI
variable "instance_type_t3_small" {
  default = "t3.small"
}

variable "instance_type_t3_medium" {
  default = "t3.medium"
}

variable "ami" {
  default = "ami-04b4f1a9cf54c11d0"
}

# Read installation scripts
locals {
  jenkins_install_script = file("${path.module}/jenkins_install.sh")
  docker_install_script  = file("${path.module}/docker_install.sh")
}

# Create a VPC
resource "aws_vpc" "jenkins_k3s" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "Jenkins-k3s-vpc"
  }
}

# Create a public subnet
resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.jenkins_k3s.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "us-east-1a"

  tags = {
    Name = "public-subnet"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.jenkins_k3s.id

  tags = {
    Name = "jenkins-k3s-igw"
  }
}

# Route Table
resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.jenkins_k3s.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "public-route-table"
  }
}

# Route Table Association
resource "aws_route_table_association" "public_route_table_assoc" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_route_table.id
}

# Security Group for Jenkins Master
resource "aws_security_group" "jenkins_master_sg" {
  name        = "jenkins-master-sg"
  description = "Jenkins Master Security Group"
  vpc_id      = aws_vpc.jenkins_k3s.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "SSH access"
  }

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Jenkins web interface"
  }

  ingress {
    from_port   = 50000
    to_port     = 50000
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
    description = "Jenkins agent connection"
  }

  ingress {
    from_port   = 6443
    to_port     = 6443
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
    description = "Kubernetes API access"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = {
    Name = "jenkins-master-sg"
  }
}

# Security Group for k3s Master
resource "aws_security_group" "k3s_master_sg" {
  name        = "k3s-master-sg"
  description = "k3s Master Security Group"
  vpc_id      = aws_vpc.jenkins_k3s.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "SSH access"
  }

  ingress {
    from_port   = 6443
    to_port     = 6443
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
    description = "Kubernetes API server"
  }

  ingress {
    from_port   = 2379
    to_port     = 2380
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
    description = "etcd client and peer communication"
  }

  ingress {
    from_port   = 10250
    to_port     = 10250
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
    description = "Kubelet API"
  }

  ingress {
    from_port   = 30000
    to_port     = 32767
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "NodePort Services"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = {
    Name = "k3s-master-sg"
  }
}

# EC2 Jenkins Master
resource "aws_instance" "jenkins_master" {
  ami                         = var.ami
  instance_type               = var.instance_type_t3_medium
  subnet_id                   = aws_subnet.public_subnet.id
  vpc_security_group_ids      = [aws_security_group.jenkins_master_sg.id]
  key_name                    = "jenkins_k3s"
  user_data                   = base64encode(<<EOF
#!/bin/bash

# Create a directory for the scripts
mkdir -p /opt/scripts

# Write Jenkins installation script
cat > /opt/scripts/jenkins_install.sh << 'EOL'
${local.jenkins_install_script}
EOL

# Write Docker installation script
cat > /opt/scripts/docker_install.sh << 'EOL'
${local.docker_install_script}
EOL

# Make scripts executable
chmod +x /opt/scripts/jenkins_install.sh
chmod +x /opt/scripts/docker_install.sh

# Run installation scripts with sudo
echo "Running Docker installation script..."
sudo /opt/scripts/docker_install.sh || echo "Error: Docker installation failed"

echo "Running Jenkins installation script..."
sudo /opt/scripts/jenkins_install.sh || echo "Error: Jenkins installation failed"

# Install kubectl
echo "Installing kubectl..."
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Create .kube directory
echo "Creating .kube directory..."
sudo mkdir -p /var/lib/jenkins/.kube

# Ensure Jenkins user exists before assigning ownership
if id "jenkins" &>/dev/null; then
  echo "Jenkins user exists. Assigning ownership of .kube directory..."
  sudo chown jenkins:jenkins /var/lib/jenkins/.kube
else
  echo "Warning: Jenkins user does not exist. Skipping ownership assignment."
fi
EOF
)
  lifecycle {
    create_before_destroy = true
  }
  
  tags = {
    Name = "Jenkins Master Node"
  }
}

# EC2 k3s Master
resource "aws_instance" "k3s_master" {
  ami                         = var.ami
  instance_type               = var.instance_type_t3_medium
  subnet_id                   = aws_subnet.public_subnet.id
  vpc_security_group_ids      = [aws_security_group.k3s_master_sg.id]
  key_name                    = "jenkins_k3s"
  user_data                   = base64encode(<<EOF
#!/bin/bash
# Install k3s
curl -sfL https://get.k3s.io | sh -
# Wait for k3s to be ready
sleep 30
# Make kubeconfig accessible
sudo chmod 644 /etc/rancher/k3s/k3s.yaml
EOF
)
  lifecycle {
    create_before_destroy = true
  }
  
  tags = {
    Name = "k3s Master Node"
  }
}

# Outputs
output "jenkins_master_public_ip" {
  value = aws_instance.jenkins_master.public_ip
}

output "jenkins_master_private_ip" {
  value = aws_instance.jenkins_master.private_ip
}

output "k3s_master_public_ip" {
  value = aws_instance.k3s_master.public_ip
}

output "k3s_master_private_ip" {
  value = aws_instance.k3s_master.private_ip
}