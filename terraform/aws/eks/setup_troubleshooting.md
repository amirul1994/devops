***

# EKS Cluster Setup Guide & Troubleshooting Notes

**Date:** June 12, 2026
**Status:** ✅ Successful Deployment
**Infrastructure:** AWS EKS (v1.31), VPC, Managed Node Groups (AL2023)

## 1. Project Structure

Ensure your directory contains the following files:

```text
.
├── vpc.tf
├── eks.tf
├── security_group.tf
├── variables.tf      # Contains variable definitions
├── versions.tf       # Provider constraints
├── outputs.tf        # Output values
└── terraform.tfvars  # (Optional) Variable values
```

## 2. Configuration Files

### `versions.tf`
Defines provider versions to ensure compatibility with EKS Module v21+.

```hcl
terraform {
  required_version = ">= 0.12"
  required_providers {
    random = {
      source  = "hashicorp/random"
      version = "~> 3.1.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">=2.7.1"
    }
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.40"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.1.0"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.1.0"
    } 
    cloudinit = {
      source  = "hashicorp/cloudinit"
      version = "~> 2.2.0"
    }
  }
}
```

### `variables.tf`
*(Note: Ensure this file exists with the variables referenced in other files)*

```hcl
variable "kubernetes_version" {
  default     = "1.31"
  description = "Kubernetes version"
}

variable "vpc_cidr" {
  default     = "10.0.0.0/16"
  description = "Default CIDR range of the VPC"
}

variable "aws_region" {
  default     = "us-east-1"
  description = "AWS Region"
}
```

### `vpc.tf`
Creates the VPC with specific tags required for EKS load balancers.

```hcl
provider "aws" {
  region = var.aws_region
}

data "aws_availability_zones" "available" {}

locals {
  cluster_name = "amirul-eks-${random_string.suffix.result}"
}

resource "random_string" "suffix" {
  length  = 8
  special = false
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.7.0"

  name = "amirul-eks-vpc"
  cidr = var.vpc_cidr
  
  azs             = data.aws_availability_zones.available.names
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.4.0/24", "10.0.5.0/24"]
  
  enable_nat_gateway     = true
  single_nat_gateway     = true
  enable_dns_hostnames   = true
  enable_dns_support     = true

  tags = {
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
  }

  public_subnet_tags = {
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
    "kubernetes.io/role/elb"                      = "1"
  }

  private_subnet_tags = {
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
    "kubernetes.io/role/internal-elb"             = "1"
  }
}
```

### `security_group.tf`
Allows necessary traffic for worker nodes.

```hcl
resource "aws_security_group" "all_worker_mgmt" {
  name_prefix = "all_worker_management"
  vpc_id      = module.vpc.vpc_id
}

resource "aws_security_group_rule" "all_worker_mgmt_ingress" {
  description       = "allow inbound traffic from eks"
  from_port         = 0
  protocol          = "-1"
  to_port           = 0
  security_group_id = aws_security_group.all_worker_mgmt.id
  type              = "ingress"
  cidr_blocks = [
    "10.0.0.0/8",
    "172.16.0.0/12",
    "192.168.0.0/16",
  ]
}

resource "aws_security_group_rule" "all_worker_mgmt_egress" {
  description       = "allow outbound traffic to anywhere"
  from_port         = 0
  protocol          = "-1"
  security_group_id = aws_security_group.all_worker_mgmt.id
  to_port           = 0 
  type              = "egress"
  cidr_blocks       = ["0.0.0.0/0"]
}
```

### `eks.tf`
Provisions the EKS cluster using Module v21+, AL2023 AMIs, and essential addons.

```hcl
data "aws_caller_identity" "current" {}

module "eks" {
  source             = "terraform-aws-modules/eks/aws"
  version            = "~> 21.0"
  name               = local.cluster_name
  kubernetes_version = var.kubernetes_version

  enable_irsa = true

  tags = {
    cluster = "demo"
  }

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  # Essential Addons
  addons = {
    coredns = {
      most_recent = true
    }
    kube-proxy = {
      most_recent = true
    }
    vpc-cni = {
      most_recent                   = true
      before_compute                = true
      resolve_conflicts_on_create   = "OVERWRITE"
      resolve_conflicts_on_update   = "OVERWRITE"
    }
  }

  # Access Entry for Admin
  access_entries = {
    admin = {
      principal_arn = data.aws_caller_identity.current.arn
      policy_associations = {
        admin = {
          policy_arn = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy"
          access_scope = {
            type = "cluster"
          }
        }
      }
    }
  }

  eks_managed_node_groups = {
    node_group = {
      name        = "node-group"
      min_size    = 2
      max_size    = 6
      desired_size = 2

      instance_types = ["t3.medium"]
      # Using AL2023 as AL2 is deprecated/unavailable for newer K8s versions
      ami_type            = "AL2023_x86_64_STANDARD"
      ami_release_version = null 
      
      vpc_security_group_ids = [aws_security_group.all_worker_mgmt.id]
    }
  }
}
```

### `outputs.tf`

```hcl
output "cluster_id" {
  description = "EKS cluster ID"
  value       = module.eks.cluster_id
}

output "cluster_endpoint" {
  description = "Endpoint for EKS control plane"
  value       = module.eks.cluster_endpoint
}

output "cluster_security_group_id" {
  description = "Security group ids attached to the cluster control plane."
  value       = module.eks.cluster_security_group_id
}

output "region" {
  description = "AWS region"
  value       = var.aws_region
}

output "oidc_provider_arn" {
  value = module.eks.oidc_provider_arn
}
```

---

## 3. Deployment Steps

1.  **Initialize Terraform:**
    ```bash
    terraform init
    ```

2.  **Plan the Infrastructure:**
    ```bash
    terraform plan -out=tfplan
    ```

3.  **Apply the Configuration:**
    ```bash
    terraform apply tfplan
    ```

4.  **Configure `kubectl`:**
    Once applied, update your kubeconfig to access the cluster:
    ```bash
    aws eks update-kubeconfig --region us-east-1 --name $(terraform output -raw cluster_id)
    ```

5.  **Verify Connectivity:**
    ```bash
    kubectl get nodes
    kubectl get pods -n kube-system
    ```


## Network Access & Security Considerations

- **`kubectl` Access**: 
  - Does **not** require OIDC or an Ingress Controller.
  - Relies on **AWS IAM Authentication** (configured via `aws eks update-kubeconfig`).
  - Since the EKS endpoint is **Private** in this configuration, you cannot access it from the public internet. You must use a **VPN**, **Bastion Host**, or **Direct Connect** to reach the control plane. 
  - *Note: Enabling Public Endpoint access is discouraged in production environments due to security risks.*

- **OIDC Provider**: 
  - Required for **IRSA** (IAM Roles for Service Accounts) to allow Pods to securely access AWS services. It is **not** used for user/admin authentication to the cluster.

- **Ingress Controller**: 
  - Required to expose Kubernetes Services (e.g., Web Apps) to the internet via an Application Load Balancer (ALB). It is **not** required for cluster management or `kubectl` operations.

---

## 4. Troubleshooting Guide

### Issue 1: `elastic_gpu_specifications` Block Error

**Error Message:**
```text
Error: Unsupported block type
Blocks of type "elastic_gpu_specifications" are not expected here.
```

**Root Cause:**
AWS Provider 6.x (or late 5.x) removed deprecated arguments that older versions of the EKS module were attempting to use.

**Solution:**
1.  Upgrade the EKS module to **v21.x**.
2.  Ensure the AWS provider version is compatible.

**Fix in `versions.tf`:**
```hcl
aws = {
  source  = "hashicorp/aws"
  version = ">= 5.40" # Or "~> 5.0" if strict compatibility is needed
}
```

---

### Issue 2: `cluster_name` and `cluster_version` Arguments Not Expected

**Error Message:**
```text
Error: Unsupported argument
An argument named "cluster_name" is not expected here.
```

**Root Cause:**
Module v21.x changed input variable names to align with standard AWS naming conventions.

**Solution:**
Update your `eks.tf` module block arguments:
*   Change `cluster_name` → `name`
*   Change `cluster_version` → `kubernetes_version`

---

### Issue 3: SSM Parameter Not Found (AMI Lookup Failure)

**Error Message:**
```text
Error: reading SSM Parameter (/aws/service/eks/optimized-ami/1.34/amazon-linux-2/recommended/release_version): couldn't find resource
```

**Root Cause:**
1.  The specified Kubernetes version (e.g., 1.34) may not be generally available yet.
2.  **Amazon Linux 2 (AL2)** AMIs are no longer published for newer Kubernetes versions (deprecated as of late 2025).

**Solution:**
Switch to **Amazon Linux 2023 (AL2023)** and bypass the specific release version lookup by setting it to `null`.

**Fix in `eks.tf`:**
```hcl
eks_managed_node_groups = {
  node_group = {
    ami_type            = "AL2023_x86_64_STANDARD" # Use AL2023
    ami_release_version = null                     # Let AWS pick the latest compatible
  }
}
```

---

### Issue 4: CNI Plugin Not Initialized

**Error Message:**
```text
container runtime network not ready: NetworkReady=false reason:NetworkPluginNotReady 
message:Network plugin returns error: cni plugin not initialized
```

**Root Cause:**
The AWS VPC CNI add-on was not automatically installed or failed to initialize on the worker nodes.

**Solution:**
Explicitly define the `addons` block in the EKS module to ensure `vpc-cni`, `coredns`, and `kube-proxy` are installed before compute resources are created.

**Fix in `eks.tf`:**
```hcl
module "eks" {
  # ... other config
  
  addons = {
    coredns = {
      most_recent = true
    }
    kube-proxy = {
      most_recent = true
    }
    vpc-cni = {
      most_recent                 = true
      before_compute              = true
      resolve_conflicts_on_create = "OVERWRITE"
      resolve_conflicts_on_update = "OVERWRITE"
    }
  }
}
```

**Verification Commands:**
```bash
# List installed add-ons
aws eks list-addons --cluster-name YOUR_CLUSTER_NAME --region us-east-1

# Check aws-node pods status
kubectl get pods -n kube-system | grep aws-node

# If stuck, force restart the CNI daemonset pods
kubectl delete pods -n kube-system -l k8s-app=aws-node
```

---

### Issue 5: Nodes Stuck in `NotReady` State

**Symptoms:**
*   `terraform apply` completes successfully.
*   EC2 instances are running in the console.
*   `kubectl get nodes` shows status `NotReady`.

**Root Causes & Solutions:**

1.  **CNI Issue:** See *Issue 4*. Ensure `aws-node` pods are running.
2.  **Security Group Misconfiguration:**
    *   Ensure the Worker Node Security Group allows inbound traffic from the Cluster Security Group (or the VPC CIDR).
    *   In our setup, `security_group.tf` allows all internal RFC1918 traffic, which should cover this.
3.  **IAM Permissions (IRSA/Kubelet):**
    *   Ensure the Node IAM Role has the `AmazonEKSWorkerNodePolicy`, `AmazonEC2ContainerRegistryReadOnly`, and `AmazonEKS_CNI_Policy`.
    *   The Terraform EKS module v21 handles this automatically, but verify if custom roles are used.
4.  **Subnet Tagging:**
    *   Ensure private subnets have the tag: `kubernetes.io/cluster/<cluster-name>: shared`.
    *   Our `vpc.tf` includes this in `private_subnet_tags`.

**Debugging Commands:**
```bash
# Check node events for specific errors
kubectl describe node <node-name>

# Check kubelet logs on the EC2 instance (requires SSM Session Manager or SSH)
sudo journalctl -u kubelet -f

# Verify Security Groups attached to the ENI of the worker node
aws ec2 describe-network-interfaces --filters "Name=attachment.instance-id,Values=<instance-id>"
```