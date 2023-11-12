FROM sapmachine:17.0.9-jre-ubuntu-22.04 as base

WORKDIR /home

RUN apt update \
    && apt install -y --no-install-recommends ca-certificates curl gnupg \
    && install -m 0755 -d /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
    && chmod a+r /etc/apt/keyrings/docker.gpg \
    && echo \
    "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
    "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
    tee /etc/apt/sources.list.d/docker.list > /dev/null \
    && apt update \
    && apt install -y --no-install-recommends docker-ce docker-buildx-plugin \
    && apt-get remove -y --purge --autoremove curl ca-certificates gnupg

FROM base as build

RUN apt install -y wget unzip 

ARG SONAR_VERSION=5.0.1.3006-linux

RUN wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-${SONAR_VERSION}.zip && \
    unzip sonar-scanner-cli-${SONAR_VERSION}.zip && mv sonar-scanner-${SONAR_VERSION} sonar-scanner-cli


FROM base as main

COPY --from=build /home/sonar-scanner-cli /home/sonar-scanner-cli




