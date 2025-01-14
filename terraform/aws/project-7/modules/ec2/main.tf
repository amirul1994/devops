resource "aws_security_group" "this" {
    vpc_id = var.vpc_id

    ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    } 

    ingress {
        from_port = 80
        to_port = 80
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
        Name = "ec2-sg"
    }
} 

resource "aws_instance" "this" {
    ami = "ami-0866a3c8686eaeeba"
    instance_type = var.instance_type 
    subnet_id = var.subnet_id
    vpc_security_group_ids = [aws_security_group.this.id]
    key_name = var.key_name 

    user_data = <<-EOF
      #!/bin/bash
      yes | sudo apt update
      yes | sudo apt install apache2
      echo "<h1>Server Details</h1><p><strong>Hostname:</strong> $(hostname)</p><p><strong>IP Address:</strong> $(hostname -I | cut -d" " -f1)</p>" > /var/www/html/index.html
      sudo systemctl restart apache2
    EOF

    tags = {
        Name = "ec2-instance"
    }
}  

resource "aws_key_pair" "this" {
    key_name = var.key_name
    public_key = tls_private_key.this.public_key_openssh
} 

resource "tls_private_key" "this" {
    algorithm = "RSA"
    rsa_bits = 4096
} 

resource "local_file" "private_key" {
    content = tls_private_key.this.private_key_pem 
    filename = "${path.module}/${var.key_name}.pem"
    file_permission = "0400"
}