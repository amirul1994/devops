# provider "aws" {
#     region = "us-west-2"
#     alias = "west"
# }

data "aws_caller_identity" "current" {
    #provider = aws
}

resource "aws_vpc" "replica_vpc" {
    cidr_block = "192.169.0.0/16"
    enable_dns_support = true 
    enable_dns_hostnames = true

    tags = {
        Name = "replica-vpc"
    }
} 

resource "aws_subnet" "replica_priv_subnet_a" {
    vpc_id = aws_vpc.replica_vpc.id
    cidr_block = "192.169.30.0/24"
    availability_zone = "us-east-1a"

    tags = {
        Name = "replica-priv-subnet-a"
    }
} 

resource "aws_subnet" "replica_priv_subnet_b" {
    vpc_id = aws_vpc.replica_vpc.id
    cidr_block = "192.169.31.0/24"
    availability_zone = "us-east-1b"

    tags = {
        Name = "replica-priv-subnet-b"
    }
}

resource "aws_security_group" "replica_rds_sg" {
    vpc_id = aws_vpc.replica_vpc.id

    ingress {
        from_port = 3306
        to_port = 3306
        protocol = "tcp"
        cidr_blocks = ["192.169.0.0/16"]
    }

    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags = {
        Name = "replica-rds-sg"
    }
} 

resource "aws_db_subnet_group" "replica_rds_subnet_group" {
    name = "replica-rds-subnet-group"
    subnet_ids = [aws_subnet.replica_priv_subnet_a.id, aws_subnet.replica_priv_subnet_b.id]

    tags = {
        Name = "replica-rds-subnet-group"
    }
} 

resource "aws_db_instance" "read_replica" {
    #provider = aws.west
    identifier = "amir-db-replica"
    instance_class = "db.t3.micro"
    engine = "mysql"
    replicate_source_db = "arn:aws:rds:us-east-1:${data.aws_caller_identity.current.account_id}:db:amir-db"
    db_subnet_group_name = aws_db_subnet_group.replica_rds_subnet_group.name
    vpc_security_group_ids = [aws_security_group.replica_rds_sg.id]
    publicly_accessible = false 

    tags = {
        Name = "amir-mysql-replica"
    }
}