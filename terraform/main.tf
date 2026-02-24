terraform {
  required_version = ">= 1.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Resource Group
resource "azurerm_resource_group" "energy_tracker" {
  name     = var.resource_group_name
  location = var.location

  tags = {
    Environment = "Production"
    Project     = "Energy-Tracker"
    ManagedBy   = "Terraform"
  }
}

# Virtual Network
resource "azurerm_virtual_network" "energy_tracker_vnet" {
  name                = "energy-tracker-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.energy_tracker.location
  resource_group_name = azurerm_resource_group.energy_tracker.name

  tags = {
    Environment = "Production"
    Project     = "Energy-Tracker"
  }
}

# Subnet
resource "azurerm_subnet" "energy_tracker_subnet" {
  name                 = "energy-tracker-subnet"
  resource_group_name  = azurerm_resource_group.energy_tracker.name
  virtual_network_name = azurerm_virtual_network.energy_tracker_vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}

# Public IP
resource "azurerm_public_ip" "energy_tracker_pip" {
  name                = "energy-tracker-pip"
  location            = azurerm_resource_group.energy_tracker.location
  resource_group_name = azurerm_resource_group.energy_tracker.name
  allocation_method   = "Static"
  sku                 = "Standard"

  tags = {
    Environment = "Production"
    Project     = "Energy-Tracker"
  }
}

# Network Security Group
resource "azurerm_network_security_group" "energy_tracker_nsg" {
  name                = "energy-tracker-nsg"
  location            = azurerm_resource_group.energy_tracker.location
  resource_group_name = azurerm_resource_group.energy_tracker.name

  # SSH Access
  security_rule {
    name                       = "SSH"
    priority                   = 300
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  # Production Port
  security_rule {
    name                       = "Production"
    priority                   = 310
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "5000"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  # Staging Port
  security_rule {
    name                       = "Staging"
    priority                   = 320
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "5001"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  tags = {
    Environment = "Production"
    Project     = "Energy-Tracker"
  }
}

# Network Interface
resource "azurerm_network_interface" "energy_tracker_nic" {
  name                = "energy-tracker-nic"
  location            = azurerm_resource_group.energy_tracker.location
  resource_group_name = azurerm_resource_group.energy_tracker.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.energy_tracker_subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.energy_tracker_pip.id
  }

  tags = {
    Environment = "Production"
    Project     = "Energy-Tracker"
  }
}

# Connect NSG to NIC
resource "azurerm_network_interface_security_group_association" "energy_tracker_nsg_assoc" {
  network_interface_id      = azurerm_network_interface.energy_tracker_nic.id
  network_security_group_id = azurerm_network_security_group.energy_tracker_nsg.id
}

# SSH Key
resource "tls_private_key" "energy_tracker_ssh" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

# Virtual Machine
resource "azurerm_linux_virtual_machine" "energy_tracker_vm" {
  name                = var.vm_name
  location            = azurerm_resource_group.energy_tracker.location
  resource_group_name = azurerm_resource_group.energy_tracker.name
  size                = var.vm_size
  admin_username      = var.admin_username

  network_interface_ids = [
    azurerm_network_interface.energy_tracker_nic.id,
  ]

  admin_ssh_key {
    username   = var.admin_username
    public_key = tls_private_key.energy_tracker_ssh.public_key_openssh
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
    disk_size_gb         = 30
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-gen2"
    version   = "latest"
  }

  # Cloud-init to install Docker and setup environment
  custom_data = base64encode(templatefile("${path.module}/cloud-init.yaml", {
    admin_username = var.admin_username
  }))

  tags = {
    Environment = "Production"
    Project     = "Energy-Tracker"
  }
}

# Wait for VM to be ready
resource "null_resource" "wait_for_vm" {
  depends_on = [azurerm_linux_virtual_machine.energy_tracker_vm]

  provisioner "remote-exec" {
    connection {
      type        = "ssh"
      user        = var.admin_username
      private_key = tls_private_key.energy_tracker_ssh.private_key_pem
      host        = azurerm_public_ip.energy_tracker_pip.ip_address
      timeout     = "5m"
    }

    inline = [
      "echo 'Waiting for cloud-init to complete...'",
      "cloud-init status --wait",
      "echo 'VM is ready!'"
    ]
  }
}
