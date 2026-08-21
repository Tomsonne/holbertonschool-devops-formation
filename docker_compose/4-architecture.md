# Full Stack Architecture

## Overview

The application is composed of five services managed by Docker Compose: `proxy`, `web`, `api`, `db`, and `redis`. Only the proxy is exposed to the host machine. The other services communicate through the default Docker Compose network.

## Architecture Diagram

```text
                              Outside world
                                    |
                                    | HTTP localhost:8080
                                    v
                         +-----------------------+
                         |     proxy (Nginx)     |
                         |   Internal port 80    |
                         +-----------+-----------+
                                     |
                    +----------------+----------------+
                    |                                 |
               Request "/"                      Request "/api/"
                    |                                 |
                    v                                 v
          +--------------------+           +--------------------+
          |        web         |           |        api         |
          |   Web server :80   |           |   Flask API :5000  |
          +--------------------+           +---------+----------+
                                                   / \
                                                  /   \
                                                 v     v
                              +--------------------+   +--------------------+
                              |         db         |   |       redis        |
                              | PostgreSQL :5432   |   |   Cache :6379      |
                              +---------+----------+   +--------------------+
                                        |
                                        v
                              +--------------------+
                              |  postgres_data     |
                              | Persistent volume  |
                              +--------------------+

              All five services share the default Compose network.
```

## Services and Roles

### `proxy`

The `proxy` service uses Nginx and is the single entry point for the application. It publishes host port `8080` to port `80` inside the container.

Its configuration routes:

- requests starting with `/api/` to `api:5000`;
- all other requests to `web:80`.

The local `./proxy/nginx.conf` file is mounted read-only at `/etc/nginx/conf.d/default.conf` inside the container.

### `web`

The `web` service serves the frontend over its internal port `80`. It is built from the `./web` directory and is not directly exposed to the host.

### `api`

The `api` service is a Flask application built from the `./api` directory. It listens on internal port `5000` and receives API requests from the proxy.

It receives its PostgreSQL and Redis connection settings through environment variables. It waits for both `db` and `redis` to become healthy before starting.

### `db`

The `db` service uses the `postgres:17-alpine` image and listens on internal port `5432`. It stores the application's persistent database data and provides a healthcheck using `pg_isready`.

### `redis`

The `redis` service uses the `redis:7-alpine` image and listens on internal port `6379`. It provides an in-memory cache and has a healthcheck based on `redis-cli ping`.

## Network

No custom network is declared, so Docker Compose automatically creates one default network for the project. Every service joins this network and can resolve the other services by name.

Examples of internal communication are:

```text
proxy -> web:80
proxy -> api:5000
api   -> db:5432
api   -> redis:6379
```

The containers must use service names such as `db` and `redis`, not `localhost`. Inside the API container, `localhost` would refer to the API container itself.

Only `proxy` publishes a port to the host. The database, Redis, API, and web services remain accessible only through the Compose network.

## Volumes and Data

The named volume `postgres_data` is mounted at:

```text
/var/lib/postgresql/data
```

This volume keeps the PostgreSQL data independently from the lifecycle of the `db` container. Recreating the container does not delete the stored database data.

The proxy also uses a read-only bind mount:

```text
./proxy/nginx.conf -> /etc/nginx/conf.d/default.conf
```

This mount provides the Nginx routing configuration. Redis has no persistent volume in this stack, so its cached data is temporary.

## End-to-End Request Path

### Frontend request

1. A client sends a request to `http://localhost:8080/`.
2. Docker forwards host port `8080` to port `80` of the `proxy` container.
3. Nginx forwards the request to `web:80` through the Compose network.
4. The web service returns the frontend to the proxy.
5. The proxy returns the HTTP response to the client.

```text
Client -> localhost:8080 -> proxy:80 -> web:80 -> proxy -> Client
```

### API and database path

1. A client sends a request to `http://localhost:8080/api/`.
2. Docker forwards the request to the Nginx proxy.
3. Nginx forwards the request to `api:5000`.
4. For a database-backed operation, the API communicates with PostgreSQL at `db:5432`.
5. PostgreSQL sends the result back to the API.
6. The API creates an HTTP response and returns it through the proxy to the client.

```text
Client -> localhost:8080 -> proxy:80 -> api:5000
                                      -> db:5432
                                      <- database result
Client <- proxy:80 <- api response
```

The current API performs a PostgreSQL `SELECT 1` connection check when it starts. Its existing HTTP routes return simple JSON and do not yet query application data from PostgreSQL. Redis is healthy and reachable by the API, but the current routes do not yet read or write cached data.
