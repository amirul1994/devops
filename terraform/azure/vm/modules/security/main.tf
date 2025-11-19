resource "azurerm_network_security_group" "vm_nsg" {
    name = "vm-nsg"
    location = var.location
    resource_group_name = var.resource_group_name


dynamic "security_rule" {
    for_each = var.security_rules
    content {
        name = security_rule.value.name
        priority = security_rule.value.priority
        direction = security_rule.value.direction
        access = security_rule.value.access
        protocol = security_rule.value.protocol
        source_port_range = security_rule.value.source_port_range
        destination_port_range = security_rule.value.destination_port_range
        source_address_prefix = security_rule.value.source_address_prefix
        destination_address_prefix = security_rule.value.destination_address_prefix
        }
    }
} 

locals {
    k8s_security_rules = [
        {
            name = "SSH"
            priority = 1001
            direction = "Inbound"
            access = "Allow"
            protocol = "Tcp"
            source_port_range = "*"
            destination_port_range = "22"
        },
        {
            name = "HTTPS"
            priority = 1003
            direction = "Inbound"
            access = "Allow"
            protocol = "Tcp"
            source_port_range = "*"
            destination_port_range = "443"
            source_address_prefix = "*"
            destination_address_prefix = "*"
        }, 
        {
            name = "k8s-api"
            priority = 1004
            direction = "Inbound"
            access = "Allow"
            protocol = "Tcp"
            source_port_range = "*"
            destination_port_range = "6443"
            source_address_prefix = "*"
            destination_address_prefix = "*"
        }, 
        {
            name = "k8s-etcd-client"
            priority = 1005
            direction = "Inbound"
            access = "Allow"
            protocol = "Tcp"
            source_port_range = "*"
            destination_port_range = "2379-2380"
            source_address_prefix = "*"
            destination_address_prefix = "*"
        },
        {
            name = "k8s-kubelet"
            priority = 1006
            direction = "Inbound"
            access = "Allow"
            protocol = "Tcp"
            source_port_range = "*"
            destination_port_range = "10250"
            source_address_prefix = "*"
            destination_address_prefix = "*"
        },
        {
            name = "k8s-scheduler-controller"
            priority = 1007
            direction = "Inbound"
            access = "Allow"
            protocol = "Tcp"
            source_port_range = "*"
            destination_port_range = "10257-10259"
            source_address_prefix = "*"
            destination_address_prefix = "*"
        },
        {
            name                       = "K8s-nodeport"
            priority                   = 1008
            direction                  = "Inbound"
            access                     = "Allow"
            protocol                   = "Tcp"
            source_port_range          = "*"
            destination_port_range     = "30000-32767"
            source_address_prefix      = "*"
            destination_address_prefix = "*"
        }
    ]
}