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
export APP_ENV_VARS="APP_NAME CLINIC_NAME ADMIN_ROLE_NAME PATIENT_ROLE_NAME THEME_COLOR"

# Load app-specific .env if exists
if [ -f ".env" ]; then
    set -a; source ".env"; set +a
fi

# Set defaults if not in .env
export APP_NAME="${APP_NAME:-Vitality Clinic}"
export CLINIC_NAME="${CLINIC_NAME:-Vitality Health}"
export ADMIN_ROLE_NAME="${ADMIN_ROLE_NAME:-Administrator}"
export PATIENT_ROLE_NAME="${PATIENT_ROLE_NAME:-Patient}"
export THEME_COLOR="${THEME_COLOR:-emerald}"

echo "=========================================="
echo "Longevity Clinic Deployment"
echo "=========================================="
echo "Environment: $RAILWAY_ENVIRONMENT"
echo "App Name: $APP_NAME"
echo "=========================================="

# Run the generic deployment script
./reflex-railway-deploy/deploy.sh \
    -p "$RAILWAY_PROJECT" \
    -e "$RAILWAY_ENVIRONMENT" \
    -b "$BACKEND_SERVICE" \
    -f "$FRONTEND_SERVICE" \
    --env-file ".env"
