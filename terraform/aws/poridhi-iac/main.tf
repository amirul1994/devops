module "vpc" {
    source = "./modules/vpc"
    create_vpc = false
    cidr = "10.10.0.0/16"
 }