provider "aws" {
    region = "us-east-1"
} 

resource "aws_vpc" "db_vpc" {
    cidr_block = "192.168.0.0/16"
    enable_dns_support = true 
    enable_dns_hostnames = true

    lifecycle {
        create_before_destroy = true
    } 
    
    tags = {
        Name = "db-vpc"
    }
} 

resource "aws_subnet" "pub_sbnt" {
    vpc_id = aws_vpc.db_vpc.id
    cidr_block = "192.168.10.0/24"
    map_public_ip_on_launch = true
    availability_zone = "us-east-1a"

    tags = {
        Name = "pub-sbnt"
    }
} 

resource "aws_subnet" "priv_sbnt_1" {
    vpc_id = aws_vpc.db_vpc.id 
    cidr_block = "192.168.20.0/24"
    availability_zone = "us-east-1a"

    tags = {
        Name = "priv-sbnt-1"
    }
} 

resource "aws_subnet" "priv_sbnt_2" {
    vpc_id = aws_vpc.db_vpc.id
    cidr_block = "192.168.30.0/24"
    availability_zone = "us-east-1b"

    tags = {
        Name = "priv-sbnt-2"
    }
} 

resource "aws_subnet" "priv_sbnt_3" {
    vpc_id = aws_vpc.db_vpc.id
    cidr_block = "192.168.40.0/24"
    availability_zone = "us-east-1b"

    tags = {
        Name = "priv-sbnt-3"
    }
} 

resource "aws_subnet" "priv_sbnt_4" {
    vpc_id = aws_vpc.db_vpc.id
    cidr_block = "192.168.50.0/24"
    availability_zone = "us-east-1c"

    tags = {
        Name = "priv-sbnt-4"
    }
} 

resource "aws_internet_gateway" "igw" {
    vpc_id = aws_vpc.db_vpc.id 
    
    tags = {
        Name = "igw"
    }
} 

resource "aws_route_table" "pub_rtb" {
    vpc_id = aws_vpc.db_vpc.id

    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = aws_internet_gateway.igw.id
    } 

    tags = {
        Name = "pub-rtb"
    }
}

resource "aws_route_table_association" "pub_rtb_assoc" {
    subnet_id = aws_subnet.pub_sbnt.id 
    route_table_id = aws_route_table.pub_rtb.id
} 

resource "aws_eip" "elip" {
    domain = "vpc"
} 

resource "aws_nat_gateway" "ngw" {
    allocation_id = aws_eip.elip.id
    subnet_id = aws_subnet.pub_sbnt.id

    lifecycle {
        create_before_destroy = true
    } 

    tags = {
        Name = "db-ngw"
    }
} 

resource "aws_route_table" "priv_rtb" {
    vpc_id = aws_vpc.db_vpc.id 

    route {
        cidr_block = "0.0.0.0/0"
        nat_gateway_id = aws_nat_gateway.ngw.id
    } 

    lifecycle {
        create_before_destroy = true
    }
    
    tags = {
        Name = "priv-rtb"
    }  
} 

resource "aws_route_table_association" "priv_assoc_1" {
    subnet_id = aws_subnet.priv_sbnt_1.id 
    route_table_id = aws_route_table.priv_rtb.id
    
    lifecycle {
        create_before_destroy = true
    }
} 

resource "aws_route_table_association" "priv_assoc_2" {
    subnet_id = aws_subnet.priv_sbnt_2.id
    route_table_id = aws_route_table.priv_rtb.id

    lifecycle {
        create_before_destroy = true
    }
} 

resource "aws_route_table_association" "priv_assoc_3" {
    subnet_id = aws_subnet.priv_sbnt_3.id
    route_table_id = aws_route_table.priv_rtb.id

    lifecycle {
        create_before_destroy = true
    }
} 

resource "aws_route_table_association" "priv_assoc_4" {
    subnet_id = aws_subnet.priv_sbnt_4.id 
    route_table_id = aws_route_table.priv_rtb.id

    lifecycle {
        create_before_destroy = true
    }
} 

resource "aws_security_group" "rds_sg" {
    vpc_id = aws_vpc.db_vpc.id 

    ingress {
        from_port = 3306
        to_port = 3306
        protocol = "tcp"
        cidr_blocks = ["192.168.0.0/16"]
    } 

    egress {
        from_port = 0
        to_port = 0 
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    } 

    tags = {
        Name = "rds-sg"
    }
} 

resource "aws_db_subnet_group" "rds_sbnt_grp" {
    name = "rds-sbnt-grp" 

    subnet_ids = [
        aws_subnet.priv_sbnt_1.id,
        aws_subnet.priv_sbnt_2.id,
        aws_subnet.priv_sbnt_3.id,
        aws_subnet.priv_sbnt_4.id
    ] 

    tags = {
        Name = "rds-subnt-grp"
    }
} 

variable "rds_passwd" {
    description = "the password for the rds master user"
    type = string 

    sensitive = true
}

resource "aws_db_instance" "mysql_rds" {
    identifier = "amir-db"
    engine = "mysql"
    
    instance_class = "db.t3.micro"
    allocated_storage = 30 
    storage_type = "gp2"
    engine_version = "8.0.32"
    username = "admin"
    password = var.rds_passwd
    
    db_subnet_group_name = aws_db_subnet_group.rds_sbnt_grp.name
    multi_az = true
    publicly_accessible = false
    skip_final_snapshot = false 
    backup_retention_period = 1 

    vpc_security_group_ids = [aws_security_group.rds_sg.id] 

    lifecycle {
        create_before_destroy = true
    }

    tags = {
        Name = "amir-mysql"
    }

}

resource "tls_private_key" "bastion_ssh_key" {
    algorithm = "RSA"
    rsa_bits = 4096
} 

resource "aws_key_pair" "bastion_key" {
    key_name = "bastion-key"
    public_key = tls_private_key.bastion_ssh_key.public_key_openssh
} 

resource "local_file" "private_key" {
    content = tls_private_key.bastion_ssh_key.private_key_pem
    filename = "${path.module}/bastion-key.pem"
} 

resource "aws_security_group" "bastion_sg" {
    vpc_id = aws_vpc.db_vpc.id

    ingress {
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
        Name = "bastion-ng"
    }
}

resource "aws_instance" "bastion" {
    ami = "ami-0866a3c8686eaeeba"
    instance_type = "t2.micro"
    subnet_id = aws_subnet.pub_sbnt.id 
    key_name = aws_key_pair.bastion_key.key_name

    vpc_security_group_ids = [aws_security_group.bastion_sg.id]

    tags = {
        Name = "bastion-host"
    }
} 

output "bastion_public_ip" {
    value = aws_instance.bastion.public_ip
}