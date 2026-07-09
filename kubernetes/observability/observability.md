# 🚀 Complete Observability Stack Deployment Guide

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Prometheus & Grafana](#prometheus--grafana)
3. [ELK Stack (Elasticsearch, Kibana, Logstash)](#elk-stack-elasticsearch-kibana-logstash)
4. [OpenTelemetry Collector](#opentelemetry-collector)
5. [Elastic APM Server](#elastic-apm-server)
6. [Troubleshooting Guide](#troubleshooting-guide)
7. [Access URLs](#access-urls)

---

## Prerequisites

```bash
# Verify Kubernetes cluster
kubectl get nodes

# Verify Helm installation
helm version
```

---

## Prometheus & Grafana

### 1. Add Helm Repository

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

### 2. Create Namespace

```bash
kubectl create namespace monitoring
```

### 3. Install kube-prometheus-stack

```bash
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace
```

### 4. Fix Node-Exporter (if needed)

If node-exporter fails with `CreateContainerError`:

```bash
# Check the error
kubectl describe pod -n monitoring -l app=prometheus-node-exporter

# Fix mount propagation
kubectl patch daemonset prometheus-prometheus-node-exporter -n monitoring --type='json' -p='[
  {"op": "remove", "path": "/spec/template/spec/containers/0/volumeMounts/1"}
]'
```

### 5. Access Prometheus & Grafana

```bash
# Get Grafana password
kubectl get secret prometheus-grafana -n monitoring -o jsonpath="{.data.admin-password}" | base64 -d ; echo

# Port-forward
kubectl port-forward svc/prometheus-grafana -n monitoring 3000:80 &
kubectl port-forward svc/prometheus-kube-prometheus-prometheus -n monitoring 9090:9090 &
```

---

## ELK Stack (Elasticsearch, Kibana, Logstash)

### 1. Add Elastic Helm Repository

```bash
helm repo add elastic https://helm.elastic.co
helm repo update
```

### 2. Create Namespace

```bash
kubectl create namespace logging
```

### 3. Deploy Elasticsearch 8.x

```bash
helm install elasticsearch elastic/elasticsearch \
  --namespace logging \
  --version 8.5.1 \
  --set replicas=1 \
  --set minimumMasterNodes=1 \
  --set persistence.enabled=false \
  --set xpack.security.enabled=true \
  --set esJavaOpts="-Xmx1g -Xms1g" \
  --set resources.requests.memory="1Gi" \
  --set resources.requests.cpu="500m"
```

### 4. Deploy Kibana 8.x

```bash
# Get Elasticsearch password
ES_PASSWORD=$(kubectl get secret elasticsearch-master-credentials -n logging -o jsonpath="{.data.password}" | base64 -d)

helm install kibana elastic/kibana \
  --namespace logging \
  --version 8.5.1 \
  --set elasticsearchHosts="https://elasticsearch-master:9200" \
  --set service.type=ClusterIP \
  --set kibanaConfig."elasticsearch\.hosts"="https://elasticsearch-master:9200" \
  --set kibanaConfig."server\.host"="0.0.0.0" \
  --set kibanaConfig."elasticsearch\.ssl\.verificationMode"="none" \
  --set resources.requests.memory="512Mi" \
  --set resources.requests.cpu="200m"
```

### 5. Deploy Filebeat (Log Shipper)

```bash
cat > filebeat-values.yaml <<'EOF'
filebeatConfig:
  filebeat.yml: |
    filebeat.inputs:
    - type: container
      paths:
        - /var/log/containers/*.log
      processors:
        - add_kubernetes_metadata:
            host: ${NODE_NAME}
            matchers:
            - logs_path:
                logs_path: "/var/log/containers/"

    output.logstash:
      hosts: ["logstash:5044"]

    logging.level: info
EOF

helm install filebeat elastic/filebeat -n logging -f filebeat-values.yaml
```

### 6. Deploy Logstash

```bash
ES_PASSWORD=$(kubectl get secret elasticsearch-master-credentials -n logging -o jsonpath="{.data.password}" | base64 -d)

cat > logstash-values.yaml <<EOF
replicas: 1

logstashConfig:
  logstash.yml: |
    http.host: "0.0.0.0"
    xpack.monitoring.enabled: false

logstashPipeline:
  pipelines.yml: |
    - pipeline.id: main
      path.config: "/usr/share/logstash/pipeline"

config:
  pipeline:
    - pipeline.id: main
      config.string: |
        input {
          beats {
            port => 5044
            host => "0.0.0.0"
          }
        }
        output {
          elasticsearch {
            hosts => ["https://elasticsearch-master:9200"]
            index => "logstash-%{+YYYY.MM.dd}"
            user => "elastic"
            password => "${ES_PASSWORD}"
            ssl => true
            ssl_certificate_verification => false
          }
        }

service:
  ports:
  - name: beats
    port: 5044
    targetPort: 5044
    protocol: TCP
EOF

helm install logstash elastic/logstash -n logging -f logstash-values.yaml
```

### 7. Create Logstash Service

```bash
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: logstash
  namespace: logging
spec:
  selector:
    app: logstash-logstash
  ports:
  - name: beats
    port: 5044
    targetPort: 5044
    protocol: TCP
EOF
```

### 8. Fix Filebeat Config

```bash
cat > filebeat-values.yaml <<'EOF'
filebeatConfig:
  filebeat.yml: |
    filebeat.inputs:
    - type: container
      paths:
        - /var/log/containers/*.log
      processors:
        - add_kubernetes_metadata:
            host: ${NODE_NAME}
            matchers:
            - logs_path:
                logs_path: "/var/log/containers/"

    output.logstash:
      hosts: ["logstash:5044"]

    logging.level: info
EOF

helm upgrade filebeat elastic/filebeat -n logging -f filebeat-values.yaml
```

### 9. Access Kibana

```bash
# Get Kibana NodePort
kubectl get svc kibana-kibana -n logging

# Port-forward
kubectl port-forward svc/kibana-kibana -n logging 5601:5601 &
```

---

## OpenTelemetry Collector

### 1. Add Helm Repository

```bash
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
helm repo update
```

### 2. Deploy OpenTelemetry Collector

```bash
ES_PASSWORD=$(kubectl get secret elasticsearch-master-credentials -n logging -o jsonpath="{.data.password}" | base64 -d)
ES_BASE64_AUTH=$(echo -n "elastic:${ES_PASSWORD}" | base64)

cat > otel-values.yaml <<EOF
mode: daemonset

image:
  repository: "otel/opentelemetry-collector-contrib"

presets:
  kubernetesAttributes:
    enabled: true

config:
  exporters:
    debug:
      verbosity: normal
    otlphttp/apm:
      endpoint: "http://apm-server-apm-server:8200"
      tls:
        insecure: true

  receivers:
    otlp:
      protocols:
        grpc:
          endpoint: 0.0.0.0:4317
        http:
          endpoint: 0.0.0.0:4318

  processors:
    batch:
      timeout: 10s
      send_batch_size: 1024
    memory_limiter:
      check_interval: 5s
      limit_mib: 512
    k8s_attributes:
      passthrough: true

  service:
    pipelines:
      traces:
        receivers: [otlp]
        processors: [memory_limiter, k8s_attributes, batch]
        exporters: [debug, otlphttp/apm]

resources:
  limits:
    cpu: 200m
    memory: 256Mi
  requests:
    cpu: 100m
    memory: 128Mi

useGOMEMLIMIT: false
EOF

helm install opentelemetry-collector open-telemetry/opentelemetry-collector -n logging -f otel-values.yaml
```

---

## Elastic APM Server

### 1. Deploy APM Server

```bash
ES_PASSWORD=$(kubectl get secret elasticsearch-master-credentials -n logging -o jsonpath="{.data.password}" | base64 -d)

cat > apm-values.yaml <<EOF
imageTag: "8.5.1"
replicas: 1

elasticsearchHosts: "https://elasticsearch-master:9200"

secretPassword: "${ES_PASSWORD}"

es:
  username: "elastic"
  password: "${ES_PASSWORD}"

tls:
  selfSignedCertificate:
    enabled: true

apmConfig:
  apm-server.yml: |
    apm-server:
      host: "0.0.0.0:8200"
      rum:
        enabled: false
      instrumentation:
        enabled: false
    output:
      elasticsearch:
        hosts: ["https://elasticsearch-master:9200"]
        username: "elastic"
        password: "${ES_PASSWORD}"
        ssl:
          verification_mode: none

resources:
  requests:
    cpu: 100m
    memory: 256Mi
  limits:
    cpu: 200m
    memory: 512Mi
EOF

helm install apm-server elastic/apm-server -n logging -f apm-values.yaml
```

### 2. Install APM Integration in Kibana

1. Go to `http://192.168.0.10:30561`
2. Click on **APM** in the left sidebar
3. Click **"Add Elastic APM"**
4. Configure:
   - **Host**: `0.0.0.0:8200`
   - **URL**: `http://apm-server-apm-server:8200`
5. Click **Save and Continue**

### 3. Test APM

```bash
kubectl run test-trace4 --rm -it --image=curlimages/curl --restart=Never -n logging -- curl -X POST "http://apm-server-apm-server:8200/intake/v2/events" -H "Content-Type: application/x-ndjson" -d '{"metadata": {"service": {"name": "test-service", "agent": {"name": "test-agent", "version": "1.0.0"}}}}
{"transaction": {"id": "1234567890123456", "trace_id": "12345678901234567890123456789012", "name": "test-transaction", "type": "request", "duration": 1000, "timestamp": 1731590400000, "result": "success", "span_count": {"started": 0}}}
' 2>&1
```

---

## Troubleshooting Guide

### 🔧 CoreDNS Issues

```bash
# Enable route_localnet
sudo sysctl -w net.ipv4.conf.all.route_localnet=1
sudo sysctl -w net.ipv4.conf.default.route_localnet=1
sudo sysctl -w net.ipv4.conf.ens33.route_localnet=1
sudo sysctl -w net.ipv4.conf.lo.route_localnet=1

# Restart CoreDNS
kubectl delete pods -n kube-system -l k8s-app=kube-dns
```

### 🔧 Calico Network Policies

```bash
# Check policies
kubectl get networkpolicies.crd.projectcalico.org --all-namespaces

# Allow DNS from all namespaces
cat <<EOF | kubectl apply -f -
apiVersion: projectcalico.org/v3
kind: GlobalNetworkPolicy
metadata:
  name: allow-dns-global
spec:
  order: 0
  selector: all()
  types:
  - Ingress
  - Egress
  ingress:
  - action: Allow
    protocol: UDP
    destination:
      ports:
      - 53
  - action: Allow
    protocol: TCP
    destination:
      ports:
      - 53
  egress:
  - action: Allow
    protocol: UDP
    destination:
      ports:
      - 53
  - action: Allow
    protocol: TCP
    destination:
      ports:
      - 53
EOF

# Allow all traffic in monitoring namespace
cat <<EOF | kubectl apply -f -
apiVersion: projectcalico.org/v3
kind: NetworkPolicy
metadata:
  name: allow-all-monitoring
  namespace: monitoring
spec:
  order: 0
  selector: all()
  types:
  - Ingress
  - Egress
  ingress:
  - action: Allow
  egress:
  - action: Allow
EOF
```

### 🔧 NodePort Access Issues

```bash
# Enable route_localnet for NodePort access
sudo sysctl -w net.ipv4.conf.lo.route_localnet=1
echo "net.ipv4.conf.lo.route_localnet=1" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

### 🔧 Logstash Configuration Issues

```bash
# Check Logstash logs
kubectl logs -n logging logstash-logstash-0 --tail=50

# Check mounted config
kubectl exec -it logstash-logstash-0 -n logging -- cat /usr/share/logstash/pipeline/logstash.conf

# Update ConfigMap
kubectl get configmap logstash-logstash-pipeline -n logging -o yaml

# Force reload
kubectl delete pod logstash-logstash-0 -n logging
```

### 🔧 Elasticsearch SSL Issues

```bash
# For Logstash/Filebeat, disable SSL verification
# In config:
ssl_certificate_verification => false
# or
ssl: false

# For Kibana:
elasticsearch.ssl.verificationMode: none
```

---

## Access URLs

| Service | URL | Credentials |
|---------|-----|-------------|
| **Prometheus** | `http://192.168.0.10:30090` | No auth |
| **Grafana** | `http://192.168.0.10:30030` | admin / (get password) |
| **Kibana** | `http://192.168.0.10:30561` | elastic / (get password) |

### Get Passwords

```bash
# Grafana
kubectl get secret prometheus-grafana -n monitoring -o jsonpath="{.data.admin-password}" | base64 -d ; echo

# Elasticsearch (Kibana)
kubectl get secret elasticsearch-master-credentials -n logging -o jsonpath="{.data.password}" | base64 -d ; echo
```

---

## Complete Stack Status

```bash
# Monitoring namespace
kubectl get pods -n monitoring

# Logging namespace
kubectl get pods -n logging
```

---

## 🔑 Key Takeaways

1. **Always use HTTPS for Elasticsearch 8.x** with `ssl_certificate_verification => false` for self-signed certs
2. **Calico network policies** can block DNS and inter-service communication
3. **route_localnet** is required for NodePort access on localhost
4. **CoreDNS** needs proper configuration for service discovery
5. **APM Server** requires the integration to be installed via Kibana
6. **Filebeat** should send logs to Logstash for processing (or directly to Elasticsearch)

---