resource "aws_subnet" "kodiko_public_subnet_k8s" {
  for_each                = { for idx, cidr in var.vpc_public_subnet_k8s_cidr_blocks : idx => cidr }
  vpc_id                  = aws_vpc.kodiko_vpc.id
  cidr_block              = each.value
  availability_zone       = var.vpc_azs[each.key % length(var.vpc_azs)]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.vpc_name}-public-k8s"
  }
}
resource "aws_subnet" "kodiko_public_subnet_app" {
  for_each                = { for idx, cidr in var.vpc_public_subnet_app_cidr_blocks : idx => cidr }
  vpc_id                  = aws_vpc.kodiko_vpc.id
  cidr_block              = each.value
  availability_zone       = var.vpc_azs[each.key % length(var.vpc_azs)]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.vpc_name}-public-app"
  }
}


resource "aws_subnet" "kodiko_private_subnet" {
  for_each                = { for idx, cidr in var.vpc_private_subnet_cidr_blocks : idx => cidr }
  vpc_id                  = aws_vpc.kodiko_vpc.id
  cidr_block              = each.value
  availability_zone       = var.vpc_azs[each.key % 2]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.vpc_name}-private"
  }
}
