variable "resource_group_name" {
  description = "Name of the Azure resource group"
  type        = string
  default     = "energy-tracker-rg"
}

variable "location" {
  description = "Azure region for resources"
  type        = string
  default     = "East US"
  # Other options: "West Europe", "Southeast Asia", "Central India"
}

variable "vm_name" {
  description = "Name of the virtual machine"
  type        = string
  default     = "energy-tracker-vm"
}

variable "vm_size" {
  description = "Size of the virtual machine"
  type        = string
  default     = "Standard_B1s"
  # Standard_B1s is Azure's cheapest option (similar to AWS t2.micro)
  # Options: Standard_B1s (1 vCPU, 1GB RAM), Standard_B2s (2 vCPU, 4GB RAM)
}

variable "admin_username" {
  description = "Admin username for the VM"
  type        = string
  default     = "azureuser"
}

variable "allowed_ssh_ip" {
  description = "IP address allowed to SSH (use your IP for security, or * for any)"
  type        = string
  default     = "*"
  # For better security, set this to your IP: "1.2.3.4/32"
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default = {
    Environment = "Production"
    Project     = "Energy-Tracker"
    ManagedBy   = "Terraform"
  }
}
