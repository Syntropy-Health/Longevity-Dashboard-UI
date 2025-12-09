#!/bin/bash
# deploy_longevity_clinic.sh - Deploy Longevity Clinic to Railway
# Usage: ./scripts/deploy_longevity_clinic.sh [ENVIRONMENT]
#
# This is an app-specific wrapper around the generic deploy_all.sh script.
# It sets app-specific configuration and calls the generic deployment.

set -e

# === CONFIG ===
RAILWAY_PROJECT="syntropy"
RAILWAY_ENVIRONMENT="${1:-test}"
BACKEND_SERVICE="longevity-clinic-backend"
FRONTEND_SERVICE="longevity-clinic"

# Variables to sync to Railway (APP_ENV_VARS used by deploy_all.sh)
export APP_ENV_VARS="APP_NAME,CLINIC_NAME,ADMIN_ROLE_NAME,PATIENT_ROLE_NAME,THEME_COLOR"

# === LOAD ENVIRONMENT ===
echo "Loading environment..."
load_env() { [ -f "$1" ] && { set -a; source "$1"; set +a; echo "  ✓ $1"; } || true; }

# Set APP_ENV based on target environment
[ "$RAILWAY_ENVIRONMENT" = "prod" ] || [ "$RAILWAY_ENVIRONMENT" = "production" ] && export APP_ENV="prod" || export APP_ENV="prod"

load_env "envs/.env.base"
load_env "envs/.env.${APP_ENV}"
load_env "envs/.env.secrets"

# Defaults from .env.base
export APP_NAME="${APP_NAME:-Vitality Clinic}"
export CLINIC_NAME="${CLINIC_NAME:-Vitality Health}"
export ADMIN_ROLE_NAME="${ADMIN_ROLE_NAME:-Administrator}"
export PATIENT_ROLE_NAME="${PATIENT_ROLE_NAME:-Patient}"
export THEME_COLOR="${THEME_COLOR:-emerald}"

echo ""
echo "=== Longevity Clinic Deployment ==="
echo "Target: $RAILWAY_ENVIRONMENT | App Env: $APP_ENV"
echo "Backend: $BACKEND_SERVICE | Frontend: $FRONTEND_SERVICE"
echo ""

# === DEPLOY ===
./reflex-railway-deploy/deploy_all.sh \
    -p "$RAILWAY_PROJECT" \
    -e "$RAILWAY_ENVIRONMENT" \
    -b "$BACKEND_SERVICE" \
    -n "$FRONTEND_SERVICE" \
    --skip-db \
    -y
