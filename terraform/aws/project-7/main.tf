provider "aws" {
    region = var.region
} 

module "vpc1" {
    source = "./modules/vpc"

    vpc_cidr = "10.0.0.0/16"
    public_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
    private_subnets = ["10.0.3.0/24"]
    azs = ["us-east-1a", "us-east-1b"]
    vpc_name = "vpc1"
} 

module "vpc2" {
    source = "./modules/vpc"

    vpc_cidr = "10.1.0.0/16"
    public_subnets = ["10.1.1.0/24", "10.1.2.0/24"]
    private_subnets = ["10.1.3.0/24"]
    azs = ["us-east-1a", "us-east-1b"]
    vpc_name = "vpc2"
} 

module "ec2_vpc1" {
    source = "./modules/ec2"

    vpc_id = module.vpc1.vpc_id
    subnet_id = module.vpc1.private_subnets[0]
    instance_type = "t2.micro"
    key_name = "ssh-key"
} 

module "ec2_vpc2" {
    source = "./modules/ec2"
    
    vpc_id = module.vpc2.vpc_id
    subnet_id = module.vpc2.private_subnets[0]
    instance_type = "t2.micro"
    key_name = "ssh-key"
} 

module "alb_vpc1" {
    source = "./modules/alb"

    vpc_id = module.vpc1.vpc_id
    subnets = module.vpc1.public_subnets
    target_id = module.ec2_vpc1.instance_id
    alb_name = "alb-vpc1"
} 

module "alb_vpc2" {
    source = "./modules/alb"

    vpc_id = module.vpc2.vpc_id
    subnets = module.vpc2.public_subnets
    target_id = module.ec2_vpc2.instance_id
    alb_name = "alb-vpc2"
} 

module "route53" {
    source = "./modules/route53"

    domain_name = "www.uty.com"
    alb_vpc1_dns = module.alb_vpc1.alb_dns_name
    alb_vpc2_dns = module.alb_vpc2.alb_dns_name
    alb_vpc1_zone_id = module.alb_vpc1.alb_zone_id
    alb_vpc2_zone_id = module.alb_vpc2.alb_zone_id
    weight_vpc1 = 155
    weight_vpc2 = 100
}