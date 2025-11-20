variable "vm_name" {
  description = "Name of the resource group"
  type = string
}

variable "resource_group_name" {
  description = "Name of the resource group"
  type = string
}

variable "location" {
  description = "Azure region location"
  type = string
}

variable "subnet_id" {
    description = "ID of the subnet to attach"
    type = string
}

variable "public_ip_id" {
  description = "ID of the public ip to attach"
  type = string
} 

variable "admin_username" {
  description = "Admin username for the VM"
  type = string
}

variable "ssh_public_key" {
  description = "SSH public key for authentication"
  type = string
} 

variable "vm_size" {
  description = "Size of the virtual machine"
  type = string
  default = "Standard_B2s"
} 

variable "disk_size_gb" {
  description = "OS disk size in gb"
  type = number
  default = 30
} 

variable "nsg_id" {
  description = "Network Seciurity Group ID"
  type = string
} 

variable "nic_id" {
  description = "Network Interface ID (optional - will be created if not provided)"
  type = string
  default = null
}