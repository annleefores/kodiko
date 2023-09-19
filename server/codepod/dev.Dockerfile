FROM node:18-bookworm-slim

WORKDIR /app

RUN apt update && apt install -y make python3 build-essential tini

COPY package.json .
# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.npm to speed up subsequent builds.
RUN --mount=type=cache,target=/root/.npm \
    npm i 

COPY . .

# make tini run as main process to handle signals correctly
ENTRYPOINT ["/tini", "--"]

CMD ["npm", "run", "dev"]