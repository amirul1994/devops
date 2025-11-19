variable "resource_group_name" {
    description = "Name of the resource group"
    type = string
}

variable "location" {
    description = "Azure region location"
    type = string
}

variable "security_rules" {
    description = "Custom security rules to add"
    type = list(object({
        name = string
        priority = number
        direction = string
        access = string
        protocol = string
        source_port_range = string
        destination_port_range = string
        source_address_prefix = string
        destination_address_prefix = string
    })) 
    default = []
}