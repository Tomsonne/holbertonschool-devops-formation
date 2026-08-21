from flask import Flask, jsonify
import psycopg, os


app = Flask(__name__)

def check_database_connection():
    """Check that PostgreSQL is ready before starting the API."""
    connection = psycopg.connect(
        host=os.environ["DATABASE_HOST"],
        port=os.environ["DATABASE_PORT"],
        dbname=os.environ["DATABASE_NAME"],
        user=os.environ["DATABASE_USER"],
        password=os.environ["DATABASE_PASSWORD"]
    )

    with connection.cursor() as cursor:
        cursor.execute("SELECT 1;")
        cursor.fetchone()

    connection.close()

    print(
        "Database connection successful. API is starting.",
        flush=True
    )


@app.route("/")
def home():
    return jsonify({
        "message": "Hello from the API"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


if __name__ == "__main__":
    check_database_connection()
    app.run(host="0.0.0.0", port=5000)