variable "resource_group_name" {
    description = "Name of the resource group"
    type = string
} 

variable "vnet_name" {
    description = "Name of the virtual network"
    type = string
} 

variable "location" {
    description = "Azure region location"
    type = string
} 

variable "subnet_prefixes" {
    description = "Subnet address prefixes for m2 and m3"
    type = object({
        m2 = string
        m3 = string
    })
}