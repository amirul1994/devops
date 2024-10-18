locals {
    vpc_count = length(var.vpc_config)
    public_subnet_configs = length(var.public_subnet_configs)
}

resource "aws_vpc" "this" {
    count = var.create_vpc ? local.vpc_count:0
    cidr_block = var.vpc_config[count.index].cidr_block
}

resource "aws_subnet" "public" {
    count = local.public_subnet_configs ? 1:0
    #vpc_id = 
}