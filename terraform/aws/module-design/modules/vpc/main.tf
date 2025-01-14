locals {
    vpc_count = length(var.vpc_config)
    public_subnet_count = length(var.public_subnet_configs)
    private_subnet_count = length(var.private_subnet_configs)
}

resource "aws_vpc" "this" {
    count = var.create_vpc ? local.vpc_count:0
    cidr_block = element(var.vpc_config, count.index).cidr_block
    enable_dns_support = element(var.vpc_config, count.index).enable_dns_support
    enable_dns_hostnames = element(var.vpc_config, count.index).enable_dns_hostnames
}

resource "aws_subnet" "public" {
    count = local.public_subnet_count > 0 ? local.public_subnet_count : 0
    vpc_id = aws_vpc.this[count.index].id 
    cidr_block = lookup(var.public_subnet_configs[count.index], "cidr_block", "10.0.1.0/24")
    availability_zone = lookup(var.public_subnet_configs[count.index], "availability_zone", "us-east-1a")
} 

resource "aws_subnet" "private" {
    count = local.private_subnet_count > 0 ? local.private_subnet_count : 0
    vpc_id = aws_vpc.this[count.index].id
    cidr_block = lookup(var.private_subnet_configs[count.index], "cidr_block", "10.0.2.0/24")
    availability_zone = lookup(var.private_subnet_configs[count.index], "availability_zone", "us-east-1b")
} 

# resource "aws_subnet" "merged_subnet" {
#     count = local.public_subnet_count > 0 ? local.public_subnet_count : 0
#     vpc_id = aws_vpc.this[count.index].id
#     cidr_block = coalescelist([lookup(var.public_subnet_configs[count.index], "cidr_block", null), "10.0.1.0/24"])[0]
# } 

output "subnet_ids" {
    value = coalesce(
        aws_subnet.public.*.id,
        aws_subnet.private.*.id
    )
}