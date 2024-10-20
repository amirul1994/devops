data "aws_db_instance" "amir_db" {
    db_instance_identifier = "amir-db"
}

data "aws_vpc" "existing_vpc" {
    filter {
        name = "tag:Name"
        values = ["db-vpc"]
    }
} 

data "aws_security_group" "existing_rds_sg" {
    filter {
        name = "tag:Name"
        values = ["rds-sg"]
    }
}

locals {
    source_db = data.aws_db_instance.amir_db.id
}

resource "aws_db_instance" "read_replica" {
   
    count = local.source_db != null ? 1 : 0
    
    identifier = "${lower(local.source_db)}-replica"
    instance_class = "db.t3.micro"
    engine = "mysql"
    replicate_source_db = local.source_db
    
    
    publicly_accessible = false 

    tags = {
        Name = "${lower(local.source_db)}-replica"
    }
}