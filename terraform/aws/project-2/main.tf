
 provider "aws" {
     region = "us-east-1"
     access_key = var.AWS_ACCESS_KEY
     secret_key = var.AWS_SECRET_ACCESS_KEY
 }

resource "tls_private_key" "access-key" {
    algorithm = "RSA"
    rsa_bits = 4096
}

resource "aws_key_pair" "access-key" {
    key_name = "access-key"
    public_key = tls_private_key.access-key.public_key_openssh
}

resource "local_file" "private_key" {
  content         = tls_private_key.access-key.private_key_pem
  filename        = "${path.module}/access-key.pem"
  file_permission = "0600"
}
 

resource "aws_vpc" "prod-vpc" {
    cidr_block = "10.0.0.0/16"
    tags = {
        Name = "production"
    }
}

resource "aws_internet_gateway" "gw" {
    vpc_id = aws_vpc.prod-vpc.id 
    tags = {
        Name = "igw"
    }
} 

resource "aws_route_table" "prod-route-table" {
    vpc_id = aws_vpc.prod-vpc.id

    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = aws_internet_gateway.gw.id
    } 

    tags = {
        Name = "prod-route-table"
    }
} 

resource "aws_subnet" "subnet-1" {
    vpc_id = aws_vpc.prod-vpc.id
    cidr_block = "10.0.1.0/24"
    availability_zone = "us-east-1a"

    tags = {
        Name = "prod-subnet"
    }
}

resource "aws_route_table_association" "a" {
    subnet_id = aws_subnet.subnet-1.id
    route_table_id = aws_route_table.prod-route-table.id
}

resource "aws_security_group" "allow_web_ssh" {
    name = "allow_web_ssh_traffic"
    description = "allow web & ssh traffic"
    vpc_id = aws_vpc.prod-vpc.id

    ingress {
        description = "HTTPS"
        from_port = 443
        to_port = 443
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        description = "HTTP"
        from_port = 80
        to_port = 80
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    } 

    ingress {
        description = "SSH"
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    } 

    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags = {
        Name = "allow_web_ssh"
    }
} 

resource "aws_network_interface" "web-server-nic" {
    subnet_id = aws_subnet.subnet-1.id
    private_ips = ["10.0.1.50"]
    security_groups = [aws_security_group.allow_web_ssh.id]
} 

resource "aws_eip" "one" {
    #vpc = true
    domain = "vpc" 
    network_interface = aws_network_interface.web-server-nic.id
    associate_with_private_ip = "10.0.1.50"
    depends_on = [aws_internet_gateway.gw]
} 

resource "aws_instance" "web-server-instance" {
  ami           = "ami-0e86e20dae9224db8"
  instance_type = "t2.micro"
  availability_zone = "us-east-1a"
  key_name      = "access-key"

  network_interface {
    device_index         = 0
    network_interface_id = aws_network_interface.web-server-nic.id
  }

  user_data = <<-EOF
                #!/bin/bash
                sudo apt update -y
                sudo apt install apache2 -y
                sudo systemctl start apache2
                sudo systemctl enable apache2
                sudo mkdir -p /var/www/html
                sudo bash -c 'echo "your web server" > /var/www/html/index.html'
                EOF 
    tags = {
        Name = "web-server"
    }
}