terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket         = "my-terraform-state-bucket-321858344734"
    key            = "state/terraform.tfstate"
    region         = "us-west-2"
    dynamodb_table = "terraform-locks"
  }
}

provider "aws" {
  region = "us-west-2"
}

module "vpc" {
  source = "./vpc"
}

module "ecr" {
  source = "./ecr"
}

module "eks" {
  source       = "./eks"
  vpc_id       = module.vpc.vpc_id
  subnet_ids   = module.vpc.subnet_ids
  eks_role_arn = "arn:aws:iam::321858344734:role/EKSManagedRole"
}
