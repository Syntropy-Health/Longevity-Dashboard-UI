# Agent Knowledge Base - Longevity Clinic Dashboard

> Comprehensive codebase knowledge for AI agents working on this repository.
> Last updated: December 28, 2025

## Project Overview

**Longevity Clinic Dashboard** is a Reflex web application (Python 3.13+, Reflex v0.8.20+) for a longevity/wellness clinic with role-based admin and patient portals. Uses "Apple Glass" glassmorphism UI design with teal accents.

### Tech Stack
- **Framework**: Reflex (Python reactive web framework)
- **Database**: SQLite with SQLModel ORM
- **Styling**: Tailwind CSS with glassmorphism constants
- **LLM Integration**: OpenAI GPT-4o-mini for check-in extraction
- **Package Manager**: uv

### Key Commands
```bash
uv run reflex run                    # Dev server (localhost:3000)
uv run reflex run --loglevel debug   # Verbose logging
uv run pytest tests/                 # Run tests
reflex db init && reflex db makemigrations && reflex db migrate  # DB migrations
```

---

## Architecture

### Entry Point
- **Main app**: `longevity_clinic/longevity_clinic.py` (NOT `app/app.py`)
- Routes registered via `app.add_page()`
- Environment config in `rxconfig.py` with hierarchical `.env` loading from `envs/`

### Directory Structure
```
longevity_clinic/
├── longevity_clinic.py          # App entrypoint, route registration
└── app/
    ├── config.py                # App configuration, DemoUserConfig
    ├── components/              # Reusable UI components
    │   ├── layout.py            # authenticated_layout() wrapper
    │   ├── sidebar.py           # Role-aware navigation
    │   ├── charts.py            # Victory chart wrappers
    │   └── shared/              # health_metrics.py, search_input, etc.
    ├── data/
    │   ├── schemas/             # Pydantic/SQLModel schemas
    │   │   ├── db/              # Database schema package
    │   │   │   ├── models/      # SQLModel models (refactored)
    │   │   │   ├── enums.py     # Enum tables
    │   │   │   └── domain_enums.py  # StrEnum definitions
    │   │   └── llm.py           # LLM extraction models
    │   ├── demo.py              # Seed data (DemoPatientSeed)
    │   └── db_helpers.py        # Sync DB query functions
    ├── functions/               # Extracted business logic (testable)
    │   ├── db_utils.py          # Database utilities
    │   ├── vlogs_agent.py       # Call log CDC pipeline
    │   ├── patients/            # Patient-specific functions
    │   └── admins/              # Admin-specific functions
    ├── pages/
    │   ├── admin/               # Admin pages (dashboard, treatments, patient-health)
    │   ├── patient/             # Patient pages (portal, analytics, settings, checkins)
    │   └── shared/              # Auth, appointments, notifications
    ├── states/                  # Reflex State classes
    │   ├── auth/                # AuthState
    │   ├── patient/             # BiomarkerState, PatientState
    │   ├── admin/               # AdminDashboardState, AdminPatientHealthState
    │   ├── shared/
    │   │   ├── dashboard/       # Decomposed health states
    │   │   └── checkin.py       # CheckinState
    │   └── treatments/          # TreatmentState, TreatmentSearchState
    └── styles/
        └── constants.py         # GlassStyles constants
```

---

## State Management

### State-Driven Pattern (NOT Redux)
All application state uses **Reflex State classes**:
- State classes inherit from `rx.State`
- Event handlers use `@rx.event` decorator (async: `@rx.event(background=True)`)
- Computed properties use `@rx.var` decorator
- Access: `StateName.property`, call handlers: `StateName.handler_name`

### Decomposed Dashboard States (CURRENT)
Health data is managed by domain-specific states in `states/shared/dashboard/`:

| State | File | Purpose |
|-------|------|---------|
| `FoodState` | `food.py` | Food entries, nutrition summary, pagination |
| `MedicationState` | `medication.py` | Medication entries, prescriptions, log_dose |
| `ConditionState` | `condition.py` | Health conditions, filtering, pagination |
| `SymptomState` | `symptom.py` | Symptoms, logs, trends, save_symptom_log |
| `DataSourceState` | `data_source.py` | Connected devices/apps, integration suggestions |
| `SettingsState` | `settings.py` | User preferences, tab navigation (active_tab) |

### Admin States
| State | File | Purpose |
|-------|------|---------|
| `AdminDashboardState` | `states/admin/dashboard.py` | Admin tab navigation only |
| `AdminPatientHealthState` | `states/admin/patient_health.py` | Admin viewing patient data by ID |
| `AdminMetricsState` | `states/admin_metrics_state.py` | Clinic metrics/charts |

### Core States
| State | File | Purpose |
|-------|------|---------|
| `AuthState` | `states/auth/base.py` | Authentication, user session, role |
| `BiomarkerState` | `states/patient/biomarker.py` | Biomarker analytics, panels |
| `PatientState` | `states/patient/state.py` | Patient CRUD, selection |
| `CheckinState` | `states/shared/checkin.py` | Unified check-ins (patient & admin) |
| `TreatmentState` | `states/treatments/treatment_state.py` | Treatment protocols (admin) |
| `TreatmentSearchState` | `states/shared/treatment.py` | Treatment search (patient) |

### Loading Guard Pattern
All background handlers use guards to prevent duplicate loads:
```python
@rx.event(background=True)
async def load_data(self):
    async with self:
        if self._data_loaded:
            return
        self.is_loading = True
    
    auth_state = await self.get_state(AuthState)
    user_id = auth_state.user_id  # ALWAYS use AuthState.user_id
    # ... fetch data ...
```

### User ID Pattern
**Always** use `AuthState.user_id` for the authenticated user's database ID:
```python
# ✅ Correct
auth_state = await self.get_state(AuthState)
user_id = auth_state.user_id

# ❌ Wrong (deprecated)
user_id = get_primary_demo_user_id()
```

---

## Recent Migration: HealthDashboardState → Decomposed States

### What Changed (December 2025)
The monolithic `HealthDashboardState` was decomposed into domain-specific states:

**Before**: All health data in one massive state class
**After**: Separate states for each domain (Food, Medication, Condition, Symptom, DataSource, Settings)

### Files Updated
| File | Change |
|------|--------|
| `pages/patient/page.py` | Uses `SettingsState.active_tab` |
| `pages/patient/settings_page.py` | Uses `SettingsState`, `DataSourceState` |
| `pages/patient/modals.py` | Uses domain-specific states for each modal |
| `pages/patient/components.py` | Uses `SettingsState` for tabs |
| `components/shared/health_metrics.py` | Uses all decomposed states |
| `pages/admin/tabs/patient_health.py` | Uses `AdminPatientHealthState` |
| `states/admin/dashboard.py` | New home for `AdminDashboardState` |

### Modal → State Mapping
| Modal | State Used |
|-------|-----------|
| `medication_modal()` | `MedicationState` |
| `condition_modal()` | `ConditionState` |
| `symptom_modal()` | `SymptomState` |
| `connect_source_modal()` | `DataSourceState` |
| `add_food_modal()` | `FoodState` |
| `suggest_integration_modal()` | `DataSourceState` |

---

## Data Flow

### Check-in Pipeline
```
Patient Input (voice/text)
    → CheckinState.save_checkin_and_log_health()
    → LLM extraction (medications, food, symptoms)
    → Database tables (MedicationEntry, FoodLogEntry, SymptomEntry)
    → Decomposed states fetch on next load
```

### Call Log CDC Pipeline (VlogsAgent)
```
External call logs API
    → VlogsAgent.process_and_sync()
    → LLM extraction with structured output
    → Database sync (CallLog, health entries)
    → Dashboard states refresh
```

---

## Styling System

### GlassStyles Constants
Use `GlassStyles` from `styles/constants.py`:
```python
from ...styles.constants import GlassStyles

# Panels
class_name=GlassStyles.PANEL           # Glass card
class_name=GlassStyles.MODAL           # Modal backdrop

# Buttons
class_name=GlassStyles.BUTTON_PRIMARY  # Teal gradient CTA
class_name=GlassStyles.BUTTON_SECONDARY  # Subtle secondary

# Inputs
class_name=GlassStyles.INPUT_LIGHT     # Form inputs

# Typography
class_name=GlassStyles.HEADING_LIGHT   # Gradient headings

# Cards
class_name=GlassStyles.BIOMARKER_CARD      # Dark mode biomarker cards
class_name=GlassStyles.TREATMENT_CARD      # Light mode treatment cards
class_name=GlassStyles.TREATMENT_CARD_CONTENT  # Card content with descender-safe padding

# Collapsible/Accordion
class_name=GlassStyles.COLLAPSIBLE_ITEM      # Accordion item container
class_name=GlassStyles.COLLAPSIBLE_TRIGGER   # Clickable header
class_name=GlassStyles.COLLAPSIBLE_CONTENT   # Expandable content
class_name=GlassStyles.COLLAPSIBLE_CONTAINER # Accordion root
```

### Typography & Card Padding Guidelines

**IMPORTANT**: When creating cards or containers with text content:
- Use adequate padding (`p-6` minimum, `pb-7` for bottom) to prevent letter descender cutoff
- Letters like `g`, `p`, `y`, `q`, `j` have descenders that extend below the baseline
- See `GlassStyles.TREATMENT_CARD_CONTENT` (`p-6 pb-7`) as reference
- Use `leading-relaxed` or `leading-loose` for line-height to improve readability

---

## Database Models

### Models Package Structure (`data/schemas/db/models/`)
Models are organized into domain-specific modules:

| File | Models | Purpose |
|------|--------|--------|
| `base.py` | `utc_now()` | UTC datetime helper |
| `user.py` | `User` | Users with role (admin/patient), external_id |
| `call_logs.py` | `CallLog`, `CallTranscript` | Voice call logs from external API |
| `checkins.py` | `CheckIn` | Patient check-ins with LLM-extracted data |
| `notifications.py` | `Notification` | System notifications & medication reminders |
| `appointments.py` | `Appointment` | Scheduled appointments |
| `health_entries.py` | `MedicationEntry`, `FoodLogEntry`, `SymptomEntry` | Health data from check-ins |
| `conditions.py` | `Condition`, `SymptomTrend`, `DataSource` | Health conditions & connected devices |
| `treatments.py` | `Treatment`, `PatientTreatment` | Treatment protocols & patient assignments |
| `biomarkers.py` | `BiomarkerDefinition`, `BiomarkerReading` | Biomarker definitions & readings |
| `clinic_metrics.py` | `PatientVisit`, `TreatmentProtocolMetric`, `BiomarkerAggregate`, `ClinicDailyMetrics`, `ProviderMetrics` | Admin dashboard metrics |

### Importing Models
```python
# From main package (recommended)
from longevity_clinic.app.data.schemas.db import User, CheckIn, Treatment

# Direct imports from submodules
from longevity_clinic.app.data.schemas.db.models.health_entries import FoodLogEntry
from longevity_clinic.app.data.schemas.db.models.treatments import PatientTreatment
```

---

## Authentication

### Demo Credentials
- **Admin**: `admin` / `admin` → `/admin/dashboard`
- **Patient**: `patient` / `patient` → `/patient/portal`

### Demo User Configuration
Primary demo user configured in `config.py`:
```python
current_config.demo_user.full_name  # "Sarah Chen"
current_config.demo_user.phone      # "+12126804645"
current_config.demo_user.email      # "sarah.chen@longevityclinic.com"
```

---

## Environment Configuration

Hierarchical loading from `envs/` directory:
1. `.env.base` → `.env.{APP_ENV}` → `.env.secrets`
2. Set `APP_ENV=dev|prod` to switch environments
3. API keys in `.env.secrets` (gitignored)

**Required Secrets**:
- `OPENAI_API_KEY` - For LLM extraction
- `CALL_API_TOKEN` - For call log API

---

## Component Patterns

### Page Template
```python
def my_page() -> rx.Component:
    return authenticated_layout(
        rx.el.div(
            # Page header
            rx.el.h1("Page Title", class_name=f"text-2xl {GlassStyles.HEADING_LIGHT}"),
            # Content
            my_content(),
            # Modals
            my_modal(),
            on_mount=MyState.init,
        )
    )
```

### Modal Pattern
```python
def my_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(rx.fragment()),
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(...),
            rx.radix.primitives.dialog.content(...),
        ),
        open=MyState.show_modal,
        on_open_change=MyState.set_show_modal,
    )
```

### Pagination Pattern
Each decomposed state has pagination support:
```python
# State properties
items_paginated      # Current page slice
items_page           # Current page number
items_total_pages    # Total pages
items_has_previous   # Can go back
items_has_next       # Can go forward
items_page_info      # "Page X of Y"

# Handlers
items_previous_page()
items_next_page()
```

---

## Testing

```python
# tests/conftest.py loads env automatically
@pytest.mark.asyncio
async def test_something():
    agent = VlogsAgent(config=VlogsConfig(extract_with_llm=False))
    result = await agent.process(...)
```

---

## File Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Pages | `pages/<role>/<domain>/page.py` | `pages/patient/portal/page.py` |
| States | `states/<domain>/<name>.py` | `states/shared/dashboard/food.py` |
| Components | `components/<category>/<name>.py` | `components/shared/health_metrics.py` |
| Page-local modals | Co-located with pages | `pages/admin/treatments/modals.py` |

---

## Known Issues & TODOs

1. **Seed data**: Run `python scripts/seed_db.py` after migrations
2. **Call log sync**: Requires `CALL_API_TOKEN` in `.env.secrets`
3. **AdminDashboardState**: Only used for tab navigation, could be merged into other admin states

---

## Recent Changes (December 28, 2025)

### Models Refactoring
Refactored monolithic `models.py` (500+ lines) into `models/` package:
- **Before**: Single `data/schemas/db/models.py` file
- **After**: `data/schemas/db/models/` package with domain-specific modules
- All imports remain backward-compatible via `__init__.py` re-exports

### Detail Modals for Health Tabs
Added clickable detail modals for health tab cards:
- `components/modals/health_detail.py` - Shared modal components
- Each state now has `show_*_modal`, `selected_*`, and computed vars for fields
- Pattern: Click card → opens modal with full entry details

### TAB_CARD_THEMES
Standardized card theming across health tabs:
```python
from ...components.tabs import TAB_CARD_THEMES
# Keys: "food", "medication", "symptom", "condition", "data_source"
# Each has: icon_bg, icon_color, accent_color, gradient
```

---

## Quick Reference: State Imports

```python
# Main states
from ...states import AuthState, BiomarkerState, PatientState, CheckinState

# Decomposed dashboard states
from ...states.shared.dashboard import (
    FoodState,
    MedicationState,
    ConditionState,
    SymptomState,
    DataSourceState,
    SettingsState,
)

# Admin states
from ...states.admin import AdminPatientHealthState
from ...states import AdminDashboardState
```
