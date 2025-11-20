output "m2_subnet_id" {
    description = "ID of m2 subnet"
    value = azurerm_subnet.m2_subnet.id
} 

output "m3_subnet_id" {
    description = "ID of m3 subnet"
    value = azurerm_subnet.m3_subnet.id
} 

output "m2_public_ip_id" {
    description = "ID of m2 public ip"
    value = azurerm_public_ip.m2_public_ip.id
} 

output "m3_public_ip_id" {
    description = "ID  of m3 public ip"
    value = azurerm_public_ip.m3_public_ip.id
} 

output "m2_nic_id" {
    description = "ID of m2 network interface"
    value = azurerm_network_interface.m2_nic.id
}

output "m3_nic_id" {
    description = "ID of m3 network interface"
    value = azurerm_network_interface.m3_nic.id
}