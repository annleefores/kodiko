FROM node:18-alpine

WORKDIR /app

RUN apt install -y make python build-essential

COPY package.json .
# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.npm to speed up subsequent builds.
RUN --mount=type=cache,target=/root/.npm \
    npm i 

COPY . .

CMD ["npm", "run", "dev"]