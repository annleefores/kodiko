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

data "local_file" "docker_config" {
  filename = "${path.module}/docker_config.sh"
}

resource "aws_instance" "web" {
  ami                         = data.aws_ami.ami_id.id
  instance_type               = var.instance_type
  key_name                    = var.key_name
  subnet_id                   = var.subnet_id
  associate_public_ip_address = true
  user_data                   = data.local_file.docker_config.content
  vpc_security_group_ids      = [aws_security_group.jenkins_sg.id]


  credit_specification {
    cpu_credits = var.cpu_credits
  }

  tags = {
    Name = "kodiko_jenkins"
  }
}

resource "aws_security_group" "jenkins_sg" {
  name        = "jenkins_sg"
  description = "Allow SSH and HTTP"
  vpc_id      = var.vpc_id

  tags = {
    Name = "jenkins_sg"
  }
}

resource "aws_vpc_security_group_egress_rule" "jenkins_sg_egress_1" {
  security_group_id = aws_security_group.jenkins_sg.id

  description = "all_outbound"
  cidr_ipv4   = "0.0.0.0/0"
  ip_protocol = "-1"

  tags = {
    Name = "jenkins_sg_egress_1"
  }
}

resource "aws_vpc_security_group_ingress_rule" "jenkins_sg_ingress_1" {
  security_group_id = aws_security_group.jenkins_sg.id

  description = "Jenkins"
  cidr_ipv4   = "0.0.0.0/0"
  from_port   = 8080
  ip_protocol = "tcp"
  to_port     = 8080

  tags = {
    Name = "jenkins_sg_ingress_1"
  }
}

resource "aws_vpc_security_group_ingress_rule" "jenkins_sg_ingress_2" {
  security_group_id = aws_security_group.jenkins_sg.id

  description = "SSH"
  cidr_ipv4   = "0.0.0.0/0"
  from_port   = 22
  ip_protocol = "tcp"
  to_port     = 22

  tags = {
    Name = "jenkins_sg_ingress_2"
  }
}

