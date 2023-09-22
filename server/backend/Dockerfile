# ref: https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0

ARG PYTHON_VERSION=3.10.12
FROM python:${PYTHON_VERSION}-buster as build

ARG POETRY_VER=1.5.1
RUN pip install poetry==${POETRY_VER}

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./

# Create README for poetry 
RUN touch README.md 

# Install non dev deps
# Leverage a cache mount to /tmp/poetry_cache to speed up subsequent builds.
RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --only main --no-root


FROM python:${PYTHON_VERSION}-slim-buster as runtime

WORKDIR /app

# Prevents Python from writing pyc files.
# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/.venv/bin:$PATH"

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Switch to the non-privileged user to run the application.
USER appuser

# copy deps from build image
COPY --from=build /app/.venv /opt/.venv

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["python3", "main.py"]
