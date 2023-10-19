
resource "aws_route_table" "kodiko_public_route_table" {
  vpc_id = aws_vpc.kodiko_vpc.id

  tags = {
    Name = "${var.name}-publicRT"
  }
}

resource "aws_route" "kodiko-public-route" {
  route_table_id         = aws_route_table.kodiko_public_route_table.id
  gateway_id             = aws_internet_gateway.kodiko-igw.id
  destination_cidr_block = "0.0.0.0/0"
}


resource "aws_route_table_association" "kodiko-rt-association-k8s" {
  for_each       = { for idx, subnet in aws_subnet.kodiko_public_subnet_k8s : idx => subnet.id }
  subnet_id      = each.value
  route_table_id = aws_route_table.kodiko_public_route_table.id

}

resource "aws_route_table_association" "kodiko-rt-association-app" {
  for_each       = { for idx, subnet in aws_subnet.kodiko_public_subnet_app : idx => subnet.id }
  subnet_id      = each.value
  route_table_id = aws_route_table.kodiko_public_route_table.id

}

