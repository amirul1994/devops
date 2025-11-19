variable "resource_group_name" {
    description = "Name of the existing resource group"
    type = string
    default = "1-5711e9b3-playground-sandbox"
} 

variable "vnet_name" {
    description = "Name of the existing virtual network"
    type = string 
    default = "vnet-westus"
} 

variable "subnet_prefixes" {
    description = "Subnet address prefixes"
    type = object({
        m2 = string
        m3 = string
    })
    default = {
        m2 = "172.17.0.0/24"
        m3 = "172.17.0.0/24"
    }
} 

variable "location" {
    description = "Azure region"
    type = string
    default = "westus"
}