resource "azurerm_subnet" "m2_subnet" {
    name = "snet-westus-1"
    resource_group_name = var.resource_group_name
    virtual_network_name = var.vnet_name
    address_prefixes = [var.subnet_prefixes.m2]
} 

resource "azurerm_subnet" "m3_subnet" {
    name = "snet-westus-1"
    resource_group_name = var.resource_group_name
    virtual_network_name = var.vnet_name
    address_prefixes = [var.subnet_prefixes.m3]
} 

resource "azurerm_public_ip" "m2_public_ip" {
    name = "m2_public_ip"
    location = var.location
    resource_group_name = var.resource_group_name
    allocation_method = "Static"
    sku = "Standard"
} 

resource "azurerm_public_ip" "m3_public_ip" {
    name = "m3_public_ip"
    location = var.location
    resource_group_name = var.resource_group_name
    allocation_method = "Static"
    sku = "Standard"
} 

resource "azurerm_network_interface" "m2_nic" {
    name = "m2-nic"
    location = var.location
    resource_group_name = var.resource_group_name

    ip_configuration {
        name = "internal"
        subnet_id = azurerm_subnet.m2_subnet.id
        private_ip_address_allocation = "Static"
        private_ip_address = "172.17.0.5"
        public_ip_address_id = azurerm_public_ip.m2_public_ip.id
    }
} 

resource "azurerm_network_interface" "m3_nic" {
    name = "m3-nic"
    location = var.location
    resource_group_name = var.resource_group_name

    ip_configuration {
        name = "internal"
        subnet_id = azurerm_subnet.m3_subnet.id
        private_ip_address_allocation = "Static"
        private_ip_address = "172.17.0.6"
        public_ip_address_id = azurerm_public_ip.m3_public_ip.id
    }
}