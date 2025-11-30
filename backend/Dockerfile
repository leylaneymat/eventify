ARG PYTHON_VERSION=3.11.4
FROM python:${PYTHON_VERSION}-slim-bullseye AS base
LABEL maintainer="leyla.neymat@gmail.com"
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
# Disables an automatic check for pip updates each time.
ENV PYTHONDONTWRITEBYTECODE 1
# Python will not try to write ".pyc" files.
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get --no-install-recommends install -y build-essential nano \
    && rm -rf /var/lib/apt/lists/*
    # Last line to delete apt cache and reduce dockerfile size
RUN pip install --upgrade pip
FROM base AS server
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt
# No cache to make dockerfile smaller
WORKDIR /src
COPY src /src
EXPOSE 8000
# Expose the port that the application listens on
CMD python3 manage.py runserver 8000
# Run the application