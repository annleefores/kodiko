#!/bin/bash

# Install Jenkins
# https://www.jenkins.io/doc/book/installing/linux/

sudo apt update

sudo apt install -y fontconfig openjdk-17-jre

sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key

echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null

sudo apt update
sudo apt install -y jenkins
sudo systemctl enable jenkins
sudo systemctl start jenkins

# Install Docker 
# Add Docker's official GPG key:
sudo apt install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources:
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update

sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin

# Grant Jenkins user and Ubuntu user permission to docker daemon
sudo usermod -aG docker jenkins
sudo usermod -aG docker ubuntu
sudo systemctl restart docker

# Install Sonarqube
sudo apt install -y unzip
groupadd --gid 10001 sonarqube
useradd --uid 10001 --gid 10001 -m -s /bin/bash sonarqube
sudo mkdir -p /home/sonarqube
sudo chown -R sonarqube:sonarqube /home/sonarqube

# Execute as sonarqube user
sudo -i -u sonarqube bash << EOF
wget https://binaries.sonarsource.com/Distribution/sonarqube/sonarqube-10.1.0.73491.zip
unzip sonarqube-10.1.0.73491.zip

chmod -R 755 /home/sonarqube/sonarqube-10.1.0.73491
chown -R sonarqube:sonarqube /home/sonarqube/sonarqube-10.1.0.73491

cd /home/sonarqube/sonarqube-10.1.0.73491/bin/linux-x86-64
./sonar.sh start
EOF