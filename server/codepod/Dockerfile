FROM annleefores/codepod-build:1.0.0 as build

WORKDIR /home
# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.npm to speed up subsequent builds.
# Leverage bind mounts to package.json and package-lock.json to avoid having to copy them
# into this layer.
RUN --mount=type=bind,source=package.json,target=package.json \
    --mount=type=bind,source=package-lock.json,target=package-lock.json \
    --mount=type=cache,target=/root/.npm
    
COPY . .

RUN npm ci && npm run build

################################################################################

FROM annleefores/codepod-deploy:1.0.0 as base

WORKDIR /home

ARG USERNAME=kodiko
ARG USER_UID=10001
ARG USER_GID=$USER_UID
ARG KODIKO_SERVER_ROOT="/home/.kodiko"

# Creating the user and usergroup
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USERNAME -m -s /bin/bash $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

RUN chmod g+rw /home && \
    mkdir -p /home/kodiko ${KODIKO_SERVER_ROOT} && \
    chown -R $USERNAME:$USERNAME /home/kodiko && \
    chown -R $USERNAME:$USERNAME ${KODIKO_SERVER_ROOT}

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    HOME=/home/kodiko \
    KODIKO_SERVER_ROOT=${KODIKO_SERVER_ROOT}

USER kodiko

COPY --from=build /home/dist /home/.kodiko

EXPOSE 5000

# make tini run as main process to handle signals correctly
ENTRYPOINT ["tini", "--"]
CMD ["node", "/home/.kodiko/server.js" ]