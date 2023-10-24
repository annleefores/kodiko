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
  region = var.region
}

# Create a VPC
resource "aws_vpc" "kodiko_vpc" {
  cidr_block = var.vpc_cidr_block

  tags = {
    Name = var.name
  }
}

resource "aws_internet_gateway" "kodiko-igw" {
  vpc_id = aws_vpc.kodiko_vpc.id

  tags = {
    Name = var.name
  }
}


