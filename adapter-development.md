# Import/Export Adapter Development

Guide for implementing ImportAdapter and IExportAdapter interfaces to integrate medical devices with DATEYE.

## Overview

DATEYE uses separate adapter interfaces for medical device integration:
- **ImportAdapter**: Import data from medical devices into DATEYE
- **IExportAdapter**: Export data from DATEYE to medical devices/systems

This separation provides clear boundaries, easier testing, and logical organization.

## ImportAdapter Interface

```dart
abstract class ImportAdapter {
  /// Unique adapter identifier
  String get id;

  /// Check if the adapter can parse the given file
  Future<bool> isParsable(String filePath);

  /// Parse into internal format
  Future<ImportedDataFileModel> parse(String filePath);
}
```

### Implementation Pattern

```dart
@Named('your_device')
@Singleton(as: ImportAdapter)
class YourDeviceImportAdapter implements ImportAdapter {
  const YourDeviceImportAdapter(this._dependencies);

  @override
  String get id => 'your_device';

  @override
  Future<bool> isParsable(String filePath) async {
    // Check file format, extension, content
    try {
      final content = await File(filePath).readAsString();
      return content.contains('YOUR_DEVICE_SIGNATURE');
    } catch (e) {
      return false;
    }
  }

  @override
  Future<ImportedDataFileModel> parse(String filePath) async {
    // Parse device-specific format to internal format
    final content = await File(filePath).readAsString();
    final parsed = _parseDeviceFormat(content);
    return ImportedDataFileModel.fromDeviceData(parsed);
  }
}
```

## IExportAdapter Interface

**STATUS**: ❌ NOT YET IMPLEMENTED - Implementation needed

**File**: `lib/infrastructure/adapters/i_export_adapter.dart`

```dart
// NEEDS IMPLEMENTATION - This interface does not exist yet
abstract class IExportAdapter {
  /// Unique identifier for this adapter
  String get id;

  /// Human-readable display name
  String get displayName;

  /// Icon name for UI display (optional)
  String? get iconName => null;

  /// Test if this adapter can connect to the given target
  Future<Either<Failure, bool>> testConnection(ExportDestination target);

  /// Export data to the specified target
  Future<Either<Failure, ExportResult>> export({
    required ExportableDataFile data,
    required ExportDestination target,
  });

  /// Get configuration schema for this adapter
  Map<String, dynamic> get configSchema => {};

  /// Validate configuration for this adapter
  Either<Failure, Unit> validateConfig(Map<String, dynamic> config) {
    return const Right(unit);
  }
}
```

**Implementation Priority**: HIGH - Needed for any export functionality
```

### Implementation Pattern

```dart
@Named('your_export_device')
@Singleton(as: IExportAdapter)
class YourExportAdapter implements IExportAdapter {
  const YourExportAdapter(this._httpClient);

  final IHttpClient _httpClient;

  @override
  String get id => 'your_export_device';

  @override
  String get displayName => 'Your Export Device';

  @override
  String? get iconName => 'device_icon';

  @override
  Map<String, dynamic> get configSchema => {
    'type': 'object',
    'required': ['host', 'port'],
    'properties': {
      'host': {
        'type': 'string',
        'title': 'Device IP Address',
        'pattern': r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$',
      },
      'port': {
        'type': 'integer',
        'title': 'Port',
        'default': 8080,
        'minimum': 1,
        'maximum': 65535,
      },
    },
  };

  @override
  Either<Failure, Unit> validateConfig(Map<String, dynamic> config) {
    final host = config['host'] as String?;
    final port = config['port'] as int?;

    if (host == null || host.isEmpty) {
      return Left(ValidationFailure('Host is required'));
    }

    if (port == null || port <= 0 || port > 65535) {
      return Left(ValidationFailure('Valid port required'));
    }

    return const Right(unit);
  }

  @override
  Future<Either<Failure, bool>> testConnection(ExportTarget target) async {
    try {
      final host = target.config['host'] as String;
      final port = target.config['port'] as int;

      final response = await _httpClient.get(
        'http://$host:$port/status',
        options: HttpRequestOptions(connectTimeout: Duration(seconds: 5)),
      );

      return Right(response.statusCode == 200);
    } catch (e) {
      return Left(NetworkFailure('Connection test failed: $e'));
    }
  }

  @override
  Future<Either<Failure, ExportResult>> export({
    required ExportableDataFile data,
    required ExportTarget target,
  }) async {
    try {
      // Validate configuration
      final validation = validateConfig(target.config);
      if (validation.isLeft()) return Left(validation.getLeft().toNullable()!);

      // Convert data to device format
      final deviceData = _convertToDeviceFormat(data);

      // Send to device
      final response = await _httpClient.post(
        'http://${target.config['host']}:${target.config['port']}/import',
        data: deviceData,
      );

      if (response.statusCode == 200) {
        return const Right(ExportResult.success(
          message: 'Data exported successfully',
        ));
      } else {
        return Left(NetworkFailure('Export failed: ${response.statusCode}'));
      }
    } catch (e) {
      return Left(ExportFailure('Export error: $e'));
    }
  }

  Map<String, dynamic> _convertToDeviceFormat(ExportableDataFile data) {
    // Convert DATEYE format to device-specific format
    return {
      'patients': [], // Extract from data
      'timestamp': DateTime.now().toIso8601String(),
    };
  }
}
```

## Data Models

### ImportedDataFileModel

The internal data structure for imported data:

```dart
@freezed
class ImportedDataFileModel with _$ImportedDataFileModel {
  const factory ImportedDataFileModel({
    required XmlDataPolarExportation xmlDataPolarExportation,
  }) = _ImportedDataFileModel;

  factory ImportedDataFileModel.fromJson(Map<String, dynamic> json) =>
      _$ImportedDataFileModelFromJson(json);
}
```

### ExportableDataFile

The data structure for export operations:

```dart
@freezed
class ExportableDataFile with _$ExportableDataFile {
  const factory ExportableDataFile({
    required DataFile file,
    required ExportDestination destination,
    @Default(0) double progress,
  }) = _ExportableDataFile;
}
```

### ExportTarget and ExportResult

```dart
class ExportTarget {
  const ExportTarget({
    required this.id,
    required this.name,
    required this.adapterId,
    required this.config,
    this.enabled = true,
  });

  final String id;
  final String name;
  final String adapterId;
  final Map<String, dynamic> config;
  final bool enabled;
}

// Result types
abstract class ExportResult {
  const factory ExportResult.success({
    String? message,
    Map<String, dynamic>? metadata,
  }) = ExportSuccess;

  const factory ExportResult.failure({
    required String error,
    String? errorCode,
    bool retryable = true,
  }) = ExportFailure;
}
```

## Example Implementations

### Topcon MYAH Import Adapter

```dart
@Named('topcon_myah')
@Singleton(as: ImportAdapter)
class TopconMyahImportAdapter implements ImportAdapter {
  const TopconMyahImportAdapter(this._parser);

  final IXmlParser _parser;

  @override
  String get id => 'topcon_myah';

  @override
  Future<bool> isParsable(String filePath) async {
    try {
      final xmlString = await getXmlStringFromFilePath(filePath);
      return _parser.isParsable(xmlString);
    } catch (e) {
      return false;
    }
  }

  @override
  Future<ImportedDataFileModel> parse(String filePath) async {
    // Read UTF-16 encoded XML file
    final xmlBytes = await File(filePath).readAsBytes();
    final utf16CodeUnits = xmlBytes.buffer.asUint16List();
    final xmlString = String.fromCharCodes(utf16CodeUnits);

    // Parse XML to JSON
    final jsonData = await _parser.parse(xmlString);

    // Handle single PatientEyeData conversion to list
    if (jsonData['XMLDataPolarExportation']?['PatientEyeData'] is Map) {
      jsonData['XMLDataPolarExportation']['PatientEyeData'] = 
          [jsonData['XMLDataPolarExportation']['PatientEyeData']];
    }

    return ImportedDataFileModel.fromJson(jsonData);
  }

  Future<String> getXmlStringFromFilePath(String filePath) async {
    final xmlBytes = await File(filePath).readAsBytes();
    final utf16CodeUnits = xmlBytes.buffer.asUint16List();
    return String.fromCharCodes(utf16CodeUnits);
  }
}
```

### Mediworks AL550 Export Adapter

**STATUS**: ❌ NOT YET IMPLEMENTED - High priority reference implementation

**File**: `lib/infrastructure/adapters/al550_export_adapter.dart`

```dart
// NEEDS IMPLEMENTATION - This adapter does not exist yet
@Named('al550_export')
@Singleton(as: IExportAdapter)
class AL550ExportAdapter implements IExportAdapter {
  const AL550ExportAdapter(this._httpClient);

  final IHttpClient _httpClient;

  @override
  String get id => 'al550_export';

  @override
  String get displayName => 'Mediworks AL550';

  @override
  Map<String, dynamic> get configSchema => {
    'type': 'object',
    'required': ['host', 'port'],
    'properties': {
      'host': {
        'type': 'string',
        'title': 'Device IP Address',
        'pattern': r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}

## Adapter Registration

```dart
// Automatic registration via Injectable
@module
abstract class AdapterModule {
  @singleton
  Map<String, ImportAdapter> get importAdapters {
    final getIt = GetIt.instance;
    return {
      'topcon_myah': getIt<ImportAdapter>(instanceName: 'topcon_myah'),
      // Add more import adapters here
    };
  }

  @singleton
  Map<String, IExportAdapter> get exportAdapters {
    final getIt = GetIt.instance;
    return {
      'al550_export': getIt<IExportAdapter>(instanceName: 'al550_export'),
      // Add more export adapters here
    };
  }
}
```

## Error Handling

### Import Error Handling

```dart
Future<Either<Failure, ImportResult>> processImport(String filePath) async {
  try {
    final adapter = _getAdapterForFile(filePath);
    if (adapter == null) {
      return Left(ImportFailure('No suitable adapter found'));
    }

    if (!await adapter.isParsable(filePath)) {
      return Left(ImportFailure('File format not supported'));
    }

    final result = await adapter.parse(filePath);
    return Right(ImportResult.success(result));
  } on FileSystemException catch (e) {
    return Left(ImportFailure('File access error: $e'));
  } on FormatException catch (e) {
    return Left(ImportFailure('Invalid file format: $e'));
  } catch (e) {
    return Left(ImportFailure('Unexpected error: $e'));
  }
}
```

### Export Error Handling

```dart
Future<Either<Failure, ExportResult>> processExport(
  ExportableDataFile data,
  ExportTarget target,
) async {
  try {
    final adapter = _getExportAdapter(target.adapterId);
    if (adapter == null) {
      return Left(ExportFailure('Export adapter not found'));
    }

    // Test connection first
    final connectionTest = await adapter.testConnection(target);
    if (connectionTest.isLeft()) {
      return Left(connectionTest.getLeft().toNullable()!);
    }

    if (!connectionTest.getRight().toNullable()!) {
      return Left(NetworkFailure('Cannot connect to target device'));
    }

    // Perform export
    return await adapter.export(data: data, target: target);
  } catch (e) {
    return Left(ExportFailure('Export failed: $e'));
  }
}
```

## Testing Strategies

### Import Adapter Testing

```dart
void main() {
  group('TopconMyahImportAdapter', () {
    late TopconMyahImportAdapter adapter;
    late MockXmlParser mockParser;

    setUp(() {
      mockParser = MockXmlParser();
      adapter = TopconMyahImportAdapter(mockParser);
    });

    test('parses valid MYAH file', () async {
      // Arrange
      const filePath = 'test/data/valid_myah.xml';
      final expectedJson = {'XMLDataPolarExportation': {...}};
      
      when(mockParser.isParsable(any)).thenReturn(true);
      when(mockParser.parse(any)).thenAnswer((_) async => expectedJson);

      // Act
      final result = await adapter.parse(filePath);

      // Assert
      expect(result, isA<ImportedDataFileModel>());
      verify(mockParser.parse(any)).called(1);
    });

    test('rejects invalid file format', () async {
      // Arrange
      const filePath = 'test/data/invalid.txt';
      when(mockParser.isParsable(any)).thenReturn(false);

      // Act
      final canParse = await adapter.isParsable(filePath);

      // Assert
      expect(canParse, false);
    });
  });
}
```

### Export Adapter Testing

```dart
void main() {
  group('AL550ExportAdapter', () {
    late AL550ExportAdapter adapter;
    late MockHttpClient mockHttpClient;

    setUp(() {
      mockHttpClient = MockHttpClient();
      adapter = AL550ExportAdapter(mockHttpClient);
    });

    test('successfully exports patient data', () async {
      // Arrange
      final target = ExportTarget(
        id: 'test',
        name: 'Test AL550',
        adapterId: 'al550_export',
        config: {'host': '192.168.1.100', 'port': 8080},
      );
      
      final data = createTestExportData();
      
      when(mockHttpClient.get(any, options: anyNamed('options')))
          .thenAnswer((_) async => HttpResponse(statusCode: 200, data: []));
      when(mockHttpClient.post(any, data: anyNamed('data')))
          .thenAnswer((_) async => HttpResponse(statusCode: 200, data: 'ok'));

      // Act
      final result = await adapter.export(data: data, target: target);

      // Assert
      expect(result.isRight(), true);
      expect(result.getRight().toNullable()!.isSuccess, true);
    });

    test('handles connection failure', () async {
      // Arrange
      final target = createTestTarget();
      when(mockHttpClient.get(any, options: anyNamed('options')))
          .thenThrow(SocketException('Connection failed'));

      // Act
      final result = await adapter.testConnection(target);

      // Assert
      expect(result.isLeft(), true);
      expect(result.getLeft().toNullable(), isA<NetworkFailure>());
    });
  });
}
```

## Configuration Schema

For export adapters that need configuration:

```dart
@override
Map<String, dynamic> get configSchema => {
  'type': 'object',
  'required': ['host'],
  'properties': {
    'host': {
      'type': 'string',
      'title': 'Device IP Address',
      'description': 'IP address of the device',
      'pattern': r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$',
    },
    'port': {
      'type': 'integer',
      'title': 'Port Number',
      'default': 8080,
      'minimum': 1,
      'maximum': 65535,
    },
    'timeout': {
      'type': 'integer',
      'title': 'Timeout (seconds)',
      'default': 10,
      'minimum': 1,
      'maximum': 60,
    },
    'enableSSL': {
      'type': 'boolean',
      'title': 'Enable SSL',
      'default': false,
    },
  },
};
```

## Implementation Guidelines

### Best Practices

1. **Error Handling**: Always use Either pattern for error handling
2. **Validation**: Validate all input data and configurations
3. **Testing**: Write comprehensive unit tests for all adapters
4. **Documentation**: Document data format requirements and limitations
5. **Dependencies**: Inject all dependencies for testability

### Performance Considerations

1. **File Operations**: Use async file operations
2. **Network Requests**: Implement proper timeouts
3. **Memory Usage**: Stream large files instead of loading entirely
4. **Caching**: Cache parsed data when appropriate

### Security Requirements

1. **Input Validation**: Sanitize all external data
2. **Network Security**: Use HTTPS where possible
3. **Credential Storage**: Never log sensitive information
4. **Error Messages**: Don't expose internal system details

## Related Documentation

- [Architecture](architecture.md) - System design overview
- [Data Formats](data-formats.md) - JSON schema specifications
- [Testing Guide](testing.md) - Testing strategies and patterns
,
      },
      'port': {
        'type': 'integer',
        'title': 'Port',
        'default': 8080,
        'minimum': 1,
        'maximum': 65535,
      },
    },
  };

  @override
  Future<Either<Failure, bool>> testConnection(ExportDestination target) async {
    try {
      final host = target.config['host'] as String;
      final port = target.config['port'] as int;

      final response = await _httpClient.get(
        'http://$host:$port/getPatients',
        options: HttpRequestOptions(connectTimeout: Duration(seconds: 5)),
      );

      return Right(response.statusCode == 200);
    } catch (e) {
      return Left(NetworkFailure('AL550 connection failed: $e'));
    }
  }

  @override
  Future<Either<Failure, ExportResult>> export({
    required ExportableDataFile data,
    required ExportDestination target,
  }) async {
    // Implementation following Mediworks API documentation
    // See: docs/external-apis/mediworks/setPatients-en.md
    
    // TODO: Implement patient registration via HTTP POST
    // TODO: Handle existing patient detection
    // TODO: Format data according to AL550 API requirements
    throw UnimplementedError('AL550 export adapter needs implementation');
  }
}
```

**Implementation Notes**:
- Reference Mediworks API documentation in `/docs/external-apis/mediworks/`
- Use existing IHttpClient from infrastructure layer
- Follow exact same DI pattern as TopconMyahImportAdapter
- Test with actual AL550 device during development

## Adapter Registration

```dart
// Automatic registration via Injectable
@module
abstract class AdapterModule {
  @singleton
  Map<String, ImportAdapter> get importAdapters {
    final getIt = GetIt.instance;
    return {
      'topcon_myah': getIt<ImportAdapter>(instanceName: 'topcon_myah'),
      // Add more import adapters here
    };
  }

  @singleton
  Map<String, IExportAdapter> get exportAdapters {
    final getIt = GetIt.instance;
    return {
      'al550_export': getIt<IExportAdapter>(instanceName: 'al550_export'),
      // Add more export adapters here
    };
  }
}
```

## Error Handling

### Import Error Handling

```dart
Future<Either<Failure, ImportResult>> processImport(String filePath) async {
  try {
    final adapter = _getAdapterForFile(filePath);
    if (adapter == null) {
      return Left(ImportFailure('No suitable adapter found'));
    }

    if (!await adapter.isParsable(filePath)) {
      return Left(ImportFailure('File format not supported'));
    }

    final result = await adapter.parse(filePath);
    return Right(ImportResult.success(result));
  } on FileSystemException catch (e) {
    return Left(ImportFailure('File access error: $e'));
  } on FormatException catch (e) {
    return Left(ImportFailure('Invalid file format: $e'));
  } catch (e) {
    return Left(ImportFailure('Unexpected error: $e'));
  }
}
```

### Export Error Handling

```dart
Future<Either<Failure, ExportResult>> processExport(
  ExportableDataFile data,
  ExportTarget target,
) async {
  try {
    final adapter = _getExportAdapter(target.adapterId);
    if (adapter == null) {
      return Left(ExportFailure('Export adapter not found'));
    }

    // Test connection first
    final connectionTest = await adapter.testConnection(target);
    if (connectionTest.isLeft()) {
      return Left(connectionTest.getLeft().toNullable()!);
    }

    if (!connectionTest.getRight().toNullable()!) {
      return Left(NetworkFailure('Cannot connect to target device'));
    }

    // Perform export
    return await adapter.export(data: data, target: target);
  } catch (e) {
    return Left(ExportFailure('Export failed: $e'));
  }
}
```

## Testing Strategies

### Import Adapter Testing

```dart
void main() {
  group('TopconMyahImportAdapter', () {
    late TopconMyahImportAdapter adapter;
    late MockXmlParser mockParser;

    setUp(() {
      mockParser = MockXmlParser();
      adapter = TopconMyahImportAdapter(mockParser);
    });

    test('parses valid MYAH file', () async {
      // Arrange
      const filePath = 'test/data/valid_myah.xml';
      final expectedJson = {'XMLDataPolarExportation': {...}};
      
      when(mockParser.isParsable(any)).thenReturn(true);
      when(mockParser.parse(any)).thenAnswer((_) async => expectedJson);

      // Act
      final result = await adapter.parse(filePath);

      // Assert
      expect(result, isA<ImportedDataFileModel>());
      verify(mockParser.parse(any)).called(1);
    });

    test('rejects invalid file format', () async {
      // Arrange
      const filePath = 'test/data/invalid.txt';
      when(mockParser.isParsable(any)).thenReturn(false);

      // Act
      final canParse = await adapter.isParsable(filePath);

      // Assert
      expect(canParse, false);
    });
  });
}
```

### Export Adapter Testing

```dart
void main() {
  group('AL550ExportAdapter', () {
    late AL550ExportAdapter adapter;
    late MockHttpClient mockHttpClient;

    setUp(() {
      mockHttpClient = MockHttpClient();
      adapter = AL550ExportAdapter(mockHttpClient);
    });

    test('successfully exports patient data', () async {
      // Arrange
      final target = ExportTarget(
        id: 'test',
        name: 'Test AL550',
        adapterId: 'al550_export',
        config: {'host': '192.168.1.100', 'port': 8080},
      );
      
      final data = createTestExportData();
      
      when(mockHttpClient.get(any, options: anyNamed('options')))
          .thenAnswer((_) async => HttpResponse(statusCode: 200, data: []));
      when(mockHttpClient.post(any, data: anyNamed('data')))
          .thenAnswer((_) async => HttpResponse(statusCode: 200, data: 'ok'));

      // Act
      final result = await adapter.export(data: data, target: target);

      // Assert
      expect(result.isRight(), true);
      expect(result.getRight().toNullable()!.isSuccess, true);
    });

    test('handles connection failure', () async {
      // Arrange
      final target = createTestTarget();
      when(mockHttpClient.get(any, options: anyNamed('options')))
          .thenThrow(SocketException('Connection failed'));

      // Act
      final result = await adapter.testConnection(target);

      // Assert
      expect(result.isLeft(), true);
      expect(result.getLeft().toNullable(), isA<NetworkFailure>());
    });
  });
}
```

## Configuration Schema

For export adapters that need configuration:

```dart
@override
Map<String, dynamic> get configSchema => {
  'type': 'object',
  'required': ['host'],
  'properties': {
    'host': {
      'type': 'string',
      'title': 'Device IP Address',
      'description': 'IP address of the device',
      'pattern': r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$',
    },
    'port': {
      'type': 'integer',
      'title': 'Port Number',
      'default': 8080,
      'minimum': 1,
      'maximum': 65535,
    },
    'timeout': {
      'type': 'integer',
      'title': 'Timeout (seconds)',
      'default': 10,
      'minimum': 1,
      'maximum': 60,
    },
    'enableSSL': {
      'type': 'boolean',
      'title': 'Enable SSL',
      'default': false,
    },
  },
};
```

## Implementation Guidelines

### Best Practices

1. **Error Handling**: Always use Either pattern for error handling
2. **Validation**: Validate all input data and configurations
3. **Testing**: Write comprehensive unit tests for all adapters
4. **Documentation**: Document data format requirements and limitations
5. **Dependencies**: Inject all dependencies for testability

### Performance Considerations

1. **File Operations**: Use async file operations
2. **Network Requests**: Implement proper timeouts
3. **Memory Usage**: Stream large files instead of loading entirely
4. **Caching**: Cache parsed data when appropriate

### Security Requirements

1. **Input Validation**: Sanitize all external data
2. **Network Security**: Use HTTPS where possible
3. **Credential Storage**: Never log sensitive information
4. **Error Messages**: Don't expose internal system details

## Related Documentation

- [Architecture](architecture.md) - System design overview
- [Data Formats](data-formats.md) - JSON schema specifications
- [Testing Guide](testing.md) - Testing strategies and patterns
