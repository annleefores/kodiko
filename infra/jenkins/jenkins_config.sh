#!/bin/bash

# https://linux.how2shout.com/how-to-install-docker-on-amazon-linux-2023/


sudo yum update -y

# Install Docker 
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ec2-user

# Install Jenkins
# https://www.jenkins.io/doc/tutorials/tutorial-for-installing-jenkins-on-AWS/
sudo wget -O /etc/yum.repos.d/jenkins.repo \
    https://pkg.jenkins.io/redhat-stable/jenkins.repo

sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key

sudo yum upgrade

sudo dnf install java-17-amazon-corretto -y

sudo yum install jenkins -y

sudo systemctl enable jenkins

sudo systemctl start jenkins