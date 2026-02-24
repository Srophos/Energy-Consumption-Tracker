output "vm_public_ip" {
  description = "Public IP address of the VM"
  value       = azurerm_public_ip.energy_tracker_pip.ip_address
}

output "vm_name" {
  description = "Name of the VM"
  value       = azurerm_linux_virtual_machine.energy_tracker_vm.name
}

output "ssh_command" {
  description = "SSH command to connect to the VM"
  value       = "ssh ${var.admin_username}@${azurerm_public_ip.energy_tracker_pip.ip_address}"
}

output "ssh_private_key" {
  description = "Private SSH key (save this securely!)"
  value       = tls_private_key.energy_tracker_ssh.private_key_pem
  sensitive   = true
}

output "ssh_public_key" {
  description = "Public SSH key"
  value       = tls_private_key.energy_tracker_ssh.public_key_openssh
}

output "production_url" {
  description = "Production application URL"
  value       = "http://${azurerm_public_ip.energy_tracker_pip.ip_address}:5000"
}

output "staging_url" {
  description = "Staging application URL"
  value       = "http://${azurerm_public_ip.energy_tracker_pip.ip_address}:5001"
}

output "resource_group_name" {
  description = "Name of the resource group"
  value       = azurerm_resource_group.energy_tracker.name
}

output "github_secrets_summary" {
  description = "Summary of values needed for GitHub Secrets"
  value = <<-EOT
  
  ════════════════════════════════════════════════════════
  📋 GitHub Secrets Configuration
  ════════════════════════════════════════════════════════
  
  Add these to: GitHub Repo → Settings → Secrets → Actions
  
  1. AZURE_VM_HOST
     Value: ${azurerm_public_ip.energy_tracker_pip.ip_address}
  
  2. AZURE_VM_USER
     Value: ${var.admin_username}
  
  3. AZURE_VM_SSH_KEY
     Get value with: terraform output -raw ssh_private_key
  
  4. DOCKERHUB_USERNAME
     Value: fpaz531
  
  5. DOCKERHUB_TOKEN
     Value: <your Docker Hub token>
  
  ════════════════════════════════════════════════════════
  🌐 Application URLs
  ════════════════════════════════════════════════════════
  
  Production: http://${azurerm_public_ip.energy_tracker_pip.ip_address}:5000
  Staging:    http://${azurerm_public_ip.energy_tracker_pip.ip_address}:5001
  
  ════════════════════════════════════════════════════════
  EOT
}
