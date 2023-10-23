# Update env with returned client secret
# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cognito_user_pool_client#client_secret
output "cognito_app_client_secret" {
  value     = aws_cognito_user_pool_client.userpool_client.client_secret
  sensitive = true
}
