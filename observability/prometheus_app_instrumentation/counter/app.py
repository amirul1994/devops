from flask import Flask, request
from prometheus_client import Counter, generate_latest, start_http_server

app = Flask(__name__)

# Prometheus Counter for tracking HTTP requests
http_requests_total = Counter(
    'http_requests_total', 
    'Total HTTP requests', 
    ['method', 'endpoint']
)

# Endpoint for /cars
@app.route('/cars', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def cars():
    # Increment the Prometheus counter
    http_requests_total.labels(method=request.method, endpoint='/cars').inc()

    # Handle different HTTP methods
    if request.method == 'GET':
        return {"message": "Fetching all cars."}
    elif request.method == 'POST':
        return {"message": "Creating a new car."}
    elif request.method == 'PATCH':
        return {"message": "Updating car details."}
    elif request.method == 'DELETE':
        return {"message": "Deleting a car."}

# Endpoint for /boats
@app.route('/boats', methods=['GET', 'POST'])
def boats():
    # Increment the Prometheus counter
    http_requests_total.labels(method=request.method, endpoint='/boats').inc()

    # Handle different HTTP methods
    if request.method == 'GET':
        return {"message": "Fetching all boats."}
    elif request.method == 'POST':
        return {"message": "Creating a new boat."}

# Endpoint for /metrics (Prometheus metrics)
@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain; charset=utf-8'}

# Main entry point
if __name__ == '__main__':
    # Start the Prometheus HTTP server on port 8000
    start_http_server(8000)

    # Start the Flask app on port 5000
    app.run(host='0.0.0.0', port=5000)