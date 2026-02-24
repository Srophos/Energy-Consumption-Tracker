# ⚡ Quick Start - Automated Azure VM Setup

## 🎯 Goal
Create a fully configured Azure VM with Docker in **5 minutes** using Terraform.

---

## 📋 Prerequisites Checklist

- [ ] Terraform installed (`terraform --version`)
- [ ] Azure CLI installed (`az --version`)
- [ ] Logged into Azure (`az login`)
- [ ] Active Azure subscription

---

## 🚀 Steps

### 1. Login to Azure
```bash
az login
```

### 2. Navigate to Terraform Directory
```bash
cd terraform/
```

### 3. Initialize Terraform
```bash
terraform init
```

### 4. Create Everything
```bash
terraform apply
```
Type `yes` when prompted.

⏰ **Wait 5-10 minutes...**

### 5. Get Connection Details
```bash
# VM IP Address
terraform output vm_public_ip

# SSH Command
terraform output ssh_command

# SSH Private Key (for GitHub)
terraform output -raw ssh_private_key
```

### 6. Test Connection
```bash
# Save SSH key
terraform output -raw ssh_private_key > azure_vm_key.pem
chmod 600 azure_vm_key.pem

# Connect
ssh -i azure_vm_key.pem azureuser@$(terraform output -raw vm_public_ip)

# Verify Docker
docker --version
```

### 7. Update GitHub Secrets

Go to: **GitHub Repo → Settings → Secrets → Actions**

Add/Update:
- `AZURE_VM_HOST` = Output from `terraform output vm_public_ip`
- `AZURE_VM_USER` = `azureuser`
- `AZURE_VM_SSH_KEY` = Output from `terraform output -raw ssh_private_key`

### 8. Deploy Your App
```bash
# Push to Development branch
git push origin Development

# GitHub Actions will deploy automatically!
```

---

## ✅ Done!

Your infrastructure is ready!

**Production:** `http://<VM_IP>:5000`  
**Staging:** `http://<VM_IP>:5001`

---

## 🗑️ Clean Up (When Done)

```bash
terraform destroy
```

Type `yes` to delete everything.

---

## 🆘 Problems?

**Can't connect to VM?**
- Wait 5 more minutes for cloud-init
- Check: `cloud-init status --wait`

**No Terraform command?**
- Install from: https://www.terraform.io/downloads

**No Azure CLI?**
- Install from: https://aka.ms/installazurecliwindows

---

**That's it! Infrastructure as Code made easy.** 🎉
