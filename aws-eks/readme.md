# 🚀 AWS EKS Infrastructure Setup via Terraform

This project provisions a complete **production-ready AWS EKS cluster** using Terraform. It includes:

* Custom VPC with public/private subnets
* EKS control plane with managed node group
* IAM-based RBAC with `eks-admin` user
* Kubernetes provider configuration
* Secure `kubeconfig` access from any EC2 or local machine

---

## 📁 Directory Structure

```
aws-eks/
│
├── main.tf                # VPC, EKS, IAM, kubernetes_config_map (auth)
├── variables.tf           # Input variables
├── versions.tf            # Terraform + provider versions
├── outputs.tf             # Useful outputs (cluster name, kubeconfig command)
└── README.md              # This file
```

---

## 🛠️ Prerequisites

* Terraform >= 1.3.0
* AWS CLI configured with IAM user: **eks-admin**
* kubectl installed and available in \$PATH
* IAM user `eks-admin` must have permissions to:

  * EKS full access
  * EC2/VPC (for VPC module)
  * IAM (to allow role bindings for worker nodes)
  * CloudWatch Logs (for EKS logging)

---

## 🔧 Setup Guide

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd aws-eks/
```

### 2. Configure AWS Profile

Ensure your AWS CLI profile is configured:

```bash
aws configure --profile eks-admin
```

Or manually export:

```bash
export AWS_PROFILE=eks-admin
```

### 3. Initialize Terraform

```bash
terraform init
```

### 4. Preview Plan

```bash
terraform plan
```

### 5. Apply Infrastructure

```bash
terraform apply
```

On success, you’ll see output like:

```bash
Outputs:

cluster_name = "helm-eks-cluster"
cluster_endpoint = "https://....eks.amazonaws.com"
kubeconfig_command = "aws eks update-kubeconfig --region us-east-1 --name helm-eks-cluster --profile eks-admin"
```

---

## 🔐 AWS Auth Config

IAM user `eks-admin` is mapped to Kubernetes `system:masters` group via:

```hcl
manage_aws_auth_configmap = true

aws_auth_users = [
  {
    userarn  = "arn:aws:iam::<account_id>:user/eks-admin"
    username = "eks-admin"
    groups   = ["system:masters"]
  }
]
```

---

## 📱 Connect with kubectl

Update kubeconfig:

```bash
aws eks update-kubeconfig --region us-east-1 --name helm-eks-cluster --profile eks-admin
```

Test the connection:

```bash
kubectl get nodes
```

---

## 📦 What This Infra Creates

### 1. **VPC** (`terraform-aws-modules/vpc/aws`)

* CIDR: `10.0.0.0/16`
* Public subnets: `10.0.101.0/24`, `10.0.102.0/24`
* Private subnets: `10.0.1.0/24`, `10.0.2.0/24`
* NAT Gateway + IGW
* DNS hostnames enabled

### 2. **EKS Cluster** (`terraform-aws-modules/eks/aws`)

* Kubernetes version: 1.29
* Cluster public and private endpoints enabled
* Managed Node Group:

  * Instance type: `t2.medium`
  * Desired: 2
  * Max: 3
  * Min: 1

### 3. **IAM Auth & RBAC**

* `eks-admin` user mapped to `system:masters`
* Auth setup automated by `manage_aws_auth_configmap = true`

---

## 🧰 Useful Terraform Outputs

* `cluster_name`: Your EKS cluster name
* `cluster_endpoint`: API Server endpoint
* `kubeconfig_command`: How to connect with kubectl

---

## 🧹 Cleanup

To destroy the entire infrastructure:

```bash
terraform destroy
```

Make sure you’re in the root `aws-eks/` directory and using the correct AWS profile.

---

## ❗ Common Issues

| Issue                                                                                              | Solution                                                                       |
| -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `You must be logged in to the server (the server has asked for the client to provide credentials)` | Ensure AWS\_PROFILE in kubeconfig is correct and exists                        |
| `AccessDenied` when applying Terraform                                                             | Ensure `eks-admin` IAM user has full permissions for EKS, IAM, EC2, CloudWatch |
| `Unsupported argument: manage_aws_auth_configmap`                                                  | Use module version `v19.21.0` instead of `v20.x` for backwards compatibility   |

---

## 🧠 References

* [Terraform AWS EKS Module](https://github.com/terraform-aws-modules/terraform-aws-eks)
* [AWS EKS Docs](https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html)
* [IAM Roles for Service Accounts (IRSA)](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html)

---

## 👤 Author

* Infra owner: `eks-admin`
* Region: `us-east-1`
* Hosted from EC2: `ap-south-1`

---

## 🏁 Next Steps

* Add Helm charts to deploy apps
* Enable OIDC + IRSA for finer-grained IAM
* Integrate with GitOps or CI/CD pipeline

