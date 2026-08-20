# Docker Compose Healthchecks

This project extends the stack created in `0-first_stack` by adding a real PostgreSQL healthcheck and a conditional dependency.

The API no longer starts as soon as the PostgreSQL container is created. Docker Compose waits until PostgreSQL reports a healthy status before starting the API.

## Project structure

```text
1-healthchecks/
├── compose.yaml
├── README.md
├── api/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
└── web/
    ├── index.html
    └── Dockerfile
```

## Services

The stack contains three services:

| Service | Role                | Published port |
| ------- | ------------------- | -------------: |
| `web`   | Nginx web server    |         `8080` |
| `api`   | Flask API           |         `5001` |
| `db`    | PostgreSQL database |  Not published |

Docker Compose creates a default network automatically. The containers communicate through this network by using their service names.

For example, the API connects to PostgreSQL using `db` as its database hostname.

## Changes from `0-first_stack`

The previous stack used a simple dependency:

```yaml
depends_on:
  - db
```

This only guaranteed that Docker started the database container before the API container. It did not guarantee that PostgreSQL was ready to accept connections.

This task introduces two important changes:

1. A real healthcheck for the PostgreSQL service.
2. A dependency condition that makes the API wait for a healthy database.

### PostgreSQL healthcheck

The database service now contains:

```yaml
healthcheck:
  test:
    - CMD-SHELL
    - pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}
  interval: 5s
  timeout: 5s
  retries: 5
  start_period: 5s
```

The `pg_isready` command checks whether PostgreSQL is ready to accept connections.

The healthcheck configuration means:

* `interval: 5s`: run the check every five seconds;
* `timeout: 5s`: fail an individual check if it takes longer than five seconds;
* `retries: 5`: declare the container unhealthy after five consecutive failures;
* `start_period: 5s`: allow PostgreSQL five seconds to begin starting before failures are counted.

The double dollar signs in:

```yaml
$${POSTGRES_USER}
$${POSTGRES_DB}
```

ensure that these variables are evaluated inside the PostgreSQL container rather than substituted by Docker Compose while reading the Compose file.

### Conditional dependency

The API dependency is now:

```yaml
depends_on:
  db:
    condition: service_healthy
```

The API therefore waits until the database healthcheck succeeds.

The startup sequence is:

```text
PostgreSQL container starts
        ↓
PostgreSQL initializes or recovers its data
        ↓
pg_isready checks PostgreSQL
        ↓
PostgreSQL becomes healthy
        ↓
Docker Compose starts the API
        ↓
The API connects to PostgreSQL
        ↓
The Flask server starts
```

## Real database connection

The API uses `psycopg` to communicate with PostgreSQL:

```text
Flask==3.1.2
psycopg[binary]==3.2.9
```

When the API starts, it opens a real connection to PostgreSQL and executes:

```sql
SELECT 1;
```

If PostgreSQL successfully executes the query, the API prints:

```text
Database connection successful. API is starting.
```

This proves that the API can communicate with the database before the Flask server starts.

## Requirements

* Docker
* Docker Compose

Verify the installation:

```bash
docker --version
docker compose version
```

## Validate the Compose configuration

Before starting the stack, validate the Compose file:

```bash
docker compose config
```

This command renders the final configuration and reports invalid YAML or unsupported Compose options.

## Build and run the stack

Build the images and start all services:

```bash
docker compose up --build
```

To start the stack in the background:

```bash
docker compose up --build -d
```

If the API image must be completely rebuilt without using the Docker build cache:

```bash
docker compose build --no-cache api
docker compose up
```

## Tests and results

### 1. Check the running services

The following command was used:

```bash
docker compose ps
```

Result:

```text
NAME                   IMAGE                SERVICE   STATUS                    PORTS
1-healthchecks-api-1   1-healthchecks-api   api       Up 20 seconds             0.0.0.0:5001->5000/tcp
1-healthchecks-db-1    postgres:17-alpine   db        Up 25 seconds (healthy)   5432/tcp
1-healthchecks-web-1   1-healthchecks-web   web       Up 20 seconds             0.0.0.0:8080->80/tcp
```

The database is explicitly marked as:

```text
Up 25 seconds (healthy)
```

The API and web services started approximately five seconds after the database. This is consistent with the configured healthcheck and conditional dependency.

### 2. Inspect the database health status

The health status was checked directly with:

```bash
docker inspect 1-healthchecks-db-1 \
  --format '{{.State.Health.Status}}'
```

Result:

```text
healthy
```

This confirms that the PostgreSQL container has a working healthcheck and that its latest check succeeded.

### 3. Check the PostgreSQL startup logs

The database logs contained:

```text
database system is ready to accept connections
```

This confirms that PostgreSQL completed its startup and became ready to accept client connections.

### 4. Check the API logs

The following command was used:

```bash
docker compose logs api
```

Result:

```text
api-1  | Database connection successful. API is starting.
api-1  |  * Serving Flask app 'app'
api-1  |  * Debug mode: off
api-1  |  * Running on all addresses (0.0.0.0)
api-1  |  * Running on http://127.0.0.1:5000
api-1  |  * Running on http://172.26.0.3:5000
```

The database connection message appears before the Flask startup messages.

This proves that:

1. Docker Compose waited for the database healthcheck.
2. The API started after PostgreSQL became healthy.
3. The API established a real connection to PostgreSQL.
4. The database successfully executed the test query.
5. Flask started only after the connection test succeeded.

The Flask development server warning is expected for this learning project:

```text
WARNING: This is a development server. Do not use it in a production deployment.
```

### 5. Test PostgreSQL directly

The following command executes a query inside the database container:

```bash
docker compose exec db \
  psql -U compose_user -d compose_db -c "SELECT 1;"
```

Result:

```text
 ?column?
----------
        1
(1 row)
```

This proves that PostgreSQL accepts connections and executes SQL queries successfully.

### 6. Test the API

Test the main endpoint:

```bash
curl http://localhost:5001
```

Expected response:

```json
{"database":"connected","message":"The API is running"}
```

Test the API health endpoint:

```bash
curl http://localhost:5001/health
```

Expected response:

```json
{"status":"healthy"}
```

### 7. Test the web service

Open the following address in a browser:

```text
http://localhost:8080
```

The Nginx web page should be displayed.

## Requirement validation

| Requirement                                | Implementation                      | Status |
| ------------------------------------------ | ----------------------------------- | ------ |
| The database defines a real healthcheck    | `pg_isready` checks PostgreSQL      | Passed |
| The API depends on a healthy database      | `condition: service_healthy`        | Passed |
| The startup ordering is demonstrated       | Container status and API logs       | Passed |
| The API communicates with PostgreSQL       | `psycopg` connection and `SELECT 1` | Passed |
| The complete stack starts with one command | `docker compose up --build`         | Passed |

## Useful commands

Display the running services:

```bash
docker compose ps
```

Follow all logs:

```bash
docker compose logs --follow
```

Display only the API logs:

```bash
docker compose logs api
```

Display only the database logs:

```bash
docker compose logs db
```

Open a shell inside the API container:

```bash
docker compose exec api sh
```

Check the PostgreSQL health status:

```bash
docker inspect 1-healthchecks-db-1 \
  --format '{{.State.Health.Status}}'
```

## Stop the stack

Stop and remove the containers and the default network:

```bash
docker compose down
```

The named PostgreSQL volume is preserved by default.

To also remove the volume and all stored database data:

```bash
docker compose down --volumes
```

The `--volumes` option permanently removes the database data stored by this stack.
