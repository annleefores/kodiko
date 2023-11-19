FROM jenkins/jenkins:2.432-jdk17
# Pipelines with Blue Ocean UI and Kubernetes
RUN jenkins-plugin-cli --plugins blueocean kubernetes workflow-aggregator git configuration-as-code role-strategy sonar job-dsl