provider "azurerm" {
    features {}
} 

resource "tls_private_key" "vm_ssh" {
    algorithm = "RSA"
    rsa_bits = 4096
} 

resource "local_file" "ssh_private_key" {
    content = tls_private_key.vm_ssh.private_key_pem
    filename = "azure_vm_key.pem"
    file_permission = "0600"
} 

resource "local_file" "ssh_public_key" {
    content = tls_private_key.vm_ssh.public_key_openssh
    filename = "azure_vm_key.pub"
} 

data "azurerm_virtual_network" "main" {
    name = var.vnet_name
    resource_group_name = data.azurerm_resource_group.main.name

} 

module "security" {
    source = "./modules/security"

    resource_group_name = data.azurerm_resource_group.main.name
    location = data.azurerm_resource_group.main.location
}

module "network" {
    source = "./modules/network"

    resource_group_name = data.azurerm_resource_group.main.name
    vnet_name = data.azurerm_virtual_network.main.name
    location = data.azurerm_resource_group.main.location
    subnet_prefixes = var.subnet_prefixes
}  

module "vm_m2" {
    source = "./modules/vm"

    vm_name = "m2"
    resource_group_name = data.azurerm_resource_group.main.name
    location = data.azurerm_resource_group.main.location
    subnet_id = module.network.m2_subnet_id
    public_ip_id = module.network.m2_public_ip_id
    admin_username = "azureuser"
    ssh_public_key = tls_private_key.vm_ssh.public_key_openssh
    vm_size = "Standard_B2s"
    nsg_id = module.security.nsg_id
}

module "vm_m3" {
    source = "./modules/vm"

    vm_name = "m3"
    resource_group_name = data.azurerm_resource_group.main.name
    location = data.azurerm_resource_group.main.location
    subnet_id = module.network.m3_subnet_id
    public_ip_id = module.network.m3_public_ip_id
    admin_username = "azureuser"
    ssh_public_key = tls_private_key.vm_ssh.public_key_openssh
    vm_size = "Standard_B2s"
    nsg_id = module.security.nsg_id
}