## Interacting with a Docker Container

## Environment variable

The Flask application reads the `MESSAGE` environment variable. If the variable is not defined, it displays `Hello from my first Docker image!` by default.

## Build the image

```bash
cd 1-first_image
docker build -t first-image-app .

## Run the container with an environment variable

```bash
docker run -d --name first-image-container -p 5001:5000 -e 'MESSAGE=Hello Thomas from Docker!' first-image-app
```

The host port `5001` is mapped to port `5000` inside the container.

## Test the application

```bash
curl http://localhost:5001
```

Output:

```text
Hello Thomas from Docker!
```

The output changed because the `MESSAGE` variable was passed to the container at runtime.

## Read the variable from inside the container

```bash
docker exec first-image-container printenv MESSAGE
```

Output:

```text
Hello Thomas from Docker!
```

This confirms that the environment variable exists inside the running container.

## Inspect the container

```bash
docker inspect first-image-container --format '{{json .Config.Env}}'
```

The output contains:

```text
MESSAGE=Hello Thomas from Docker!
```

This shows that Docker stored the variable in the container configuration.

## Read the container logs

```bash
docker logs first-image-container
```

The logs show that the Flask server started and listens on port `5000`. They also show the HTTP request made with `curl`.

## Clean up

```bash
docker stop first-image-container
docker rm first-image-container
```

## Observations

1. The same Docker image can display different messages depending on the environment variable passed with `-e`.
2. `docker exec` can execute a command inside an already running container and confirm its runtime environment.
3. `docker inspect` provides detailed container configuration, including its environment variables, while `docker logs` shows the application output.