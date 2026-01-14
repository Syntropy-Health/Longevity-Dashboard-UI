# Syntropy-Journals Migration to Longevity-Dashboard-UI

This document describes the migration of core components from `Syntropy-Journals` into `Longevity-Dashboard-UI`.

## Migration Summary

**Date:** January 2026
**Source:** `apps/Syntropy-Journals`
**Target:** `apps/Longevity-Dashboard-UI`

## Migrated Components

### 1. Database Schemas (`longevity_dashboard/app/data/schemas/db/syntropy/`)

| File | Description |
|------|-------------|
| `admin.py` | AdminConfig, Subscription, SubscriptionFeature models |
| `catalog.py` | CatalogItem, CategoryItem TypedDicts |
| `chat.py` | ChatMessage, ChatSession models and utilities |
| `notification.py` | SyntropyNotification, NotificationType definitions |
| `orders.py` | Order, OrderItem, ProductInfo models |
| `settings.py` | SyntropySettings model for user preferences |
| `subscription.py` | Plan TypedDict for subscription plans |
| `langgraph/` | LangGraph checkpoint models (Checkpoint, CheckpointBlob, etc.) |

### 2. State Modules (`longevity_dashboard/app/states/syntropy/`)

| File | Description |
|------|-------------|
| `base.py` | ConfigurableState mixin with admin config loading |
| `app/catalog.py` | CatalogState for health product catalog management |
| `app/notification.py` | SyntropyNotificationState for AI-generated tips/alerts |
| `app/settings.py` | SyntropySettingsState for order integrations & preferences |
| `app/landing.py` | LandingState for landing page content management |
| `chat/chat.py` | SyntropyChatState for main chat session management |
| `chat/landing_chat.py` | LandingChatState for landing page chat interactions |
| `chat/transcription.py` | TranscriptionState for audio transcription |

### 3. Pages

| Route | Page | Description |
|-------|------|-------------|
| `/admin/chat` | `admin_chat_page` | AI Medical Expert for admin users |
| `/patient/chat` | `ai_chat_page` | AI Clinician for patient users |

### 4. Sidebar Updates

- **Admin sidebar:** Added "AI Medical Expert" link → `/admin/chat`
- **Patient sidebar:** Added "AI Clinician" link → `/patient/chat`

## Excluded Components

The following were **not migrated** as requested:
- `journal.py` - Journal-specific models and functionality
- Journal-related pages and components

## Configuration Changes

### Dependencies Added (`pyproject.toml`)

```toml
langgraph = ">=0.2.0"
langchain-postgres = ">=0.0.6"
psycopg = { version = ">=3.1.0", extras = ["binary"] }
```

### Patient Portal Default Tab

Changed default `initial_tab` from `"overview"` to `"checkins"` in `patient/page.py`.

## State Deduplication Notes

The Syntropy states were prefixed with `Syntropy` to avoid conflicts with existing states:

| Syntropy State | Existing State | Purpose |
|----------------|----------------|---------|
| `SyntropySettingsState` | `SettingsState` | Order integrations vs. UI settings |
| `SyntropyNotificationState` | `NotificationState` | AI tips/alerts vs. DB notifications |

## File Structure

```
longevity_dashboard/app/
├── data/schemas/db/syntropy/
│   ├── __init__.py
│   ├── admin.py
│   ├── catalog.py
│   ├── chat.py
│   ├── notification.py
│   ├── orders.py
│   ├── settings.py
│   ├── subscription.py
│   └── langgraph/
│       ├── __init__.py
│       └── checkpoints.py
├── states/syntropy/
│   ├── __init__.py
│   ├── base.py
│   ├── app/
│   │   ├── __init__.py
│   │   ├── catalog.py
│   │   ├── landing.py
│   │   ├── notification.py
│   │   └── settings.py
│   └── chat/
│       ├── __init__.py
│       ├── chat.py
│       ├── landing_chat.py
│       └── transcription.py
└── pages/
    ├── admin/chat.py
    └── patient/chat/
        ├── __init__.py
        └── page.py
```

## Testing

To validate the migration:

```bash
cd apps/Longevity-Dashboard-UI
uv run reflex db migrate  # Run migrations for new models
uv run reflex run         # Start the application
```

## Known Issues

1. **Database migrations required:** New Syntropy models require database migration before use
2. **API keys needed:** `OPENROUTER_API_KEY` required for AI chat functionality
3. **Audio capture deprecation:** `rx.Base` deprecation warning in `reflex_audio_capture`

## Next Steps

1. Run database migrations to create new tables
2. Configure environment variables for AI features
3. Test chat functionality with valid API keys
4. Migrate tests from Syntropy-Journals (pending)
