# Topcon MYAH ImportAdapter

ImportAdapter for Topcon MYAH myopia control device.

## Overview

The MYAH ImportAdapter processes the following measurement data:
- Axial length (optical biometry)
- Keratometry values (FlatK, SteepK)
- White-to-white measurements
- Pupil center coordinates
- Corneal topography matrices (stored but not mapped)

## File Format

MYAH exports data as XML files with UTF-16 encoding:

```xml
<?xml version="1.0" encoding="UTF-16"?>
<XMLDataPolarExportation>
  <Patient>
    <ID>1066234</ID>
    <LastName>Beno</LastName>
    <FirstName>Dominik</FirstName>
    <BirthDate>2012-05-02</BirthDate>
    <Sex>Male</Sex>
  </Patient>

  <PatientEyeData>
    <ID>12345</ID>
    <PatientID>1066234</PatientID>
    <Eye>OD</Eye>
    <Date>2025-01-07</Date>

    <Data>
      <FlatK>7.89</FlatK>
      <FlatAngle>178</FlatAngle>
      <SteepK>7.72</SteepK>
      <SteepAngle>88</SteepAngle>

      <AxialLength>24.52</AxialLength>

      <PupilCenter>
        <X>0.12</X>
        <Y>-0.08</Y>
      </PupilCenter>

      <WTW>
        <Diameter>11.8</Diameter>
        <OffsetX>0.1</OffsetX>
        <OffsetY>-0.05</OffsetY>
      </WTW>

      <!-- Corneal topography data matrices -->
      <CornealHeight>
        <Cols>24</Cols>
        <Rows>24</Rows>
        <MissingDataValue>-1.0</MissingDataValue>
        <!-- Matrix data -->
      </CornealHeight>

      <AxialCurvatures>
        <Cols>24</Cols>
        <Rows>24</Rows>
        <MissingDataValue>-1.0</MissingDataValue>
        <!-- Matrix data -->
      </AxialCurvatures>

      <TangentialCurvatures>
        <Cols>24</Cols>
        <Rows>24</Rows>
        <MissingDataValue>-1.0</MissingDataValue>
        <!-- Matrix data -->
      </TangentialCurvatures>

      <PolarAngle>
        <Cols>24</Cols>
        <Rows>24</Rows>
        <MissingDataValue>-1.0</MissingDataValue>
        <!-- Matrix data -->
      </PolarAngle>

      <PolarRadius>
        <Cols>24</Cols>
        <Rows>24</Rows>
        <MissingDataValue>-1.0</MissingDataValue>
        <!-- Matrix data -->
      </PolarRadius>
    </Data>
  </PatientEyeData>
</XMLDataPolarExportation>
```

## Import Methods

### File-based Transfer
- Export from MYAH device to USB/network
- Configure source path in DATEYE
- Supports UTF-16 encoded XML files

### Watch Folder
- Configure network path: `\\MYAH-PC\Exports\`
- Automatic transfer on file detection

## Field Mappings

### Patient Demographics

| MYAH | DATEYE | Notes |
|------|--------|-------|
| `Patient/ID` | `external_pid` | Prefixed with "MYAH-" |
| `Patient/FirstName` | `first_name` | |
| `Patient/LastName` | `last_name` | |
| `Patient/BirthDate` | `birth_date` | YYYY-MM-DD |
| `Patient/Sex` | `gender` | Male/Female → male/female |

### Available Measurements

| MYAH | DATEYE | Unit | Description |
|------|--------|------|-----------|
| **Axial Length** ||||
| `AxialLength` | `axial_length.value_mm` | mm | Eye length |
| **Cornea** ||||
| `FlatK` | `cornea.k1_mm` | mm | Flat meridian |
| `SteepK` | `cornea.k2_mm` | mm | Steep meridian |
| `FlatAngle` | `cornea.axis_k1` | ° | 0-180 |
| `SteepAngle` | `cornea.axis_k2` | ° | 0-180 |
| `WTW/Diameter` | `cornea.corneal_diameter` | mm | White-to-white |

### NOT Available from MYAH

The following fields are NOT provided by MYAH (will be null):
- `anterior_chamber.acd` - Anterior chamber depth
- `lens.thickness` - Lens thickness
- `cornea.corneal_thickness` - Central corneal thickness
- `pupil.diameter` - Pupil diameter (only center coordinates available)
- `axial_length.signal_noise` - SNR/quality metrics
- Any refraction data

### Data Transformation

**CRITICAL**: The adapter currently parses the XML but does NOT transform it to DATEYE format.
A transformation step is needed between parsing and storage:

```dart
// Current: XML → ImportedDataFileModel (keeps XML structure)
// Needed: XML → ImportedDataFileModel → DATEYE Measurement format
```

Keratometry values are stored in mm. To convert to diopters: `D = 337.5 / mm`

### Corneal Topography Data

The following matrices are stored but not currently mapped to DATEYE fields:
- `CornealHeight` - Elevation data (24x24 matrix)
- `AxialCurvatures` - Axial curvature map (24x24 matrix)
- `TangentialCurvatures` - Tangential curvature map (24x24 matrix)
- `PolarAngle` - Polar coordinates angle (24x24 matrix)
- `PolarRadius` - Polar coordinates radius (24x24 matrix)

Missing value indicator: `-1.0`

## Data Storage Philosophy

### Available from MYAH
The MYAH export provides the fields listed above. All available data is stored in the DATEYE format.

### Optional Fields (Not in MYAH Export)
The following fields are stored as `null` when importing from MYAH, but may be available from other devices:
- ACD (Anterior Chamber Depth)
- LT (Lens Thickness)
- CCT (Central Corneal Thickness)
- PupilDiameter (Photopic/Mesopic/Scotopic)
- QualityScore
- AxialLengthSNR (signal_noise)
- Standard Deviation

**DATEYE stores all available data** - if a device provides these fields, they will be stored. If not, they remain `null`. No manual entry required.

## Data Mapping

### XML to DATEYE Format

```xml
<!-- MYAH XML -->
<FlatK>7.89</FlatK>
<SteepK>7.72</SteepK>
<AxialLength>24.52</AxialLength>
```

```dart
// DATEYE Format
Measurement.axialLength(
  eye: 'right',
  value_mm: 24.52,
  signal_noise: null,  // Not provided by MYAH
  measurements: 5,     // Device default
  standard_deviation: null,  // Not provided
  data_source: 'device',
  measured_at: '2025-01-07T10:30:00Z',
)

Measurement.cornea(
  eye: 'right',
  k1_mm: 7.89,
  k2_mm: 7.72,
  axis_k1: 178,
  axis_k2: 88,
  corneal_diameter: 11.8,  // From WTW
  corneal_thickness: null,  // Not provided
  data_source: 'device',
)
```

### Field Mappings

| MYAH XML Field | DATEYE Field | Conversion |
|----------------|--------------|------------|
| `AxialLength` | `axial_length.value_mm` | String → double |
| - | `axial_length.signal_noise` | null (not available) |
| - | `axial_length.measurements` | 5 (default) |
| - | `axial_length.data_source` | "device" |
| `FlatK` | `cornea.k1_mm` | String → double |
| `SteepK` | `cornea.k2_mm` | String → double |
| `FlatAngle` | `cornea.axis_k1` | String → int |
| `SteepAngle` | `cornea.axis_k2` | String → int |
| `WTW.Diameter` | `cornea.corneal_diameter` | String → double |
| - | `cornea.corneal_thickness` | null (not available) |
| - | `cornea.data_source` | "device" |

### Available Fields

MYAH provides:
- ✅ Axial Length (value only, no quality metrics)
- ✅ Cornea - Keratometry (K1, K2)
- ✅ Cornea - White-to-white diameter
- ✅ Pupil Center
- ❌ Cornea - Central thickness (CCT)
- ❌ ACD (not available)
- ❌ Lens Thickness (not available)
- ❌ Signal-to-noise ratio
- ❌ Standard deviation

## Implementation Details

### UTF-16 Encoding
The XML files are encoded in UTF-16. The adapter handles this automatically:

```dart
final xmlBytes = await File(filePath).readAsBytes();
final utf16CodeUnits = xmlBytes.buffer.asUint16List();
final xmlString = String.fromCharCodes(utf16CodeUnits);
```

### Multiple Eye Data
A single export file can contain data for both eyes (OD and OS). The adapter processes all `PatientEyeData` entries in the file.

### Data Model
The internal data model (`ImportedDataFileModel`) reflects the XML structure:
- `XMLDataPolarExportation` (root)
  - `Patient` (patient demographics)
  - `PatientEyeData[]` (array of eye measurements)
    - `Data` (measurement values and matrices)

## Validation

The adapter validates:
- XML structure matches expected format
- Required fields are present
- Numeric values are parseable
- Date formats are valid
- Axial length values within range (15-35 mm)

## Error Handling

Common errors:
- Invalid XML structure
- Missing required fields
- UTF-16 encoding issues
- Invalid numeric values
- Out of range measurements

All errors are logged with details for troubleshooting.

## Future Enhancements

1. Support for additional MYAH export formats
2. Extraction of values from topography matrices
3. Automatic calculation of derived parameters
4. Support for progressive myopia tracking
5. Quality metrics extraction if available in future versions
