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
  region = "ap-south-1"
}

module "vpc" {
  source = "./vpc"

  region = var.region
}
