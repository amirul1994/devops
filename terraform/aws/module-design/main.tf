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
        {
            cidr_block = "10.11.0.0/16",
            enable_dns_hostnames = true,
            enable_dns_support = true            
        }
    ]
 }