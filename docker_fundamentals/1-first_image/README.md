# My First Docker Image

This project contains a small Flask application running inside a Docker container.

## Build the image

```bash
docker build --no-cache -t first-image-app .
```

## Run the container

```bash
docker run -d --name first-image-container -p 5001:5000 first-image-app
```

## Test the application

```bash
curl http://localhost:5001
```

Expected response:

```text
Hello from my first Docker image!
```

## Stop and remove the container

```bash
docker stop first-image-container
docker rm first-image-container
```