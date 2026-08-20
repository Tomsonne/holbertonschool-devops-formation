# My First Docker Compose Stack

This project demonstrates how Docker Compose can build and run a multi-container application with a single command.

The stack contains three services:

* A web server built with Nginx.
* A Python Flask API.
* A PostgreSQL database.

## Project structure

```text
0-first_stack/
├── compose.yaml
├── README.md
├── api/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
└── web/
    ├── Dockerfile
    └── index.html
```

## Compose file explanation

The `compose.yaml` file defines the three services required by the application.

### Web service

The `web` service is built from the Dockerfile located in the `web` directory:

```yaml
web:
  build:
    context: ./web
```

It publishes port `80` from the container on port `8080` of the host machine:

```yaml
ports:
  - "8080:80"
```

The web page is therefore available at:

```text
http://localhost:8080
```

The service declares a dependency on the API:

```yaml
depends_on:
  - api
```

This means that Docker Compose starts the API before starting the web service.

### API service

The `api` service is built from the Dockerfile located in the `api` directory:

```yaml
api:
  build:
    context: ./api
```

The Flask application listens on port `5000` inside its container. This port is published as port `5001` on the host machine:

```yaml
ports:
  - "5001:5000"
```

The API is therefore available at:

```text
http://localhost:5001
```

The `environment` section provides the API with the information required to locate and access PostgreSQL:

```yaml
environment:
  DATABASE_HOST: db
  DATABASE_PORT: 5432
  DATABASE_NAME: compose_db
  DATABASE_USER: compose_user
  DATABASE_PASSWORD: compose_password
```

The database hostname is `db`, which is the name of the PostgreSQL service on the Docker Compose network.

The API declares a dependency on the database:

```yaml
depends_on:
  - db
```

This starts the database container before the API container. It does not guarantee that PostgreSQL is ready to accept connections. A healthcheck can be added to handle database readiness.

### Database service

The `db` service uses the official PostgreSQL Alpine image:

```yaml
db:
  image: postgres:17-alpine
```

The PostgreSQL environment variables create the database and its user when the database is initialized:

```yaml
environment:
  POSTGRES_DB: compose_db
  POSTGRES_USER: compose_user
  POSTGRES_PASSWORD: compose_password
```

A named volume stores the PostgreSQL data:

```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
```

The volume is declared at the end of the Compose file:

```yaml
volumes:
  postgres_data:
```

This allows the database data to remain available when the containers are stopped or recreated.

Docker Compose also creates a default network automatically. The services can communicate through this network by using their service names, such as `api` and `db`.

## Requirements

* Docker
* Docker Compose

Verify the installation with:

```bash
docker --version
docker compose version
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

## Test the application

Open the web application:

```text
http://localhost:8080
```

Test the API:

```bash
curl http://localhost:5001
```

Expected response:

```json
{"message":"Hello from the API"}
```

Check the running services:

```bash
docker compose ps
```

Display the logs:

```bash
docker compose logs
```

## Stop the stack

Stop and remove the containers and the default network:

```bash
docker compose down
```

The PostgreSQL volume is preserved by default.

To also remove the database volume and its data:

```bash
docker compose down --volumes
```
