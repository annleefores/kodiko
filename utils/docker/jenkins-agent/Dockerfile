# codepod-build 

FROM ubuntu:22.04 as base

WORKDIR /home

RUN apt update && \
    apt install -y openjdk-17-jre


FROM base as build

RUN apt install -y wget unzip 

ARG SONAR_VERSION=5.0.1.3006-linux

RUN wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-${SONAR_VERSION}.zip && \
    unzip sonar-scanner-cli-${SONAR_VERSION}.zip && mv sonar-scanner-${SONAR_VERSION} sonar-scanner-cli


FROM base as main

COPY --from=build /home/sonar-scanner-cli /home/sonar-scanner-cli

