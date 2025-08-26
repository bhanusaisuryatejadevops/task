terraform {
  required_version = ">= 1.4.0"

  backend "s3" {
    bucket         = "my-terraform-state-bucket"
    key            = "aws-infra/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-lock"
    encrypt        = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.10"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

module "vpc" {
  source  = "./modules/vpc"
}

module "ecr" {
  source = "./modules/ecr"
}

module "eks" {
  source       = "./modules/eks"
  vpc_id       = module.vpc.vpc_id
  subnets      = module.vpc.private_subnets
  ecr_repo_url = module.ecr.repository_url
}