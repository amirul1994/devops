module "vpc" {
    source = "./modules/vpc"
    #vpc_count = 1
    create_vpc = true 
    #cidr = "10.10.0.0/16"
    vpc_config = [
        {
            cidr_block = "10.10.0.0/16",
            enable_dns_hostnames = true,
            enable_dns_support = true
        },
    ]

    public_subnet_configs = [
        {
            cidr_block = "10.10.1.0/24",
            availability_zone = "us-east-1a"
        },
    ] 

    private_subnet_configs = [
        {
            cidr_block = "10.10.2.0/24",
            availability_zone = "us-east-1a"
        }, 
    ]
 }