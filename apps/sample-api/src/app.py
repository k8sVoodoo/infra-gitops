from flask import Flask, jsonify, request
import os
import random
import socket
import time

app = Flask(__name__)

SERVICE_NAME = os.getenv("SERVICE_NAME", "sample-api")
VERSION = os.getenv("VERSION", "v1")


@app.before_request
def log_request():
    print(
        {
            "service": SERVICE_NAME,
            "version": VERSION,
            "method": request.method,
            "path": request.path,
            "remote_addr": request.remote_addr,
            "timestamp": time.time(),
        },
        flush=True,
    )


@app.route("/")
def root():
    return jsonify(
        {
            "service": SERVICE_NAME,
            "version": VERSION,
            "hostname": socket.gethostname(),
            "message": "Hello from sample-api",
        }
    )


@app.route("/healthz")
def healthz():
    return jsonify({"status": "healthy"})


@app.route("/api/message")
def message():
    return jsonify(
        {
            "message": "GitOps + Flux + Grafana + Loki is working",
            "random_number": random.randint(1, 100),
            "hostname": socket.gethostname(),
        }
    )


@app.route("/api/error")
def random_error():
    print(
        {
            "service": SERVICE_NAME,
            "level": "error",
            "message": "This is a fake error for Grafana Loki testing",
        },
        flush=True,
    )
    return jsonify({"error": "fake test error"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)