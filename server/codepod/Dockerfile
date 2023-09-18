# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/engine/reference/builder/

ARG NODE_VERSION=18

################################################################################
# Use node image for base image for all stages.
FROM node:${NODE_VERSION}-bookworm-slim as base

################################################################################
# Create a stage for installing production dependecies.
FROM base as deps

# Set working directory for all build stages.
WORKDIR /app

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.npm to speed up subsequent builds.
# Leverage bind mounts to package.json and package-lock.json to avoid having to copy them
# into this layer.
RUN --mount=type=bind,source=package.json,target=package.json \
    --mount=type=bind,source=package-lock.json,target=package-lock.json \
    --mount=type=cache,target=/root/.npm \
    npm ci

################################################################################
# Create a stage for building the application.
FROM deps as build

# Copy the rest of the source files into the image.
COPY . .
# Run the build script.
RUN apt update && apt install -y make python3 build-essential \
    && npm run build

################################################################################
# Create a new stage to run the application with minimal runtime dependencies
# where the necessary files are copied from the build stage.
FROM node:${NODE_VERSION}-alpine

WORKDIR /app

ENV NODE_ENV production

RUN adduser --system --uid 1001 expressjs

# COPY --from=build /app/public ./public

# Automatically leverage output traces to reduce image size
COPY --from=build /app/build ./

USER expressjs

EXPOSE 5000

CMD ["node", "server.js"]