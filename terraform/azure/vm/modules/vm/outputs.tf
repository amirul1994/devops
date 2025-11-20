output "vm_id" {
  description = "ID of the virtual machine"
  value = azurerm_linux_virtual_machine.vm.id
} 

output "private_ip" {
  description = "Private IP address of the VM"
  value = azurerm_network_interface.vm_nic.private_ip_address
}