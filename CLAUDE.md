# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Longevity Clinic Dashboard - A Reflex web application for managing longevity clinic operations with role-based access for administrators and patients. The application features an "Apple Glass" UI design system with glassmorphism effects, transparency, and light hues.

**Tech Stack**: Python 3.13+, Reflex framework (v0.8.20+), TailwindCSS v4

## Development Commands

### Running the Application
```bash
reflex run              # Start development server with hot reload
reflex run --loglevel debug  # Run with verbose logging
```

### Database & State Management
```bash
reflex db init          # Initialize database
reflex db makemigrations  # Create new migrations
reflex db migrate       # Apply migrations
```

### Building & Deployment
```bash
reflex export           # Export production build
reflex deploy           # Deploy to production
```

## Architecture

### Application Structure

The app follows Reflex's state-driven architecture with a clear separation between pages, components, and state management:

```
longevity_clinic/app/
├── rxconfig.py              # Main app entry point, route definitions
├── config.py           # Pydantic-based configuration (theme, styling)
├── pages/              # Page components (auth, admin, patient views)
├── components/         # Reusable UI components (header, sidebar, charts, layout)
└── states/             # Reflex state classes for business logic
```

### State Management Pattern

The codebase uses **Reflex State** classes (not Redux/Zustand) for all application state:

- **AuthState** (`states/auth_state.py`): Authentication, user sessions, role-based access
- **PatientState** (`states/patient_state.py`): Patient CRUD operations, filtering, assignment
- **TreatmentState** (`states/treatment_state.py`): Treatment protocol management
- **PatientAnalyticsState** (`states/patient_analytics_state.py`): Biomarker analytics for patient portal
- **BiomarkerState** (`states/patient/biomarker.py`): Historical biomarker tracking
- **TreatmentSearchState** (`states/treatment_search_state.py`): Patient-facing treatment search

State updates use `@rx.event` decorated methods, and computed properties use `@rx.var` decorators.

### Role-Based Access

Two primary user roles with different navigation and permissions:
- **Admin/Staff**: Access to admin dashboard (`/admin/*`), patient management, treatment protocols
- **Patient**: Access to patient portal (`/patient/*`), biomarker analytics, treatment search

Authentication is demo-only with hardcoded credentials:
- Admin: username=`admin`, password=`admin` → redirects to `/admin/dashboard`
- Patient: username=`patient`, password=`patient` → redirects to `/patient/portal`

### UI Design System

The app uses a custom **Apple Glass UI design system** defined in `app/config.py` with:
- Glassmorphism effects via `backdrop-blur-*` utilities
- Radial gradients with subtle color transitions
- Rounded corners (`rounded-[2rem]`, `rounded-2xl`)
- Light transparency layers (`bg-white/60`, `bg-white/30`)
- Smooth transitions and hover states

**Key styling constants** from `AppConfig` (Pydantic model):
- `glass_panel_style`: Main content panels
- `glass_input_style`: Form inputs with focus states
- `glass_button_primary`: Primary CTAs (emerald theme)
- `glass_button_secondary`: Secondary actions
- `glass_header_style`, `glass_sidebar_style`: Navigation components

When creating new components, always reference these config constants rather than hardcoding styles.

### Page Routing

Routes are defined in `app/longevity_clinic.py`:
- `/` and `/login` → `auth_page`
- `/admin/dashboard` → `admin_dashboard` (patient management, clinic metrics)
- `/admin/treatments` → `treatments_page` (treatment protocol library)
- `/patient/portal` → `patient_portal` (biomarker display)
- `/patient/analytics` → `analytics_page` (detailed biomarker trends)
- `/patient/treatment-search` → `treatment_search_page` (search/request treatments)

### Key Component Patterns

- **Layout**: `components/layout.py` provides the main app wrapper
- **Header**: `components/header.py` with user profile, logout, mobile menu toggle
- **Sidebar**: `components/sidebar.py` with role-based navigation (admin vs patient links)
- **Charts**: `components/charts.py` uses Victory charts for data visualization (line, bar, area)

## Development Guidelines

### Adding New Pages

1. Create page function in `longevity_clinic/app/pages/<page_name>.py`
2. Import and add route in `longevity_clinic/app/longevity_clinic.py`:
   ```python
   from .pages.<page_name> import <page_function>
   app.add_page(<page_function>, route="/<route_path>")
   ```
3. Add navigation link to appropriate sidebar section in `components/sidebar.py`

### Working with State

- State classes inherit from `rx.State`
- Use `@rx.event` for event handlers (user actions, async operations)
- Use `@rx.var` for computed properties (derived from state)
- State is accessed in components via `ClassName.property_name`
- Event handlers are called via `ClassName.event_name`

### Styling Consistency

- Always use `current_config` from `longevity_clinic.app.config` for styling constants
- Follow glassmorphism pattern: transparency + blur + subtle borders
- Use emerald (`emerald-500`) as the primary accent color
- Maintain consistent spacing with Tailwind utilities

### Demo Data

All data in state files (patients, treatments, biomarkers) is hardcoded for demo purposes. When adding features, continue using in-memory data structures. No database backend is currently implemented.

## Configuration

- **rxconfig.py**: Reflex configuration with plugins (Sitemap, TailwindV4)
- **pyproject.toml**: Python dependencies (uv package manager)
- **.python-version**: Python 3.13 required

## Testing Demo Credentials

When testing locally:
- Admin login: `admin` / `admin`
- Patient login: `patient` / `patient`
