#!/bin/bash
# deploy_longevity_clinic.sh - Deploy Longevity Clinic to Railway
# Usage: ./scripts/deploy_longevity_clinic.sh [ENVIRONMENT]
#
# App-specific wrapper for Railway deployment.
# Loads env files and delegates to reflex-railway-deploy/deploy_all.sh.
#
# Environment: APP_ENV=test (default) | APP_ENV=prod
# Railway env: test (default) | prod

set -e

# ╔═══════════════════════════════════════════════════════════════════╗
# ║ CONFIGURATION                                                      ║
# ╚═══════════════════════════════════════════════════════════════════╝

# Railway project settings
RAILWAY_PROJECT="syntropy"
RAILWAY_ENVIRONMENT="${1:-test}"
BACKEND_SERVICE="longevity-clinic-backend"
FRONTEND_SERVICE="longevity-clinic"

# Map Railway environment to APP_ENV
case "$RAILWAY_ENVIRONMENT" in
    prod|production) export APP_ENV="prod" ;;
    *)               export APP_ENV="test" ;;
esac

# App-specific variables to sync to Railway (from .env files)
export APP_ENV_VARS="APP_NAME,CLINIC_NAME,ADMIN_ROLE_NAME,PATIENT_ROLE_NAME,THEME_COLOR"

# ╔═══════════════════════════════════════════════════════════════════╗
# ║ DEPLOYMENT                                                         ║
# ╚═══════════════════════════════════════════════════════════════════╝

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         LONGEVITY CLINIC DEPLOYMENT                          ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║ Railway Project:  $RAILWAY_PROJECT"
echo "║ Environment:      $RAILWAY_ENVIRONMENT (APP_ENV=$APP_ENV)"
echo "║ Backend Service:  $BACKEND_SERVICE"
echo "║ Frontend Service: $FRONTEND_SERVICE"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Call the generic deployment script
# Note: deploy_all.sh handles env file loading via functions/env.sh
exec ./reflex-railway-deploy/deploy_all.sh \
    -p "$RAILWAY_PROJECT" \
    -e "$RAILWAY_ENVIRONMENT" \
    -b "$BACKEND_SERVICE" \
    -n "$FRONTEND_SERVICE"
