# DATEYE Project Structure

Clean Architecture implementation for maintainable medical software development.

## Overview

DATEYE implements Clean Architecture principles with clear separation of concerns across three distinct layers:

```
┌─────────────────────────────────────────┐
│         Presentation Layer              │  Flutter UI
│         (UI & State Management)         │
├─────────────────────────────────────────┤
│         Infrastructure Layer            │  Technical Implementation
│         (Adapters & Data Access)        │
├─────────────────────────────────────────┤
│            Core Layer                   │  Business Logic
│         (Entities & Use Cases)          │
└─────────────────────────────────────────┘
```

## Dependency Rule

The fundamental architectural rule: **Dependencies only point inward**

- Presentation → Infrastructure → Core (Allowed)
- Core → Infrastructure (Prohibited)
- Infrastructure → Presentation (Prohibited)

## Layer Specifications

### Core Layer (`lib/core/`)

Pure business logic with zero external dependencies.

```
core/
├── entities/           # Business objects
│   ├── exam/          # Examination data models
│   ├── import/        # Import-related entities
│   └── export/        # Export-related entities
├── repositories/      # Repository interfaces (contracts)
│   ├── i_importing_repository.dart
│   └── i_exporting_repository.dart
├── usecases/          # Business rules/operations
│   ├── import/        # Import operations
│   ├── export/        # Export operations
│   └── settings/      # Settings management
└── errors/            # Domain-specific errors
```

**Entity Example:**
```dart
// core/entities/exam/axial_length.dart
@freezed
class AxialLength with _$AxialLength {
  const factory AxialLength({
    required String eye,
    required double value,
  }) = _AxialLength;
}
```

**Use Case Example:**
```dart
// core/usecases/import/import_file.dart
@injectable
class ImportFile {
  final IImportingRepository _repository;
  
  const ImportFile(this._repository);
  
  Future<Either<Failure, ImportResult>> call(String filePath) async {
    // Pure business logic - no UI, no file access
    return _repository.importFile(filePath);
  }
}
```

### Infrastructure Layer (`lib/infrastructure/`)

Technical implementation details and external system integration.

```
infrastructure/
├── adapters/          # Device adapters (Topcon, etc.)
│   ├── topcon_myah_import_adapter.dart
│   └── i_import_adapter.dart
├── datasources/       # Data access (files, network)
│   ├── logging_datasource.dart
│   └── importing_datasource.dart
├── repositories/      # Repository implementations
│   ├── importing_repository.dart
│   └── exporting_repository.dart
├── models/            # Data transfer objects
│   └── import/
│       └── imported_data_file_model.dart
└── storage/           # File/database access
    └── database/
        └── json_file_storage_database.dart
```

**Repository Implementation Example:**
```dart
// infrastructure/repositories/importing_repository.dart
@Injectable(as: IImportingRepository)
class ImportingRepository implements IImportingRepository {
  final IDatabase _database;
  final Map<String, ImportAdapter> _adapters;
  
  const ImportingRepository(this._database, this._adapters);
  
  @override
  Future<Either<Failure, ImportResult>> importFile(String path) async {
    // Technical implementation using adapters and database
  }
}
```

### Presentation Layer (`lib/presentation/`)

Flutter-specific UI implementation.

```
presentation/
├── bloc/              # State management
│   ├── import/        # Import-related cubits
│   ├── export/        # Export-related cubits
│   └── dashboard/     # Dashboard state
├── pages/             # Screen widgets
│   ├── dashboard/
│   ├── import_settings/
│   └── export_settings/
├── widgets/           # Reusable UI components
│   ├── common/
│   └── dialogs/
└── theme/             # App theming
```

**Page with BLoC Example:**
```dart
// presentation/pages/dashboard/dashboard_page.dart
class DashboardPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocBuilder<DashboardCubit, DashboardState>(
      builder: (context, state) {
        // Pure UI code - no business logic
        return Scaffold(
          body: EventList(events: state.recentEvents),
        );
      },
    );
  }
}
```

## File Organization Patterns

### Feature-First Organization

Code organized by feature within each layer:

```
usecases/
├── import/
│   ├── import_file.dart
│   ├── validate_import.dart
│   └── get_import_history.dart
├── export/
│   ├── export_data.dart
│   └── retry_failed_export.dart
└── settings/
    ├── update_language.dart
    └── toggle_auto_import.dart
```

### Naming Conventions

- **Interfaces**: Prefix with `I` (e.g., `IImportAdapter`)
- **Implementations**: No prefix (e.g., `ImportingRepository`)
- **Models**: Suffix with `Model` (e.g., `ImportedDataFileModel`)
- **Use Cases**: Verb phrases (e.g., `ImportFile`, `GetPatientData`)

## Dependency Injection Structure

```
injection.dart         # DI configuration
├── @injectableInit   # Auto-generated initialization
└── GetIt instance    # Service locator
```

## Architectural Benefits

### 1. Testability
Independent layer testing:
```dart
// Test use case without UI or file system
test('ImportFile validates file path', () {
  final mockRepo = MockImportingRepository();
  final useCase = ImportFile(mockRepo);
  // Test pure business logic
});
```

### 2. Maintainability
- Rapid code location by feature and layer
- Isolated change impact
- Clear architectural boundaries

### 3. Scalability
- Feature addition without existing code modification
- Parallel development capability
- Simplified onboarding process

### 4. Flexibility
- UI framework replacement capability
- Storage mechanism changes
- Preserved business logic

## Common Implementation Patterns

### Repository Pattern
```dart
// Core defines interface
abstract class IPatientRepository {
  Future<Patient> getPatient(String id);
}

// Infrastructure implements
class PatientRepository implements IPatientRepository {
  @override
  Future<Patient> getPatient(String id) {
    // Implementation details
  }
}
```

### Use Case Pattern
```dart
// Single responsibility - one operation
class GetPatientMeasurements {
  Future<List<Measurement>> call(String patientId) {
    // Business logic only
  }
}
```

### Error Handling Flow
```dart
// Error propagation through layers
Infrastructure Error → Domain Failure → UI Error Message
```

## Implementation Guidelines

### Recommended Practices
- Maintain layer independence
- Utilize dependency injection
- Test layers independently
- Follow naming conventions
- One class per file

### Practices to Avoid
- UI imports in Core layer
- Business logic in UI components
- Direct layer bypassing (UI → Database)
- Mixed concerns in single class

## Related Documentation

- [Architecture](../architecture.md) - System design overview
- [Dependency Injection](dependency-injection.md) - DI implementation
- [State Management](state-management.md) - BLoC pattern
- [Testing Guide](../testing.md) - Layer testing strategies