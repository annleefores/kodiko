variable "vpc_cidr_block" {
  type    = string
  default = "10.0.0.0/16"
}

variable "vpc_subnet_cidr_block" {
  type    = string
  default = "10.0.0.0/24"
}

variable "name" {
  type    = string
  default = "kodiko"
}
