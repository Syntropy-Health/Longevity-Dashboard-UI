# Deployment Guide - Longevity Clinic

This guide covers the complete deployment workflow from local development to production.

## Table of Contents

1. [Local Database Setup](#1-local-database-setup)
2. [Testing & QA](#2-testing--qa)
3. [Production Data Migration](#3-production-data-migration)
4. [Deployment](#4-deployment)
5. [CI/CD with GitHub Actions](#5-cicd-with-github-actions)
6. [Maintenance](#6-maintenance)

---

## 1. Local Database Setup

### Initialize Database Schema

```bash
# Initialize Alembic migrations
reflex db init

# Create migration from models
reflex db makemigrations --message "Initial schema"

# Apply migrations
reflex db migrate
```

### Seed Development Data

```bash
# Load seed data (creates demo users, treatments, biomarkers, etc.)
python scripts/load_seed_data.py

# Reset and reload (WARNING: destroys existing data)
python scripts/load_seed_data.py --reset
```

The seeding system uses modular seeders in `scripts/seeding/`:
- `users.py` - Demo patients and admin users
- `treatments.py` - Treatment protocols
- `biomarkers.py` - Biomarker definitions and readings
- `checkins.py` - Sample check-ins
- `appointments.py` - Scheduled appointments
- `notifications.py` - System notifications

### Verify Seed Data

```bash
# Check database contents
sqlite3 reflex.db ".tables"
sqlite3 reflex.db "SELECT COUNT(*) FROM user;"
```

---

## 2. Testing & QA

### Run Test Suite

```bash
# Run all tests
uv run pytest tests/ -v

# Run specific test modules
uv run pytest tests/test_database_seeding.py -v
uv run pytest tests/test_demo_data.py -v
uv run pytest tests/test_vlogs_agent.py -v

# Run with coverage
uv run pytest tests/ --cov=longevity_clinic --cov-report=html
```

### Test Categories

| Test File | Purpose |
|-----------|---------|
| `test_database_seeding.py` | Verifies seed data integrity and relationships |
| `test_demo_data.py` | Tests demo mode data structures and filtering |
| `test_vlogs_agent.py` | Tests voice log processing pipeline |
| `e2e/test_checkin_vlogs.py` | End-to-end check-in flow tests |

### Manual QA Checklist

1. **Authentication**: Login as admin (`admin`/`admin`) and patient (`patient`/`patient`)
2. **Admin Dashboard**: Verify patient list, check-in management, treatment protocols
3. **Patient Portal**: Test check-ins (voice/text), biomarker views, appointments
4. **Voice Processing**: Test voice transcription and LLM extraction
5. **Responsive Design**: Test on mobile and desktop viewports

### Run Development Server

```bash
# Start with hot reload
reflex run

# With debug logging
reflex run --loglevel debug
```

---

## 3. Production Data Migration

### Export Local Data to SQL

```bash
# Export all tables as PostgreSQL INSERT statements
python scripts/export_data.py > data_dump.sql

# Export specific tables
python scripts/export_data.py --tables users,treatments,biomarker_definitions

# Export to file
python scripts/export_data.py --output schema/seed_data.sql
```

### Import to Production Database

```bash
# Connect to Railway PostgreSQL
railway connect Postgres

# Or use psql directly with DATABASE_URL
psql "$DATABASE_URL" < data_dump.sql
```

### Run Migrations on Production

```bash
# Set production database URL
export REFLEX_DB_URL="postgresql://..."

# Run migrations
reflex db migrate
```

---

## 4. Deployment

### Prerequisites

1. **Railway CLI** installed: `npm install -g @railway/cli`
2. **Railway account** linked: `railway login`
3. **Project created** on Railway with:
   - PostgreSQL service (named "Postgres")
   - Backend service (named "longevity-clinic-backend")
   - Frontend service (named "longevity-clinic")

### Environment Configuration

Create environment files in `envs/`:

```bash
envs/
├── .env.base          # Shared defaults
├── .env.dev           # Development overrides
├── .env.prod          # Production overrides
└── .env.secrets       # API keys (gitignored)
```

Required secrets in `.env.secrets`:
```bash
OPENAI_API_KEY=sk-...
CALL_API_TOKEN=your_call_api_token
```

### Deploy Script

```bash
# Deploy to test environment
./scripts/deploy_longevity_clinic.sh test

# Deploy to production
./scripts/deploy_longevity_clinic.sh prod
```

### Deployment Script Details

The `deploy_longevity_clinic.sh` script:

1. **Loads environment** from `envs/` hierarchy
2. **Sets Railway context** (project: `syntropy`, environment: `test`/`prod`)
3. **Syncs environment variables** to Railway services
4. **Runs database migrations** on Railway PostgreSQL
5. **Triggers deployment** via `deploy_all.sh`

Key configuration:
```bash
RAILWAY_PROJECT="syntropy"
BACKEND_SERVICE="longevity-clinic-backend"
FRONTEND_SERVICE="longevity-clinic"
```

### Manual Deployment Steps

If you need to deploy manually:

```bash
# 1. Link to Railway project
railway link

# 2. Switch environment
railway environment test  # or prod

# 3. Set variables
railway variables --set "APP_NAME=Longevity Clinic" --service longevity-clinic-backend

# 4. Deploy backend
railway up --service longevity-clinic-backend

# 5. Deploy frontend
railway up --service longevity-clinic
```

---

## 5. CI/CD with GitHub Actions

### Setup Railway Token

1. Go to [Railway Dashboard](https://railway.app/account/tokens)
2. Create a new token with project access
3. Add to GitHub repository secrets as `RAILWAY_TOKEN`

### GitHub Actions Workflow

The workflow at `.github/workflows/deploy.yml` provides:

- **Manual trigger** via `workflow_dispatch`
- **Environment selection** (test/prod)
- **Automated testing** before deployment
- **Railway CLI deployment**

### Trigger Deployment

1. Go to **Actions** tab in GitHub
2. Select **Deploy to Railway** workflow
3. Click **Run workflow**
4. Choose environment (`test` or `prod`)
5. Click **Run workflow**

### Workflow Features

| Feature | Description |
|---------|-------------|
| Manual trigger | Deploy on-demand via GitHub UI |
| Environment matrix | Deploy to test or production |
| Test gate | Runs pytest before deployment |
| Caching | UV cache for faster builds |
| Secrets | Uses `RAILWAY_TOKEN` from repository secrets |

---

## 6. Maintenance

### Monitoring

```bash
# View Railway logs
railway logs --service longevity-clinic-backend
railway logs --service longevity-clinic

# Check service status
railway status
```

### Database Backups

```bash
# Export production data
railway connect Postgres
pg_dump "$DATABASE_URL" > backup_$(date +%Y%m%d).sql
```

### Rolling Back

```bash
# Railway keeps deployment history
railway rollback --service longevity-clinic-backend

# Or redeploy previous commit
git checkout <previous-commit>
./scripts/deploy_longevity_clinic.sh prod
```

### Environment Variables

Key variables managed:

| Variable | Service | Description |
|----------|---------|-------------|
| `REFLEX_DB_URL` | Backend | PostgreSQL connection string |
| `REFLEX_API_URL` | Frontend | Backend API endpoint |
| `REFLEX_DEPLOY_URL` | Both | Public service URL |
| `OPENAI_API_KEY` | Backend | OpenAI API key |
| `APP_ENV` | Both | Environment (dev/prod) |

### Updating Dependencies

```bash
# Update all dependencies
uv lock --upgrade

# Update specific package
uv add package@latest

# Sync environment
uv sync
```

---

## Quick Reference

```bash
# Local development
reflex run                              # Start dev server
uv run pytest tests/ -v                 # Run tests
python scripts/load_seed_data.py        # Seed database

# Deployment
./scripts/deploy_longevity_clinic.sh test   # Deploy to test
./scripts/deploy_longevity_clinic.sh prod   # Deploy to production

# Maintenance
railway logs --service longevity-clinic-backend  # View logs
railway variables --service Postgres             # Check DB vars
```

---

## Troubleshooting

### Database Connection Issues

```bash
# Check DATABASE_URL is set
railway variables --service Postgres

# Test connection
psql "$DATABASE_URL" -c "SELECT 1;"
```

### Deployment Failures

```bash
# Check build logs
railway logs --service longevity-clinic-backend --build

# Verify Dockerfiles exist
ls reflex-railway-deploy/Dockerfile.*
```

### Environment Variable Issues

```bash
# List all variables
railway variables --service longevity-clinic-backend

# Compare with local
cat envs/.env.prod
```
