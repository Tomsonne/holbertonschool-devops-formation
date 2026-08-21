# Docker Compose Full Stack

This project extends `1-healthchecks` by adding:

* an Nginx reverse proxy as the single public entry point;
* a Redis cache service available to the API through the Docker network.

The complete stack starts with a single `docker compose up` command.

## Project structure

```text
2-full_stack/
├── compose.yaml
├── README.md
├── api/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── web/
│   ├── index.html
│   └── Dockerfile
└── proxy/
    └── nginx.conf
```

## Services

The stack contains five services:

| Service | Role                                          |
| ------- | --------------------------------------------- |
| `proxy` | Receives external traffic and routes requests |
| `web`   | Serves the frontend                           |
| `api`   | Runs the Flask API                            |
| `db`    | Runs the PostgreSQL database                  |
| `redis` | Provides the cache service                    |

Docker Compose creates a private network automatically. Services communicate through this network by using their service names, such as `web`, `api`, `db`, and `redis`.

## Architecture

```text
Client
  |
  | http://localhost:8080
  v
Nginx reverse proxy
  |
  |-- /       --> web:80
  |
  `-- /api/   --> api:5000
                       |
                       |-- db:5432
                       `-- redis:6379
```

Only the reverse proxy publishes a port to the host machine.

The other services are available only inside the Docker Compose network.

## Changes from `1-healthchecks`

The previous stack exposed the web service and API directly:

```text
Frontend: localhost:8080
API:      localhost:5001
```

In this task, their published ports are removed. External traffic must pass through the reverse proxy:

```text
Frontend: localhost:8080/
API:      localhost:8080/api/
```

A Redis service is also added. The API receives the Redis connection information through these environment variables:

```yaml
REDIS_HOST: redis
REDIS_PORT: 6379
```

The value `redis` corresponds to the Redis service name in `compose.yaml`.

This is more reliable than using a container IP address because Docker can assign a different IP address whenever the stack is recreated.

## Reverse proxy configuration

The reverse proxy uses the following Nginx configuration:

```nginx
server {
    listen 80;

    location /api/ {
        proxy_pass http://api:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        proxy_pass http://web:80/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Requests beginning with `/api/` are sent to the Flask API.

All other requests are sent to the web service.

The configuration file is mounted inside the proxy container:

```yaml
volumes:
  - ./proxy/nginx.conf:/etc/nginx/conf.d/default.conf:ro
```

The `:ro` option mounts the file as read-only.

## Redis healthcheck

Redis uses a healthcheck based on:

```bash
redis-cli ping
```

A healthy Redis server responds with:

```text
PONG
```

The API waits for Redis and PostgreSQL to become healthy before starting:

```yaml
depends_on:
  db:
    condition: service_healthy
  redis:
    condition: service_healthy
```

## Run the stack

Build the application images and start all services:

```bash
docker compose up --build
```

To run the stack in the background:

```bash
docker compose up --build -d
```

## Important tests

### 1. Check the complete stack

```bash
docker compose ps
```

Result:

```text
NAME                   SERVICE   STATUS                    PORTS
2-full_stack-api-1     api       Up                        5000/tcp
2-full_stack-db-1      db        Up (healthy)              5432/tcp
2-full_stack-proxy-1   proxy     Up                        0.0.0.0:8080->80/tcp
2-full_stack-redis-1   redis     Up (healthy)              6379/tcp
2-full_stack-web-1     web       Up                        80/tcp
```

All five services are running.

PostgreSQL and Redis are healthy, and only the reverse proxy publishes a port to the host.

### 2. Test the reverse proxy

Test the frontend route:

```bash
curl http://localhost:8080/
```

The command returns the HTML page served by the `web` service.

Test the API route:

```bash
curl http://localhost:8080/api/
```

Result:

```json
{"message":"Hello from the API"}
```

Test the API health route:

```bash
curl http://localhost:8080/api/health
```

Result:

```json
{"status":"healthy"}
```

These results prove that Nginx routes `/` to the web service and `/api/` to the API service.

### 3. Test Redis from the API container

First, Redis was tested directly:

```bash
docker compose exec redis redis-cli ping
```

Result:

```text
PONG
```

The connection was then tested from inside the API container using the Redis service name:

```bash
docker compose exec api python -c \
'import socket; print("Redis IP:", socket.gethostbyname("redis")); connection = socket.create_connection(("redis", 6379), timeout=3); print("Redis reachable by service name"); connection.close()'
```

Result:

```text
Redis IP: 172.26.0.4
Redis reachable by service name
```

This proves that:

1. the API container can resolve the service name `redis`;
2. Docker translates the service name into an internal IP address;
3. the API container can connect to Redis on port `6379`.

The internal IP address may change when the stack is recreated, but the service name `redis` remains stable.

## Requirement validation

| Requirement                             | Evidence                                         | Status |
| --------------------------------------- | ------------------------------------------------ | ------ |
| A reverse proxy routes external traffic | `/` reaches `web` and `/api/` reaches `api`      | Passed |
| Redis is present                        | Redis is running and healthy                     | Passed |
| Redis is reachable by service name      | The API connects to `redis:6379`                 | Passed |
| The full stack starts with one command  | `docker compose up --build` starts five services | Passed |

## Stop the stack

Stop and remove the containers and the default network:

```bash
docker compose down
```

The PostgreSQL named volume is preserved.

To also remove the database volume and its data:

```bash
docker compose down --volumes
```
