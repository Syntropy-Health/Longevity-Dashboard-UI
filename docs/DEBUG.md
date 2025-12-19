# Debugging Guide

## Quick Commands

```bash
# Start app with logs
cd /home/mo/projects/Hackathon/longevity_clinic
uv run reflex run 2>&1 | tee -a dev.logs

# Watch logs (filter for key events)
tail -f dev.logs | grep -E "(dashboard|call_logs|checkin)"

# Test state imports
uv run python -c "from longevity_clinic.app.states.dashboard import PatientDashboardState; print('OK')"
```

## Common Issues

### UI Button Not Responding

**Symptoms**: "Check-in Now" or other buttons don't respond

**Debug Steps**:
1. Check `dev.logs` for handler logs (`open_checkin_modal called`)
2. If log appears → backend received event, check state update
3. If no log → frontend blocked, check browser console (F12)

**Key Files**:
- `states/dashboard.py` - modal handlers
- `pages/patient/components.py` - button components

### Call Logs Not Updating

**Symptoms**: Recent Check-ins section doesn't update

**Debug Steps**:
1. Check logs for `Fetching call logs` and `Fetched X call logs`
2. Verify `process_call_logs` completes
3. Check if `PatientDashboardState.checkins` is updated

**Key Files**:
- `states/functions/utils.py` - `fetch_call_logs`
- `states/functions/vlogs_agent.py` - `VlogsAgent` class
- `states/patient_checkin_state.py` - `refresh_call_logs`

### Page Redefinition Warnings

**Cause**: Page registered twice (via `@rx.page()` decorator AND `app.add_page()`)

**Fix**: Use only ONE registration method. Current pattern uses `app.add_page()` in `app.py`.

## Logging Configuration

Logs are written to `dev.logs` via `config.py`:
- DEBUG level for detailed tracing
- Format: `timestamp - logger_name - level - message`

## State Architecture

```
PatientState          → Patient CRUD operations
PatientDashboardState → Dashboard UI state, biomarkers
PatientCheckinState   → Call logs fetch/sync
AdminCheckinsState    → Admin view of all check-ins
```

## Background Task Pattern

```python
@rx.event(background=True)
async def fetch_data(self):
    # Do network/heavy work OUTSIDE state lock
    data = await fetch_from_api()
    
    # Quick state update INSIDE lock
    async with self:
        self.data = data
```
