# DATEYE Adapter Overview

## Summary of All Adapters

### Topcon MYAH
- **Type**: ImportAdapter only
- **Direction**: MYAH → DATEYE
- **Data Imported**:
  - **Patient data**: ID, Name, Birth date, Gender
  - **Measurements**: Axial length, Keratometry (K1/K2), White-to-white, Pupil center position
  - **Missing**: ACD, Lens thickness, CCT, Pupil diameter, Quality score
- **Format**: XML (UTF-16)

### Mediworks AL550
- **ImportAdapter**: AL550 → DATEYE
  - **Patient data**: ID, Name, Birth date, Gender
  - **Measurements**: Complete biometry including Axial length, Keratometry, ACD, Lens thickness, CCT, White-to-white, Pupil diameter
  - **Format**: JSON
- **ExportAdapter**: DATEYE → AL550
  - **Exports**: ONLY patient registration (ID, Name, Birth date, Gender)
  - **Purpose**: Patient must be registered before measurement
  - **Format**: JSON via HTTP API

### Eye-Office
- **Type**: ImportAdapter only
- **Direction**: Eye-Office → DATEYE
- **Data Imported**:
  - **Patient data**: ID, Name, Birth date, Gender
  - **Measurements**: Refraction values (Sphere, Cylinder, Axis, Addition), Visual acuity, Prism values
  - **Missing**: Biometry data (no axial length, keratometry, etc.)
- **Format**: REST API (JSON)
- **Note**: Export capability planned but not implemented

### ZEISS IOLMaster
- **Type**: ImportAdapter only
- **Direction**: IOLMaster → DATEYE
- **Data Imported**:
  - **Patient data**: ID, Name, Birth date, Gender
  - **Measurements**: Axial length, Keratometry, ACD, White-to-white
  - **IOLMaster 700 adds**: Lens thickness, CCT, Total keratometry
- **Format**: DICOM or XML
- **Models**: IOLMaster 500 and 700

## Data Categories by Adapter

### Patient Data (ALL adapters import this)
- Patient ID (external)
- First name
- Last name
- Birth date
- Gender

### Biometry Data
- **Complete set**: AL550, IOLMaster 700
- **Partial set**: MYAH (missing ACD, LT, CCT), IOLMaster 500 (missing LT)
- **None**: Eye-Office

### Refraction Data
- **Available**: Eye-Office only
- **Not available**: MYAH, AL550, IOLMaster

## Data Flow Patterns

### Pattern 1: Import Only (MYAH, IOLMaster, Eye-Office)
```
Device/System → DATEYE (Patient + Measurements)
```
These devices/systems only provide data to DATEYE.

### Pattern 2: Bidirectional (AL550)
```
Import:  AL550 → DATEYE (Patient + Complete measurements)
Export:  DATEYE → AL550 (Patient registration only)
```
The AL550 can both provide and receive data, but only accepts patient registration.

## Key Principles

1. **ALL adapters import patient data** - This is fundamental
2. **Import Adapters**: Store all available data, set unavailable fields to null
3. **Export Adapters**: Send only what the target device accepts
4. **No data transformation**: Simple field mapping
5. **No validation for missing optional fields**: Store what's available

## Measurement Availability Matrix

| Field | MYAH | AL550 | IOLMaster 500 | IOLMaster 700 | Eye-Office |
|-------|------|-------|---------------|---------------|------------|
| **Patient Data** | ✓ | ✓ | ✓ | ✓ | ✓ |
| Axial Length | ✓ | ✓ | ✓ | ✓ | ✗ |
| Keratometry | ✓ | ✓ | ✓ | ✓ | ✗ |
| ACD | ✗ | ✓ | ✓ | ✓ | ✗ |
| Lens Thickness | ✗ | ✓ | ✗ | ✓ | ✗ |
| CCT | ✗ | ✓ | ✗ | ✓ | ✗ |
| White-to-white | ✓ | ✓ | ✓ | ✓ | ✗ |
| Pupil Diameter | ✗ | ✓ | ✗ | ✗ | ✗ |
| Refraction | ✗ | ✗ | ✗ | ✗ | ✓ |
| Visual Acuity | ✗ | ✗ | ✗ | ✗ | ✓ |

## Documentation Status

All adapter documentation is:
- ✓ Complete in English
- ✓ Technically accurate
- ✓ Consistent with implementation
- ✓ Clear about import/export capabilities
- ✓ Clear about patient data import (all adapters)