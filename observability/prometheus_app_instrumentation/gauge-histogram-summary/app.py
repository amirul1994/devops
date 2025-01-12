from flask import Flask, request
from prometheus_client import Histogram, Summary, Gauge, generate_latest
import time

app = Flask(__name__)

# Define Prometheus metrics
REQUEST_LATENCY = Histogram(
    'http_requests_latency_seconds',
    'Histogram of HTTP request latency in seconds',
    ['method', 'path'],
    buckets=[0.1, 0.5, 1, 2.5, 5, 10]
)

REQUEST_SUMMARY = Summary(
    'http_requests_latency_summary_seconds',
    'Summary of HTTP request latency in seconds',
    ['method', 'path']
)

INPROGRESS_REQUESTS = Gauge(
    'http_inprogress_requests',
    'Number of in-progress HTTP requests',
    ['method', 'path']
)

# Track request start time and increment in-progress requests
@app.before_request
def before_request():
    request.start_time = time.time()
    INPROGRESS_REQUESTS.labels(method=request.method, path=request.path).inc()

# Track request latency, decrement in-progress requests, and update metrics
@app.after_request
def after_request(response):
    latency = time.time() - request.start_time
    REQUEST_LATENCY.labels(method=request.method, path=request.path).observe(latency)
    REQUEST_SUMMARY.labels(method=request.method, path=request.path).observe(latency)
    INPROGRESS_REQUESTS.labels(method=request.method, path=request.path).dec()
    return response

# Home route
@app.route('/')
def home():
    return "Hello, World!"

# Slow route to simulate a slow request
@app.route('/slow')
def slow():
    time.sleep(2)  # Simulate a slow request
    return "This was slow!"

# Metrics endpoint for Prometheus
@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain; charset=utf-8'}

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)