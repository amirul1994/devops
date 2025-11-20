resource "azurerm_network_interface_security_group_association" "vm_nsg" {
  network_interface_id = var.nic_id 
  network_security_group_id = var.nsg_id
} 

resource "azurerm_linux_virtual_machine" "vm" {
  name = var.vm_name
  resource_group_name = var.resource_group_name
  location = var.location
  size = var.vm_size
  admin_username = var.admin_username
  network_interface_ids = [var.nic_id]

  admin_ssh_key {
    username = var.admin_username
    public_key = var.ssh_public_key
  } 

  os_disk {
    caching = "ReadWrite"
    storage_account_type = "Standard"
    disk_size_gb = var.disk_size_gb
  } 

  source_image_reference {
    publisher = "Canonical"
    offer = "0001-com-ubuntu-server-jammy"
    sku = "22_04-lts-gen2"
    version = "latest"
  }
}