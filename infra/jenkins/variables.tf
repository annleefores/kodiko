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
  default = "ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"
}

variable "ami_owners" {
  type    = list(string)
  default = ["099720109477"]
}

variable "instance_type" {
  type    = string
  default = "t2.large"

}

variable "cpu_credits" {
  type    = string
  default = "unlimited"

}


