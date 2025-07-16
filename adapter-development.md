# Import/Export Adapter Development

Guide for implementing ImportAdapter and IExportAdapter interfaces to integrate medical devices with DATEYE.

## Overview

DATEYE uses separate adapter interfaces:
- **ImportAdapter**: Import data from medical devices into DATEYE
- **IExportAdapter**: Export data from DATEYE to medical devices/systems

## ImportAdapter Interface

```dart
abstract class ImportAdapter {
  String get id;
  Future<bool> isParsable(String filePath);
  Future<ImportedDataFileModel> parse(String filePath);
}
```

**Implementation Status**: ✅ Complete (Topcon MYAH reference implementation exists)

## IExportAdapter Interface

**STATUS**: ❌ NOT YET IMPLEMENTED - Critical priority

```dart
abstract class IExportAdapter {
  String get id;
  String get displayName;
  String? get iconName => null;
  
  Future<Either<Failure, bool>> testConnection(ExportTarget target);
  Future<Either<Failure, ExportResult>> export({
    required ExportableDataFile data,
    required ExportTarget target,
  });
  
  Map<String, dynamic> get configSchema => {};
  Either<Failure, Unit> validateConfig(Map<String, dynamic> config);
}
```

## Implementation Examples

### Topcon MYAH Import Adapter (Working Reference)

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
}
```

### AL550 Export Adapter (Needs Implementation)

```dart
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
  Future<Either<Failure, bool>> testConnection(ExportTarget target) async {
    try {
      final response = await _httpClient.get(
        'http://${target.config['host']}:${target.config['port']}/getPatients',
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
    required ExportTarget target,
  }) async {
    // TODO: Implement patient registration via HTTP POST
    // See: docs/external-apis/mediworks/setPatients-en.md
    throw UnimplementedError('AL550 export adapter needs implementation');
  }
}
```

## Adapter Registration

```dart
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

## Configuration Schema

Export adapters define their configuration requirements:

```dart
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
```

## Error Handling

Always use Either pattern:

```dart
Future<Either<Failure, ImportResult>> processImport(String filePath) async {
  try {
    final adapter = _getAdapterForFile(filePath);
    if (adapter == null) {
      return Left(ImportFailure('No suitable adapter found'));
    }
    final result = await adapter.parse(filePath);
    return Right(ImportResult.success(result));
  } catch (e) {
    return Left(ImportFailure('Import failed: $e'));
  }
}
```

## Testing Example

```dart
test('parses valid MYAH file', () async {
  final mockParser = MockXmlParser();
  final adapter = TopconMyahImportAdapter(mockParser);
  
  when(mockParser.isParsable(any)).thenReturn(true);
  when(mockParser.parse(any)).thenAnswer((_) async => testData);

  final result = await adapter.parse('test.xml');
  
  expect(result, isA<ImportedDataFileModel>());
});
```

## Implementation Checklist

- [ ] Use Either pattern for error handling
- [ ] Inject all dependencies via constructor
- [ ] Write comprehensive unit tests
- [ ] Document device-specific requirements
- [ ] Validate all inputs
- [ ] Use async operations for I/O
- [ ] Never expose internal errors in messages

## Related Documentation

- [Architecture](architecture.md) - System design overview
- [Data Formats](data-formats.md) - JSON specifications
- [Mediworks AL550](adapters/mediworks-al550.md) - Example device integration