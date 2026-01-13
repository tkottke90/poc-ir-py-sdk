# iRacing Session Extract Models

This directory contains Pydantic models for parsing iRacing session extract JSON files.

## Overview

The models are organized into 4 main files, each representing a root-level entity in the session extract JSON:

### 1. `weekend.py`
Contains models for weekend/event information including track details, weather, and session configuration.

**Models:**
- `Weekend` (root) - Main weekend/event data
- `WeekendOptions` - Session configuration options
- `TelemetryOptions` - Telemetry recording settings

**Key Fields:**
- Track information (name, location, configuration, weather)
- Session metadata (SeriesID, SessionID, EventType)
- Build information (version, type, target)

### 2. `session.py`
Contains models for session data including results and lap times.

**Models:**
- `Session` (root) - Session container
- `SessionInfo` - Individual session details (warmup, race, etc.)
- `ResultsPosition` - Driver position and lap data
- `ResultsFastestLap` - Fastest lap information

**Key Fields:**
- Session type, laps, time limits
- Driver positions and results
- Lap times and incidents

### 3. `driver_info.py`
Contains models for driver and car information.

**Models:**
- `DriverInfo` (root) - Driver list container
- `Driver` - Individual driver/car details

**Key Fields:**
- Driver information (name, ID, team)
- Car details (model, class, setup)
- License and rating information
- Livery and customization data

### 4. `car_setup.py`
Contains models for car setup configuration with consolidated reusable models.

**Root Model:**
- `CarSetup` - Main setup container

**Reusable Models** (used multiple times):
- `TireData` - Used for all 4 tire positions (LeftFront, RightFront, LeftRear, RightRear)
- `CornerSetup` - Used for all 4 corner setups
- `DamperSettings` - Used for front and rear dampers

**Nested Models:**
- `TiresAero` - Tire and aerodynamic settings
- `Chassis` - Chassis configuration
- `Dampers` - Damper settings
- Plus various sub-models for specific components

## Usage

```python
import json
from models import Weekend, Session, DriverInfo, CarSetup

# Load session extract JSON
with open('session_extract.json', 'r') as f:
    data = json.load(f)

# Parse into models
weekend = Weekend(**data['weekend'])
session = Session(**data['session'])
driver_info = DriverInfo(**data['driver'])
car_setup = CarSetup(**data['carSetup'])

# Access data with type safety
print(f"Track: {weekend.TrackDisplayName}")
print(f"Drivers: {len(driver_info.Drivers)}")
print(f"Tire Type: {car_setup.TiresAero.TireType.TireType}")
```

## Testing

Run the test script to validate models against a session extract file:

```bash
cd src/models
python test_models.py
```

## Design Decisions

### Consolidated Models
Instead of creating separate models for each tire position or corner, we use reusable models:
- **Before:** 4 separate tire models (LeftFrontTire, RightFrontTire, etc.)
- **After:** 1 `TireData` model used 4 times

This approach:
- Reduces code duplication
- Improves maintainability
- Ensures consistency across similar components
- Follows DRY (Don't Repeat Yourself) principle

### Type Flexibility
Some fields accept multiple types (e.g., `Union[int, str]`) to handle variations in the iRacing data format:
- `LicColor` can be an integer or string like `'0xundefined'`
- `SessionLaps` can be an integer or string like `'unlimited'`

## Requirements

- Python 3.10+
- pydantic >= 2.0.0

Install dependencies:
```bash
pip install -r requirements.txt
```

