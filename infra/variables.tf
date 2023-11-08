variable "region" {
  type    = string
  default = "ap-south-1"

}

variable "google_client_id" {
  type      = string
  default   = "None"
  sensitive = true
}

variable "google_client_secret" {
  type      = string
  default   = "None"
  sensitive = true
}

variable "google_callback_url_main" {
  type = string
}

variable "google_callback_url_dev" {
  type = string
}

variable "google_callback_url_local" {
  type    = string
  default = "http://localhost:3000/api/auth/callback/cognito_google"
}

variable "vpc_cidr_block" {
  type    = string
  default = "10.0.0.0/16"
}

variable "vpc_public_subnet_k8s_cidr_blocks" {
  type    = list(string)
  default = ["10.0.0.0/24", "10.0.1.0/24"]
}

variable "vpc_public_subnet_app_cidr_blocks" {
  type    = list(string)
  default = ["10.0.2.0/24", "10.0.3.0/24"]
}

variable "vpc_private_subnet_cidr_blocks" {
  type    = list(string)
  default = ["10.0.4.0/24", "10.0.5.0/24"]

}

variable "vpc_azs" {
  type    = list(string)
  default = ["ap-south-1a", "ap-south-1b"]

}

variable "vpc_name" {
  type    = string
  default = "kodiko"
}

variable "key_name" {
  type      = string
  sensitive = true

}
