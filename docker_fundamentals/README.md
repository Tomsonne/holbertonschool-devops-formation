# Docker Fundamentals

This project introduces the essential Docker workflow: pulling images, running containers, writing Dockerfiles, debugging broken images, publishing ports, and using environment variables.

## Tasks

- `0-first_container.md`: run and inspect an official Nginx container.
- `1-first_image/`: build a small Flask application image.
- `2-fix_flask/`: fix a Flask Dockerfile without changing the application.
- `3-fix_express/`: fix an Express Dockerfile and install its dependencies.
- `4-interact.md`: configure a running container with an environment variable and inspect it with Docker commands.

## Requirements

- Docker Desktop or Docker Engine
- A running Docker daemon

Verify the installation:

```bash
docker --version
docker run hello-world
```

## Build and Run the Flask Image

```bash
cd 1-first_image
docker build -t first-image-app .
docker run -d --name first-image-container -p 5001:5000 first-image-app
curl http://localhost:5001
```

The Flask application listens on port `5000` inside the container and is available on port `5001` of the host.

## Useful Commands

```bash
docker ps
docker logs first-image-container
docker exec first-image-container printenv MESSAGE
docker stop first-image-container
docker rm first-image-container
```

## Main Concepts

- An image is a reusable template; a container is a running instance of that image.
- A Dockerfile describes how an image is built.
- `EXPOSE` documents an internal port, while `-p` publishes it to the host.
- Dependencies must be installed inside the image.
- Environment variables can configure a container at runtime without rebuilding the image.