data "aws_availability_zones" "available" {
    state = "available"
}

resource "aws_vpc" "my_vpc" {
    cidr_block = var.vpc_cidr
    enable_dns_support = true 
    enable_dns_hostnames = true
} 

resource "aws_subnet" "public" {
    count = length(var.public_subnets)
    vpc_id = aws_vpc.my_vpc.id 
    cidr_block = var.public_subnets[count.index]
    availability_zone = data.aws_availability_zones.available.names[count.index]
    map_public_ip_on_launch = true 
} 

resource "aws_subnet" "private" {
    count = length(var.private_subnets)
    vpc_id = aws_vpc.my_vpc.id
    cidr_block = var.private_subnets[count.index]
    availability_zone = data.aws_availability_zones.available.names[count.index]
} 

resource "aws_internet_gateway" "igw" {
    vpc_id = aws_vpc.my_vpc.id
} 

resource "aws_route_table" "public_rt" {
    vpc_id = aws_vpc.my_vpc.id

    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = aws_internet_gateway.igw.id
    }
} 

resource "aws_route_table_association" "public_rta" {
    count = length(var.public_subnets)
    subnet_id = aws_subnet.public[count.index].id 
    route_table_id = aws_route_table.public_rt.id
} 

resource "aws_nat_gateway" "nat_gw" {
    allocation_id = aws_eip.nat_eip.id
    subnet_id = aws_subnet.public[0].id
} 

resource "aws_eip" "nat_eip" {
    domain = "vpc" 
} 

resource "aws_route_table" "private_rt" {
    vpc_id = aws_vpc.my_vpc.id 

    route {
        cidr_block = "0.0.0.0/0"
        nat_gateway_id = aws_nat_gateway.nat_gw.id
    }
} 

resource "aws_route_table_association" "private_rta" {
    count = length(var.private_subnets)
    subnet_id = aws_subnet.private[count.index].id
    route_table_id = aws_route_table.private_rt.id
}

resource "aws_security_group" "alb_sg" {
    vpc_id = aws_vpc.my_vpc.id

    ingress {
        from_port = 80
        to_port = 80
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    } 

    ingress {
        from_port = 443
        to_port = 443
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    } 

    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
} 

resource "aws_security_group" "ec2_sg" {
    vpc_id = aws_vpc.my_vpc.id

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
        security_groups = [aws_security_group.alb_sg.id]
    } 

    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}