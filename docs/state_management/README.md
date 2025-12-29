# State Management Documentation

> Reflex state patterns for the Longevity Clinic app

## Documentation Index

| Document | Description |
|----------|-------------|
| [README.md](./README.md) (this file) | State architecture, loading patterns, best practices |
| [processes/CHECKIN.md](./processes/CHECKIN.md) | Check-in data flow: patient input, call log CDC, dashboard sync |
| [SYSTEM.md](./SYSTEM.md) | System architecture, future work: webhooks, task queues |

## Quick Reference

### Route → on_load Mapping

| Route | on_load Handlers | States Initialized |
|-------|-----------------|-------------------|
| `/` | - | - |
| `/login` | - | - |
| `/admin/dashboard` | - | `AdminMetricsState` (via on_mount) |
| `/admin/checkins` | `CheckinState.load_admin_checkins` | `CheckinState` |
| `/admin/treatments` | `TreatmentState.load_protocols` | `TreatmentState` |
| `/patient/portal` | `BiomarkerState.load_biomarkers`, decomposed dashboard states | `BiomarkerState`, `FoodState`, `MedicationState`, etc. |
| `/patient/checkins` | `BiomarkerState.load_biomarkers`, `CheckinState.refresh_call_logs` | `BiomarkerState`, `CheckinState` |
| `/patient/treatment-search` | `TreatmentSearchState.load_treatments` | `TreatmentSearchState` |
| `/patient/analytics` | - | - |
| `/patient/settings` | - | - |

### on_mount vs on_load

| Hook | Scope | Timing | Use Case |
|------|-------|--------|----------|
| `on_load` | Page | Before render, on route navigation | Data fetching, auth checks |
| `on_mount` | Component | After DOM mount | UI initialization, tab defaults |

## State Architecture

```mermaid
graph TD
    subgraph "Auth Flow"
        A[AuthState] -->|login| B{Role?}
        B -->|admin| C[/admin/dashboard]
        B -->|patient| D[/patient/portal]
    end

    subgraph "Admin States"
        C -->|on_mount| E[AdminMetricsState.load_metrics]
        F[/admin/checkins] -->|on_load| G[CheckinState.load_admin_checkins]
        H[/admin/treatments] -->|on_load| I[TreatmentState.load_protocols]
        J[Admin Patient Health] -->|on_click| K[AdminPatientHealthState.load_patient_health_data]
    end

    subgraph "Patient States (Decomposed)"
        D -->|on_load| L[BiomarkerState.load_biomarkers]
        D -->|on_load| M[FoodState.load_food_entries]
        D -->|on_load| N[MedicationState.load_medications]
        D -->|on_mount| O[SettingsState.set_active_tab]
        P[/patient/checkins] -->|on_load| Q[CheckinState.refresh_call_logs]
    end
```

## State Classes

### Core States

| State | Location | Purpose | Loading Guard |
|-------|----------|---------|---------------|
| `AuthState` | `states/auth/base.py` | Authentication, user session | `is_loading` |
| `BiomarkerState` | `states/patient/biomarker.py` | Biomarker analytics | `is_loading`, `_data_loaded` |
| `FoodState` | `states/shared/dashboard/food.py` | Food tracking, nutrition | `is_loading`, `_data_loaded` |
| `MedicationState` | `states/shared/dashboard/medication.py` | Medications, prescriptions | `is_loading`, `_data_loaded` |
| `ConditionState` | `states/shared/dashboard/condition.py` | Health conditions | `is_loading`, `_data_loaded` |
| `SymptomState` | `states/shared/dashboard/symptom.py` | Symptoms, logs, trends | `is_loading`, `_data_loaded` |
| `DataSourceState` | `states/shared/dashboard/data_source.py` | Connected devices/apps | `is_loading`, `_data_loaded` |
| `SettingsState` | `states/shared/dashboard/settings.py` | User preferences, tab nav | (none) |
| `CheckinState` | `states/shared/checkin.py` | Check-ins for both roles | `is_loading`, `_admin_data_loaded` |
| `TreatmentState` | `states/treatments/treatment_state.py` | Treatment protocols (admin) | `_loaded` |
| `TreatmentSearchState` | `states/shared/treatment.py` | Treatment search (patient) | `_loaded` |
| `PatientState` | `states/patient/state.py` | Patient CRUD, selection | `is_loading`, `_data_loaded` |
| `AdminDashboardState` | `states/admin/dashboard.py` | Admin tab navigation only | (none) |
| `AdminPatientHealthState` | `states/admin/patient_health.py` | Admin viewing patient data | `is_loading`, `_data_loaded` |
| `AdminMetricsState` | `states/admin_metrics_state.py` | Clinic metrics/charts | `is_loading`, `_data_loaded` |

## Loading Guard Pattern

All background event handlers use a guard pattern to prevent duplicate loads:

```python
@rx.event(background=True)
async def load_data(self):
    async with self:
        if self._data_loaded:  # Guard: skip if already loaded
            return
        self.is_loading = True  # Set loading state

    # Get user ID from AuthState (ALWAYS use this pattern)
    auth_state = await self.get_state(AuthState)
    user_id = auth_state.user_id
    if not user_id:
        logger.warning("No authenticated user")
        async with self:
            self.is_loading = False
        return

    try:
        data = await asyncio.to_thread(_fetch_sync, user_id)  # DB query
        async with self:
            self.data = data
            self.is_loading = False
            self._data_loaded = True
    except Exception as e:
        async with self:
            self.is_loading = False
```

### User ID Pattern

**Always** use `AuthState.user_id` for the authenticated user's database ID:

```python
# ✅ Correct: Get user ID from AuthState
auth_state = await self.get_state(AuthState)
user_id = auth_state.user_id

# ❌ Wrong: Hardcoded demo user lookups (DEPRECATED)
# user_id = get_primary_demo_user_id()  # Don't use this!
```

### Guard Variables

| State | Guard Variable | Reset On |
|-------|---------------|----------|
| `BiomarkerState` | `_data_loaded` | - |
| `FoodState` | `_data_loaded` | `clear_data()` |
| `MedicationState` | `_data_loaded` | `clear_data()` |
| `ConditionState` | `_data_loaded` | `clear_data()` |
| `SymptomState` | `_data_loaded` | `clear_data()` |
| `AdminPatientHealthState` | `_data_loaded` | `clear_patient_health_data()` |
| `CheckinState` | `_admin_data_loaded` | - |
| `AdminMetricsState` | `_data_loaded` | `refresh_metrics()` |
| `TreatmentState` | `_loaded` | - |

## Event Handler Types

Sync events for UI actions, background events for data loading.
See [processes/CHECKIN.md](./processes/CHECKIN.md) for detailed data flow documentation.
