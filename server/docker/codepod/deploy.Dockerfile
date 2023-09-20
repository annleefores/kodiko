# codepod-deploy 

FROM node:18-bookworm-slim as base

RUN apt update && apt -y install tini git sudo htop curl