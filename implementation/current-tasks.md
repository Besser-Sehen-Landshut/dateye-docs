# DATEYE Development Tasks

**Status**: Import complete, Export missing, Transformation broken

## Code Reality Check

### Working
- ✅ `i_import_adapter.dart` - Interface exists
- ✅ `topcon_myah_import_adapter.dart` - Parses XML correctly
- ✅ Core entities and models - Freezed models ready
- ✅ Storage structure - NDJSON implementation

### Broken/Missing
- ❌ `injection.config.dart` - Not generated
- ❌ `i_export_adapter.dart` - Does not exist
- ❌ `al550_export_adapter.dart` - Does not exist  
- ❌ `adapter_module.dart` - Does not exist
- ❌ `exporting_datasource.dart` - All methods throw `UnimplementedError()`
- ❌ Data transformation - ImportAdapter doesn't convert to DATEYE format

## Priority Tasks (Order Matters!)

### Task 1: Generate Dependency Injection (5 min)
```bash
cd /Users/culfin/Documents/Projekte/Dateye/repository
dart run build_runner build --delete-conflicting-outputs
```
**Verify**: `lib/injection.config.dart` exists

### Task 2: Create Export Interface (10 min)
Create `/repository/lib/infrastructure/adapters/i_export_adapter.dart`:
```dart
import 'package:dateye/core/entities/export/export_destination.dart';
import 'package:dateye/core/entities/export/exportable_data_file.dart';
import 'package:dateye/core/errors/failures.dart';
import 'package:fpdart/fpdart.dart';

abstract class IExportAdapter {
  String get id;
  String get displayName;
  
  Future<Either<Failure, bool>> testConnection(ExportDestination destination);
  Future<Either<Failure, Unit>> export({
    required ExportableDataFile data,
    required ExportDestination destination,
  });
}
```

### Task 3: Create AL550 Adapter (30 min)
Create `/repository/lib/infrastructure/adapters/al550_export_adapter.dart`:
```dart
import 'package:injectable/injectable.dart';
import 'package:dio/dio.dart';
// Copy full implementation from docs/adapters/mediworks-al550.md

@Named('al550_export')  
@Singleton(as: IExportAdapter)
class AL550ExportAdapter implements IExportAdapter {
  // CRITICAL: AL550 only registers patients, NOT measurements!
}
```

### Task 4: Wire Adapters (15 min)
Create `/repository/lib/infrastructure/adapters/adapter_module.dart`:
```dart
@module
abstract class AdapterModule {
  @singleton
  Map<String, ImportAdapter> get importAdapters => {
    'topcon_myah': GetIt.I<ImportAdapter>(instanceName: 'topcon_myah'),
  };
  
  @singleton
  Map<String, IExportAdapter> get exportAdapters => {
    'al550_export': GetIt.I<IExportAdapter>(instanceName: 'al550_export'),
  };
}
```

### Task 5: Fix ExportingDatasource (20 min)
Edit `/repository/lib/infrastructure/datasources/exporting_datasource.dart`:

1. Uncomment constructor
2. Add export adapters injection:
```dart
final Map<String, IExportAdapter> _exportAdapters;
```
3. Replace `UnimplementedError()` in `exportToTarget`:
```dart
final adapter = _exportAdapters[data.destination.adapterId];
if (adapter == null) return Left(ExportFailure('Adapter not found'));
return adapter.export(data: data, destination: data.destination);
```

### Task 6: Add Data Transformation (CRITICAL!)
Edit `/repository/lib/infrastructure/adapters/topcon_myah_import_adapter.dart`:

Add after parse method:
```dart
// In ImportService or wherever data is processed
Future<List<Measurement>> processImportedData(ImportedDataFileModel data) {
  // Transform XML structure to DATEYE measurements
  // See architecture.md "Data Transformation Pattern" section
}
```

## File Locations

```
repository/
├── lib/
│   ├── infrastructure/
│   │   ├── adapters/
│   │   │   ├── i_import_adapter.dart      ✅
│   │   │   ├── i_export_adapter.dart      ❌ CREATE (Task 2)
│   │   │   ├── topcon_myah_import_adapter.dart ✅ (needs Task 6)
│   │   │   ├── al550_export_adapter.dart  ❌ CREATE (Task 3)
│   │   │   └── adapter_module.dart        ❌ CREATE (Task 4)
│   │   └── datasources/
│   │       └── exporting_datasource.dart  ❌ FIX (Task 5)
│   └── injection.config.dart              ❌ GENERATE (Task 1)
```

## Testing After Each Task

### After Task 1 (build_runner):
```bash
flutter analyze
# Should show no "injection.config.dart not found" errors
```

### After Task 3 (AL550):
```dart
// Test connection
final adapter = AL550ExportAdapter(dio);
final result = await adapter.testConnection(destination);
// Should return Right(true) or Left(NetworkFailure)
```

### After Task 5 (ExportingDatasource):
```bash
flutter test test/infrastructure/datasources/exporting_datasource_test.dart
```

## Common Pitfalls

1. **Wrong annotation name**: `@Named('al550_export')` must match exactly
2. **Missing imports**: Check all imports after creating new files
3. **Build runner**: Must run after ANY @injectable changes
4. **Dio not injected**: Add Dio to injection configuration
5. **Export only patients**: AL550 can't receive measurements!

## Next Features (After Above Complete)

### Feature 1: File Export Adapter (2 hours)

**Purpose**: Export patient data to JSON/CSV files for backup or external analysis.

#### Step 1: Create File Export Adapter
Create `/repository/lib/infrastructure/adapters/file_export_adapter.dart`:
```dart
import 'dart:io';
import 'dart:convert';
import 'package:csv/csv.dart';
import 'package:injectable/injectable.dart';
import 'package:path/path.dart' as p;

@Named('file_export')  
@Singleton(as: IExportAdapter)
class FileExportAdapter implements IExportAdapter {
  @override
  String get id => 'file_export';
  
  @override
  String get displayName => 'File Export (JSON/CSV)';
  
  @override
  Future<Either<Failure, bool>> testConnection(ExportDestination destination) async {
    try {
      final path = destination.config['output_path'] as String;
      final dir = Directory(path);
      return Right(await dir.exists());
    } catch (e) {
      return Left(FileSystemFailure('Invalid path: $e'));
    }
  }
  
  @override
  Future<Either<Failure, Unit>> export({
    required ExportableDataFile data,
    required ExportDestination destination,
  }) async {
    try {
      final format = destination.config['format'] as String; // 'json' or 'csv'
      final path = destination.config['output_path'] as String;
      final includePersonal = destination.config['include_personal'] ?? false;
      
      final filename = '${data.file.secretPid}_${DateTime.now().millisecondsSinceEpoch}';
      
      if (format == 'json') {
        await _exportJson(data, '$path/$filename.json', includePersonal);
      } else {
        await _exportCsv(data, '$path/$filename.csv');
      }
      
      return Right(unit);
    } catch (e) {
      return Left(ExportFailure('File export failed: $e'));
    }
  }
  
  Future<void> _exportJson(ExportableDataFile data, String filePath, bool includePersonal) async {
    final json = {
      'export_date': DateTime.now().toIso8601String(),
      'patient_id': data.file.secretPid,
      if (includePersonal) 'patient': data.file.patientData,
      'measurements': data.file.measurements.map((m) => m.toJson()).toList(),
    };
    
    await File(filePath).writeAsString(jsonEncode(json));
  }
  
  Future<void> _exportCsv(ExportableDataFile data, String filePath) async {
    // CSV: One row per measurement
    final rows = <List<dynamic>>[
      ['Date', 'Type', 'Eye', 'Value', 'Unit'],
    ];
    
    for (final measurement in data.file.measurements) {
      if (measurement.type == 'axial_length') {
        rows.add([
          measurement.data['measured_at'],
          'Axial Length',
          measurement.data['eye'],
          measurement.data['value'],
          'mm'
        ]);
      }
      // Add more measurement types as needed
    }
    
    final csv = const ListToCsvConverter().convert(rows);
    await File(filePath).writeAsString(csv);
  }
}
```

#### Step 2: Add to adapter_module.dart
```dart
'file_export': GetIt.I<IExportAdapter>(instanceName: 'file_export'),
```

#### Step 3: Add CSV dependency
In `pubspec.yaml`:
```yaml
dependencies:
  csv: ^5.0.0
```

### Feature 2: Myopia.cloud Adapter (3 hours)

**Purpose**: Upload anonymized data to myopia.cloud for population analytics.

#### Step 1: Create Myopia Cloud Adapter
Create `/repository/lib/infrastructure/adapters/myopia_cloud_adapter.dart`:
```dart
@Named('myopia_cloud')  
@Singleton(as: IExportAdapter)
class MyopiaCloudAdapter implements IExportAdapter {
  const MyopiaCloudAdapter(this._dio);
  
  final Dio _dio;
  
  @override
  String get id => 'myopia_cloud';
  
  @override
  String get displayName => 'Myopia.cloud Analytics';
  
  @override
  Future<Either<Failure, bool>> testConnection(ExportDestination destination) async {
    try {
      final response = await _dio.get(
        '${destination.config['api_url']}/health',
        options: Options(
          headers: {'X-API-Key': destination.config['api_key']},
          connectTimeout: const Duration(seconds: 5),
        ),
      );
      return Right(response.statusCode == 200);
    } catch (e) {
      return Left(NetworkFailure('Connection failed: $e'));
    }
  }
  
  @override
  Future<Either<Failure, Unit>> export({
    required ExportableDataFile data,
    required ExportDestination destination,
  }) async {
    try {
      // Anonymize data - NO personal information
      final payload = {
        'study_id': destination.config['study_id'],
        'site_id': destination.config['site_id'],
        'upload_date': DateTime.now().toIso8601String(),
        'measurements': _anonymizeMeasurements(data),
      };
      
      final response = await _dio.post(
        '${destination.config['api_url']}/measurements',
        data: payload,
        options: Options(
          headers: {
            'X-API-Key': destination.config['api_key'],
            'Content-Type': 'application/json',
          },
        ),
      );
      
      if (response.statusCode == 201) {
        return Right(unit);
      } else {
        return Left(NetworkFailure('Upload failed: ${response.statusCode}'));
      }
    } catch (e) {
      return Left(ExportFailure('Cloud export failed: $e'));
    }
  }
  
  List<Map<String, dynamic>> _anonymizeMeasurements(ExportableDataFile data) {
    // Extract age from birth date (if available)
    final birthDate = data.file.patientData?['birth_date'];
    final ageYears = birthDate != null 
      ? DateTime.now().difference(DateTime.parse(birthDate)).inDays ~/ 365
      : null;
    
    return data.file.measurements.map((m) => {
      'type': m.type,
      'data': {
        ...m.data,
        // Replace any personal data
        if (ageYears != null) 'age_years': ageYears,
      },
      // Remove any identifying fields
    }).toList();
  }
}
```

#### Step 2: Configuration UI needs
- API URL (default: https://api.myopia.cloud)
- API Key (encrypted storage)
- Study ID
- Site ID

### Feature 3: Patient Encryption (4 hours)

**Purpose**: Encrypt patient identities while keeping measurements searchable.

#### Step 1: Create Encryption Service
Create `/repository/lib/infrastructure/services/encryption_service.dart`:
```dart
import 'package:encrypt/encrypt.dart';
import 'package:injectable/injectable.dart';

@singleton
class EncryptionService {
  static const _keyFileName = 'identity.key';
  late final Encrypter _encrypter;
  late final Key _key;
  late final IV _iv;
  
  Future<void> initialize() async {
    _key = await _loadOrGenerateKey();
    _iv = IV.fromSecureRandom(16);
    _encrypter = Encrypter(AES(_key));
  }
  
  String encryptPatient(Map<String, dynamic> patientData) {
    final plainText = jsonEncode(patientData);
    final encrypted = _encrypter.encrypt(plainText, iv: _iv);
    return encrypted.base64;
  }
  
  Map<String, dynamic> decryptPatient(String encryptedData) {
    final encrypted = Encrypted.fromBase64(encryptedData);
    final decrypted = _encrypter.decrypt(encrypted, iv: _iv);
    return jsonDecode(decrypted) as Map<String, dynamic>;
  }
  
  Future<Key> _loadOrGenerateKey() async {
    final appDir = await getApplicationSupportDirectory();
    final keyFile = File('${appDir.path}/secure/$_keyFileName');
    
    if (await keyFile.exists()) {
      final keyBase64 = await keyFile.readAsString();
      return Key.fromBase64(keyBase64);
    }
    
    // Generate new key
    final key = Key.fromSecureRandom(32); // 256-bit
    await keyFile.create(recursive: true);
    await keyFile.writeAsString(key.base64);
    
    // Show backup dialog (implement in UI)
    _notifyKeyCreated(key.base64);
    
    return key;
  }
}
```

#### Step 2: Modify Storage Layer
Edit `/repository/lib/infrastructure/datasources/logging_datasource.dart`:
```dart
// Add encryption service
final EncryptionService _encryptionService;

// When saving patient data
Future<void> savePatientWithEncryption(Event event) async {
  // Extract patient data
  final patientData = event.patientData;
  if (patientData != null) {
    // Encrypt and store separately
    final encryptedData = _encryptionService.encryptPatient(patientData);
    await _saveToPatientFile(event.secretPid, encryptedData);
    
    // Save event without patient data
    final sanitizedEvent = event.copyWith(patientData: null);
    await _database.insert(sanitizedEvent);
  }
}
```

#### Step 3: Add dependency
```yaml
dependencies:
  encrypt: ^5.0.0
```

### Feature 4: UI Workflow Screens (6 hours)

**Purpose**: User-friendly screens for configuring import sources and export destinations.

#### Step 1: Import Source List Screen
Create `/repository/lib/presentation/pages/import_sources/import_sources_page.dart`:
```dart
class ImportSourcesPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Import Sources')),
      body: BlocBuilder<ImportSourcesCubit, ImportSourcesState>(
        builder: (context, state) {
          return ListView.builder(
            itemCount: state.sources.length,
            itemBuilder: (context, index) {
              final source = state.sources[index];
              return ListTile(
                leading: Icon(_getIconForAdapter(source.adapterId)),
                title: Text(source.name),
                subtitle: Text(source.config['path'] ?? 'API'),
                trailing: Switch(
                  value: source.enabled,
                  onChanged: (enabled) => context
                    .read<ImportSourcesCubit>()
                    .toggleSource(source.id, enabled),
                ),
                onTap: () => _editSource(context, source),
              );
            },
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _addSource(context),
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

#### Step 2: Add Source Dialog
Create `/repository/lib/presentation/dialogs/add_import_source_dialog.dart`:
```dart
class AddImportSourceDialog extends StatefulWidget {
  @override
  _AddImportSourceDialogState createState() => _AddImportSourceDialogState();
}

class _AddImportSourceDialogState extends State<AddImportSourceDialog> {
  String? _selectedAdapter;
  final _formKey = GlobalKey<FormState>();
  final _config = <String, dynamic>{};
  
  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('Add Import Source'),
      content: Form(
        key: _formKey,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            // Adapter selection
            DropdownButtonFormField<String>(
              value: _selectedAdapter,
              items: [
                DropdownMenuItem(value: 'topcon_myah', child: Text('Topcon MYAH')),
                DropdownMenuItem(value: 'eye_office', child: Text('Eye-Office API')),
              ],
              onChanged: (adapter) => setState(() => _selectedAdapter = adapter),
              decoration: const InputDecoration(labelText: 'Device Type'),
            ),
            
            // Dynamic config based on adapter
            if (_selectedAdapter == 'topcon_myah') ...[
              TextFormField(
                decoration: const InputDecoration(labelText: 'Watch Folder'),
                onSaved: (value) => _config['path'] = value,
                validator: (value) => value?.isEmpty ?? true ? 'Required' : null,
              ),
              CheckboxListTile(
                title: const Text('Delete after import'),
                value: _config['delete_after_import'] ?? false,
                onChanged: (value) => setState(() => _config['delete_after_import'] = value),
              ),
            ],
          ],
        ),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.of(context).pop(),
          child: const Text('Cancel'),
        ),
        ElevatedButton(
          onPressed: _save,
          child: const Text('Add'),
        ),
      ],
    );
  }
  
  void _save() {
    if (_formKey.currentState!.validate()) {
      _formKey.currentState!.save();
      
      final source = ImportingDevice(
        id: const Uuid().v4(),
        adapterId: _selectedAdapter!,
        name: _config['name'] ?? _getDefaultName(),
        config: _config,
        enabled: true,
        created: DateTime.now(),
      );
      
      context.read<ImportSourcesCubit>().addSource(source);
      Navigator.of(context).pop();
    }
  }
}
```

#### Step 3: Export Destinations (Similar pattern)
- Copy pattern from import sources
- Add configuration for each export adapter type
- Include "Test Connection" button

#### Step 4: Connection Overview Screen
Create `/repository/lib/presentation/pages/connections/connections_page.dart`:
```dart
class ConnectionsPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 3,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Connections'),
          bottom: const TabBar(
            tabs: [
              Tab(text: 'Active'),
              Tab(text: 'Import Sources'),
              Tab(text: 'Export Targets'),
            ],
          ),
        ),
        body: TabBarView(
          children: [
            _ActiveConnectionsTab(),
            _ImportSourcesTab(),
            _ExportTargetsTab(),
          ],
        ),
      ),
    );
  }
}
```

## Implementation Order & Time Estimates

1. **Core Export (Tasks 1-6)**: 2 hours ⬅️ DO THIS FIRST!
2. **File Export**: 2 hours
3. **Myopia.cloud**: 3 hours  
4. **Encryption**: 4 hours
5. **UI Screens**: 6 hours

**Total**: ~17 hours for complete system

## Testing Each Feature

### File Export Test
```bash
# Create test export
final adapter = FileExportAdapter();
final result = await adapter.export(
  data: testData,
  destination: ExportDestination(
    adapterId: 'file_export',
    config: {'format': 'json', 'output_path': '/tmp/dateye'},
  ),
);
# Check /tmp/dateye/ for output file
```

### Myopia.cloud Test
```bash
# Use test endpoint
config: {
  'api_url': 'https://sandbox.myopia.cloud',
  'api_key': 'test_key_123',
}
```

### Encryption Test
```dart
// Verify round-trip
final original = {'name': 'Test Patient'};
final encrypted = service.encryptPatient(original);
final decrypted = service.decryptPatient(encrypted);
assert(decrypted['name'] == original['name']);
```