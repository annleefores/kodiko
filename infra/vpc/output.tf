output "vpc_id" {
  value = aws_vpc.kodiko_vpc.id
}

output "public_app_subnet_id" {
  value = aws_subnet.kodiko_public_subnet_app[0].id
}
