from flask import Flask, jsonify, request
import os
import random
import socket
import time

from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter


SERVICE_NAME = os.getenv("SERVICE_NAME", "sample-api")
VERSION = os.getenv("VERSION", "v1")
OTEL_ENDPOINT = os.getenv(
    "OTEL_EXPORTER_OTLP_ENDPOINT",
    "http://otel-collector.observability.svc.cluster.local:4317",
)

resource = Resource.create(
    {
        "service.name": SERVICE_NAME,
        "service.version": VERSION,
        "deployment.environment": "homelab",
    }
)

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(
    OTLPSpanExporter(
        endpoint=OTEL_ENDPOINT,
        insecure=True,
    )
)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)


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
    with tracer.start_as_current_span("generate_random_message"):
        return jsonify(
            {
                "message": "GitOps + Flux + Grafana + Loki + Tempo is working",
                "random_number": random.randint(1, 100),
                "hostname": socket.gethostname(),
            }
        )


@app.route("/api/error")
def random_error():
    with tracer.start_as_current_span("fake_error"):
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
    with tracer.start_as_current_span("api_work_request") as span:
        span.set_attribute("app.endpoint", "/api/work")

        with tracer.start_as_current_span("authentication"):
            time.sleep(0.05)

        with tracer.start_as_current_span("database_lookup"):
            time.sleep(0.10)

        with tracer.start_as_current_span("external_api_call"):
            time.sleep(0.20)

        with tracer.start_as_current_span("response_formatting"):
            time.sleep(0.03)

        return jsonify(
            {
                "status": "done",
                "service": SERVICE_NAME,
                "version": VERSION,
                "hostname": socket.gethostname(),
                "steps": {
                    "authentication_ms": 50,
                    "database_lookup_ms": 100,
                    "external_api_call_ms": 200,
                    "response_formatting_ms": 30,
                },
                "total_simulated_ms": 380,
            }
        )


@app.route("/api/slow")
def slow():
    delay = random.uniform(0.5, 2.0)

    with tracer.start_as_current_span("slow_request") as span:
        span.set_attribute("delay_seconds", round(delay, 2))

        with tracer.start_as_current_span("slow_dependency"):
            time.sleep(delay)

        return jsonify(
            {
                "status": "slow request completed",
                "delay_seconds": round(delay, 2),
                "hostname": socket.gethostname(),
            }
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)