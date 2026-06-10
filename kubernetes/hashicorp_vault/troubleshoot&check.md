## 1. Job Pod Crashing - Missing openssl

**Check:**
```bash
kubectl logs -n vault vault-certs-generator-2r8xz
```

**If you see:** `openssl: not found`

**Fix:** Change image from `bitnami/kubectl:latest` to `alpine:latest` and install openssl + kubectl in the command

---

## 2. ServiceAccount Missing Permissions

**Check:**
```bash
kubectl describe role vault-cert-generator-role -n vault
```

**If you see:** Only `create` verb, no `get` or `patch`

**Fix:** Add `get`, `list`, `patch`, `update`, `apply` verbs to the Role

---

## 3. ServiceAccount Token Not Mounted

**Check:**
```bash
kubectl describe pod vault-certs-generator-2r8xz -n vault | grep -A5 "Volumes"
```

**If you see:** No service account token volume

**Fix:** Add `automountServiceAccountToken: true` to pod spec

---

## 4. PVC Stuck in Pending

**Check:**
```bash
kubectl get pvc -n vault
kubectl get storageclass
```

**If you see:** No storageclass, PVC status Pending

**Fix:** Install local-path provisioner and set as default
```bash
kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/master/deploy/local-path-storage.yaml
kubectl patch storageclass local-path -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
```

---

## 5. ImagePullPolicy Error

**Check:**
```bash
kubectl describe pod vault-0 -n vault | grep -A10 "Events"
```

**If you see:** `ErrImageNeverPull`

**Fix:** Change `imagePullPolicy: Never` to `imagePullPolicy: IfNotPresent`

---

## 6. Vault Config Not Expanding Variables

**Check:**
```bash
kubectl exec -n vault vault-0 -- cat /tmp/vault.hcl 2>/dev/null
```

**If you see:** `${HOSTNAME}` instead of `vault-0`

**Fix:** Use `$HOSTNAME` (no curly braces) and run `envsubst '$HOSTNAME'` before starting Vault

---

## 7. envsubst Command Not Found

**Check:**
```bash
kubectl logs -n vault vault-0 | grep envsubst
```

**If you see:** `envsubst: not found`

**Fix:** Add `apk add --no-cache gettext` before using envsubst

---

## 8. Vault API Connection Refused

**Check:**
```bash
kubectl exec -n vault vault-0 -- netstat -tulpn | grep 8200
```

**If you see:** Port is listening but `vault status` fails

**Fix:** Use full command with VAULT_ADDR and VAULT_CACERT
```bash
kubectl exec -n vault vault-0 -- sh -c 'export VAULT_ADDR=https://127.0.0.1:8200 VAULT_CACERT=/vault/tls/ca.crt && vault status'
```

---

## 9. TLS Certificate Not Trusted

**Check:**
```bash
kubectl logs -n vault vault-0 | grep "certificate signed by unknown authority"
```

**If you see:** `tls: failed to verify certificate: x509: certificate signed by unknown authority`

**Fix:** Add `VAULT_CACERT=/vault/tls/ca.crt` to environment variables

---

## 10. Raft Retry Join Failing

**Check:**
```bash
kubectl logs -n vault vault-0 | grep "failed to get raft challenge"
```

**If you see:** Errors about joining vault-1 and vault-2

**Fix:** Remove `retry_join` blocks from ConfigMap for single node deployment

---

## 11. Vault Sealed After Restart

**Check:**
```bash
kubectl exec -n vault vault-0 -- sh -c 'export VAULT_ADDR=https://127.0.0.1:8200 VAULT_CACERT=/vault/tls/ca.crt && vault status'
```

**If you see:** `Sealed: true`

**Fix:** Unseal with the stored unseal key
```bash
kubectl exec -n vault vault-0 -- sh -c 'export VAULT_ADDR=https://127.0.0.1:8200 VAULT_CACERT=/vault/tls/ca.crt && vault operator unseal <your-unseal-key>'
```

---

## 12. Pod Stuck in Terminating

**Check:**
```bash
kubectl get pods -n vault
```

**If you see:** Pod stuck in Terminating for minutes

**Fix:** Force delete
```bash
kubectl delete pod vault-0 -n vault --force --grace-period=0
```

---

## 13. Vault Not Initialized

**Check:**
```bash
kubectl exec -n vault vault-0 -- sh -c 'export VAULT_ADDR=https://127.0.0.1:8200 VAULT_CACERT=/vault/tls/ca.crt && vault status'
```

**If you see:** `Initialized: false`

**Fix:** Initialize Vault
```bash
kubectl exec -n vault vault-0 -- sh -c 'export VAULT_ADDR=https://127.0.0.1:8200 VAULT_CACERT=/vault/tls/ca.crt && vault operator init -key-shares=1 -key-threshold=1'
```

---

## 14. Cannot Enable Secrets Engine

**Check:**
```bash
kubectl exec -n vault vault-0 -- sh -c 'export VAULT_ADDR=https://127.0.0.1:8200 VAULT_CACERT=/vault/tls/ca.crt && vault status'
```

**If you see:** `Sealed: true`

**Fix:** Unseal first, then enable secrets
```bash
kubectl exec -n vault vault-0 -- sh -c 'export VAULT_ADDR=https://127.0.0.1:8200 VAULT_CACERT=/vault/tls/ca.crt && vault operator unseal <key>'
kubectl exec -n vault vault-0 -- sh -c 'export VAULT_ADDR=https://127.0.0.1:8200 VAULT_CACERT=/vault/tls/ca.crt && vault secrets enable -path=secret kv-v2'
```

You're right. Here are the final verification commands after everything was working:

## Final Verification Commands

**Check Vault status:**
```bash
kubectl exec -n vault vault-0 -- sh -c 'export VAULT_ADDR=https://127.0.0.1:8200 VAULT_CACERT=/vault/tls/ca.crt && vault status'
```
**Expected:** `Initialized: true`, `Sealed: false`

**Login to Vault:**
```bash
kubectl exec -n vault vault-0 -- sh -c 'export VAULT_ADDR=https://127.0.0.1:8200 VAULT_CACERT=/vault/tls/ca.crt && vault login <YOUR_ROOT_TOKEN>'
```
**Expected:** `Success! You are now authenticated`

**Enable KV secrets engine:**
```bash
kubectl exec -n vault vault-0 -- sh -c 'export VAULT_ADDR=https://127.0.0.1:8200 VAULT_CACERT=/vault/tls/ca.crt && vault secrets enable -path=secret kv-v2'
```
**Expected:** `Success! Enabled the kv-v2 secrets engine`

**Create test secret:**
```bash
kubectl exec -n vault vault-0 -- sh -c 'export VAULT_ADDR=https://127.0.0.1:8200 VAULT_CACERT=/vault/tls/ca.crt && vault kv put secret/myapp username=admin password=password123'
```
**Expected:** `Success! Data written to: secret/data/myapp`

**Read test secret:**
```bash
kubectl exec -n vault vault-0 -- sh -c 'export VAULT_ADDR=https://127.0.0.1:8200 VAULT_CACERT=/vault/tls/ca.crt && vault kv get secret/myapp'
```
**Expected:** Shows username=admin, password=password123

**Enable Kubernetes auth:**
```bash
kubectl exec -n vault vault-0 -- sh -c 'export VAULT_ADDR=https://127.0.0.1:8200 VAULT_CACERT=/vault/tls/ca.crt && vault auth enable kubernetes'
```
**Expected:** `Success! Enabled kubernetes auth method`

**Configure Kubernetes auth:**
```bash
kubectl exec -n vault vault-0 -- sh -c 'export VAULT_ADDR=https://127.0.0.1:8200 VAULT_CACERT=/vault/tls/ca.crt && vault write auth/kubernetes/config kubernetes_host="https://$KUBERNETES_SERVICE_HOST:$KUBERNETES_SERVICE_PORT"'
```
**Expected:** `Success! Data written to: auth/kubernetes/config`

**Enable audit logging:**
```bash
kubectl exec -n vault vault-0 -- sh -c 'export VAULT_ADDR=https://127.0.0.1:8200 VAULT_CACERT=/vault/tls/ca.crt && vault audit enable file file_path=/dev/stdout'
```
**Expected:** `Success! Enabled the file audit device`

**Check audit logs:**
```bash
kubectl logs -n vault vault-0 | tail -20
```
**Expected:** Shows audit entries with request/response logs

**Check Raft cluster peers:**
```bash
kubectl exec -n vault vault-0 -- sh -c 'export VAULT_ADDR=https://127.0.0.1:8200 VAULT_CACERT=/vault/tls/ca.crt && vault operator raft list-peers'
```
**Expected:** Shows vault-0 as leader

**Access Vault UI:**
```bash
kubectl port-forward -n vault vault-0 8200:8200
```
**Expected:** UI accessible at `https://localhost:8200`

**Check all pods running:**
```bash
kubectl get pods -n vault
```
**Expected:** vault-0 Running, vault-certs-generator Completed

**Check all secrets created:**
```bash
kubectl get secrets -n vault
```
**Expected:** vault-ca, vault-tls present

**Check Job completed:**
```bash
kubectl get jobs -n vault
```
**Expected:** vault-certs-generator Complete