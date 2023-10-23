variable "google_client_id" {
  type    = string
  default = "None"
}

variable "google_client_secret" {
  type    = string
  default = "None"

}

variable "google_callback_url" {
  type    = string
  default = "http://localhost:3000/api/auth/callback/cognito_google"
}
