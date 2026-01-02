# Version Management

This document describes how version tagging and feature tagging work in the Longevity Clinic project.

## Version Format

The project uses semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes or significant rewrites
- **MINOR**: New features, backwards compatible
- **PATCH**: Bug fixes, small improvements (auto-incremented on deploy)

Current version is stored in `pyproject.toml` and displayed in the app footer.

## Feature Tags

Feature tags provide a quick visual indicator of the latest feature in a build.
They appear in the footer as: `v0.2.2 • profile-editing`

Feature tags are stored in `longevity_clinic/app/version.py`:

```python
FEATURE_TAG = "profile-editing"
```

## Files Involved

| File | Purpose |
|------|---------|
| `pyproject.toml` | Source of truth for version number |
| `longevity_clinic/app/version.py` | Version module + FEATURE_TAG |
| `longevity_clinic/app/components/layout.py` | Footer displaying version |
| `scripts/bump_version.py` | CLI tool to bump versions |

## Automatic Version Bumping

### On Push to Main

When code is pushed to `main` branch:
1. CI runs lint + tests
2. If tests pass, deploy job auto-bumps the **patch** version
3. Commits with `[skip ci]` to avoid infinite loops
4. Deploys to Railway

### Manual Trigger (workflow_dispatch)

When manually triggering deployment:

1. Go to **Actions** → **Deploy to Railway**
2. Click **Run workflow**
3. Select options:
   - **Environment**: `test` or `prod`
   - **Version bump type**: `none`, `patch`, `minor`, or `major`
   - **Feature tag**: Optional, e.g., `auth-improvements`

## Manual Version Bump

Use the bump script locally:

```bash
# Bump patch version (0.2.1 → 0.2.2)
uv run python scripts/bump_version.py patch

# Bump minor version (0.2.1 → 0.3.0)
uv run python scripts/bump_version.py minor

# Bump with feature tag
uv run python scripts/bump_version.py patch --feature "new-dashboard"

# Dry run (see what would change)
uv run python scripts/bump_version.py minor --dry-run
```

Then commit the changes:
```bash
git add pyproject.toml longevity_clinic/app/version.py
git commit -m "chore: bump version to X.Y.Z"
```

## Pre-commit Hooks

The project includes a pre-commit hook that reminds you to update `FEATURE_TAG`
when modifying state, page, or component files:

```
⚠️  Remember to update FEATURE_TAG in longevity_clinic/app/version.py if adding features
```

To install pre-commit hooks:
```bash
pre-commit install
pre-commit install --hook-type pre-push
```

## Footer Display

The version footer is rendered by `app_footer()` in `layout.py`:

```
Longevity Clinic • v0.2.2 • profile-editing
```

The footer appears at the bottom of all authenticated pages.

## CI/CD Integration

The deploy workflow (`.github/workflows/deploy.yml`) handles:

1. **Lint** (ruff check + format)
2. **Test** (pytest)
3. **Version bump** (auto patch on push, configurable on manual trigger)
4. **Deploy** to Railway

Version commits use `[skip ci]` suffix to prevent recursive workflow runs.
