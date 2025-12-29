#!/bin/bash
# sync_env_secrets.sh - Sync .env.test secrets to GitHub before deployment
# Called by pre-push hook to ensure CI has latest credentials
#
# Usage: ./scripts/sync_env_secrets.sh [--check-only]
#
# Options:
#   --check-only    Only check if sync is needed, don't actually sync

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ENV_TEST_FILE="$PROJECT_ROOT/envs/.env.test"
REPOS=("Healome/longevity_clinic" "Syntropy-Health/Longevity-Dashboard-UI")

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log()     { echo -e "${BLUE}[sync]${NC} $1"; }
success() { echo -e "${GREEN}[✓]${NC} $1"; }
warn()    { echo -e "${YELLOW}[!]${NC} $1"; }
error()   { echo -e "${RED}[✗]${NC} $1"; }

CHECK_ONLY=false
[ "$1" = "--check-only" ] && CHECK_ONLY=true

# Check prerequisites
if ! command -v gh &>/dev/null; then
    warn "GitHub CLI not installed - skipping secret sync"
    exit 0
fi

if ! gh auth status &>/dev/null 2>&1; then
    warn "GitHub CLI not authenticated - skipping secret sync"
    exit 0
fi

# Load .env.test
if [ ! -f "$ENV_TEST_FILE" ]; then
    error "Missing $ENV_TEST_FILE"
    exit 1
fi

# Extract REFLEX_DB_URL from .env.test
REFLEX_DB_URL=$(grep -E "^REFLEX_DB_URL=" "$ENV_TEST_FILE" | cut -d'=' -f2-)

if [ -z "$REFLEX_DB_URL" ]; then
    warn "No REFLEX_DB_URL found in .env.test"
    exit 0
fi

log "Checking REFLEX_DB_URL sync status..."

# Function to check if secret needs update
needs_update() {
    local repo=$1
    # We can't read secret values, so we check if it exists
    # For full comparison, we'd need a hash stored somewhere
    if gh secret list --repo "$repo" 2>/dev/null | grep -q "REFLEX_DB_URL"; then
        return 1  # Secret exists (may or may not need update)
    else
        return 0  # Secret doesn't exist, needs to be set
    fi
}

# Sync to each repo
sync_count=0
for repo in "${REPOS[@]}"; do
    if $CHECK_ONLY; then
        if needs_update "$repo"; then
            warn "REFLEX_DB_URL needs to be set in $repo"
        fi
    else
        log "Syncing REFLEX_DB_URL to $repo..."
        if echo "$REFLEX_DB_URL" | gh secret set REFLEX_DB_URL --repo "$repo" 2>/dev/null; then
            success "  $repo: synced"
            sync_count=$((sync_count + 1))
        else
            error "  $repo: failed to sync"
        fi
    fi
done

if ! $CHECK_ONLY && [ $sync_count -gt 0 ]; then
    success "Synced REFLEX_DB_URL to $sync_count repo(s)"
fi

exit 0
