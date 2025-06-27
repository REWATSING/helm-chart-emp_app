#!/bin/bash

set -e

NAMESPACE="default"
SECRET_FILE="manifests/sealed-secrets/db-secret.yaml"
SEALED_FILE="manifests/sealed-secrets/db-secret-sealed.yaml"
CONTROLLER_NS="kube-system"
CONTROLLER_NAME="sealed-secrets-controller"

echo "[*] Sealing secret from: $SECRET_FILE"

kubeseal \
  --controller-namespace=$CONTROLLER_NS \
  --controller-name=$CONTROLLER_NAME \
  --format=yaml \
  < "$SECRET_FILE" > "$SEALED_FILE"

echo "[✔] Sealed secret written to: $SEALED_FILE"

