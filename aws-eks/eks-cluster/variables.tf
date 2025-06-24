variable "cluster_name" {
  default = "helm-eks-cluster"
}
variable "aws_region" {
  default = "us-east-1"
}
variable "node_instance_type" {
  default = "t2.medium"
}
variable "desired_capacity" {
  default = 2
}
variable "max_capacity" {
  default = 3
}
variable "min_capacity" {
  default = 1
}

variable "admin_user_arn" {
  description = "IAM user or role ARN to be mapped as system:masters"
  default     = "arn:aws:iam::207567778537:user/eks-admin"
}

variable "aws_profile" {
  default = "eks-admin"
}
