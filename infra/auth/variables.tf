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

variable "region" {
  type    = string
  default = "ap-south-1"
}
