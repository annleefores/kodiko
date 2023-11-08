resource "aws_cognito_identity_provider" "google_provider" {
  user_pool_id  = aws_cognito_user_pool.pool.id
  provider_name = "Google"
  provider_type = "Google"

  provider_details = {
    authorize_scopes = "profile email openid"
    client_id        = var.google_client_id
    client_secret    = var.google_client_secret
  }

  attribute_mapping = {
    email              = "email"
    username           = "sub"
    name               = "given_name"
    picture            = "picture"
    preferred_username = "name"
  }
}

resource "aws_cognito_user_pool_client" "userpool_client" {
  name                                 = "kodiko"
  user_pool_id                         = aws_cognito_user_pool.pool.id
  access_token_validity                = 60
  auth_session_validity                = 3
  id_token_validity                    = 60
  refresh_token_validity               = 30
  enable_token_revocation              = true
  generate_secret                      = true
  callback_urls                        = [var.google_callback_url_main, var.google_callback_url_dev, var.google_callback_url_local]
  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_flows                  = ["code"]
  allowed_oauth_scopes                 = ["email", "openid", "profile"]
  explicit_auth_flows                  = ["ALLOW_REFRESH_TOKEN_AUTH", "ALLOW_USER_SRP_AUTH"]
  prevent_user_existence_errors        = "ENABLED"
  supported_identity_providers         = ["Google"]


  token_validity_units {
    access_token  = "minutes"
    id_token      = "minutes"
    refresh_token = "days"
  }
}
