# Copilot Instructions - Longevity Clinic Dashboard

## Project Overview

Reflex web app (Python 3.13+, Reflex v0.8.20+) for a longevity clinic with role-based admin/patient portals. Uses "Apple Glass" glassmorphism UI with teal accents.

## Architecture

### State-Driven Pattern (NOT Redux)

All application state uses **Reflex State classes** in `longevity_clinic/app/states/`:
- State classes inherit from `rx.State`
- Event handlers use `@rx.event` decorator (async handlers use `@rx.event(background=True)`)
- Computed properties use `@rx.var` decorator
- Access in components: `StateName.property`, call handlers: `StateName.handler_name`

**State organization** (by domain):
- `states/auth/` - Authentication, sessions (`AuthState`)
- `states/patient/` - Biomarkers, analytics (`BiomarkerState`, `PatientAnalyticsState`)
- `states/shared/` - Cross-role state (`HealthDashboardState`, `AdminDashboardState`)
- `states/treatments/` - Protocol search/management
- `states/checkins/` - Unified check-in for both roles (`CheckinState`)
- `states/functions/` - **Extracted business logic** (stateless functions, testable)

### Functions Module (`states/functions/`)

Business logic extracted from state classes for testability:
- `vlogs_agent.py` - Call log processing with LLM (CDC pattern)
- `patients/` - Patient-specific: `checkins.py`, `voice.py`, `biomarkers.py`, `analytics.py`, `dashboard.py`
- `admins/` - Admin-specific: `checkins.py` (filtering, status management)
- `utils.py` - Shared utilities (`fetch_call_logs`, `format_timestamp`, `normalize_phone`)

### Page Structure

Pages organized by role in `longevity_clinic/app/pages/`:
- `pages/admin/` - Admin-only pages (dashboard, treatments, patient-health)
- `pages/patient/` - Patient-only pages (portal, analytics, treatment-search, checkins, settings)
- `pages/shared/` - Shared pages (auth, appointments, notifications)

Routes defined in `longevity_clinic/longevity_clinic.py` via `app.add_page()`. Pages use `authenticated_layout()` wrapper from `components/layout.py`.

```python
# Adding a new page:
# 1. Create page in longevity_clinic/app/pages/<role>/<domain>/page.py
# 2. Register in longevity_clinic/longevity_clinic.py:
app.add_page(my_page, route="/path", on_load=[MyState.load_data])
# 3. Add nav link in components/sidebar.py
```

**Note**: App entrypoint is `longevity_clinic/longevity_clinic.py` (not `app/app.py` which was removed).

### Component Organization

Components in `longevity_clinic/app/components/`:
- `layout.py` - `authenticated_layout()` wrapper with sidebar/header
- `sidebar.py` - Role-aware navigation sidebar
- `header.py` - App header with notifications
- `charts.py` - Generic chart wrappers (area, bar, line, biomarker)
- `page_components.py` - Shared page helpers (page_header, section_header)
- `shared/` - Shared UI components (search_input, loading_spinner, health_metrics)
- `modals/` - Reusable state-agnostic modals (transcription, status_update_modal)

**Note**: Page-specific modals stay co-located with their pages (e.g., `pages/admin/treatments/modals.py`).

### Styling System

**Use `GlassStyles` constants** from `styles/constants.py`, NOT hardcoded Tailwind:
- `GlassStyles.PANEL_LIGHT` - Glass card/panel
- `GlassStyles.BUTTON_PRIMARY_LIGHT` - Primary CTA (teal gradient)
- `GlassStyles.INPUT_LIGHT` - Form inputs with focus states
- `GlassStyles.HEADING_LIGHT` - Gradient text headings

**Legacy styles** in `config.py` (`current_config.glass_*`) - prefer `GlassStyles` for new code.

## Key Commands

```bash
reflex run                    # Dev server with hot reload
reflex run --loglevel debug   # Verbose logging
uv run pytest tests/          # Run tests (uses pytest-asyncio)
```

### Database (when enabled)
```bash
reflex db init && reflex db makemigrations && reflex db migrate
```

## Environment Configuration

Hierarchical env loading from `envs/` directory (see `rxconfig.py`):
1. `.env.base` → `.env.{APP_ENV}` → `.env.secrets`
2. Set `APP_ENV=dev|prod` to switch environments
3. API keys in `.env.secrets` (gitignored) - copy from `.env.secrets.example`

**Required secrets**: `OPENAI_API_KEY`, `CALL_API_TOKEN`

## Demo Authentication

Hardcoded credentials for demo (no real auth backend):
- Admin: `admin`/`admin` → `/admin/dashboard`
- Patient: `patient`/`patient` → `/patient/portal`

## Key Patterns

### VlogsAgent (Call Log Processing)

Location: `states/functions/vlogs_agent.py` - processes voice call logs with CDC (Change Data Capture) pattern.
```python
# Uses LangChain structured output for extraction
agent = VlogsAgent.from_config()  # Uses app defaults (gpt-4o-mini)
agent = VlogsAgent(config=VlogsConfig(extract_with_llm=False))  # Skip LLM

# CDC pipeline: fetch → diff → process → sync to DB
new_count, outputs = await agent.process_and_sync(phone_number="+1...")
```

### CheckinState Integration

`CheckinState` in `states/checkins/checkin.py` is the unified state for both admin and patient check-in views:
- Uses `VlogsAgent` for call log syncing (`refresh_call_logs`)
- Calls `fetch_all_checkins` from `functions/admins/` for admin data
- Calls `extract_checkin_from_text` from `functions/patients/` for patient submissions

### Component Composition

Pages compose from reusable components in `components/`:
- `layout.py` - `authenticated_layout()` wrapper with sidebar/header
- `charts.py` - Victory chart wrappers
- `modals/` - Shared modal components

### Data Layer

**Database-first pattern** - use `data/db_helpers.py` for lookups instead of hardcoded dicts:
```python
from longevity_clinic.app.data.db_helpers import get_patient_name_by_phone

# Instead of: PHONE_TO_PATIENT.get(phone)
name = get_patient_name_by_phone(phone)  # DB lookup with fallback
```

Data organization:
- `model.py` - SQLModel definitions (User, CheckIn, CallLog, etc.)
- `db_helpers.py` - Sync DB queries (`get_user_by_phone_sync`, `get_checkins_sync`)
- `demo.py` - **Seed data only** with `DemoPatientSeed` class
- `state_schemas.py` - State-level TypedDicts

**Demo mode**: Set `IS_DEMO=true` (default) to use demo data, `IS_DEMO=false` for database.

### Demo User Configuration

The primary demo user is defined in `config.py` via `DemoUserConfig`:
```python
from longevity_clinic.app.config import current_config

# Primary demo user (Sarah Chen)
current_config.demo_user.full_name  # "Sarah Chen"
current_config.demo_user.phone      # "+12126804645"
current_config.demo_user.email      # "sarah.chen@longevityclinic.com"
```

Demo data in `demo.py` derives from this config:
- `DemoPatientSeed.from_demo_config()` - creates primary patient from config
- `get_all_demo_patients()` - returns primary + secondary patients
- `PHONE_TO_PATIENT_SEED` - built from demo patients
- All demo check-ins/appointments reference the primary user

### Configuration Classes

`config.py` has modular configuration:
```python
current_config.is_demo          # True = demo data, False = database
current_config.demo_user.phone  # Demo user's phone number
current_config.glass.panel_style  # Modularized glass styles (GlassStyleConfig)
```

## Testing

```python
# tests/conftest.py loads env automatically
# Use pytest-asyncio for async tests
@pytest.mark.asyncio
async def test_something():
    agent = VlogsAgent(config=VlogsConfig(extract_with_llm=False))
    result = await agent.process(...)
```

## File Naming Conventions

- Pages: `pages/<role>/<domain>/page.py` with `<domain>_page()` function
- States: `states/<domain>/<domain>_state.py` with `<Domain>State` class
- Admin-specific state: `pages/admin/state.py` for page-local state
- Page-local modals: Co-located with pages (e.g., `pages/admin/treatments/modals.py`)
