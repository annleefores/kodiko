# codepod-build 

FROM node:18-bookworm-slim as base

RUN apt update && apt install -y make python3 build-essential