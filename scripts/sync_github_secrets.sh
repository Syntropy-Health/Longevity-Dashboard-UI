#!/bin/bash
# sync_github_secrets.sh - Sync environment secrets to GitHub repository
# Usage: ./scripts/sync_github_secrets.sh [REPO]
#
# Prerequisites:
# - GitHub CLI (gh) installed and authenticated: gh auth login
# - Repository access with admin/write permissions
#
# This script reads from:
# - envs/.env.secrets (API keys, tokens)
# - envs/.env.prod (production config)
# And pushes them as GitHub Actions secrets.

set -e

# === CONFIGURATION ===
REPO="${1:-Healome/longevity_clinic}"
SECRETS_FILE="envs/.env.secrets"
PROD_FILE="envs/.env.prod"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log()     { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[✓]${NC} $1"; }
warn()    { echo -e "${YELLOW}[!]${NC} $1"; }
error()   { echo -e "${RED}[✗]${NC} $1"; exit 1; }

# === CHECK PREREQUISITES ===
command -v gh >/dev/null 2>&1 || error "GitHub CLI (gh) is not installed. Install with: brew install gh"

# Check authentication
gh auth status >/dev/null 2>&1 || error "Not authenticated. Run: gh auth login"

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║           GitHub Secrets Sync - Longevity Clinic               ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
log "Target repository: $REPO"
echo ""

# === SECRETS TO SYNC ===
# Define which secrets to sync (key=description)
declare -A SECRETS_MAP=(
    # From .env.secrets
    ["OPENAI_API_KEY"]="OpenAI API key for LLM features"
    ["CALL_API_TOKEN"]="Call logs API authentication token"
    # From .env.prod
    ["REFLEX_DB_URL"]="Production PostgreSQL connection string"
)

# Railway token is special - prompt if not in env
declare -A EXTRA_SECRETS=(
    ["RAILWAY_TOKEN"]="Railway deployment token (from railway.app/account/tokens)"
)

# === LOAD ENV FILES ===
load_env() {
    local file=$1
    if [ -f "$file" ]; then
        log "Loading $file..."
        set -a
        source "$file"
        set +a
        success "Loaded $file"
    else
        warn "File not found: $file"
    fi
}

load_env "$SECRETS_FILE"
load_env "$PROD_FILE"

# === SYNC SECRETS ===
echo ""
log "Syncing secrets to GitHub..."
echo ""

sync_secret() {
    local key=$1
    local desc=$2
    local value="${!key}"
    
    if [ -z "$value" ]; then
        warn "  $key: Not set (skipping)"
        return 1
    fi
    
    # Mask the value for display
    local masked="${value:0:4}...${value: -4}"
    
    echo -n "  $key ($masked): "
    if echo "$value" | gh secret set "$key" --repo "$REPO" 2>/dev/null; then
        echo -e "${GREEN}✓${NC}"
        return 0
    else
        echo -e "${RED}✗${NC}"
        return 1
    fi
}

# Sync main secrets
synced=0
failed=0

for key in "${!SECRETS_MAP[@]}"; do
    if sync_secret "$key" "${SECRETS_MAP[$key]}"; then
        ((synced++))
    else
        ((failed++))
    fi
done

# === HANDLE RAILWAY TOKEN ===
echo ""
log "Checking Railway token..."

if [ -n "$RAILWAY_TOKEN" ]; then
    if sync_secret "RAILWAY_TOKEN" "Railway deployment token"; then
        ((synced++))
    else
        ((failed++))
    fi
else
    warn "RAILWAY_TOKEN not found in environment"
    echo ""
    echo "To add Railway token:"
    echo "  1. Go to https://railway.app/account/tokens"
    echo "  2. Create a new token"
    echo "  3. Run: gh secret set RAILWAY_TOKEN --repo $REPO"
    echo ""
    read -p "Enter Railway token now (or press Enter to skip): " -s railway_token
    echo ""
    
    if [ -n "$railway_token" ]; then
        RAILWAY_TOKEN="$railway_token"
        if sync_secret "RAILWAY_TOKEN" "Railway deployment token"; then
            ((synced++))
        else
            ((failed++))
        fi
    else
        warn "Skipping RAILWAY_TOKEN"
        ((failed++))
    fi
fi

# === SUMMARY ===
echo ""
echo "════════════════════════════════════════════════════════════════"
echo -e "  ${GREEN}Synced: $synced${NC}  |  ${YELLOW}Skipped/Failed: $failed${NC}"
echo "════════════════════════════════════════════════════════════════"
echo ""

# === VERIFY ===
log "Verifying secrets in repository..."
echo ""
gh secret list --repo "$REPO"

echo ""
success "GitHub secrets sync complete!"
echo ""
echo "Next steps:"
echo "  1. Go to GitHub Actions: https://github.com/$REPO/actions"
echo "  2. Select 'Deploy to Railway' workflow"
echo "  3. Click 'Run workflow' and choose environment"
echo ""
