# Dependency Injection in DATEYE

Technical implementation of dependency injection using GetIt and Injectable for component lifecycle management.

## Overview

DATEYE implements Dependency Injection (DI) using GetIt as service locator and Injectable for code generation. This architecture ensures testability, modularity, and maintainable component dependencies.

## Dependency Injection Rationale

### Traditional Approach - Limitations
```dart
class TopconAdapter {
  // Hard-coded dependencies
  final parser = XmlParser();        // Untestable
  final logger = FileLogger();       // Cannot disable
  final crypto = AesCrypto();       // Forces encryption in tests
}
```

### DI Approach - Benefits
```dart
@injectable
class TopconAdapter {
  // Constructor injection
  const TopconAdapter(
    this._parser,
    this._logger, 
    this._crypto,
  );
  
  final IXmlParser _parser;    // Mockable interface
  final ILogger _logger;       // Configurable implementation
  final ICrypto _crypto;       // Testable abstraction
}
```

## Service Container Architecture

GetIt provides service location and instance management:

```dart
// Automatic registration via annotations
getIt.registerFactory<IXmlParser>(() => XmlParser());
getIt.registerSingleton<ILogger>(FileLogger());

// Automatic resolution in constructors
final parser = getIt<IXmlParser>();  // Returns configured instance
```

## Annotation System

### @injectable
Registers class for dependency injection:
```dart
@injectable
class PatientService {
  // Registered as PatientService type
}
```

### @Singleton
Ensures single instance throughout application lifecycle:
```dart
@Singleton(as: ILogger)
class FileLogger implements ILogger {
  // Shared instance across all consumers
}
```

### @Named
Differentiates multiple implementations of same interface:
```dart
@Named('topcon_myah')
@Singleton(as: ImportAdapter)
class TopconMyahAdapter implements ImportAdapter {
  // Resolution: getIt<ImportAdapter>(instanceName: 'topcon_myah')
}
```

## Implementation Examples

### Adapter Registration Pattern
```dart
// Self-registering import adapter
@Named('topcon_myah')
@Singleton(as: ImportAdapter)
class TopconMyahImportAdapter implements ImportAdapter {
  const TopconMyahImportAdapter(this._parser);
  final IXmlParser _parser;  // Automatically injected
}

// Alternative implementation
@Named('eye_office')  
@Singleton(as: ImportAdapter)
class EyeOfficeImportAdapter implements ImportAdapter {
  const EyeOfficeImportAdapter(this._jsonParser);
  final IJsonParser _jsonParser;  // Different dependency type
}
```

### Repository Pattern with DI
```dart
// Repository receives all adapters
@injectable
class ImportingRepository {
  final Map<String, ImportAdapter> _adapters;
  
  // GetIt injects all ImportAdapter implementations
  ImportingRepository(this._adapters);
  
  Future<void> importFile(String adapterId, String path) async {
    final adapter = _adapters[adapterId];
    if (adapter == null) throw UnknownAdapterException();
    
    await adapter.parse(path);
  }
}
```

### Testing with Dependency Injection
```dart
// Unit test with mocked dependencies
test('imports valid file', () async {
  // Arrange
  final mockParser = MockXmlParser();
  final adapter = TopconMyahImportAdapter(mockParser);
  
  when(mockParser.parse(any)).thenReturn(testData);
  
  // Act
  final result = await adapter.parse('test.xml');
  
  // Assert
  expect(result, isNotNull);
  verify(mockParser.parse('test.xml')).called(1);
});
```

## Implementation Guidelines

### Recommended Practices
- Use interface abstractions for all dependencies
- Apply @Named annotation for adapter identification
- Use @Singleton for stateless service components
- Maintain simple constructors - dependency storage only

### Anti-patterns to Avoid
- Direct GetIt usage in business logic
- Manual instantiation of classes with dependencies
- Mutable state in singleton instances
- Missing build_runner execution after changes

## Code Generation Configuration

Dependency injection requires build-time code generation:

```bash
# Single build execution
dart run build_runner build

# Continuous build during development  
dart run build_runner watch

# Clean and rebuild
dart run build_runner build --delete-conflicting-outputs
```

## Common Issues and Solutions

### Resolution Failures

**Issue**: "GetIt: Object not found"
- Verify @injectable annotation present
- Execute build_runner
- Confirm registration name matches

**Issue**: "Cannot inject abstract class"
- Register concrete implementation: `@Singleton(as: ILogger)`
- Ensure implementation class exists

**Issue**: "Circular dependency detected"
- Refactor to eliminate circular references
- Consider lazy injection pattern
- Review architectural dependencies

## Architecture Benefits

1. **Testability**: Isolated component testing with mocks
2. **Flexibility**: Simple addition of new implementations
3. **Maintainability**: Explicit dependency declaration
4. **Consistency**: Standardized dependency management

## Related Documentation

- [Adapter Development](../adapter-development.md) - Creating adapters with DI
- [Architecture](../architecture.md) - System design overview
- [Testing Guide](../testing.md) - Mock injection strategies