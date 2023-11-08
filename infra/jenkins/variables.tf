variable "region" {
  type    = string
  default = "ap-south-1"
}

variable "key_name" {
  type      = string
  sensitive = true
}

variable "vpc_id" {
  type = string
}

variable "subnet_id" {
  type = string
}

variable "ami_image_name" {
  type    = string
  default = "al2023-ami-2023.2.20231030.1-kernel-6.1-x86_64"
}

variable "ami_owners" {
  type    = list(string)
  default = ["137112412989"]
}

variable "instance_type" {
  type    = string
  default = "t2.micro"

}

variable "cpu_credits" {
  type    = string
  default = "unlimited"

}


