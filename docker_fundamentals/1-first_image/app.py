from flask import Flask

app = Flask(__name__)

@app.get("/")
def home():
    return "Hello from my first Docker image!\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)