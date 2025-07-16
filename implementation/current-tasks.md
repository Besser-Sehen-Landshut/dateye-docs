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

### Feature 2: Myopia.cloud Adapter (3 hours)

**Purpose**: Upload anonymized data to myopia.cloud for population analytics.

### Feature 3: Patient Encryption (4 hours)

**Purpose**: Encrypt patient identities while keeping measurements searchable.

### Feature 4: UI Workflow Screens (6 hours)

**Purpose**: User-friendly screens for configuring import sources and export destinations.

## Implementation Order & Time Estimates

1. **Core Export (Tasks 1-6)**: 2 hours ⬅️ DO THIS FIRST!
2. **File Export**: 2 hours
3. **Myopia.cloud**: 3 hours  
4. **Encryption**: 4 hours
5. **UI Screens**: 6 hours

**Total**: ~17 hours for complete system