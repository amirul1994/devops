***

## Phase 1: Native Kubernetes Secrets

Kubernetes Secrets are special objects designed to store sensitive information securely.

### Create Basic Secrets Using `kubectl`
Create a Secret directly from the command line. This method is quick and perfect for small-scale setups or testing environments.

```bash
kubectl create secret generic my-secret --from-literal=username=myuser --from-literal=password=mypassword
```

### Create Secrets Using YAML
Defining a Kubernetes Secret using a YAML file provides more control and allows you to manage your secrets in a structured, reusable way.

First, encode your sensitive values into Base64:
```bash
echo -n "myuser" | base64
echo -n "mypassword" | base64
```

Create a YAML file:
```bash
nano secret.yml
```

Add the following content (using the Base64 output from the previous step):
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-secret-yaml
type: Opaque
data:
  username: bXl1c2Vy # Base64-encoded myuser
  password: bXlwYXNzd29yZA== # Base64-encoded mypassword
```

Apply and verify:
```bash
kubectl apply -f secret.yml
kubectl get secrets
```

---

## Phase 2: Enable and Verify Encryption at Rest

> **🚨 IMPORTANT NOTE:** The following steps require direct access to your Kubernetes control plane node(s) and modify the `kube-apiserver` manifest. **Do not attempt this on managed cloud clusters (EKS, GKE, AKS)** as you do not have access to modify the API server configuration. This is strictly for self-managed clusters (e.g., Minikube, Kubeadm).

Before making any changes, back up the Kubernetes API server configuration file:
```bash
cp /etc/kubernetes/manifests/kube-apiserver.yaml /etc/kubernetes/manifests/kube-apiserver.yaml.bak
```

Tell Kubernetes to use your encryption configuration by appending a line to the API server arguments:
```bash
sed -i '/--authorization-mode=Node,RBAC/a\    --encryption-provider-config=/etc/kubernetes/encryption-config.yaml' /etc/kubernetes/manifests/kube-apiserver.yaml
```

Verify the line was added correctly:
```bash
grep encryption-provider-config /etc/kubernetes/manifests/kube-apiserver.yaml
```

Create the cryptographic key that Kubernetes will use to encrypt and decrypt your secrets:
```bash
head -c 32 /dev/urandom | base64
```
> **Note:** Copy the output of this command. You will need it in the next step.

Create the encryption configuration file:
```bash
vi /etc/kubernetes/encryption-config.yaml
```

Add the following content, replacing `BASE64-KEY-FROM-PREVIOUS-STEP` with the key you just generated:
```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
      - secrets
    providers:
      - aescbc:
          keys:
            - name: key1
              secret: BASE64-KEY-FROM-PREVIOUS-STEP
      - identity: {}
```

Verify the file and restart the kubelet to apply changes:
```bash
cat /etc/kubernetes/encryption-config.yaml
systemctl restart kubelet
```

> **⚠️ NOTE:** Restarting kubelet will temporarily restart your API server. It may take a minute for your cluster to become responsive again.

Verify encryption is working by creating a new secret and checking its format:
```bash
kubectl create secret generic encrypted-secret --from-literal=username=secureUser --from-literal=password=securePass
kubectl get secret encrypted-secret -o yaml
```

---

## Phase 3: Configure and Test RBAC Policies

### Create a Role
A Role defines permissions within a specific namespace.

```bash
nano secret-role.yml
```

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: secret-reader
  namespace: default
rules:
  - apiGroups: [""]
    resources: ["secrets"]
    verbs: ["get", "list"]
```

Apply and verify:
```bash
kubectl apply -f secret-role.yml
kubectl get roles -n default
```

### Create a RoleBinding
A RoleBinding connects a Role to a user, group, or ServiceAccount.

```bash
nano secret-binding.yml
```

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-secrets
  namespace: default
subjects:
  - kind: User
    name: mo
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: secret-reader
  apiGroup: rbac.authorization.k8s.io
```

Apply and verify:
```bash
kubectl apply -f secret-binding.yml
kubectl get rolebindings
```

### Test RBAC Permissions
Test allowed actions:
```bash
kubectl auth can-i get secrets --namespace=default --as=mo
```

Test denied actions:
```bash
kubectl auth can-i delete secrets --namespace=default --as=mo
```

### Bind Role to a ServiceAccount
Often, access is needed for pods rather than human users. Create a ServiceAccount:
```bash
kubectl create serviceaccount secret-accessor
```

Update `secret-binding.yml` to use the ServiceAccount instead of the User. Replace the `subjects` section:
```yaml
subjects:
  - kind: ServiceAccount
    name: secret-accessor
    namespace: default
```

Reapply the binding:
```bash
kubectl apply -f secret-binding.yml
```

---

## Phase 4: Inject Secrets into Pods

### Method 1: Environment Variables

```bash
nano secret-env-pod.yml
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-env-pod
spec:
  containers:
    - name: nginx-container
      image: nginx:latest
      imagePullPolicy: IfNotPresent
      env:
        - name: SECRET_USERNAME
          valueFrom:
            secretKeyRef:
              name: my-secret
              key: username
        - name: SECRET_PASSWORD
          valueFrom:
            secretKeyRef:
              name: my-secret
              key: password
```

Apply and check environment variables:
```bash
kubectl apply -f secret-env-pod.yml
kubectl exec secret-env-pod -- env | grep SECRET_
```

### Method 2: Mount as Files

```bash
nano secret-volume-pod.yml
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-volume-pod
spec:
  containers:
    - name: nginx-container
      image: nginx:latest
      imagePullPolicy: IfNotPresent
      volumeMounts:
        - name: secret-volume
          mountPath: "/etc/secrets"
          readOnly: true
  volumes:
    - name: secret-volume
      secret:
        secretName: my-secret
```

Apply and verify files exist:
```bash
kubectl apply -f secret-volume-pod.yml
kubectl exec secret-volume-pod -- ls /etc/secrets
```

### Validate Secure Access
Ensure applications can reach secrets:
```bash
kubectl exec secret-env-pod -- env | grep SECRET_
kubectl exec secret-volume-pod -- sh -c "cat /etc/secrets/password && echo"
```

---

## Phase 5: Deploy HashiCorp Vault

> **🚨 IMPORTANT NOTE:** The following creates a Vault instance using TLS and persistent storage. Before starting, ensure your environment supports `PersistentVolumeClaims` with the `local-path` storage class, or modify the StatefulSet accordingly if running strictly locally.

### Step 1: Prepare Manifest Files
Create a directory for your Vault manifests and save the following files with their respective names.

**`00-namespace.yaml`**
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: vault
```

**`01-certs-rbac.yaml`**
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: vault-cert-generator
  namespace: vault
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: vault-cert-generator-role
  namespace: vault
rules:
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["create", "get", "list", "patch", "update", "apply"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: vault-cert-generator-binding
  namespace: vault
subjects:
- kind: ServiceAccount
  name: vault-cert-generator
  namespace: vault
roleRef:
  kind: Role
  name: vault-cert-generator-role
  apiGroup: rbac.authorization.k8s.io
```

**`02-certs-job.yaml`**
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: vault-certs-generator
  namespace: vault
spec:
  backoffLimit: 3
  template:
    spec:
      serviceAccountName: vault-cert-generator
      automountServiceAccountToken: true
      restartPolicy: OnFailure
      containers:
        - name: certgen
          image: alpine:latest
          command:
            - /bin/sh
            - -c
            - |
              # Install OpenSSL and kubectl
              apk add --no-cache openssl curl

              curl -LO "https://dl.k8s.io/release/v1.28.0/bin/linux/amd64/kubectl"
              chmod +x kubectl
              mv kubectl /usr/local/bin/

              # Generate CA certificate
              openssl genrsa -out ca.key 2048

              openssl req \
                -new \
                -x509 \
                -days 365 \
                -key ca.key \
                -out ca.crt \
                -subj "/C=US/ST=State/L=City/O=Vault/CN=vault-ca"

              # Generate server key
              openssl genrsa -out server.key 2048

              # Create CSR configuration with SANs
              cat > csr.cnf <<'EOF'
              [req]
              default_bits = 2048
              prompt = no
              default_md = sha256
              distinguished_name = dn

              [dn]
              C = US
              ST = State
              L = City
              O = Vault
              CN = vault.vault.svc.cluster.local

              [v3_req]
              subjectAltName = @alt_names

              [alt_names]
              DNS.1 = vault.vault.svc.cluster.local
              DNS.2 = vault.vault.svc
              DNS.3 = vault-0.vault.vault.svc.cluster.local
              DNS.4 = vault-1.vault.vault.svc.cluster.local
              DNS.5 = vault-2.vault.vault.svc.cluster.local
              DNS.6 = localhost
              IP.1 = 127.0.0.1
              EOF

              # Generate CSR and sign certificate
              openssl req \
                -new \
                -key server.key \
                -out server.csr \
                -config csr.cnf

              openssl x509 \
                -req \
                -days 365 \
                -in server.csr \
                -CA ca.crt \
                -CAkey ca.key \
                -CAcreateserial \
                -out server.crt \
                -extensions v3_req \
                -extfile csr.cnf

              # Create/update Kubernetes secrets
              kubectl create secret generic vault-ca \
                --namespace=vault \
                --from-file=ca.crt \
                --dry-run=client \
                -o yaml | kubectl apply -f -

              kubectl create secret generic vault-tls \
                --namespace=vault \
                --from-file=server.crt \
                --from-file=server.key \
                --dry-run=client \
                -o yaml | kubectl apply -f -

              echo "Certificates generated successfully"
```

**`03-vault-configmap.yaml`**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: vault-config
  namespace: vault
data:
  vault.hcl: |
    storage "raft" {
      path = "/vault/data"
      node_id = "$HOSTNAME"
    }
    
    listener "tcp" {
      address       = "0.0.0.0:8200"
      cluster_address = "0.0.0.0:8201"
      tls_cert_file = "/vault/tls/server.crt"
      tls_key_file  = "/vault/tls/server.key"
    }
    
    disable_mlock = true
    api_addr = "https://$HOSTNAME.vault.vault.svc.cluster.local:8200"
    cluster_addr = "https://$HOSTNAME.vault.vault.svc.cluster.local:8201"
    ui = true
```

**`04-vault-service.yaml`**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: vault
  namespace: vault
  labels:
    app: vault
spec:
  clusterIP: None # Makes it headless
  selector:
    app: vault
  ports:
  - name: api
    port: 8200
  - name: cluster
    port: 8201
```

**`05-vault-statefulset.yaml`**
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: vault
  namespace: vault
spec:
  serviceName: vault
  replicas: 1
  selector:
    matchLabels:
      app: vault
  template:
    metadata:
      labels:
        app: vault
    spec:
      initContainers:
      - name: wait-for-certs
        image: busybox:1.36
        command: ['sh', '-c', 'until ls /vault/tls/server.crt; do echo "waiting for certs..."; sleep 2; done']
        volumeMounts:
        - name: tls
          mountPath: /vault/tls
      containers:
      - name: vault
        image: hashicorp/vault:latest
        imagePullPolicy: IfNotPresent
        env:
        - name: HOSTNAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: VAULT_CACERT
          value: /vault/tls/ca.crt
        ports:
        - containerPort: 8200
          name: api
        - containerPort: 8201
          name: cluster
        securityContext:
          capabilities:
            add: ["IPC_LOCK"]
          runAsUser: 0
        command:
        - /bin/sh
        - -c
        - |
          apk add --no-cache gettext
          cp /vault/tls/ca.crt /usr/local/share/ca-certificates/
          update-ca-certificates
          envsubst '$HOSTNAME' < /vault/config/vault.hcl > /tmp/vault.hcl
          exec vault server -config=/tmp/vault.hcl
        volumeMounts:
        - name: config
          mountPath: /vault/config
        - name: tls
          mountPath: /vault/tls
        - name: data
          mountPath: /vault/data
        readinessProbe:
          httpGet:
            scheme: HTTPS
            path: /v1/sys/health?standbyok=true
            port: 8200
          initialDelaySeconds: 15
          periodSeconds: 5
        livenessProbe:
          httpGet:
            scheme: HTTPS
            path: /v1/sys/health?standbyok=true
            port: 8200
          initialDelaySeconds: 30
          periodSeconds: 10
      volumes:
      - name: config
        configMap:
          name: vault-config
      - name: tls
        projected:
          sources:
          - secret:
              name: vault-tls
              items:
                - key: server.crt
                  path: server.crt
                - key: server.key
                  path: server.key
          - secret:
              name: vault-ca
              items:
                - key: ca.crt
                  path: ca.crt
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: local-path
      resources:
        requests:
          storage: 1Gi
```

### Step 2: Deploy Infrastructure
Apply the manifests in order. Because the StatefulSet relies on the certificates, we must wait for the Job to finish first.

```bash
# Apply namespace, RBAC, and Job
kubectl apply -f 00-namespace.yaml
kubectl apply -f 01-certs-rbac.yaml
kubectl apply -f 02-certs-job.yaml

# Wait for the cert generation job to complete
kubectl wait --for=condition=complete job/vault-certs-generator -n vault --timeout=60s

# Apply Vault configuration, Service, and StatefulSet
kubectl apply -f 03-vault-configmap.yaml
kubectl apply -f 04-vault-service.yaml
kubectl apply -f 05-vault-statefulset.yaml

# Wait for vault-0 to be ready for initialization
kubectl wait --for=condition=ready pod/vault-0 -n vault --timeout=120s
```

### Step 3: Initialize and Unseal Vault

> **⚠️ IMPORTANT:** The following commands must be executed **inside the Vault pod** because the pod contains the necessary CA certificates (`VAULT_CACERT`) and the correct internal network configuration. Running these from your local machine via port-forward may fail due to certificate verification issues or incorrect API addresses.

Initialize the Vault (saving the output securely):
```bash
kubectl exec -n vault vault-0 -- vault operator init -key-shares=1 -key-threshold=1 -format=json > cluster-keys.json
```

Extract the unseal key and root token:
```bash
VAULT_UNSEAL_KEY=$(cat cluster-keys.json | jq -r ".unseal_keys_b64[]")
VAULT_ROOT_TOKEN=$(cat cluster-keys.json | jq -r ".root_token")
```

Unseal `vault-0`:
```bash
kubectl exec -n vault vault-0 -- vault operator unseal $VAULT_UNSEAL_KEY
```

Login using the Root Token (inside the pod):
```bash
kubectl exec -n vault vault-0 -- vault login $VAULT_ROOT_TOKEN
```

---

## Phase 6: Configure Vault

> **⚠️ IMPORTANT:** All subsequent Vault CLI commands should be executed **inside the pod** to ensure they use the correct TLS certificates and internal service discovery.

### 1. Enable & Manage Secrets
In non-dev mode, the `secret/` path isn't enabled by default. We will enable KV v2 (which allows versioning).

```bash
# Enable the KV v2 secrets engine
kubectl exec -n vault vault-0 -- vault secrets enable -path=secret kv-v2

# Store a secret
kubectl exec -n vault vault-0 -- vault kv put secret/my-secret username=admin password=adminpass

# Retrieve a secret
kubectl exec -n vault vault-0 -- vault kv get secret/my-secret
```

### 2. Enable Kubernetes Authentication
When Vault runs inside Kubernetes, the best way for it to verify a pod's identity is to use the local service account token.

```bash
# Enable the auth method
kubectl exec -n vault vault-0 -- vault auth enable kubernetes

# Configure it to use the in-cluster Kubernetes API
kubectl exec -n vault vault-0 -- vault write auth/kubernetes/config \
    kubernetes_host="https://$KUBERNETES_SERVICE_HOST:$KUBERNETES_SERVICE_PORT"
```

### 3. Audit Secret Access
Writing audit logs to a file inside a container is an anti-pattern; if the pod restarts, the logs are destroyed. Instead, write to `stdout` so Kubernetes captures them natively.

```bash
kubectl exec -n vault vault-0 -- vault audit enable file file_path=stdout
```

Test the audit log by reading the secret again, and then checking the pod logs:
```bash
# Trigger an audited event
kubectl exec -n vault vault-0 -- vault kv get secret/my-secret

# View the audit logs captured by Kubernetes
kubectl logs -n vault vault-0 | tail -n 5
```