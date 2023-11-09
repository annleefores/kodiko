data "aws_ami" "ami_id" {
  most_recent = true

  filter {
    name   = "name"
    values = [var.ami_image_name]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = var.ami_owners
}
