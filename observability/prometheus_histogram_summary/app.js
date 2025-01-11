const express = require('express');
const client = require('prom-client');
const app = express();

// Register metrics
const register = new client.Registry();
client.collectDefaultMetrics({ register });

// Histogram setup
const httpRequestDurationHistogram = new client.Histogram({
    name: 'http_request_duration_seconds',
    help: 'Duration of HTTP requests in seconds histogram',
    labelNames: ['method', 'route'],
    buckets: [0.1, 0.5, 1, 2, 5]
});

// Summary setup
const httpRequestDurationSummary = new client.Summary({
    name: 'http_request_duration_summary_seconds',
    help: 'Duration of HTTP requests in seconds summary',
    labelNames: ['method', 'route'],
    percentiles: [0.5, 0.9, 0.95, 0.99]
});

register.registerMetric(httpRequestDurationHistogram);
register.registerMetric(httpRequestDurationSummary);

app.use((req, res, next) => {
    const start = process.hrtime();
    res.on('finish', () => {
        const duration = process.hrtime(start);
        const durationSeconds = duration[0] + duration[1] / 1e9;
        httpRequestDurationHistogram.labels(req.method, req.route?.path || req.path).observe(durationSeconds);
        httpRequestDurationSummary.labels(req.method, req.route?.path || req.path).observe(durationSeconds);
    });
    next();
});

// Endpoint for Prometheus metrics
app.get('/metrics', async (req, res) => {
    res.setHeader('Content-Type', register.contentType);
    res.send(await register.metrics());
});

// Additional endpoints for testing
app.get('/fast', (req, res) => res.json({ message: 'Fast response' }));
app.get('/medium', (req, res) => setTimeout(() => res.json({ message: 'Medium response' }), 500));
app.get('/slow', (req, res) => setTimeout(() => res.json({ message: 'Slow response' }), 2000));

const PORT = 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));