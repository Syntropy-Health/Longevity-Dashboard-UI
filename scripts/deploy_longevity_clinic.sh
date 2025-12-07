#!/bin/bash
# deploy_longevity_clinic.sh - App-specific deployment script for Longevity Clinic
# 
# Usage: ./scripts/deploy_longevity_clinic.sh [ENVIRONMENT]
# 
# This script wraps the generic Railway deployment with app-specific configuration.

set -e

# App-specific configuration
RAILWAY_PROJECT="syntropy"
RAILWAY_ENVIRONMENT="${1:-test}"  # Default to 'test', can be overridden by first argument

# Service naming convention: <app>-<service>-<environment> or <app>-<environment>
BACKEND_SERVICE="longevity-clinic-backend"
FRONTEND_SERVICE="longevity-clinic"

# App-specific environment variables to sync to Railway
export APP_ENV_VARS="APP_NAME CLINIC_NAME ADMIN_ROLE_NAME PATIENT_ROLE_NAME THEME_COLOR APP_ENV OPENAI_API_KEY CALL_API_TOKEN"

# Determine which env file to load based on deployment environment
if [ "$RAILWAY_ENVIRONMENT" == "prod" ] || [ "$RAILWAY_ENVIRONMENT" == "production" ]; then
    ENV_FILE="envs/.env.prod"
    export APP_ENV="prod"
else
    ENV_FILE="envs/.env.dev"
    export APP_ENV="dev"
fi

# Load hierarchical env files
echo "Loading environment configuration..."
[ -f "envs/.env.base" ] && { set -a; source "envs/.env.base"; set +a; echo "  ✓ Loaded: envs/.env.base"; }
[ -f "$ENV_FILE" ] && { set -a; source "$ENV_FILE"; set +a; echo "  ✓ Loaded: $ENV_FILE"; }
[ -f "envs/.env.secrets" ] && { set -a; source "envs/.env.secrets"; set +a; echo "  ✓ Loaded: envs/.env.secrets"; }
[ -f ".env" ] && { set -a; source ".env"; set +a; echo "  ✓ Loaded: .env (override)"; }

# Set defaults if not in env files
export APP_NAME="${APP_NAME:-Vitality Clinic}"
export CLINIC_NAME="${CLINIC_NAME:-Vitality Health}"
export ADMIN_ROLE_NAME="${ADMIN_ROLE_NAME:-Administrator}"
export PATIENT_ROLE_NAME="${PATIENT_ROLE_NAME:-Patient}"
export THEME_COLOR="${THEME_COLOR:-emerald}"

echo "=========================================="
echo "Longevity Clinic Deployment"
echo "=========================================="
echo "Environment: $RAILWAY_ENVIRONMENT"
echo "App Env: $APP_ENV"
echo "App Name: $APP_NAME"
echo "Backend URL: ${REFLEX_API_URL:-localhost}"
echo "=========================================="

# Run the generic deployment script
./reflex-railway-deploy/deploy.sh \
    -p "$RAILWAY_PROJECT" \
    -e "$RAILWAY_ENVIRONMENT" \
    -b "$BACKEND_SERVICE" \
    -f "$FRONTEND_SERVICE" \
    --env-file ".env"
