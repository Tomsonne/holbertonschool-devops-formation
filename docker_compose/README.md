# Docker Compose

This project demonstrates how Docker Compose defines, starts, connects, monitors, and repairs multi-container applications.

## Tasks

- `0-first_stack/`: run a web service, a Flask API, and PostgreSQL together.
- `1-healthchecks/`: make the API wait until PostgreSQL is healthy.
- `2-full_stack/`: add Redis and an Nginx reverse proxy to create a five-service stack.
- `3-fix_stack/`: repair database credentials and incorrect port mappings in a broken Compose file.
- `4-architecture.md`: document the services, network, volumes, and request flow.

## Requirements

- Docker Desktop or Docker Engine
- Docker Compose

Verify the installation:

```bash
docker --version
docker compose version
```

## Run the Full Stack

```bash
cd 2-full_stack
docker compose up --build -d
docker compose ps
```

The Nginx proxy is the only public entry point:

```text
Frontend: http://localhost:8080/
API:      http://localhost:8080/api/
Health:   http://localhost:8080/api/health
```

Quick checks:

```bash
curl http://localhost:8080/
curl http://localhost:8080/api/
docker compose exec redis redis-cli ping
```

## Full Stack Services

- `proxy`: routes external traffic to the frontend or API.
- `web`: serves the frontend over the private Compose network.
- `api`: runs the Flask application on internal port `5000`.
- `db`: runs PostgreSQL with a healthcheck and persistent volume.
- `redis`: provides a cache service with a healthcheck.

Docker Compose creates a default private network. Services communicate through stable service names such as `api`, `db`, and `redis`.

PostgreSQL stores its data in the named volume `postgres_data`, so the data survives container recreation.

## Stop the Stack

```bash
docker compose down
```

To also delete the PostgreSQL data:

```bash
docker compose down --volumes
```

The `--volumes` option permanently removes the database volume.