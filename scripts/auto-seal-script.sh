#!/bin/bash
set -e

# ─────────────────────────────────────────────────────────────
# Configurable section
NAMESPACE="default"
SECRET_FILE="../manifests/db-secret.yaml"
SEALED_FILE="../manifests/db-secret-sealed.yaml"
CONTROLLER_NS="kube-system"
CONTROLLER_NAME="sealed-secrets"
KUBESEAL_VERSION=$(curl -s https://api.github.com/repos/bitnami-labs/sealed-secrets/releases/latest | grep tag_name | cut -d '"' -f 4 | sed 's/^v//')
# ─────────────────────────────────────────────────────────────

echo "[+] Adding Bitnami repo and installing sealed-secrets controller..."
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Install or upgrade the sealed-secrets controller
helm upgrade --install sealed-secrets bitnami/sealed-secrets \
  --namespace "$CONTROLLER_NS" \
  --create-namespace

echo "[+] Waiting for sealed-secrets controller to be ready..."
kubectl rollout status deployment/sealed-secrets -n "$CONTROLLER_NS"

# ─────────────────────────────────────────────────────────────
# Install kubeseal CLI (latest version)
if ! command -v kubeseal &> /dev/null; then
  echo "[+] Downloading kubeseal CLI version $KUBESEAL_VERSION..."
  curl -LO "https://github.com/bitnami-labs/sealed-secrets/releases/download/v${KUBESEAL_VERSION}/kubeseal-${KUBESEAL_VERSION}-linux-amd64.tar.gz"
  tar -xzf kubeseal-${KUBESEAL_VERSION}-linux-amd64.tar.gz kubeseal
  sudo install -m 755 kubeseal /usr/local/bin/kubeseal
  rm kubeseal kubeseal-${KUBESEAL_VERSION}-linux-amd64.tar.gz
else
  echo "[✔] kubeseal already installed"
fi

kubeseal --version
# ─────────────────────────────────────────────────────────────

# Seal the secret
echo "[*] Sealing secret from: $SECRET_FILE"
kubeseal \
  --controller-namespace="$CONTROLLER_NS" \
  --controller-name="$CONTROLLER_NAME" \
  --format=yaml \
  < "$SECRET_FILE" > "$SEALED_FILE"

echo "[✔] Sealed secret written to: $SEALED_FILE"

echo "appling the secret yaml for deplyment of secrets"
kubectl apply -f ../manifests/db-secret-sealed.yaml
