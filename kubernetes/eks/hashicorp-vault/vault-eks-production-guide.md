# Production-Ready Guide: Deploy HashiCorp Vault on EKS with AWS KMS Auto-Unseal

> **Version:** 2.0 (Production-Hardened)  
> **Scope:** This guide is intended for production deployments. For development environments, see the "Development Mode" section at the end.  
> **Last Updated:** 2026-06-13

---

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Prerequisites & Security Warnings](#prerequisites--security-warnings)
3. [Create EKS Cluster](#create-eks-cluster)
4. [Create IAM Role and KMS Key](#create-iam-role-and-kms-key)
5. [Install EBS CSI Driver](#install-ebs-csi-driver)
6. [TLS Certificate Setup](#tls-certificate-setup)
7. [Deploy Vault with Helm (HA Mode)](#deploy-vault-with-helm-ha-mode)
8. [Initialize and Unseal Vault](#initialize-and-unseal-vault)
9. [Configure Vault Policies and Access](#configure-vault-policies-and-access)
10. [Enable Kubernetes Authentication](#enable-kubernetes-authentication)
11. [Testing and Verification](#testing-and-verification)
12. [Backup and Disaster Recovery](#backup-and-disaster-recovery)
13. [Troubleshooting](#troubleshooting)
14. [Cleanup](#cleanup)
15. [Development Mode (Quick Start)](#development-mode-quick-start)

---

## Architecture Overview

### Why This Architecture?

| Component | Purpose | Why It Matters |
|-----------|---------|----------------|
| **AWS KMS Auto-Unseal** | Encrypts Vault's master key | Eliminates manual unsealing on restarts, enables true HA |
| **IAM Role + OIDC** | Short-lived credentials for KMS access | No long-term secrets stored in pods; automatic credential rotation |
| **EBS CSI Driver** | Persistent, encrypted block storage | Survives pod restarts and node failures; required for Raft |
| **Raft Storage (HA)** | Distributed consensus backend | 3-node cluster with automatic failover; no external dependency |
| **TLS Everywhere** | Encrypted in-transit data | Prevents MITM attacks, credential sniffing, compliance violations |
| **Pod Anti-Affinity** | Distributes pods across nodes | Prevents single node failure from taking down Vault |
| **Audit Logging** | Immutable operation logs | Required for forensics, compliance (SOC2, PCI-DSS, etc.) |
| **Network Policies** | Namespace-level firewall | Restricts Vault access to authorized pods only |

### Architecture Diagram (Conceptual)

```
┌─────────────────────────────────────────────────────────────┐
│                        EKS Cluster (EC2)                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │  vault-0    │  │  vault-1    │  │  vault-2    │           │
│  │  (Leader)   │  │  (Follower) │  │  (Follower) │           │
│  │  + Raft     │  │  + Raft     │  │  + Raft     │           │
│  │  + Audit    │  │  + Audit    │  │  + Audit    │           │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘           │
│         │                │                │                  │
│         └────────────────┴────────────────┘                  │
│                          │                                   │
│              ┌─────────────┴─────────────┐                    │
│              │    Kubernetes Service     │                    │
│              │    (Active Node Routing)  │                    │
│              └─────────────┬─────────────┘                    │
│                            │                                 │
│              ┌─────────────┴─────────────┐                    │
│              │   NetworkPolicy (Ingress)   │                    │
│              │   Only: authorized pods    │                    │
│              └───────────────────────────┘                    │
└─────────────────────────────────────────────────────────────┘
                            │
              ┌─────────────┴─────────────┐
              │        AWS KMS Key         │
              │   (Auto-Unseal Master Key) │
              └───────────────────────────┘
```

---

## Prerequisites & Security Warnings

### Required Tools
```bash
# Verify versions before starting
aws --version        # >= 2.15
eksctl version       # >= 0.180
kubectl version      # >= 1.28
helm version         # >= 3.14
jq --version         # >= 1.7
openssl version      # >= 3.0
```

### ⚠️ Critical Security Warnings

1. **Never disable TLS in production.** The development mode section at the end shows how to test without TLS, but production requires certificates.
2. **Never store root tokens in plain text files.** Use AWS Secrets Manager or a secure vault (e.g., 1Password, HashiCorp Vault itself with a separate unseal key).
3. **Never delete the KMS key while Vault is in use.** Schedule deletion only after Vault is fully decommissioned and data is migrated.
4. **Always test backup/restore before going live.** An untested backup is not a backup.
5. **Always enable audit logging.** Without it, you cannot detect unauthorized access or meet compliance requirements.

---

## Create EKS Cluster

> **EC2-based cluster is required.** Fargate does not support EBS persistent volumes, privileged containers, or DaemonSets that Vault needs for Raft storage and audit logging.

```bash
# Create cluster with OIDC enabled (required for IAM roles for service accounts)
# Note: --zones must be defined when using --node-zones, and must be a superset of node-zones
# 
# SECURITY WARNING: eksctl enables public API endpoint access by default.
# For production, disable public access and use bastion host or VPN:
#   --vpc-private-subnets 
#   --vpc-public-subnets (for NAT/bastion)
#   --managed=false (to customize endpoint access)
# Then use: eksctl utils update-cluster-endpoints --private-access=true --public-access=false
eksctl create cluster \
  --name vault-production \
  --region us-east-1 \
  --version 1.31 \
  --zones us-east-1a,us-east-1b,us-east-1c \
  --nodegroup-name vault-nodes \
  --node-type t3.medium \
  --nodes 3 \
  --nodes-min 3 \
  --nodes-max 6 \
  --with-oidc \
  --managed \
  --node-private-networking \
  --node-zones us-east-1a,us-east-1b,us-east-1c

# Verify cluster readiness
kubectl get nodes
# Expected: 3 nodes in Ready status, spread across AZs
```

### Retrieve OIDC Provider URL
```bash
export CLUSTER_NAME="vault-production"
export AWS_REGION="us-east-1"
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

export OIDC_URL=$(aws eks describe-cluster   --name $CLUSTER_NAME   --region $AWS_REGION   --query "cluster.identity.oidc.issuer"   --output text)

export OIDC_ID=$(echo $OIDC_URL | cut -d '/' -f 5)

echo "OIDC URL: $OIDC_URL"
echo "OIDC ID: $OIDC_ID"
```

---

## Create IAM Role and KMS Key

### Step 1: Create KMS Key for Auto-Unseal

```bash
# Create KMS key with explicit policy (scoped, not wildcard)
export KMS_KEY_ID=$(aws kms create-key   --description "Vault auto-unseal key for EKS cluster $CLUSTER_NAME"   --region $AWS_REGION   --query 'KeyMetadata.KeyId'   --output text)

# Create alias for easier management
aws kms create-alias   --alias-name "alias/vault-auto-unseal-$CLUSTER_NAME"   --target-key-id $KMS_KEY_ID   --region $AWS_REGION

echo "KMS Key ID: $KMS_KEY_ID"
```

### Step 2: Create IAM Policy (Scoped to Specific KMS Key)

```bash
cat > vault-kms-policy.json <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "kms:Decrypt",
                "kms:Encrypt",
                "kms:DescribeKey"
            ],
            "Resource": "arn:aws:kms:$AWS_REGION:$AWS_ACCOUNT_ID:key/$KMS_KEY_ID"
        }
    ]
}
EOF

aws iam create-policy   --policy-name VaultKMSUnsealPolicy-$CLUSTER_NAME   --policy-document file://vault-kms-policy.json

export KMS_POLICY_ARN=$(aws iam list-policies   --query "Policies[?PolicyName=='VaultKMSUnsealPolicy-$CLUSTER_NAME'].Arn"   --output text)
```

### Step 3: Create IAM Role with OIDC Trust

```bash
cat > trust-policy.json <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Federated": "arn:aws:iam::$AWS_ACCOUNT_ID:oidc-provider/oidc.eks.$AWS_REGION.amazonaws.com/id/$OIDC_ID"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringEquals": {
                    "oidc.eks.$AWS_REGION.amazonaws.com/id/$OIDC_ID:sub": "system:serviceaccount:vault:vault",
                    "oidc.eks.$AWS_REGION.amazonaws.com/id/$OIDC_ID:aud": "sts.amazonaws.com"
                }
            }
        }
    ]
}
EOF

aws iam create-role   --role-name vault-auto-unseal-role-$CLUSTER_NAME   --assume-role-policy-document file://trust-policy.json

aws iam attach-role-policy   --role-name vault-auto-unseal-role-$CLUSTER_NAME   --policy-arn $KMS_POLICY_ARN

export VAULT_ROLE_ARN="arn:aws:iam::$AWS_ACCOUNT_ID:role/vault-auto-unseal-role-$CLUSTER_NAME"
```

### Step 4: Update KMS Key Policy to Allow IAM Role

> **Why a file?** Passing inline JSON with shell variable expansion via `--policy` often causes `MalformedPolicyDocumentException` due to quote escaping conflicts. Using a file avoids this entirely.

```bash
# Create the KMS key policy file with expanded variables
cat > kms-key-policy.json <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"AWS": "arn:aws:iam::$AWS_ACCOUNT_ID:root"},
            "Action": "kms:*",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Principal": {"AWS": "$VAULT_ROLE_ARN"},
            "Action": ["kms:Decrypt", "kms:Encrypt", "kms:DescribeKey"],
            "Resource": "*"
        }
    ]
}
EOF

# Apply the policy from file
aws kms put-key-policy \
  --key-id $KMS_KEY_ID \
  --policy-name default \
  --policy file://kms-key-policy.json
```

---

## Install EBS CSI Driver

```bash
# Create IAM service account for EBS CSI driver
eksctl create iamserviceaccount   --name ebs-csi-controller-sa   --namespace kube-system   --cluster $CLUSTER_NAME   --region $AWS_REGION   --attach-policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy   --approve   --role-only   --role-name AmazonEKS_EBS_CSI_DriverRole-$CLUSTER_NAME

export EBS_ROLE_ARN=$(aws iam get-role   --role-name AmazonEKS_EBS_CSI_DriverRole-$CLUSTER_NAME   --query 'Role.Arn'   --output text)

# Install EBS CSI driver addon
eksctl create addon   --name aws-ebs-csi-driver   --cluster $CLUSTER_NAME   --region $AWS_REGION   --service-account-role-arn $EBS_ROLE_ARN   --force

# Verify driver is running
kubectl get pods -n kube-system | grep ebs-csi
# Expected: ebs-csi-controller and ebs-csi-node pods in Running state
```

### Create StorageClass

```bash
cat <<EOF | kubectl apply -f -
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gp2
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
provisioner: ebs.csi.aws.com
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
parameters:
  type: gp2
  encrypted: "true"
EOF

# Note: gp3 with kmsKeyId can cause EBS CSI driver issues (AlreadyExists/InvalidVolume.NotFound)
# If you need gp3, create it without kmsKeyId or ensure the EBS CSI driver addon is fully ready first
```

---

## TLS Certificate Setup

> **Production Requirement:** Vault must use TLS for all communications. We use cert-manager with Let's Encrypt (or self-signed for internal use).

### Install cert-manager

```bash
helm repo add jetstack https://charts.jetstack.io
helm repo update

helm install cert-manager jetstack/cert-manager   --namespace cert-manager   --create-namespace   --version v1.14.0   --set installCRDs=true

kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=cert-manager -n cert-manager --timeout=120s
```

### Generate Self-Signed Certificate (Production: Use ACM or Let's Encrypt)

```bash
# Create CA key and certificate
openssl genrsa -out vault-ca-key.pem 2048
openssl req -x509 -new -nodes -key vault-ca-key.pem   -sha256 -days 3650 -out vault-ca-cert.pem   -subj "/CN=Vault CA/O=Your Organization"

# Create Vault server certificate
openssl genrsa -out vault-key.pem 2048
openssl req -new -key vault-key.pem -out vault-csr.pem   -subj "/CN=vault.vault.svc.cluster.local/O=Vault"

# Create extensions file for SANs
cat > vault-ext.cnf <<EOF
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = vault.vault.svc.cluster.local
DNS.2 = vault.vault.svc
DNS.3 = vault
DNS.4 = localhost
IP.1 = 127.0.0.1
EOF

openssl x509 -req -in vault-csr.pem -CA vault-ca-cert.pem -CAkey vault-ca-key.pem   -CAcreateserial -out vault-cert.pem -days 365 -sha256 -extfile vault-ext.cnf

# Create Kubernetes TLS secret
kubectl create namespace vault --dry-run=client -o yaml | kubectl apply -f -

kubectl create secret tls vault-tls   --cert=vault-cert.pem   --key=vault-key.pem   --namespace vault   --dry-run=client -o yaml | kubectl apply -f -

kubectl create secret generic vault-ca   --from-file=ca.crt=vault-ca-cert.pem   --namespace vault   --dry-run=client -o yaml | kubectl apply -f -
```

---

## Deploy Vault with Helm (HA Mode)

### Add HashiCorp Helm Repository

```bash
helm repo add hashicorp https://helm.releases.hashicorp.com
helm repo update
```

### Create Production Values File

```bash
cat > vault-values.yaml <<EOF
global:
  namespace: vault
  tlsDisable: false  # ⚠️ NEVER set to true in production

injector:
  enabled: true
  replicaCount: 2
  # Security hardening for injector
  securityContext:
    runAsNonRoot: true
    runAsUser: 65534
    readOnlyRootFilesystem: true
  resources:
    requests:
      memory: "256Mi"
      cpu: "250m"
    limits:
      memory: "512Mi"
      cpu: "500m"

server:
  # Service account with IAM role for KMS access
  serviceAccount:
    create: true
    name: vault
    annotations:
      eks.amazonaws.com/role-arn: $VAULT_ROLE_ARN

  # High Availability with Raft storage
  ha:
    enabled: true
    replicas: 3
    raft:
      enabled: true
      setNodeId: true
      config: |
        ui = true

        listener "tcp" {
          address = "[::]:8200"
          cluster_address = "[::]:8201"
          tls_cert_file = "/vault/userconfig/vault-tls/tls.crt"
          tls_key_file  = "/vault/userconfig/vault-tls/tls.key"
          tls_disable = false
        }

        seal "awskms" {
          region     = "$AWS_REGION"
          kms_key_id = "$KMS_KEY_ID"
        }

        storage "raft" {
          path = "/vault/data"
          node_id = "NODE_ID"
          retry_leader_election = true
          retry_join {
            leader_api_addr = "https://vault-0.vault-internal:8200"
            leader_ca_cert_file = "/vault/userconfig/vault-ca/vault-ca/ca.crt"
          }
          retry_join {
            leader_api_addr = "https://vault-1.vault-internal:8200"
            leader_ca_cert_file = "/vault/userconfig/vault-ca/vault-ca/ca.crt"
          }
          retry_join {
            leader_api_addr = "https://vault-2.vault-internal:8200"
            leader_ca_cert_file = "/vault/userconfig/vault-ca/vault-ca/ca.crt"
          }
        }

        service_registration "kubernetes" {}

        disable_mlock = true
        log_level = "info"

  # Data storage (Raft data)
  dataStorage:
    enabled: true
    size: 20Gi
    storageClass: gp2
    accessMode: ReadWriteOnce

  # Audit log storage (immutable, required for compliance)
  auditStorage:
    enabled: true
    size: 10Gi
    storageClass: gp2
    accessMode: ReadWriteOnce

  # Security contexts (run as non-root, read-only filesystem)
  securityContext:
    runAsNonRoot: true
    runAsUser: 100
    runAsGroup: 1000
    fsGroup: 1000
    readOnlyRootFilesystem: true
    allowPrivilegeEscalation: false
    seccompProfile:
      type: RuntimeDefault

  # Resource limits
  resources:
    requests:
      memory: "1Gi"
      cpu: "500m"
    limits:
      memory: "2Gi"
      cpu: "1000m"

  # Pod anti-affinity: spread across nodes
  affinity: |
    podAntiAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        - labelSelector:
            matchLabels:
              app.kubernetes.io/name: vault
              app.kubernetes.io/instance: vault
              component: server
          topologyKey: kubernetes.io/hostname

  # Node affinity: spread across AZs (optional but recommended)
  nodeAffinity: |
    preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        preference:
          matchExpressions:
            - key: topology.kubernetes.io/zone
              operator: In
              values:
                - us-east-1a
                - us-east-1b
                - us-east-1c

  # Extra volumes for TLS certificates
  extraVolumes:
    - type: secret
      name: vault-tls
      path: "/vault/userconfig/vault-tls"
    - type: secret
      name: vault-ca
      path: "/vault/userconfig/vault-ca"

  # Note: The Helm chart mounts secrets at /vault/userconfig/<name>/<name>/
  # So the actual paths are:
  # - /vault/userconfig/vault-tls/vault-tls/tls.crt
  # - /vault/userconfig/vault-ca/vault-ca/ca.crt"

  # Extra environment variables
  extraEnvironmentVars:
    VAULT_CACERT: "/vault/userconfig/vault-ca/ca.crt"
    VAULT_ADDR: "https://127.0.0.1:8200"

  # Pod Disruption Budget (ensure quorum during node maintenance)
  podDisruptionBudget:
    enabled: true
    maxUnavailable: 1

ui:
  enabled: true
  serviceType: ClusterIP  # Use ingress or port-forward, not public LoadBalancer
  # For production, expose via Ingress with TLS termination
  # activeVaultPodOnly: true  # Only route to active node

# Network Policy: restrict ingress to authorized namespaces
networkPolicy:
  enabled: true
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: vault
        - namespaceSelector:
            matchLabels:
              name: kube-system
      ports:
        - protocol: TCP
          port: 8200
        - protocol: TCP
          port: 8201
EOF
```

### Install Vault

```bash
helm install vault hashicorp/vault   --namespace vault   --values vault-values.yaml   --wait   --timeout 15m

# Watch pods come up (should see 3 pods, one becomes leader)
kubectl get pods -n vault -w
# Press Ctrl+C once all pods show Running and 1/1 ready
```

### Verify PVCs are Bound

```bash
kubectl get pvc -n vault
# Expected: 3 data PVCs and 3 audit PVCs, all Bound
```

---

## Initialize and Unseal Vault

### Initialize Vault (One-Time Operation)

```bash
# Initialize with key shares (for recovery, not unsealing)
kubectl exec -n vault vault-0 -- vault operator init   -key-shares=5   -key-threshold=3   -format=json > cluster-keys.json

# Extract root token
export ROOT_TOKEN=$(cat cluster-keys.json | jq -r '.root_token')

# Extract recovery keys (for disaster recovery, not daily unsealing)
cat cluster-keys.json | jq -r '.recovery_keys_b64[]' > vault-recovery-keys.txt

# Store root token in AWS Secrets Manager (PRODUCTION REQUIREMENT)
aws secretsmanager create-secret   --name vault-root-token-$CLUSTER_NAME   --description "Root token for Vault cluster $CLUSTER_NAME"   --secret-string "$ROOT_TOKEN"   --region $AWS_REGION

echo "Root token stored in AWS Secrets Manager: vault-root-token-$CLUSTER_NAME"
echo "Recovery keys saved to: vault-recovery-keys.txt (STORE SECURELY OFFLINE)"
```

### Verify Auto-Unseal is Working

```bash
# Check status - should show Initialized: true, Sealed: false
kubectl exec -n vault vault-0 -- vault status

# Verify all nodes are unsealed
for i in 0 1 2; do
  echo "=== vault-$i ==="
  kubectl exec -n vault vault-$i -- vault status | grep -E "Sealed|Initialized|HA Mode"
done
```

### Test Auto-Unseal by Restarting a Pod

```bash
# Delete a follower pod
kubectl delete pod vault-1 -n vault
sleep 60

# Verify it comes back unsealed
kubectl exec -n vault vault-1 -- vault status
# Expected: Sealed: false (KMS auto-unsealed it)
```

### Join Raft Cluster (Nodes 1 and 2)

```bash
# Get leader API address
export VAULT_LEADER=$(kubectl exec -n vault vault-0 -- sh -c 'echo https://$(hostname -i):8200')

# Join vault-1 to the cluster
kubectl exec -n vault vault-1 -- vault operator raft join   -leader-ca-cert="$(kubectl get secret vault-ca -n vault -o jsonpath='{.data.ca\.crt}' | base64 -d)"   $VAULT_LEADER

# Join vault-2 to the cluster
kubectl exec -n vault vault-2 -- vault operator raft join   -leader-ca-cert="$(kubectl get secret vault-ca -n vault -o jsonpath='{.data.ca\.crt}' | base64 -d)"   $VAULT_LEADER

# Verify cluster members
kubectl exec -n vault vault-0 -- vault login $ROOT_TOKEN
kubectl exec -n vault vault-0 -- vault operator raft list-peers
# Expected: 3 nodes, one leader, two followers
```

---

## Configure Vault Policies and Access

### Enable KV Secrets Engine v2

```bash
kubectl exec -n vault vault-0 -- vault secrets enable -path=secret kv-v2
```

### Create Application Policy (Least Privilege)

```bash
cat > myapp-policy.hcl <<EOF
path "secret/data/myapp/\+" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

path "secret/metadata/myapp/\+" {
  capabilities = ["list"]
}
EOF

kubectl cp myapp-policy.hcl vault/vault-0:/tmp/myapp-policy.hcl
kubectl exec -n vault vault-0 -- vault policy write myapp-policy /tmp/myapp-policy.hcl
```

### Create Read-Only Policy

```bash
cat > readonly-policy.hcl <<EOF
path "secret/data/myapp/\+" {
  capabilities = ["read", "list"]
}

path "secret/metadata/myapp/\+" {
  capabilities = ["list"]
}
EOF

kubectl cp readonly-policy.hcl vault/vault-0:/tmp/readonly-policy.hcl
kubectl exec -n vault vault-0 -- vault policy write readonly-policy /tmp/readonly-policy.hcl
```

### Enable Audit Logging (Required for Compliance)

```bash
# Enable file audit device (logs to persistent volume)
kubectl exec -n vault vault-0 -- vault audit enable file file_path=/vault/audit/audit.log

# Verify audit device is active
kubectl exec -n vault vault-0 -- vault audit list
```

### Create Tokens with Different Permission Levels

```bash
# Create application token (short TTL for production)
export APP_TOKEN=$(kubectl exec -n vault vault-0 -- vault token create   -policy=myapp-policy   -ttl=24h   -renewable=true   -format=json | jq -r '.auth.client_token')

# Create read-only token
export READONLY_TOKEN=$(kubectl exec -n vault vault-0 -- vault token create   -policy=readonly-policy   -ttl=24h   -renewable=true   -format=json | jq -r '.auth.client_token')

# Store tokens in AWS Secrets Manager
aws secretsmanager create-secret   --name vault-app-token-$CLUSTER_NAME   --secret-string "$APP_TOKEN"   --region $AWS_REGION

aws secretsmanager create-secret   --name vault-readonly-token-$CLUSTER_NAME   --secret-string "$READONLY_TOKEN"   --region $AWS_REGION
```

### Store Test Secrets

```bash
kubectl exec -n vault vault-0 -- vault kv put secret/myapp/database   username="admin"   password="$(openssl rand -base64 32)"   host="postgres.example.com"

kubectl exec -n vault vault-0 -- vault kv put secret/myapp/redis   host="redis.example.com"   port="6379"   password="$(openssl rand -base64 32)"
```

---

## Enable Kubernetes Authentication

> This is the primary method for applications running in EKS to authenticate to Vault without static tokens.

### Enable Kubernetes Auth Method

```bash
kubectl exec -n vault vault-0 -- vault auth enable kubernetes
```

### Configure Kubernetes Auth

```bash
# Get Kubernetes CA certificate
export KUBE_CA_CERT=$(kubectl get configmap -n kube-system extension-apiserver-authentication -o=jsonpath='{.data.client-ca-file}' | base64 | tr -d '\n')

# Get internal Kubernetes API address
export KUBE_HOST="https://\$KUBERNETES_PORT_443_TCP_ADDR:443"

kubectl exec -n vault vault-0 -- vault write auth/kubernetes/config   kubernetes_host="$KUBE_HOST"   kubernetes_ca_cert="$KUBE_CA_CERT"   token_reviewer_jwt="@/var/run/secrets/kubernetes.io/serviceaccount/token"   issuer="https://kubernetes.default.svc.cluster.local"
```

### Create Kubernetes Auth Role

```bash
kubectl exec -n vault vault-0 -- vault write auth/kubernetes/role/myapp   bound_service_account_names=myapp-sa   bound_service_account_namespaces=myapp   policies=myapp-policy   ttl=1h
```

### Example: Application Pod Using Kubernetes Auth

```yaml
# myapp-deployment.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: myapp-sa
  namespace: myapp
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: myapp
spec:
  replicas: 2
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      serviceAccountName: myapp-sa
      containers:
        - name: myapp
          image: myapp:latest
          env:
            - name: VAULT_ADDR
              value: "https://vault.vault.svc.cluster.local:8200"
            - name: VAULT_CACERT
              value: "/vault/tls/ca.crt"
          volumeMounts:
            - name: vault-ca
              mountPath: /vault/tls
              readOnly: true
      volumes:
        - name: vault-ca
          secret:
            secretName: vault-ca
```

---

## Testing and Verification

### Test 1: Verify HA and Raft Consensus

```bash
# List Raft peers
kubectl exec -n vault vault-0 -- vault operator raft list-peers

# Expected output:
# Node       Address                        State       Voter
# ----       -------                        -----       -----
# vault-0    vault-0.vault-internal:8201    leader      true
# vault-1    vault-1.vault-internal:8201    follower    true
# vault-2    vault-2.vault-internal:8201    follower    true
```

### Test 2: Verify Auto-Unseal After Pod Restart

```bash
kubectl delete pod vault-0 -n vault
sleep 90
kubectl exec -n vault vault-0 -- vault status
# Expected: Sealed: false, Initialized: true
```

### Test 3: Verify TLS is Enforced

```bash
# This should FAIL (HTTP not allowed)
kubectl exec -n vault vault-0 -- sh -c 'VAULT_ADDR=http://127.0.0.1:8200 vault status'
# Expected: Error: URL is using HTTP

# This should SUCCEED (HTTPS with CA cert)
kubectl exec -n vault vault-0 -- vault status
# Expected: Status output with HTTPS
```

### Test 4: Verify RBAC - App Token Full Access

```bash
kubectl exec -n vault vault-0 -- vault login $APP_TOKEN

# Should succeed - write to allowed path
kubectl exec -n vault vault-0 -- vault kv put secret/myapp/test data="success" && echo "✅ Write allowed"

# Should succeed - read from allowed path
kubectl exec -n vault vault-0 -- vault kv get secret/myapp/test && echo "✅ Read allowed"

# Should fail - write to unauthorized path
kubectl exec -n vault vault-0 -- vault kv put secret/otherapp/data test="value" 2>&1 | grep -q "permission denied" && echo "❌ Unauthorized path denied"
```

### Test 5: Verify RBAC - Read-Only Token

```bash
kubectl exec -n vault vault-0 -- vault login $READONLY_TOKEN

# Should succeed - read
kubectl exec -n vault vault-0 -- vault kv get secret/myapp/database && echo "✅ Read allowed"

# Should fail - write
kubectl exec -n vault vault-0 -- vault kv put secret/myapp/new data="value" 2>&1 | grep -q "permission denied" && echo "❌ Write denied"

# Should fail - delete
kubectl exec -n vault vault-0 -- vault kv delete secret/myapp/database 2>&1 | grep -q "permission denied" && echo "❌ Delete denied"
```

### Test 6: Verify Audit Logging

```bash
# Check audit log exists
kubectl exec -n vault vault-0 -- ls -la /vault/audit/

# View recent audit entries
kubectl exec -n vault vault-0 -- tail -20 /vault/audit/audit.log
```

### Test 7: Verify Network Policy

```bash
# From an unauthorized namespace, try to reach Vault
kubectl run test-pod --image=busybox -n default --rm -it --restart=Never --   wget -qO- --timeout=5 https://vault.vault.svc.cluster.local:8200/v1/sys/health 2>&1
# Expected: Connection timeout or refused (NetworkPolicy blocks it)
```

---

## Backup and Disaster Recovery

### Automated Raft Snapshots

```bash
# Enable automated snapshots (every 24 hours, retain 7)
kubectl exec -n vault vault-0 -- vault write sys/storage/raft/snapshot-auto/config/daily   interval=24h   retain=7   path=/vault/data/snapshots   storage_type=local

# Verify snapshot configuration
kubectl exec -n vault vault-0 -- vault read sys/storage/raft/snapshot-auto/config/daily
```

### Manual Snapshot (Before Critical Changes)

```bash
# Create manual snapshot
kubectl exec -n vault vault-0 -- vault operator raft snapshot save /tmp/manual-snapshot.snap

# Copy snapshot locally
kubectl cp vault/vault-0:/tmp/manual-snapshot.snap ./manual-snapshot-$(date +%Y%m%d).snap

# Upload to S3 for off-site storage
aws s3 cp ./manual-snapshot-$(date +%Y%m%d).snap s3://your-vault-backups-bucket/
```

### Restore from Snapshot (Disaster Recovery)

```bash
# WARNING: Only restore to a fresh cluster. This will overwrite existing data.
# 1. Stop all Vault pods
kubectl scale sts vault --replicas=0 -n vault

# 2. Clear data volumes (on each node)
# (Requires manual intervention or init container)

# 3. Copy snapshot to leader pod
kubectl cp ./manual-snapshot.snap vault/vault-0:/tmp/restore.snap

# 4. Restore
kubectl exec -n vault vault-0 -- vault operator raft snapshot restore /tmp/restore.snap

# 5. Scale back up
kubectl scale sts vault --replicas=3 -n vault
```

---

## Troubleshooting

### Issue 1: Pods Stuck in Pending (PVC Not Binding)

> **Note on gp3 vs gp2:** The `gp3` StorageClass with `kmsKeyId` parameter can cause EBS CSI driver issues (AlreadyExists/InvalidVolume.NotFound errors) if the driver is not fully ready. Use `gp2` for initial deployment, then migrate to `gp3` once the cluster is stable.

```bash
# Check PVC status
kubectl get pvc -n vault
kubectl describe pvc data-vault-0 -n vault

# Common causes:
# - StorageClass not set as default
# - EBS CSI driver not running
# - AZ mismatch (volume in different AZ than pod)

# Fix: Verify StorageClass and EBS driver
kubectl get storageclass
kubectl get pods -n kube-system | grep ebs-csi
```

### Issue 1b: PVC Stuck Pending with "AlreadyExists" and "InvalidVolume.NotFound"

**Symptoms:** EBS CSI controller logs show:
```
rpc error: code = AlreadyExists desc = Could not create volume "...": parameters on this idempotent request are inconsistent with parameters used in previous request(s)
InvalidVolume.NotFound: The volume 'vol-...' does not exist.
```

**Root cause:** The EBS CSI driver has stale volume creation state. It thinks the volume exists but EC2 doesn't have it. This happens when:
- The driver created a volume but the create operation timed out
- The driver was restarted mid-creation
- There are conflicting parameters from a previous PVC with the same name

**Fix — Full reset:**

```bash
# Step 1: Delete all Vault resources
helm uninstall vault -n vault

# Step 2: Force-delete all PVCs (they will be recreated by StatefulSet)
kubectl delete pvc --all -n vault --force --grace-period=0

# Step 3: Restart the EBS CSI controller to clear its internal state
kubectl rollout restart deployment ebs-csi-controller -n kube-system
kubectl rollout status deployment ebs-csi-controller -n kube-system

# Step 4: Clean up any orphaned EBS volumes in AWS (optional but recommended)
# List volumes tagged with your cluster
aws ec2 describe-volumes   --filters "Name=tag:KubernetesCluster,Values=vault-production"   --query 'Volumes[*].{ID:VolumeId,State:State,Size:Size}'   --region us-east-1

# Delete orphaned volumes (ONLY if you're sure they're not in use)
# aws ec2 delete-volume --volume-id vol-xxxxxxxxxxxxxxxxx --region us-east-1

# Step 5: Verify EBS CSI driver is healthy
kubectl get pods -n kube-system -l app=ebs-csi-controller
kubectl logs -n kube-system -l app=ebs-csi-controller --tail=20

# Step 6: Reinstall Vault
helm install vault hashicorp/vault \
  --namespace vault \
  --values vault-values.yaml \
  --wait \
  --timeout 15m
```

**Prevention:**
- Always wait for the EBS CSI addon to be ACTIVE before creating PVCs
- Don't create PVCs manually before the StatefulSet creates them
- Ensure the StorageClass exists before installing Vault

### Issue 2: Vault Pods in CrashLoopBackOff (KMS Error)

```bash
# Check logs
kubectl logs vault-0 -n vault --tail=50

# Common errors:
# - "Invalid keyId": Check KMS_KEY_ID is correct and key exists
# - "AccessDenied": IAM role not attached to service account
# - "WebIdentityErr": OIDC provider not configured correctly

# Fix: Verify IAM role annotation
kubectl get sa vault -n vault -o yaml

# Fix: Verify KMS key policy allows the IAM role
aws kms get-key-policy --key-id $KMS_KEY_ID --policy-name default
```

### Issue 3: TLS Certificate Errors

```bash
# Verify certificate is mounted correctly
kubectl exec -n vault vault-0 -- ls -la /vault/userconfig/vault-tls/

# Verify certificate validity
kubectl exec -n vault vault-0 -- openssl x509 -in /vault/userconfig/vault-tls/tls.crt -text -noout | head -20

# Fix: Regenerate certificates if expired or SANs incorrect
```

### Issue 4: Raft Cluster Not Forming

```bash
# Check if nodes can communicate on port 8201
kubectl exec -n vault vault-0 -- nc -zv vault-1.vault-internal 8201
kubectl exec -n vault vault-0 -- nc -zv vault-2.vault-internal 8201

# Check Raft logs
kubectl exec -n vault vault-0 -- vault operator raft list-peers
kubectl logs vault-0 -n vault | grep -i raft

# Fix: Ensure headless service exists for internal communication
kubectl get svc -n vault vault-internal
```

### Issue 5: Audit Log Disk Full

```bash
# Check disk usage
kubectl exec -n vault vault-0 -- df -h /vault/audit

# Fix: Increase auditStorage size or set up log rotation
# (Note: Vault audit logs should be shipped to external SIEM, not stored indefinitely)
```

### Diagnostic Commands

```bash
# Full system status
kubectl get all -n vault
kubectl get pvc -n vault
kubectl get events -n vault --sort-by='.lastTimestamp'

# Pod details
kubectl describe pod vault-0 -n vault

# Vault configuration
kubectl exec -n vault vault-0 -- cat /vault/config/extraconfig-from-values.hcl

# Vault status on all nodes
for i in 0 1 2; do
  echo "=== vault-$i ==="
  kubectl exec -n vault vault-$i -- vault status
done
```

---

## Cleanup

### Remove Vault and Data

```bash
# Uninstall Vault (retains PVCs for safety)
helm uninstall vault -n vault

# Delete PVCs (WARNING: This deletes all Vault data)
kubectl delete pvc --all -n vault

# Delete namespace
kubectl delete namespace vault
```

### Remove EBS CSI Driver

```bash
eksctl delete addon   --cluster $CLUSTER_NAME   --name aws-ebs-csi-driver   --region $AWS_REGION

eksctl delete iamserviceaccount   --name ebs-csi-controller-sa   --namespace kube-system   --cluster $CLUSTER_NAME   --region $AWS_REGION
```

### Delete EKS Cluster

```bash
# WARNING: This deletes all resources in the cluster
eksctl delete cluster --name $CLUSTER_NAME --region $AWS_REGION
```

### Remove IAM Resources

```bash
# Detach and delete IAM policy
aws iam detach-role-policy   --role-name vault-auto-unseal-role-$CLUSTER_NAME   --policy-arn $KMS_POLICY_ARN

aws iam delete-role --role-name vault-auto-unseal-role-$CLUSTER_NAME
aws iam delete-policy --policy-arn $KMS_POLICY_ARN
```

### Schedule KMS Key Deletion

```bash
# WARNING: Only do this after confirming Vault is fully decommissioned
# and all data is backed up or migrated
aws kms schedule-key-deletion   --key-id $KMS_KEY_ID   --pending-window-in-days 7   --region $AWS_REGION
```

### Remove AWS Secrets Manager Secrets

```bash
aws secretsmanager delete-secret   --secret-id vault-root-token-$CLUSTER_NAME   --force-delete-without-recovery   --region $AWS_REGION

aws secretsmanager delete-secret   --secret-id vault-app-token-$CLUSTER_NAME   --force-delete-without-recovery   --region $AWS_REGION

aws secretsmanager delete-secret   --secret-id vault-readonly-token-$CLUSTER_NAME   --force-delete-without-recovery   --region $AWS_REGION
```

### Remove Local Files

```bash
rm -f vault-values.yaml vault-kms-policy.json trust-policy.json
rm -f cluster-keys.json vault-recovery-keys.txt
rm -f myapp-policy.hcl readonly-policy.hcl
rm -f vault-*.pem vault-*.cnf vault-*.srl
```

---

## Development Mode (Quick Start)

> **⚠️ WARNING:** This section is for development/learning only. Never use these settings in production.

If you need a quick, non-production environment for testing (e.g., learning Vault concepts, testing policies):

```yaml
# dev-values.yaml - FOR DEVELOPMENT ONLY
server:
  ha:
    enabled: false
  standalone:
    enabled: true
    config: |
      ui = true
      listener "tcp" {
        address = "0.0.0.0:8200"
        tls_disable = "true"  # ⚠️ INSECURE: Only for dev
      }
      storage "file" {
        path = "/vault/data"
      }
      disable_mlock = true
  dataStorage:
    enabled: true
    size: 5Gi
  resources:
    requests:
      memory: "256Mi"
      cpu: "250m"
ui:
  enabled: true
  serviceType: LoadBalancer
```

**Key differences from production:**
- TLS disabled (insecure)
- Single node (no HA)
- File storage instead of Raft
- No audit logging
- No network policies
- No pod anti-affinity
- LoadBalancer service (exposes to internet)

---

## Production Checklist

Before declaring your Vault deployment production-ready, verify:

- [ ] TLS is enabled on all listeners (`tls_disable = false`)
- [ ] HA mode is enabled with Raft storage (3+ nodes)
- [ ] Pod anti-affinity is configured (nodes spread across hosts)
- [ ] Audit logging is enabled and logs are shipping to SIEM
- [ ] Network policies restrict ingress to authorized namespaces
- [ ] Security contexts run containers as non-root with read-only filesystem
- [ ] Resource limits are set to prevent noisy neighbor issues
- [ ] Root token is stored in AWS Secrets Manager (not local files)
- [ ] Recovery keys are stored offline in a secure location
- [ ] Backup/restore procedures are tested and documented
- [ ] KMS key policy is scoped to the specific key (not `*`)
- [ ] IAM role trust policy is scoped to the specific service account
- [ ] Kubernetes auth is enabled for workload authentication
- [ ] Pod Disruption Budget is configured for maintenance windows
- [ ] Monitoring and alerting are configured for seal status and leader changes
- [ ] Disaster recovery runbook is documented and tested

---

## Summary

This production-ready deployment provides:

| Feature | Implementation |
|---------|---------------|
| **AWS KMS Auto-Unseal** | Automatic unsealing without manual intervention |
| **High Availability** | 3-node Raft cluster with automatic failover |
| **Persistent Storage** | EBS volumes with encryption for data and audit logs |
| **IAM Roles for Service Accounts** | Short-lived, auto-rotated credentials |
| **TLS Encryption** | All communications encrypted in transit |
| **Pod Anti-Affinity** | Nodes distributed across hosts and AZs |
| **RBAC Policies** | Least-privilege access control |
| **Audit Logging** | Immutable logs for compliance and forensics |
| **Network Policies** | Namespace-level traffic isolation |
| **Kubernetes Auth** | Workload identity without static tokens |
| **Automated Backups** | Scheduled Raft snapshots with retention |
| **Secure Secret Management** | Root tokens in AWS Secrets Manager |

**Critical reminders:**
- Store recovery keys in a physical safe or HSM, not on disk
- Test backup/restore quarterly
- Monitor audit logs for anomalies
- Rotate certificates before expiration
- Never disable TLS, even temporarily, in production
