# DATEYE Data Formats

Complete specification of file formats, data structures, and measurement types used in DATEYE.

## Core Principle

"Store what's available, send what's needed"
- Import: Store all fields from device (null if missing)
- Export: Use only required fields

## Storage Architecture

### NDJSON Format
- **Format**: Newline Delimited JSON - one object per line
- **Order**: Reverse chronological (newest first)
- **Encoding**: UTF-8
- **Operations**: Append-only

### File Structure
```
DATEYE/
├── events.ndjson              # System event log
├── importingDevice.ndjson     # Import configurations
├── exportDestination.ndjson   # Export configurations
├── appConfigs.ndjson          # Application settings
└── archive/                   # Rotated logs
```

## Event Structure

### Event Types

Three-level hierarchy:
- **import**: Data received from device
- **export**: Data sent to device
- **transfer**: Complete workflow (links import+export)

### events.ndjson

```json
{"id":"import_20240115_001","timestamp":"2024-01-15T10:30:00Z","type":"import","adapter":"topcon_myah","secret_pid":"pat_001","measurements":{"axial_length":[{"eye":"right","value":24.52}]}}
{"id":"export_20240115_002","timestamp":"2024-01-15T10:31:00Z","type":"export","adapter":"mediworks_al550","secret_pid":"pat_001","target":"al550_device"}
{"id":"transfer_20240115_003","timestamp":"2024-01-15T10:32:00Z","type":"transfer","source":"topcon_myah","target":"mediworks_al550","import_id":"import_20240115_001","export_id":"export_20240115_002"}
```

### importingDevice.ndjson

```json
{"id":"import_001","adapterId":"topcon_myah","name":"MYAH Biometer","config":{"path":"/import/myah","watchFolder":true},"enabled":true,"created":"2024-01-15T10:30:00Z"}
```

### exportDestination.ndjson

```json
{"id":"export_001","adapterId":"mediworks_al550","name":"AL550 Main","config":{"host":"192.168.1.100","port":8080},"enabled":true,"created":"2024-01-15T10:30:00Z"}
```

### appConfigs.ndjson

```json
{
  "language": "en",
  "import": {
    "autoDiscovery": true,
    "defaultWatchInterval": 5000
  },
  "export": {
    "autoRetry": true,
    "defaultTimeout": 10000
  }
}
```

## Examination Data Structure

```typescript
{
  examination: {
    id: string,              // Unique examination ID
    measured_at: string,     // ISO 8601 timestamp
    device: string,          // Device name/model
    operator?: string,       // Person performing measurement
  },
  patient: PatientData,
  measurements: MeasurementData[]
}
```

### Patient Demographics

```typescript
{
  external_id: string,      // Device-specific patient ID
  first_name: string,
  last_name: string,
  birth_date: string,       // ISO 8601 date (YYYY-MM-DD)
  gender: "male" | "female" | "other",

  // Optional
  middle_name?: string,
  phone?: string,
  email?: string,
  address?: {
    street: string,
    city: string,
    postal_code: string,
    country: string
  }
}
```

## Measurement Specifications

### 1. Axial Length

```typescript
{
  type: "axial_length",
  eye: "right" | "left",
  value_mm: number,         // 15-35 mm range

  // Quality metrics
  signal_noise?: number,    // SNR (>5.0 good)
  measurements?: number,    // Count (≥5 recommended)
  standard_deviation?: number, // <0.05mm good
}
```

### 2. Cornea (Keratometry)

```typescript
{
  type: "cornea",
  eye: "right" | "left",

  // Values in mm only
  k1_mm: number,            // Flatter meridian (5.5-10.0)
  k2_mm: number,            // Steeper meridian (5.5-10.0)
  axis_k1: number,          // 0-180°
  axis_k2: number,          // 0-180°

  corneal_diameter?: number,  // 9.0-14.0 mm
  corneal_thickness?: number, // 400-700 µm
}
```

**Conversion**: Diopters = 337.5 / mm

### 3. Refraction

```typescript
{
  type: "refraction",
  eye: "right" | "left",

  sphere: number,           // -50 to +50 D
  cylinder: number,         // -20 to +20 D
  axis: number,             // 0-180°

  addition?: number,        // 0 to +4 D
  vertex?: number,          // 8-20 mm
  prism?: number,           // 0-20 prism D
  prism_base?: number,      // 0-360°

  va_cc?: number,           // 0.01-2.0 (corrected VA)
  refraction_type?: "subjective" | "objective",
}
```

### 4. Additional Measurement Types

- **Anterior Chamber**: `acd` (2-5 mm), `acd_definition`
- **Lens**: `thickness` (3-5 mm), `status` (clear/cataract/pseudophakic/aphakic)
- **Pupil**: `diameter` (1.5-9.0 mm), `condition` (photopic/mesopic/scotopic)

### Core Type Definition (Freezed)

```dart
@freezed
class Measurement with _$Measurement {
  const factory Measurement.axialLength({
    required String eye,
    required double value,
    double? snr,
  }) = AxialLength;

  const factory Measurement.refraction({
    required String eye,
    required double sphere,
    required double cylinder,
    required int axis,
    double? addition,
  }) = Refraction;

  const factory Measurement.keratometry({
    required String eye,
    required double k1,
    required double k2,
    required int axis1,
    required int axis2,
  }) = Keratometry;

  const factory Measurement.custom(
    String type,
    Map<String, dynamic> data,
  ) = CustomMeasurement;
}
```

## Validation Rules

| Measurement | Field | Valid Range | Unit | Notes |
|-------------|-------|-------------|------|-------|
| Refraction | sphere | -50 to +50 | diopters | Negative = myopia |
| Refraction | cylinder | -20 to +20 | diopters | Can be + or - |
| Refraction | axis | 0-180 | degrees | TABO notation |
| Refraction | addition | 0 to +4 | diopters | Bifocal only |
| Axial Length | value_mm | 15-35 | mm | Flag outside 20-30 |
| Axial Length | SNR | >2.0 | - | >5.0 good quality |
| Cornea | k1_mm, k2_mm | 5.5-10.0 | mm | 34-61 D |
| Cornea | diameter | 9.0-14.0 | mm | White-to-white |
| ACD | value | 2.0-5.0 | mm | Anterior chamber |
| Lens | thickness | 3.0-5.0 | mm | Crystalline lens |
| Pupil | diameter | 1.5-9.0 | mm | Light-dependent |

## Device Availability Matrix

| Field | MYAH | IOLMaster 500 | IOLMaster 700 | AL550 | Eye-Office |
|-------|------|---------------|---------------|-------|------------|
| Demographics | ✅ | ✅ | ✅ | ✅ | ✅ |
| Axial Length | ✅ | ✅ | ✅ | ✅ | ❌ |
| Keratometry | ✅ | ✅ | ✅ | ✅ | ❌ |
| Corneal WTW | ✅ | ✅ | ✅ | ✅ | ❌ |
| Corneal Thickness | ❌ | ❌ | ✅ | ✅ | ❌ |
| Refraction | ❌ | ❌ | ❌ | ❌ | ✅ |
| ACD | ❌ | ✅ | ✅ | ✅ | ❌ |
| Lens Thickness | ❌ | ❌ | ✅ | ✅ | ❌ |
| Pupil Size | ❌ | ❌ | ✅ | ✅ | ❌ |

## Storage Rules

1. **Store Everything**: If device provides it, store it
2. **Null for Missing**: Fields not provided are `null`
3. **Original Units**: Store in device-provided units
4. **Quality Metrics**: Always include if available
5. **No Manual Entry**: Never fill missing fields manually

## Identifier Patterns

- **Event IDs**: `{type}_{YYYYMMDD}_{NNN}` (e.g., `import_20240115_001`)
- **Patient IDs**: `pat_{YYYYMMDD}_{NNN}` (anonymized)
- **Connection IDs**: `conn_{NNN}` (sequential)
- **Examination IDs**: `exam_{YYYYMMDD}_{NNN}`

## Error Codes

Format: `CATEGORY_SPECIFIC_ERROR`

| Category | Prefix | Examples |
|----------|--------|----------|
| Endpoint | `ENDPOINT_` | `ENDPOINT_TIMEOUT`, `ENDPOINT_UNREACHABLE` |
| Transfer | `TRANSFER_` | `TRANSFER_DATA_INVALID`, `TRANSFER_INCOMPLETE` |
| Connection | `CONNECTION_` | `CONNECTION_CONFIG_MISSING`, `CONNECTION_REFUSED` |
| Validation | `VALIDATION_` | `VALIDATION_OUT_OF_RANGE`, `VALIDATION_REQUIRED_FIELD` |
| System | `SYSTEM_` | `SYSTEM_DISK_FULL`, `SYSTEM_PERMISSION_DENIED` |

## File Maintenance

### Daily Rotation
- Rename `events.ndjson` → `archive/events-YYYY-MM-DD.ndjson`
- Create new empty `events.ndjson`
- Log rotation event

### Monthly Cleanup
- Archive transfers >90 days old
- Compress old archives
- Clean temporary files

## Related Documentation

- [Architecture](architecture.md) - System design overview
- [Adapter Development](adapter-development.md) - Creating device adapters
- [Topcon MYAH Adapter](adapters/topcon-myah.md) - Example implementation
- [Mediworks AL550 Adapter](adapters/mediworks-al550.md) - Import/Export example