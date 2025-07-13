# State Management in DATEYE

Implementation of reactive state management using BLoC pattern for UI synchronization and data flow.

## Overview

DATEYE implements the BLoC (Business Logic Component) pattern for state management, providing:
- **Reactive UI Updates**: Automatic synchronization with data changes
- **Separation of Concerns**: Business logic isolation from presentation
- **Predictable State**: Testable and debuggable state transitions

## State Architecture

### Dual-Layer State System

**1. Persistent State (File System)**
```
log.ndjson             → Event history
importingDevice.ndjson → Device configurations  
appConfigs.ndjson      → Application settings
```

**2. UI State (Memory)**
```dart
class DashboardState {
  final List<RecentEvent> recentEvents;  // Recent activity
  final ImportProgress? activeImport;     // Current operation
  final bool isLoading;                   // Loading indicator
  final String? error;                    // Error state
}
```

### Data Flow Architecture

```
File Changes → File Watcher → Cubit → State → UI Updates
     ↓                           ↑
User Action ──────────────────────┘
```

## BLoC Pattern Implementation

### Cubit Architecture

Cubit provides simplified state management:

```dart
class ImporterListenerCubit extends Cubit<ImporterListenerState> {
  ImporterListenerCubit() : super(ImporterListenerState.initial());
  
  // State transition method
  void startImport(String filePath) {
    emit(state.copyWith(isImporting: true));
    // Import processing
    emit(state.copyWith(isImporting: false));
  }
}
```

### Immutable State Principle

State objects are immutable and replaced atomically:

```dart
// Incorrect - Direct state mutation
state.devices.add(newDevice);

// Correct - State replacement
emit(state.copyWith(
  devices: [...state.devices, newDevice],
));
```

## Implementation Examples

### Real-time Dashboard Updates

```dart
// File system monitoring integration
class DashboardCubit extends Cubit<DashboardState> {
  StreamSubscription? _eventWatcher;
  
  void startWatching() {
    _eventWatcher = _database.watchAll<LogEntry>().listen((events) {
      // Automatic UI synchronization
      emit(state.copyWith(recentEvents: events));
    });
  }
}

// Reactive UI component
BlocBuilder<DashboardCubit, DashboardState>(
  builder: (context, state) {
    return EventList(events: state.recentEvents);
  },
)
```

### Progress Tracking Implementation

```dart
// Progress state model
class ImportState {
  final String? currentFile;
  final int processedCount;
  final int totalCount;
  double get progress => processedCount / totalCount;
}

// UI progress indicator
LinearProgressIndicator(value: state.progress)
```

### Error State Management

```dart
// Error handling in Cubit
Future<void> importFile(String path) async {
  try {
    emit(state.copyWith(isLoading: true, error: null));
    await _importService.import(path);
    emit(state.copyWith(isLoading: false, success: true));
  } catch (e) {
    emit(state.copyWith(
      isLoading: false,
      error: 'Import operation failed: ${e.toString()}',
    ));
  }
}

// Error presentation in UI
if (state.error != null) {
  ScaffoldMessenger.of(context).showSnackBar(
    SnackBar(content: Text(state.error!)),
  );
}
```

## File System Integration

Reactive file monitoring with BLoC:

```dart
// Database stream provider
Stream<List<LogEntry>> watchLogs() {
  return _database.watchAll<LogEntry>(
    adapter: LogEntryAdapter(),
    limit: 50,
  );
}

// Cubit subscription management
class LogViewerCubit extends Cubit<LogViewerState> {
  void initialize() {
    _database.watchLogs().listen((logs) {
      emit(state.copyWith(logs: logs));
    });
  }
}
```

## Testing Strategies

### Unit Testing Cubits

```dart
test('import operation updates state correctly', () async {
  // Arrange
  final cubit = ImportCubit(mockImportService);
  
  // Act
  await cubit.importFile('test.xml');
  
  // Assert
  expect(cubit.state.isLoading, false);
  expect(cubit.state.success, true);
});
```

### BLoC Test Package Integration

```dart
blocTest<ImportCubit, ImportState>(
  'emits loading followed by success state',
  build: () => ImportCubit(mockService),
  act: (cubit) => cubit.importFile('test.xml'),
  expect: () => [
    ImportState(isLoading: true),
    ImportState(isLoading: false, success: true),
  ],
);
```

## Implementation Guidelines

### Recommended Practices
- Maintain state immutability using Freezed
- Use descriptive state class names
- Implement comprehensive state coverage (loading, success, error)
- Properly dispose StreamSubscriptions in close()

### Anti-patterns
- Business logic in UI components
- Direct state mutation
- Missing error state handling
- Storing sensitive data in UI state

## Project Organization

```
presentation/
  bloc/
    dashboard/
      dashboard_cubit.dart      # State management logic
      dashboard_state.dart      # State model definition
    import/
      import_cubit.dart
      import_state.dart
    export/
      export_cubit.dart
      export_state.dart
```

## Medical Application Benefits

1. **Real-time Monitoring**: Live import/export status
2. **Progress Visualization**: Operation progress tracking
3. **Error Transparency**: Clear error state presentation
4. **Data Consistency**: Synchronized multi-screen state
5. **Professional Interface**: Responsive user experience

## Related Documentation

- [Architecture](../architecture.md) - System design overview
- [Flutter Implementation](../flutter-implementation.md) - UI implementation patterns
- [Data Formats](../data-formats.md) - Persistent state specifications