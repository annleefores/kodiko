terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "annlee-s3-state"
    key            = "kodiko/kodiko_vpc.tfstate"
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

# Create a VPC
resource "aws_vpc" "kodiko_vpc" {
  cidr_block = var.vpc_cidr_block

  tags = {
    Name = var.name
  }
}

resource "aws_subnet" "kodiko_public_subnet" {
  vpc_id                  = aws_vpc.kodiko_vpc.id
  cidr_block              = var.vpc_subnet_cidr_block
  map_public_ip_on_launch = true

  tags = {
    Name = var.name
  }
}
