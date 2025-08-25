variable "vpc_id" {
  type = string
}

variable "subnet_ids" {
  type = list(string)
}

variable "eks_role_arn" {
  type = string
}

resource "aws_security_group" "eks" {
  vpc_id = var.vpc_id
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "eks-sg"
  }
}

resource "aws_eks_cluster" "main" {
  name     = "main-cluster"
  role_arn = var.eks_role_arn
  vpc_config {
    subnet_ids         = var.subnet_ids
    security_group_ids = [aws_security_group.eks.id]
    endpoint_public_access = true
  }
}

output "cluster_name" {
  value = aws_eks_cluster.main.name
}
