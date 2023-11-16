FROM jenkins/jenkins:2.431-jdk17
# Pipelines with Blue Ocean UI and Kubernetes
RUN jenkins-plugin-cli --plugins blueocean kubernetes workflow-aggregator git configuration-as-code role-strategy:689.v731678c3e0eb_ 