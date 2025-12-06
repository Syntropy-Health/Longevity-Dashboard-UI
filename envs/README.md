# Environment Configuration

This folder contains hierarchical environment configuration files.

## Structure

```
envs/
├── .env.base           # Shared config (app name, theme, ports)
├── .env.dev            # Development (localhost backend)
├── .env.prod           # Production (Railway URLs)
├── .env.secrets        # API keys (⚠️ GITIGNORED)
└── .env.secrets.example # Template for secrets
```

## Loading Order

Environment variables are loaded in this order (later files override earlier):

1. `.env.base` - Shared configuration
2. `.env.{APP_ENV}` - Environment-specific (dev, test, prod)
3. `.env.secrets` - API keys and secrets
4. `../.env` - Legacy override file (optional)

## Usage

### Development (default)
```bash
# APP_ENV defaults to "dev", uses localhost backend
reflex run
```

### Production
```bash
# Set APP_ENV=prod to use Railway URLs
APP_ENV=prod reflex run
```

### Deployment
The deploy script automatically sets APP_ENV based on the deployment target:
```bash
./scripts/deploy_longevity_clinic.sh test   # Uses dev config
./scripts/deploy_longevity_clinic.sh prod   # Uses prod config
```

## Key Variables

| Variable | Description | Dev Default | Prod Default |
|----------|-------------|-------------|--------------|
| `REFLEX_API_URL` | Backend API URL | (empty = localhost:8000) | Railway backend URL |
| `FRONTEND_DEPLOY_URL` | Frontend URL for CORS | (empty = localhost:3000) | Railway frontend URL |
| `APP_ENV` | Environment name | dev | prod |
| `LOGLEVEL` | Logging level | debug | info |

## Secrets Setup

1. Copy the example file:
   ```bash
   cp envs/.env.secrets.example envs/.env.secrets
   ```

2. Fill in your API keys in `.env.secrets`

3. The `.env.secrets` file is gitignored and should never be committed.
