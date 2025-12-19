# VlogsAgent Configuration and Testing

## Overview

VlogsAgent is a modular agent for processing voice call logs into structured health data. It supports both basic transcript processing and advanced LLM-based structured extraction.

## Architecture

### Configuration Management

**Location**: `longevity_clinic/app/config.py`

The VlogsAgent configuration is centralized in the `AppConfig` class:

```python
class AppConfig(BaseModel):
    # VlogsAgent Configuration
    vlogs_process_with_llm: bool = True  # Enable LLM parsing by default
    vlogs_llm_model: str = "gpt-4o-mini"
    vlogs_temperature: float = 0.3
    vlogs_fetch_limit: int = 50
```

### Agent Implementation

**Location**: `longevity_clinic/app/states/functions/vlogs_agent.py`

#### VlogsConfig Dataclass

```python
@dataclass
class VlogsConfig:
    """Configuration for VlogsAgent."""
    extract_with_llm: bool = True  # Default to True for better extraction
    llm_model: str = "gpt-4o-mini"
    temperature: float = 0.3
    limit: int = 50

    @classmethod
    def from_app_config(cls) -> "VlogsConfig":
        """Create VlogsConfig from app configuration."""
        return cls(
            extract_with_llm=current_config.vlogs_process_with_llm,
            llm_model=current_config.vlogs_llm_model,
            temperature=current_config.vlogs_temperature,
            limit=current_config.vlogs_fetch_limit,
        )
```

#### VlogsAgent Dataclass

```python
@dataclass
class VlogsAgent:
    """Agent for processing voice call logs into structured data."""
    config: VlogsConfig = field(default_factory=VlogsConfig)
    _llm: Optional[ChatOpenAI] = field(default=None, init=False, repr=False)
    _structured_llm: Optional[object] = field(default=None, init=False, repr=False)

    @classmethod
    def from_config(cls) -> "VlogsAgent":
        """Create VlogsAgent with configuration from app settings."""
        return cls(config=VlogsConfig.from_app_config())
```

## Usage

### Basic Usage with Default Configuration

```python
from longevity_clinic.app.states.functions.vlogs_agent import VlogsAgent

# Create agent with app config (extract_with_llm=True by default)
agent = VlogsAgent.from_config()

# Process call logs
new_count, outputs, summaries = await agent.process_logs(
    phone_number="+12126804645"
)
```

### Custom Configuration

```python
from longevity_clinic.app.states.functions.vlogs_agent import VlogsAgent, VlogsConfig

# Create custom config
config = VlogsConfig(
    extract_with_llm=False,  # Disable LLM for faster processing
    limit=10  # Fetch only 10 logs
)

# Create agent with custom config
agent = VlogsAgent(config=config)

# Process logs
new_count, outputs, summaries = await agent.process_logs(
    phone_number="+12126804645"
)
```

## Processing Modes

### Non-LLM Mode (`extract_with_llm=False`)

- **Speed**: Fast processing (~0.1s per log)
- **Extraction**: Basic summary from API transcript
- **Use Case**: Quick previews, testing, development

### LLM Mode (`extract_with_llm=True`)

- **Speed**: Moderate processing (~4s per log with gpt-4o-mini)
- **Extraction**: Structured extraction of medications, food entries, symptoms
- **Use Case**: Production, detailed health data extraction
- **Model**: gpt-4o-mini for balance of speed and accuracy

## Testing

### Test Suite Location

`tests/test_vlogs_agent.py`

### Running Tests

```bash
# Run all tests
uv run pytest tests/test_vlogs_agent.py -v

# Run manual test script
PYTHONPATH=/home/mo/projects/Hackathon/longevity_clinic:$PYTHONPATH \
    uv run python tests/test_vlogs_agent.py
```

### Test Results Summary

```
8 passed, 2 skipped in 22.39s
✅ Configuration tests: 3/3 passed
✅ Agent initialization tests: 3/3 passed  
✅ LLM processing test: 1/1 passed
✅ Manual workflow test: 1/1 passed
⏭️  Integration tests: 2 skipped (require API access)
```

### Test Coverage

1. **Configuration Tests**
   - Default configuration values
   - Custom configuration
   - Loading from app config

2. **Agent Tests**
   - Agent initialization
   - Agent from app config
   - Agent with custom config
   - Processing call logs (non-LLM)
   - Processing with LLM enabled

3. **Integration Tests**
   - Complete workflow validation
   - Data structure verification

## Key Features

### Structured Output

The agent returns three items:

```python
new_count: int  # Number of newly processed logs
outputs: list[CallLogsOutput]  # Structured health data
summaries: list[TranscriptSummary]  # UI-ready summaries
```

### CallLogsOutput Schema

```python
class CallLogsOutput(BaseModel):
    checkin: CheckInSummary  # Summary data
    medications: List[MedicationEntry]  # Extracted medications
    food_entries: List[FoodEntry]  # Extracted nutrition
    has_medications: bool  # Flag for medication discussion
    has_nutrition: bool  # Flag for nutrition discussion
```

### TranscriptSummary Schema

```python
class TranscriptSummary(BaseModel):
    summary: str  # Text summary
    patient_id: str  # Patient identifier
    patient_name: str  # Patient name
    call_log_id: str  # Call log ID
    timestamp: str  # ISO timestamp
```

## Configuration Best Practices

### Environment Variables

Configure VlogsAgent through environment variables in `.env.secrets`:

```bash
OPENAI_API_KEY=sk-...  # Required for LLM mode
```

### Development vs Production

**Development**:
```python
config = VlogsConfig(extract_with_llm=False, limit=5)  # Fast iteration
```

**Production**:
```python
agent = VlogsAgent.from_config()  # Use app settings (LLM enabled)
```

### Performance Tuning

- **Batch Processing**: Process multiple logs in parallel
- **Limit Management**: Use `limit` parameter to control batch size
- **Model Selection**: Use `gpt-4o-mini` for speed/cost balance

## Integration with Reflex App

The VlogsAgent is integrated into the patient dashboard state for real-time call log processing:

```python
from longevity_clinic.app.states.functions.vlogs_agent import VlogsAgent

class PatientDashboardState(rx.State):
    async def refresh_call_logs(self):
        """Refresh call logs using VlogsAgent."""
        agent = VlogsAgent.from_config()
        new_count, outputs, summaries = await agent.process_logs(
            phone_number=self.selected_phone
        )
        self.transcript_summaries = summaries
        # Process outputs into patient health data
```

## Troubleshooting

### Issue: AttributeError on CallLogsOutput

**Solution**: Use correct attribute names:
- ✅ `output.checkin` (not `checkin_data`)
- ✅ `output.medications` (not `output.checkin.medications`)
- ✅ `output.food_entries` (not `output.checkin.food_entries`)

### Issue: ModuleNotFoundError

**Solution**: Set PYTHONPATH when running tests:
```bash
PYTHONPATH=/home/mo/projects/Hackathon/longevity_clinic:$PYTHONPATH \
    uv run python tests/test_vlogs_agent.py
```

### Issue: OpenAI API Errors

**Solution**: Verify API key in `.env.secrets`:
```bash
echo $OPENAI_API_KEY  # Should show sk-...
```

## Migration Notes

### From Legacy call_logs.py

The VlogsAgent replaces the legacy `call_logs.py` implementation with:

1. **Better Configuration**: Centralized config in `config.py`
2. **Cleaner API**: Dataclass-based with clear interfaces
3. **Flexible Modes**: Toggle LLM processing easily
4. **Better Testing**: Comprehensive test suite
5. **Production Ready**: Default to LLM parsing for quality

### Changes Made

- ✅ Added VlogsConfig to AppConfig
- ✅ Reorganized vlogs_agent.py with better structure
- ✅ Created comprehensive test suite
- ✅ Set extract_with_llm=True as default
- ✅ Removed legacy call_logs.py code

## References

- **VlogsAgent Code**: `longevity_clinic/app/states/functions/vlogs_agent.py`
- **Configuration**: `longevity_clinic/app/config.py`
- **Tests**: `tests/test_vlogs_agent.py`
- **Schema**: `longevity_clinic/app/data/process_schema.py`
- **API Documentation**: `docs/call_logs_api.md`
