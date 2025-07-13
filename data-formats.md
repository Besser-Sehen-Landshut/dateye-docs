# DATEYE Data Formats

Comprehensive specification of all data structures, file formats, and JSON schemas used in DATEYE's ImportAdapter/ExportAdapter architecture.

## Overview

DATEYE uses NDJSON (Newline Delimited JSON) for all data storage:
- **NDJSON Format**: One JSON object per line, reverse chronological order
- **Performance Optimization**: Recent entries at file beginning for fast access
- **Character Encoding**: UTF-8 exclusively

## File Storage Implementation

### Performance Optimization

Reverse-chronological storage pattern:
- New entries prepended to file beginning
- Enables fast access to recent data without full file reads
- Optimized for typical UI access patterns (recent data first)
- File watchers provide real-time update notifications

### Database Abstraction Layer

Database abstraction over NDJSON files:
```dart
// Abstraction hierarchy
IDatabase → JsonFileStorageDatabase → .ndjson files
```

Abstraction benefits:
- Pagination support (limit/skip operations)
- File watching for reactive updates
- Consistent error handling across operations
- Future storage backend flexibility

## Core File Specifications

### events.ndjson

Immutable operation history containing all system operations:

```json
{"id":"import_20240115_001","timestamp":"2024-01-15T10:30:00Z","type":"import","mode":"automatic","status":"success","adapter":"topcon_myah","secret_pid":"pat_001","measurements":{"axial_length":[{"eye":"right","value":24.52}]}}
{"id":"export_20240115_002","timestamp":"2024-01-15T10:31:00Z","type":"export","mode":"automatic","status":"success","adapter":"mediworks_al550","secret_pid":"pat_001","target":"al550_device"}
{"id":"import_20240115_003","timestamp":"2024-01-15T10:32:00Z","type":"import","mode":"manual","status":"success","adapter":"eye_office","file_count":2}
```

**Event Types:**
- `import` - Data imported from device/source into DATEYE
- `export` - Data exported from DATEYE to device/target
- `discovery` - Endpoint discovery operations
- `connection` - Connection lifecycle events (create, edit, delete)
- `system` - System events (startup, rotation)

**Common Field Definitions:**
```typescript
{
  id: string;          // Unique event identifier
  timestamp: string;   // ISO 8601 UTC timestamp
  type: string;        // Event category
  mode?: "automatic" | "manual" | "scheduled"; // Operation trigger method
  status: "success" | "error" | "pending" | "info";
  source?: string;     // Source endpoint identifier
  target?: string;     // Target endpoint identifier
  error?: string;      // Human-readable error message
  error_code?: string; // Machine-readable error identifier
}
```

### importingDevice.ndjson

Import source configurations:

```json
{"id":"import_001","adapterId":"topcon_myah","name":"MYAH Biometer","config":{"path":"/import/myah","watchFolder":true},"enabled":true,"created":"2024-01-15T10:30:00Z","lastImport":"2024-01-15T14:25:00Z"}
{"id":"import_002","adapterId":"eye_office","name":"Eye-Office API","config":{"url":"https://eye-office.local:4450","syncInterval":300,"apiKey":"encrypted:..."},"enabled":true,"created":"2024-01-15T10:35:00Z"}
```

### exportDestination.ndjson

Export target configurations:

```json
{"id":"export_001","adapterId":"mediworks_al550","name":"AL550 Main Device","config":{"host":"192.168.1.100","port":8080},"enabled":true,"created":"2024-01-15T10:30:00Z","lastExport":"2024-01-15T14:25:00Z"}
{"id":"export_002","adapterId":"file_export","name":"Daily Backup","config":{"path":"/backup/dateye","format":"json"},"enabled":true,"created":"2024-01-15T11:00:00Z"}
```

### appConfigs.ndjson

Application configuration structure:

```json
{
  "language": "de",
  "import": {
    "autoDiscovery": true,
    "discoveryTimeout": 5000,
    "defaultWatchInterval": 5000,
    "retryPolicy": {
      "maxRetries": 10,
      "backoffMultiplier": 2,
      "initialDelayMs": 1000
    }
  },
  "export": {
    "autoRetry": true,
    "defaultTimeout": 10000,
    "batchSize": 10
  },
  "adapters": {
    "registeredAdapters": [
      {
        "id": "topcon_myah",
        "name": "Topcon MYAH",
        "type": "import",
        "defaultConfig": {
          "timeout": 5000,
          "encoding": "utf-16"
        }
      },
      {
        "id": "mediworks_al550",
        "name": "Mediworks AL550",
        "type": "export",
        "defaultConfig": {
          "port": 8080,
          "timeout": 10000
        }
      }
    ]
  }
}

## Data Model Architecture

### Type Safety with Freezed

DATEYE implements compile-time type safety using Freezed:

- **Type Safety**: Compile-time error detection
- **Immutability**: Prevents accidental data modification
- **JSON Serialization**: Automatic bidirectional conversion
- **Union Types**: Flexible handling of variant data types

### Core Model Definitions

#### TransferData

Primary data structure for Source→Target operations:

```dart
@freezed
class TransferData with _$TransferData {
  const factory TransferData({
    required String sourceEndpoint,
    required String targetEndpoint,
    required String secretPid,
    required Map<String, dynamic> patientData,
    required List<Measurement> measurements,
    required DateTime transferTime,
    String? connectionId,
    Map<String, dynamic>? metadata,
  }) = _TransferData;
}
```

#### Connection

Workflow configuration model:

```dart
@freezed
class Connection with _$Connection {
  const factory Connection({
    required String id,
    required String name,
    required String sourceEndpoint,
    required String targetEndpoint,
    required Map<String, dynamic> sourceConfig,
    required Map<String, dynamic> targetConfig,
    @Default(true) bool enabled,
    @Default('continuous') String mode,
    String? schedule,
    required DateTime created,
    DateTime? lastTransfer,
    @Default(0) int transferCount,
    @Default(0) int errorCount,
  }) = _Connection;
}
```

#### Measurement Models

```dart
// Axial Length measurement
@freezed
class AxialLength with _$AxialLength {
  const factory AxialLength({
    required String eye,  // 'right' or 'left'
    required double value, // millimeters
    double? snr,          // Signal-to-noise ratio
  }) = _AxialLength;
}

// Refraction measurement
@freezed
class ExamRefraction with _$ExamRefraction {
  const factory ExamRefraction({
    required String eye,
    required double sphere,
    required double cylinder,
    required int axis,
    double? addition,  // bifocal addition
  }) = _ExamRefraction;
}

// Complete examination
@freezed
class Examination with _$Examination {
  const factory Examination({
    required List<ExamRefraction> refractions,
    required List<AxialLength> axialLength,
    // Additional measurement types as needed
  }) = _Examination;
}
```

### Extensible Union Types

Future-proof measurement handling:

```dart
@freezed
class MeasurementData with _$MeasurementData {
  // Strongly-typed known measurements
  const factory MeasurementData.axialLength({
    required String eye,
    required double value,
    double? snr,
  }) = AxialLengthData;

  const factory MeasurementData.refraction({
    required String eye,
    required double sphere,
    required double cylinder,
    required int axis,
  }) = RefractionData;

  // Generic fallback for unknown types
  const factory MeasurementData.custom(
    String type,
    Map<String, dynamic> data,
  ) = CustomData;
}
```

Benefits:
- Type-safe handling of known measurements
- Extensibility for future measurement types
- Gradual migration path for new data types

## Transfer History Structure

Standard transfer record format:

```json
{
  "id": "transfer_001",
  "timestamp": "2024-01-15T10:30:00Z",
  "type": "transfer",
  "source": "topcon_myah",
  "target": "mediworks_al550", 
  "connection_id": "conn_001",
  "secret_pid": "pat_001",
  "measurements": [
    {
      "type": "axial_length",
      "data": {
        "eye": "right",
        "value": 24.52,
        "snr": 12.5,
        "measured_at": "2024-01-15T10:25:00Z"
      }
    }
  ],
  "metadata": {
    "source_file": "patient_001.xml",
    "processing_time_ms": 1250,
    "data_quality": "high"
  }
}
```

### Measurement Type Specifications

**Refraction (Optical prescription):**
```json
{
  "type": "refraction",
  "data": {
    "eye": "right",
    "sphere": -2.25,
    "cylinder": -0.50,
    "axis": 90,
    "addition": 2.00,  // Optional
    "vertex": 12       // Optional
  }
}
```

**Biometry (Ocular measurements):**
```json
{
  "type": "biometry", 
  "data": {
    "eye": "right",
    "axial_length": 24.52,
    "acd": 3.21,              // Anterior chamber depth
    "lens_thickness": 3.65,   // Optional
    "white_to_white": 11.8    // Optional
  }
}
```

**Keratometry (Corneal measurements):**
```json
{
  "type": "cornea",
  "data": {
    "eye": "right",
    "k1_d": 43.11,     // Flat meridian (diopters)
    "k1_mm": 7.83,     // Flat meridian (mm radius)
    "k2_d": 44.36,     // Steep meridian (diopters)
    "k2_mm": 7.61,     // Steep meridian (mm radius)
    "axis_k1": 180,
    "axis_k2": 90,
    "astigmatism": 1.25
  }
}
```

## Endpoint-to-DATEYE Mappings

### Topcon MYAH Conversion
```xml
<!-- Device XML Format -->
<FlatK>7.89</FlatK>
<SteepK>7.72</SteepK>
<AxialLength>24.52</AxialLength>
```

```dart
// DATEYE Internal Format
AxialLength(eye: 'right', value: 24.52)
// Keratometry: k1_d = 337.5 / 7.89 = 42.77 D
```

### Eye-Office Conversion
```json
// Device JSON Format
{
  "refrRight": {
    "sphere": -2.25,
    "cylinder": -0.50,
    "axisCylinder": 90
  }
}
```

```dart
// DATEYE Internal Format
ExamRefraction(
  eye: 'right',
  sphere: -2.25,
  cylinder: -0.50,
  axis: 90
)
```

### Measurement Validation Rules

| Measurement | Field | Normal Range | Unit | Notes |
|-------------|-------|-------------|------|-------|
| Refraction | sphere | -20 to +20 | diopters | Negative for myopia |
| Refraction | cylinder | -10 to 0 | diopters | Always negative convention |
| Refraction | axis | 0 to 180 | degrees | TABO notation |
| AxialLength | value | 20 to 30 | mm | Typical: 22-26mm |
| AxialLength | snr | >5.0 | - | Quality metric |
| Keratometry | k1_d, k2_d | 38 to 50 | diopters | Calculated from radius |
| Visual Acuity | value | 0.1 to 2.0 | decimal | 1.0 = 20/20 |
| Pupil | diameter | 1.5 to 9.0 | mm | Light-dependent |

## Identifier Generation

### Event IDs
Pattern: `{type}_{YYYYMMDD}_{NNN}`
- `transfer_20240115_042`
- `sync_20240115_043`
- `discovery_20240115_044`

### Connection IDs
Pattern: `conn_{NNN}`
- `conn_001`, `conn_002`, etc.
- Sequential numbering for simplicity

### Patient IDs
Pattern: `pat_YYYYMMDD_NNN`
- Timestamp-based generation
- Collision-free design
- Human-readable format

## File Maintenance

### Daily Log Rotation
Executed at midnight local time:
1. Rename `history.ndjson` to `archive/history-YYYY-MM-DD.json`
2. Create new empty `history.ndjson`
3. Log rotation event

### Monthly Archive Process
First day of each month:
1. Archive completed transfers
2. Retain only active connections
3. Clean expired discovery data

## Error Code Standards

Format: `CATEGORY_SPECIFIC_ERROR`

Categories:
- `ENDPOINT_` - Endpoint communication errors
- `TRANSFER_` - Data transfer failures  
- `CONNECTION_` - Connection configuration issues
- `VALIDATION_` - Data validation failures
- `DISCOVERY_` - Endpoint discovery problems
- `SYSTEM_` - System-level errors

Examples:
- `ENDPOINT_TIMEOUT`
- `TRANSFER_DATA_INVALID`
- `CONNECTION_CONFIG_MISSING`
- `VALIDATION_OUT_OF_RANGE`
- `DISCOVERY_NO_DEVICES_FOUND`

## Implementation Guidelines

1. **JSON Validation**: Validate before writing
2. **Atomic Operations**: Use transactions for multi-file updates
3. **Partial Read Handling**: Support incomplete JSON Lines reads
4. **Timestamp Standards**: UTC with timezone information
5. **Forward Compatibility**: Preserve unrecognized fields

## Related Documentation

- [Architecture](architecture.md) - System design overview
- [Endpoint Development](adapter-development.md) - Data format usage