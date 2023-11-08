#!/bin/bash

# https://linux.how2shout.com/how-to-install-docker-on-amazon-linux-2023/


sudo yum update -y
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ec2-user