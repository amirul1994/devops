# variable "cidr" {
#     type = string
# } 

variable "create_vpc" {
    type = bool 
} 

# variable "vpc_count" {
#     type = number
#     default = 1 
# } 

variable "vpc_config" {
    type = list(object({
        cidr_block = string,
        enable_dns_hostnames = bool,
        enable_dns_support = bool 
    }))
} 

variable "public_subnet_configs" {
    type = list(object({
        cidr_block = string,
    }))
}