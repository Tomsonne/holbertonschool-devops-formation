import os

from flask import Flask


app = Flask(__name__)


@app.route("/")
def home():
    message = os.getenv("MESSAGE", "Hello from my first Docker image!")
    return f"{message}\n"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)