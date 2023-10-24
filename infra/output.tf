# Update env with returned client secret
# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cognito_user_pool_client#client_secret
output "cognito_app_client_secret" {
  value     = module.auth.cognito_app_client_secret
  sensitive = true
}

output "cognito_user_pool_id" {
  value = module.auth.cognito_user_pool_id
}

output "cognito_app_client_id" {
  value = module.auth.cognito_app_client_id
}
