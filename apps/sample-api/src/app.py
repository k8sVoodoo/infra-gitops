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


@app.route("/api/work")
def work():
    print({"service": SERVICE_NAME, "step": "work_started"}, flush=True)

    print({"service": SERVICE_NAME, "step": "auth_started"}, flush=True)
    time.sleep(0.05)
    print({"service": SERVICE_NAME, "step": "auth_completed", "duration_ms": 50}, flush=True)

    print({"service": SERVICE_NAME, "step": "database_lookup_started"}, flush=True)
    time.sleep(0.10)
    print(
        {
            "service": SERVICE_NAME,
            "step": "database_lookup_completed",
            "duration_ms": 100,
        },
        flush=True,
    )

    print({"service": SERVICE_NAME, "step": "external_api_started"}, flush=True)
    time.sleep(0.20)
    print(
        {
            "service": SERVICE_NAME,
            "step": "external_api_completed",
            "duration_ms": 200,
        },
        flush=True,
    )

    print({"service": SERVICE_NAME, "step": "response_formatting_started"}, flush=True)
    time.sleep(0.03)
    print(
        {
            "service": SERVICE_NAME,
            "step": "response_formatting_completed",
            "duration_ms": 30,
        },
        flush=True,
    )

    print({"service": SERVICE_NAME, "step": "work_completed"}, flush=True)

    return jsonify(
        {
            "status": "done",
            "service": SERVICE_NAME,
            "version": VERSION,
            "hostname": socket.gethostname(),
            "steps": {
                "auth_ms": 50,
                "database_lookup_ms": 100,
                "external_api_ms": 200,
                "response_formatting_ms": 30,
            },
            "total_simulated_ms": 380,
        }
    )


@app.route("/api/slow")
def slow():
    delay = random.uniform(0.5, 2.0)

    print(
        {
            "service": SERVICE_NAME,
            "level": "warning",
            "message": "slow request started",
            "delay_seconds": round(delay, 2),
        },
        flush=True,
    )

    time.sleep(delay)

    print(
        {
            "service": SERVICE_NAME,
            "level": "warning",
            "message": "slow request completed",
            "delay_seconds": round(delay, 2),
        },
        flush=True,
    )

    return jsonify(
        {
            "status": "slow request completed",
            "delay_seconds": round(delay, 2),
            "hostname": socket.gethostname(),
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)