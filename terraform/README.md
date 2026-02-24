# 🚀 Terraform Infrastructure for Energy Tracker

This directory contains Terraform configuration to automatically provision and configure your Azure VM infrastructure.

## 📋 What This Does

When you run Terraform, it will:

1. ✅ Create an Azure Resource Group
2. ✅ Set up Virtual Network and Subnet
3. ✅ Create a Public IP address
4. ✅ Configure Network Security Group (firewall rules)
5. ✅ Create Network Interface
6. ✅ Generate SSH key pair automatically
7. ✅ **Create Azure VM (Standard_B1s - ~$10/month)**
8. ✅ **Install Docker automatically**
9. ✅ **Install Docker Compose**
10. ✅ **Create data directories**
11. ✅ **Configure firewall (ports 22, 5000, 5001)**
12. ✅ Output all connection details

**Total setup time: ~5-10 minutes**

---

## 🎯 Prerequisites

### 1. Install Terraform

**Windows:**
```powershell
# Using Chocolatey
choco install terraform

# Or download from: https://www.terraform.io/downloads
```

**Mac:**
```bash
brew install terraform
```

**Linux:**
```bash
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/
```

Verify installation:
```bash
terraform --version
```

---

### 2. Install Azure CLI

**Windows:**
```powershell
# Download and install from:
# https://aka.ms/installazurecliwindows
```

**Mac:**
```bash
brew install azure-cli
```

**Linux:**
```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

Verify installation:
```bash
az --version
```

---

### 3. Login to Azure

```bash
az login
```

This will open a browser for authentication.

After login, set your subscription (if you have multiple):
```bash
# List subscriptions
az account list --output table

# Set active subscription
az account set --subscription "Your Subscription Name"
```

---

## 🚀 Usage

### Step 1: Navigate to Terraform Directory

```bash
cd terraform/
```

### Step 2: Initialize Terraform

```bash
terraform init
```

This downloads the Azure provider plugin.

---

### Step 3: Preview Changes

```bash
terraform plan
```

This shows what will be created without actually creating it.

---

### Step 4: Create Infrastructure

```bash
terraform apply
```

Type `yes` when prompted.

**Wait 5-10 minutes** for:
- Azure resources to be created
- VM to boot up
- Docker to be installed
- All configuration to complete

---

### Step 5: Get Outputs

After successful apply, you'll see:

```
Outputs:

vm_public_ip = "20.123.45.67"
ssh_command = "ssh azureuser@20.123.45.67"
production_url = "http://20.123.45.67:5000"
staging_url = "http://20.123.45.67:5001"

github_secrets_summary = <<EOT
════════════════════════════════════════════════════════
📋 GitHub Secrets Configuration
════════════════════════════════════════════════════════
...
EOT
```

---

### Step 6: Get SSH Private Key

```bash
# Display the private key
terraform output -raw ssh_private_key

# Save to file
terraform output -raw ssh_private_key > azure_vm_key.pem
chmod 600 azure_vm_key.pem
```

**Copy this entire key** (including headers) to your GitHub secret `AZURE_VM_SSH_KEY`

---

### Step 7: Connect to VM

```bash
# Using the generated key
ssh -i azure_vm_key.pem azureuser@<VM_IP>

# Or use the SSH command from outputs
terraform output -raw ssh_command | sh
```

---

### Step 8: Verify Setup

Once connected to VM:

```bash
# Check Docker is installed
docker --version

# Check Docker Compose is installed
docker-compose --version

# Check data directories exist
ls -la ~/data/

# Check if setup is complete
cat ~/.vm-setup-complete
```

---

## 📝 Configuration Options

Edit `variables.tf` to customize:

```hcl
# Change Azure region
variable "location" {
  default = "East US"  # Or "West Europe", "Central India", etc.
}

# Change VM size
variable "vm_size" {
  default = "Standard_B1s"  # Or "Standard_B2s" for more power
}

# Restrict SSH access to your IP
variable "allowed_ssh_ip" {
  default = "1.2.3.4/32"  # Your public IP
}
```

---

## 🔄 Updating Infrastructure

Made changes to Terraform files?

```bash
# See what will change
terraform plan

# Apply changes
terraform apply
```

---

## 🗑️ Destroying Infrastructure

**WARNING: This deletes everything!**

```bash
terraform destroy
```

Type `yes` to confirm.

This will:
- Delete the VM
- Delete all networking
- Delete the resource group
- Free up costs

**Your Docker images on Docker Hub will remain safe**

---

## 💰 Cost Estimation

**Azure Standard_B1s VM:**
- ~$10-15/month (pay-as-you-go)
- ~$7/month (1-year reserved)
- Includes: 1 vCPU, 1GB RAM, 30GB disk
- Similar to AWS t2.micro

**Additional costs:**
- Public IP: ~$3-4/month
- Bandwidth: First 100GB free, then ~$0.087/GB

**Total: ~$13-20/month**

---

## 🎯 Integration with GitHub Actions

After Terraform creates everything:

1. **Get VM IP:**
   ```bash
   terraform output vm_public_ip
   ```

2. **Get SSH Key:**
   ```bash
   terraform output -raw ssh_private_key
   ```

3. **Update GitHub Secrets:**
   - `AZURE_VM_HOST` = VM IP from step 1
   - `AZURE_VM_USER` = `azureuser`
   - `AZURE_VM_SSH_KEY` = Complete SSH key from step 2
   - `DOCKERHUB_USERNAME` = `fpaz531`
   - `DOCKERHUB_TOKEN` = Your Docker Hub token

4. **Push to GitHub** - CI/CD will deploy automatically!

---

## 🔍 Troubleshooting

### Issue: "terraform: command not found"
**Solution:** Install Terraform (see prerequisites)

### Issue: "az: command not found"
**Solution:** Install Azure CLI (see prerequisites)

### Issue: "Azure login failed"
**Solution:** 
```bash
az login
az account set --subscription "Your Subscription"
```

### Issue: "VM not accessible"
**Solution:** 
- Wait 5-10 minutes for cloud-init to complete
- Check NSG rules allow your IP
- Verify VM is running: `az vm list --output table`

### Issue: "Docker not installed"
**Solution:**
```bash
# SSH to VM
ssh azureuser@<VM_IP>

# Check cloud-init status
cloud-init status

# If not complete, wait a few more minutes
# If failed, check logs
sudo cat /var/log/cloud-init-output.log
```

---

## 📚 Terraform Commands Reference

```bash
terraform init          # Initialize (download providers)
terraform plan          # Preview changes
terraform apply         # Create/update infrastructure
terraform destroy       # Delete everything
terraform output        # Show outputs
terraform state list    # List all resources
terraform show          # Show current state
terraform fmt           # Format .tf files
terraform validate      # Validate configuration
```

---

## 🎓 What You Learned

By using this Terraform configuration, you've learned:

- ✅ Infrastructure as Code (IaC)
- ✅ Azure resource provisioning
- ✅ Network security configuration
- ✅ Cloud-init for automated setup
- ✅ SSH key generation
- ✅ Terraform state management
- ✅ Output variables
- ✅ Resource dependencies

---

## 🔒 Security Best Practices

1. **Never commit** `.tfstate` files (contains secrets)
2. **Never commit** `terraform.tfvars` with sensitive data
3. **Use** `.gitignore` for Terraform files
4. **Store** state remotely (Azure Storage) for teams
5. **Restrict** SSH access to your IP only
6. **Rotate** SSH keys regularly
7. **Enable** Azure monitoring

---

## 🌟 Next Steps

After infrastructure is created:

1. ✅ Test SSH connection
2. ✅ Verify Docker installation
3. ✅ Update GitHub Secrets
4. ✅ Push code to trigger deployment
5. ✅ Access your app at VM_IP:5000

---

## 📞 Need Help?

- Terraform Docs: https://www.terraform.io/docs
- Azure Provider: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs
- Azure CLI: https://docs.microsoft.com/en-us/cli/azure/

---

**You now have fully automated infrastructure! One command creates everything.** 🎉
