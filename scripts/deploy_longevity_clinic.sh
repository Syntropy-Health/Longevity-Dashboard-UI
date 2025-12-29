#!/bin/bash
# deploy_longevity_clinic.sh - Deploy Longevity Clinic to Railway
# Usage: ./scripts/deploy_longevity_clinic.sh [ENVIRONMENT]
#
# Deploys both backend and frontend services to Railway using service IDs.
# This script is CI/CD friendly - no interactive prompts.
#
# Environment: test (default) | prod
# Requires: RAILWAY_TOKEN environment variable

set -e

# ╔═══════════════════════════════════════════════════════════════════╗
# ║ CONFIGURATION                                                      ║
# ╚═══════════════════════════════════════════════════════════════════╝

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Railway project ID (syntropy)
RAILWAY_PROJECT_ID="6f1a2867-4f3f-4787-bc15-3235a93dddc6"

# Environment configuration
RAILWAY_ENVIRONMENT="${1:-test}"
case "$RAILWAY_ENVIRONMENT" in
    prod|production)
        RAILWAY_ENVIRONMENT_ID="590b420e-e662-48c1-8b03-73930e535050"
        export APP_ENV="prod"
        ;;
    *)
        RAILWAY_ENVIRONMENT_ID="164a9416-0a44-4630-9dc7-060f868340e0"
        export APP_ENV="test"
        ;;
esac

# Service IDs
BACKEND_SERVICE_ID="9178afdf-da33-4114-b570-e41211aa2f69"
FRONTEND_SERVICE_ID="f5960f86-8af2-42b1-8da3-2491cce58437"
BACKEND_SERVICE_NAME="longevity-clinic-backend"
FRONTEND_SERVICE_NAME="longevity-clinic"

# Dockerfile locations
DEPLOY_DIR="$PROJECT_ROOT/reflex-railway-deploy"
DOCKERFILE_BACKEND="$DEPLOY_DIR/Dockerfile.backend"
DOCKERFILE_FRONTEND="$DEPLOY_DIR/Dockerfile.frontend"

# ╔═══════════════════════════════════════════════════════════════════╗
# ║ HELPER FUNCTIONS                                                   ║
# ╚═══════════════════════════════════════════════════════════════════╝

log() { echo "[INFO] $*"; }
success() { echo "[✓] $*"; }
error() { echo "[✗] $*" >&2; exit 1; }
warn() { echo "[!] $*"; }

load_env_files() {
    local envs_dir="$PROJECT_ROOT/envs"

    [ -f "$envs_dir/.env.base" ] && { set -a; source "$envs_dir/.env.base"; set +a; log "Loaded .env.base"; }
    [ -f "$envs_dir/.env.$APP_ENV" ] && { set -a; source "$envs_dir/.env.$APP_ENV"; set +a; log "Loaded .env.$APP_ENV"; }
    [ -f "$envs_dir/.env.secrets" ] && { set -a; source "$envs_dir/.env.secrets"; set +a; log "Loaded .env.secrets"; }
}

set_railway_env_vars() {
    local service_name=$1

    log "Setting environment variables for $service_name..."

    # Set required env vars in Railway service
    if [ -n "$REFLEX_DB_URL" ]; then
        railway variables set REFLEX_DB_URL="$REFLEX_DB_URL" \
            --service "$service_name" --environment "$RAILWAY_ENVIRONMENT" 2>/dev/null || warn "Could not set REFLEX_DB_URL"
    fi
    if [ -n "$OPENAI_API_KEY" ]; then
        railway variables set OPENAI_API_KEY="$OPENAI_API_KEY" \
            --service "$service_name" --environment "$RAILWAY_ENVIRONMENT" 2>/dev/null || warn "Could not set OPENAI_API_KEY"
    fi
    if [ -n "$CALL_API_TOKEN" ]; then
        railway variables set CALL_API_TOKEN="$CALL_API_TOKEN" \
            --service "$service_name" --environment "$RAILWAY_ENVIRONMENT" 2>/dev/null || warn "Could not set CALL_API_TOKEN"
    fi
    # Set APP_ENV
    railway variables set APP_ENV="$APP_ENV" \
        --service "$service_name" --environment "$RAILWAY_ENVIRONMENT" 2>/dev/null || warn "Could not set APP_ENV"
}

deploy_service() {
    local service_id=$1
    local service_name=$2
    local dockerfile=$3

    log "Deploying $service_name..."

    # Set environment variables in Railway before deploying
    set_railway_env_vars "$service_name"

    # Copy Dockerfile to project root
    cp "$dockerfile" "$PROJECT_ROOT/Dockerfile" || error "Failed to copy Dockerfile"

    cd "$PROJECT_ROOT"

    # Set Railway project ID for authentication context
    export RAILWAY_PROJECT_ID="$RAILWAY_PROJECT_ID"

    # Deploy using railway up with explicit service and environment flags
    railway up -d --service "$service_name" --environment "$RAILWAY_ENVIRONMENT" 2>&1 || error "Failed to deploy $service_name"

    # Cleanup
    rm -f "$PROJECT_ROOT/Dockerfile"

    success "$service_name deployed"
}

# ╔═══════════════════════════════════════════════════════════════════╗
# ║ VALIDATION                                                         ║
# ╚═══════════════════════════════════════════════════════════════════╝

# Check Railway CLI
command -v railway &>/dev/null || error "Railway CLI not found. Install: npm install -g @railway/cli"

# Check RAILWAY_TOKEN for CI/CD
if [ -z "$RAILWAY_TOKEN" ]; then
    # Try interactive login check
    if ! railway whoami &>/dev/null; then
        error "Not authenticated. Set RAILWAY_TOKEN or run: railway login"
    fi
    log "Using interactive Railway session"
else
    log "Using RAILWAY_TOKEN for authentication"
fi

# Check Dockerfiles exist
[ -f "$DOCKERFILE_BACKEND" ] || error "Backend Dockerfile not found: $DOCKERFILE_BACKEND"
[ -f "$DOCKERFILE_FRONTEND" ] || error "Frontend Dockerfile not found: $DOCKERFILE_FRONTEND"

# ╔═══════════════════════════════════════════════════════════════════╗
# ║ DEPLOYMENT                                                         ║
# ╚═══════════════════════════════════════════════════════════════════╝

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         LONGEVITY CLINIC DEPLOYMENT                          ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║ Environment:      $RAILWAY_ENVIRONMENT (APP_ENV=$APP_ENV)"
echo "║ Project ID:       $RAILWAY_PROJECT_ID"
echo "║ Environment ID:   $RAILWAY_ENVIRONMENT_ID"
echo "║ Backend:          $BACKEND_SERVICE_NAME ($BACKEND_SERVICE_ID)"
echo "║ Frontend:         $FRONTEND_SERVICE_NAME ($FRONTEND_SERVICE_ID)"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Load environment files
load_env_files

# Deploy backend
deploy_service "$BACKEND_SERVICE_ID" "$BACKEND_SERVICE_NAME" "$DOCKERFILE_BACKEND"

# Deploy frontend
deploy_service "$FRONTEND_SERVICE_ID" "$FRONTEND_SERVICE_NAME" "$DOCKERFILE_FRONTEND"

echo ""
success "Deployment complete!"
echo "  Backend:  https://$BACKEND_SERVICE_NAME-$RAILWAY_ENVIRONMENT.up.railway.app"
echo "  Frontend: https://$FRONTEND_SERVICE_NAME-$RAILWAY_ENVIRONMENT.up.railway.app"
