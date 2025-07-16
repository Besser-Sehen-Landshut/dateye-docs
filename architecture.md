# DATEYE Architecture

Offline-first medical device integration platform using ImportAdapter/ExportAdapter pattern.

## Design Philosophy

1. **No Database** - JSON file storage exclusively
2. **No Services** - Single desktop application
3. **No Network** - Offline operation by default
4. **Transparent Operations** - All actions logged and auditable

## System Overview

```
┌─────────────┐     ┌─────────┐     ┌──────────────┐
│   Import    │────▶│ DATEYE  │────▶│    Export    │
│  Adapters   │     │ Storage │     │   Adapters   │
└─────────────┘     └─────────┘     └──────────────┘
                          │
                    ┌─────▼─────┐
                    │ JSON Files│
                    └───────────┘
```

## Core Components

### 1. Import/Export Adapter System

```dart
// Import from medical devices
abstract class ImportAdapter {
  String get id;
  Future<bool> isParsable(String filePath);
  Future<ImportedDataFileModel> parse(String filePath);
}

// Export to medical devices/systems
abstract class IExportAdapter {
  String get id;
  String get displayName;
  Future<Either<Failure, bool>> testConnection(ExportTarget target);
  Future<Either<Failure, ExportResult>> export({
    required ExportableDataFile data,
    required ExportTarget target,
  });
}
```

**Design Principle**: "Store what's available, send what's needed"
- Import stores all available fields (missing as null)
- Export uses only required fields

### 2. File Storage Architecture

```
DATEYE/
├── events.ndjson              # Complete event history
├── importingDevice.ndjson     # Import device configurations
├── exportDestination.ndjson   # Export target configurations
├── appConfigs.ndjson          # Application settings
├── import/                    # Manual import directory
├── export/                    # Temporary export storage
├── archive/                   # Rotated logs
└── secure/                    # Encrypted patient data (planned)
    ├── identity.key           # Master encryption key
    └── patients.enc           # Encrypted patient identities
```

**Default paths:**
- Windows: `C:\Users\%USERNAME%\AppData\Local\DATEYE`
- macOS: `~/Library/Application Support/DATEYE`
- Linux: `~/.config/DATEYE`

### 3. Clean Architecture

```
┌─────────────────────────────────────────┐
│  Presentation (Flutter UI + BLoC)       │
├─────────────────────────────────────────┤
│  Infrastructure (Adapters + Storage)    │
├─────────────────────────────────────────┤
│  Core (Entities + Use Cases)            │
└─────────────────────────────────────────┘
```

**Dependency Rule**: Dependencies point inward only

## Data Flow

### Event Hierarchy
Three-level event structure for traceability:
- **Import Events**: Data reception from device
- **Export Events**: Data transmission to device  
- **Transfer Events**: Business workflow completion (links Import+Export)

### Pipeline
```
Import: File Detection → ImportAdapter → Parse → Storage → UI Update
Export: Export Request → ExportAdapter → Device → Result Logging
```

### Data Transformation Pattern (Critical)

**Current Issue**: ImportAdapters parse device formats but don't transform to DATEYE format.

```dart
// Current (Incorrect)
XML → ImportedDataFileModel (preserves XML structure) → Storage

// Required (Correct)
XML → ImportedDataFileModel → Transform → DATEYE Measurements → Storage
```

**Example Transformation**:
```dart
// Device XML
<AxialLength>24.52</AxialLength>
<FlatK>7.89</FlatK>

// DATEYE Format
Measurement.axialLength(
  eye: 'right',
  value_mm: 24.52,
  signal_noise: null,  // Device doesn't provide
  measured_at: DateTime.now(),
)

Measurement.cornea(
  eye: 'right', 
  k1_mm: 7.89,
  k1_d: 337.5 / 7.89,  // Calculated
)
```

**Transformation Rules**:
1. Map available fields to DATEYE schema
2. Store unavailable fields as `null` (not empty)
3. Calculate derived values (e.g., keratometry D from mm)
4. Preserve all device data for audit trail

## Implementation Status

### ✅ Complete
- ImportAdapter interface and Topcon MYAH implementation
- Core data models with Freezed
- NDJSON storage system
- BLoC state management
- Flutter UI framework

### ❌ Missing (Critical Path)
1. **Build configuration** - `injection.config.dart` not generated
2. **IExportAdapter interface** - Not implemented
3. **AL550 ExportAdapter** - Not implemented  
4. **ExportingDatasource** - All methods throw `UnimplementedError()`
5. **Data transformation** - Import parses XML but doesn't convert to DATEYE format
6. **Patient encryption** - Security layer not implemented

### Development Priority
1. Run build_runner to fix dependency injection
2. Create IExportAdapter interface
3. Implement AL550 ExportAdapter
4. Wire up ExportingDatasource
5. Add data transformation to ImportAdapter
6. Implement patient encryption before production

## Adapter Registry

| Device | Type | Import | Export | Status |
|--------|------|---------|---------|----------|
| Topcon MYAH | Biometer | ✅ | - | Complete |
| Mediworks AL550 | Biometer | Planned | ❌ | Export missing |
| ZEISS IOLMaster | Biometer | Planned | - | Not started |
| Eye-Office | Practice Mgmt | Planned | - | Not started |

## Security Model

**WARNING: Encryption not yet implemented** - Critical before production.

### Planned Implementation
- AES-256 encryption for patient identities
- Measurements stored separately (anonymized)
- Local-only encryption keys
- Manual key backup required

## System Requirements

### Minimum
- Windows 10 / macOS 10.15 / Ubuntu 20.04
- 4GB RAM
- 100MB + data storage
- No network required

### Recommended
- 8GB RAM (>1000 patients)
- SSD storage
- 1280x720 display
- Dedicated workstation

## Architecture Benefits

- **Zero Administration**: No database maintenance
- **Portability**: Single directory installation
- **Transparency**: Direct file inspection
- **Reliability**: Append-only operations
- **Offline-First**: No network dependencies

## Related Documentation

- [Adapter Development](adapter-development.md) - Creating adapters
- [Data Formats](data-formats.md) - JSON specifications
- [Flutter Implementation](flutter-implementation.md) - UI development