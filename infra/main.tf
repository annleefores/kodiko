terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "annlee-s3-state"
    key            = "kodiko/kodiko.tfstate"
    region         = "us-east-1"
    dynamodb_table = "tf-state-db"
    encrypt        = true
  }

  required_version = "~> 1.6.1"
}

# Configure the AWS Provider
provider "aws" {
  region = var.region
}

module "vpc" {
  source                            = "./vpc"
  region                            = var.region
  vpc_cidr_block                    = var.vpc_cidr_block
  vpc_public_subnet_k8s_cidr_blocks = var.vpc_public_subnet_k8s_cidr_blocks
  vpc_public_subnet_app_cidr_blocks = var.vpc_public_subnet_app_cidr_blocks
  vpc_private_subnet_cidr_blocks    = var.vpc_private_subnet_cidr_blocks
  vpc_azs                           = var.vpc_azs
  vpc_name                          = var.vpc_name
}

# module "jenkins" {
#   source    = "./jenkins"
#   region    = var.region
#   vpc_id    = module.vpc.vpc_id
#   subnet_id = module.vpc.public_app_subnet_id
#   key_name  = var.key_name
# }

module "auth" {
  source                    = "./auth"
  region                    = var.region
  google_client_id          = var.google_client_id
  google_client_secret      = var.google_client_secret
  google_callback_url_main  = var.google_callback_url_main
  google_callback_url_dev   = var.google_callback_url_dev
  google_callback_url_local = var.google_callback_url_local
}

