# DATEYE Architecture

Offline-first medical device integration platform using ImportAdapter/ExportAdapter pattern for type-safe device communication.

## Design Philosophy

DATEYE follows four core principles:

1. **No Database** - JSON file storage exclusively
2. **No Services** - Single desktop application
3. **No Network** - Offline operation by default
4. **Transparent Operations** - All actions logged and auditable

## System Overview

```
┌─────────────┐     ┌─────────┐     ┌──────────────┐
│   Import    │────▶│ DATEYE  │────▶│    Export    │
│  Adapters   │     │ Storage │     │   Adapters   │
│             │     │         │     │              │
└─────────────┘     └─────────┘     └──────────────┘
                          │
                    ┌─────▼─────┐
                    │ JSON Files│
                    └───────────┘
```

## Core Components

### 1. Import/Export Adapter System

DATEYE implements separate adapter interfaces for medical device integration:

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
  String? get iconName;
  
  Future<Either<Failure, bool>> testConnection(ExportTarget target);
  Future<Either<Failure, ExportResult>> export({
    required ExportableDataFile data,
    required ExportTarget target,
  });
}
```

**Design Benefits:**
- **Clear Separation**: Import = data source, Export = data target
- **Type Safety**: Strongly typed interfaces with Either pattern
- **Testability**: Easy mocking and isolated testing
- **Extensibility**: Simple addition of new devices

### 2. File Storage Architecture

Data stored as NDJSON (Newline Delimited JSON) in the application directory:

```
DATEYE/
├── events.ndjson              # Complete event history
├── importingDevice.ndjson     # Import device configurations
├── exportDestination.ndjson   # Export target configurations
├── appConfigs.ndjson          # Application settings
├── import/                    # Manual import directory
├── export/                    # Temporary export storage
├── archive/                   # Rotated logs
└── secure/                    # Encrypted patient data
    ├── identity.key           # Master encryption key
    └── patients.enc           # Encrypted patient identities
```

**Performance optimization**: Files use reverse chronological order - newest entries appear first for faster access.

**Default installation paths:**
- Windows: `C:\Users\%USERNAME%\AppData\Local\DATEYE`
- macOS: `~/Library/Application Support/DATEYE`
- Linux: `~/.config/DATEYE`

### 3. Data Flow Pipeline

**Import Flow:**
```
File Detection → ImportAdapter → Parse → DATEYE Storage → UI Update
```

**Export Flow:**
```
Export Request → ExportAdapter → Device/Target → Result Logging
```

**Combined Workflow:**
```
Source Device → ImportAdapter → DATEYE → ExportAdapter → Target Device
```

## Data Models

Type-safe data models using Freezed for compile-time safety:

```dart
// Import data structure
@freezed
class ImportedDataFileModel with _$ImportedDataFileModel {
  const factory ImportedDataFileModel({
    required XmlDataPolarExportation xmlDataPolarExportation,
  }) = _ImportedDataFileModel;
}

// Export data structure
@freezed
class ExportableDataFile with _$ExportableDataFile {
  const factory ExportableDataFile({
    required DataFile file,
    required ExportDestination destination,
    @Default(0) double progress,
  }) = _ExportableDataFile;
}
```

**Benefits:**
- Compile-time error checking
- Immutable medical records
- Automatic JSON serialization
- Self-documenting interfaces

## Adapter Implementations

### Import Adapters

**Current Implementation:**

| Adapter | Status | Data Types |
|---------|---------|------------|
| **Topcon MYAH** | ✅ Complete | Axial length, keratometry, pupil data |
| **ZEISS IOLMaster** | 📋 Planned | Optical biometry, IOL calculations |
| **Eye-Office** | 📋 Planned | Demographics, refraction data |

**Example Implementation:**
```dart
@Named('topcon_myah')
@Singleton(as: ImportAdapter)
class TopconMyahImportAdapter implements ImportAdapter {
  const TopconMyahImportAdapter(this._parser);
  
  final IXmlParser _parser;

  @override
  String get id => 'topcon_myah';

  @override
  Future<ImportedDataFileModel> parse(String filePath) async {
    final xmlString = await getXmlStringFromFilePath(filePath);
    final jsonData = await _parser.parse(xmlString);
    return ImportedDataFileModel.fromJson(jsonData);
  }
}
```

### Export Adapters

**Current Implementation:**

| Adapter | Status | Capabilities |
|---------|---------|--------------|
| **Mediworks AL550** | ✅ Complete | Patient registration via HTTP API |
| **File Export** | 📋 Planned | JSON/CSV file output |
| **Myopia.cloud** | 📋 Planned | Cloud analytics upload |

**Example Implementation:**
```dart
@Named('al550_export')
@Singleton(as: IExportAdapter)
class AL550ExportAdapter implements IExportAdapter {
  const AL550ExportAdapter(this._httpClient);

  @override
  String get id => 'al550_export';

  @override
  Future<Either<Failure, ExportResult>> export({
    required ExportableDataFile data,
    required ExportTarget target,
  }) async {
    // Convert data to AL550 format
    final al550Patient = _formatPatientForAL550(data);
    
    // Send via HTTP API
    final response = await _httpClient.post(
      'http://${target.config['host']}:${target.config['port']}/setPatients',
      data: FormData.fromMap({'file': al550Patient}),
    );
    
    return response.statusCode == 200
        ? const Right(ExportResult.success())
        : Left(NetworkFailure('Export failed'));
  }
}
```

## Dependency Injection

GetIt + Injectable provide automatic adapter management:

```dart
// Self-registering adapters
@Named('topcon_myah')
@Singleton(as: ImportAdapter)
class TopconMyahImportAdapter implements ImportAdapter { ... }

@Named('al550_export')
@Singleton(as: IExportAdapter)  
class AL550ExportAdapter implements IExportAdapter { ... }

// Auto-registration
@module
abstract class AdapterModule {
  @singleton
  Map<String, ImportAdapter> get importAdapters => {
    'topcon_myah': getIt<ImportAdapter>(instanceName: 'topcon_myah'),
  };

  @singleton
  Map<String, IExportAdapter> get exportAdapters => {
    'al550_export': getIt<IExportAdapter>(instanceName: 'al550_export'),
  };
}
```

**Benefits:**
- Testability through dependency injection
- Modular architecture
- Automatic dependency resolution
- Named adapter implementations

## State Management

BLoC pattern provides reactive UI updates:

```dart
// File system changes trigger UI updates
File Change → File Watcher → Cubit → State → UI

// Import/Export state management
class ImporterListenerCubit extends Cubit<ImporterListenerState> {
  void startWatching() {
    _database.watchAll<ImportingDevice>().listen((devices) {
      emit(state.copyWith(devices: devices));
    });
  }
}
```

**Two-Layer State Architecture:**
- **Persistent State**: NDJSON files as single source of truth
- **UI State**: In-memory state via BLoC for reactive updates

## Clean Architecture Implementation

Three distinct layers with unidirectional dependencies:

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
- Core: No external dependencies
- Infrastructure: Depends on Core
- Presentation: Depends on Infrastructure and Core

## UI Integration Strategy

The UI shows "Source → Target" workflows while maintaining separate adapters internally:

```dart
// UI presents unified workflow
class ConnectionsCubit extends Cubit<ConnectionsState> {
  void createConnection({
    required String sourceAdapterId,
    required String targetAdapterId,
  }) {
    // Create ImportDevice for source
    final importDevice = ImportingDevice(adapterId: sourceAdapterId, ...);
    
    // Create ExportDestination for target  
    final exportDestination = ExportDestination(adapterId: targetAdapterId, ...);
    
    // Link them logically but keep separate
    emit(state.copyWith(newConnection: ConnectionWorkflow(
      source: importDevice,
      target: exportDestination,
    )));
  }
}
```

**UI Benefits:**
- User sees intuitive "MYAH → AL550" workflow
- Technical implementation remains clean and separated
- Easy testing of import and export functionality independently

## Error Handling Strategy

### Error Isolation
- Import failures don't affect export functionality
- Export failures preserve original data integrity
- File corruption skips affected entries only
- Connection failures trigger automatic retry

### Either Pattern Implementation
```dart
// Import error handling
Future<Either<Failure, ImportResult>> importFile(String path) async {
  try {
    final adapter = _getImportAdapter(deviceType);
    final result = await adapter.parse(path);
    return Right(ImportResult.success(result));
  } catch (e) {
    return Left(ImportFailure('Import failed: $e'));
  }
}

// Export error handling
Future<Either<Failure, ExportResult>> exportData(ExportableDataFile data) async {
  try {
    final adapter = _getExportAdapter(data.destination.adapterId);
    return await adapter.export(data: data, target: data.destination);
  } catch (e) {
    return Left(ExportFailure('Export failed: $e'));
  }
}
```

## File Format Specifications

### Import Device Configuration (importingDevice.ndjson)
```json
{"id":"device_001","adapterId":"topcon_myah","name":"MYAH Biometer","config":{"path":"/import/myah","watchFolder":true},"enabled":true,"created":"2024-01-15T10:30:00Z"}
```

### Export Destination Configuration (exportDestination.ndjson)
```json
{"id":"dest_001","adapterId":"al550_export","name":"AL550 Main","config":{"host":"192.168.1.100","port":8080},"enabled":true,"created":"2024-01-15T10:30:00Z"}
```

### Event History (events.ndjson)
```json
{"id":"event_001","timestamp":"2024-01-15T10:30:00Z","type":"import","adapterId":"topcon_myah","status":"success","patientCount":1}
{"id":"event_002","timestamp":"2024-01-15T10:31:00Z","type":"export","adapterId":"al550_export","status":"success","patientCount":1}
```

## Security Model

### Current State
**WARNING: Encryption not yet implemented** - Critical priority before production deployment.

### Security Configuration

#### Encryption Key Management
**Critical: The `identity.key` file must be backed up. Loss of this file results in permanent data loss.**

Backup procedure:
1. Navigate to `DATEYE/secure/identity.key`
2. Copy to secure external storage
3. Store in physically secure location (e.g., safe)
4. Document backup location
5. Test recovery procedure quarterly

#### File System Permissions
Windows configuration:
```powershell
# Via GUI: Right-click secure folder → Properties → Security
# Remove all user permissions except current user
```

Unix-based systems:
```bash
chmod 700 ~/Library/Application\ Support/DATEYE/secure
chmod 600 ~/Library/Application\ Support/DATEYE/secure/*
```

#### Cloud Synchronization Exclusion
Prevent automatic cloud synchronization of sensitive files:
- **OneDrive**: Settings → Choose folders → Exclude DATEYE/secure
- **iCloud**: Append `.nosync` to filenames
- **Dropbox**: Selective Sync → Deselect DATEYE/secure
- **Google Drive**: Preferences → Exclude folder

### Planned Security Implementation

**Protected data:**
- Patient identities encrypted at rest (AES-256)
- Measurements stored separately from identities
- No network requirements for core operations
- Full GDPR compliance

## Implementation Status vs. Architecture Vision

### ✅ Implemented and Tested
- **ImportAdapter Pattern**: Fully functional with Topcon MYAH reference
- **Clean Architecture**: Three-layer separation implemented
- **NDJSON Storage Schema**: File formats defined and documented
- **BLoC State Management**: Infrastructure created

### 🚧 Framework Ready (Needs Implementation)
- **Storage Operations**: Database abstraction exists but untested
- **File Watching**: Code exists but integration incomplete
- **Error Handling**: Either pattern defined but not consistently used

### ❌ Planned but Not Implemented
- **IExportAdapter Pattern**: Design complete, implementation needed
- **Export Service Integration**: Repository stubs only
- **End-to-End Pipeline**: No connection between import and export
- **Device Discovery**: Framework missing
- **Patient Data Encryption**: Planned for production

## Architecture Benefits (When Complete)

### Projected Advantages
- **Zero Administration**: No database maintenance required
- **Portability**: Complete installation in single directory
- **Transparency**: Direct file inspection possible
- **Reliability**: Append-only operations prevent corruption
- **Performance**: No network latency for core operations
- **Separation of Concerns**: Clear import/export boundaries

### Design Trade-offs
- Single user limitation (intentional)
- Linear file search (acceptable for <10k patients)
- Manual log rotation requirement
- No real-time synchronization between separate adapters

## Implementation Status

### Completed
- ImportAdapter interface and Topcon MYAH implementation
- IExportAdapter interface and AL550 implementation  
- NDJSON storage system
- BLoC state management
- Clean architecture foundation

### Remaining Work
- Additional import adapters (ZEISS, Eye-Office)
- File export adapter
- Patient data encryption
- UI workflow integration

## Extensibility

Architecture supports future enhancements without breaking changes:
- Additional import adapters for new devices
- Additional export adapters for cloud services
- Caching layer implementation
- Multi-user support via file locking
- Optional network synchronization

Extensions implemented only when requirements justify complexity (YAGNI principle).

## Related Documentation

- [Adapter Development](adapter-development.md) - Creating import/export adapters
- [Data Formats](data-formats.md) - JSON schema specifications  
- [Deployment](deployment.md) - Installation and configuration
- [Flutter Implementation](flutter-implementation.md) - UI implementation
