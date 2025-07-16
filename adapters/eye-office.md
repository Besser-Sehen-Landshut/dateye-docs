# Eye-Office ImportAdapter

ImportAdapter specification for Eye-Office practice management system integration.

## Overview

The Eye-Office ImportAdapter provides:
- Patient demographic data
- Current refraction values
- Historical prescription records
- Visual acuity measurements

Import methods:
1. **Manual Import**: One-time API synchronization
2. **Automatic Import**: Scheduled delta synchronization

## API Data Format

Eye-Office REST API response structure:

```json
{
  "id": 12345,
  "firstname": "Anna",
  "lastname": "Schmidt",
  "birthday": "2010-03-15",
  "sex": "female",
  "internalData": {
    "refraction": {
      "date": "2024-01-15",
      "refrRight": {
        "useForOrder": true,
        "sphere": -2.25,
        "cylinder": -0.50,
        "axisCylinder": 90,
        "addition": 0,
        "prismHorizontalValue": 0,
        "prismVerticalValue": 0,
        "backVertexDistance": 12,
        "visusSc": 0.5,
        "visusCc": 1.0
      },
      "refrLeft": {
        "useForOrder": true,
        "sphere": -2.00,
        "cylinder": -0.75,
        "axisCylinder": 85,
        "visusSc": 0.5,
        "visusCc": 1.0
      }
    }
  }
}
```

## Import Process Architecture

### Manual Import Process
1. **Trigger**: User-initiated action
2. **Source**: Full API query for tagged patients
3. **Scope**: Complete data snapshot
4. **Deduplication**: Patient ID based

### Automatic Import Process
1. **Trigger**: Scheduled interval (default: 5 minutes)
2. **Source**: Delta API query
3. **Scope**: Modified patients only
4. **Efficiency**: Incremental updates

Data extraction pipeline:
- **Patient Mapping**: Demographics to DATEYE format
- **Refraction Conversion**: Prescription data transformation
- **Measurement Extraction**: Integrated refraction with visual acuity

## Field Mapping Specification

### Patient Demographics

| Eye-Office Field | DATEYE Field | Data Type |
|-----------------|--------------|-------|
| `firstname` | `first_name` | String (required) |
| `lastname` | `last_name` | String (required) |
| `birthday` | `birth_date` | Date (YYYY-MM-DD) |
| `sex` | `gender` | Enum (male/female/unknown) |
| `id` | `external_pid` | String (prefixed: "eo_") |

### Refraction Measurements

| Eye-Office Field | DATEYE Field | Unit | Description |
|-----------------|--------------|------|-----------|
| `sphere` | `sphere` | diopters | Spherical correction |
| `cylinder` | `cylinder` | diopters | Cylindrical correction |
| `axisCylinder` | `axis` | degrees | Cylinder axis (0-180) |
| `addition` | `addition` | diopters | Near addition |
| `backVertexDistance` | `vertex` | mm | Vertex distance |
| `visusCc` | `va_cc` | decimal | Corrected visual acuity |
| `useForOrder` | - | boolean | Current prescription flag |

### Prism Values

Prism values converted to resultant prism:

```dart
// Calculate resultant prism from components
if (prismHorizontalValue > 0 || prismVerticalValue > 0) {
  final resultantPrism = sqrt(pow(prismHorizontalValue, 2) + pow(prismVerticalValue, 2));
  final resultantBase = calculatePrismBase(prismHorizontalValue, prismHorizontalAxis,
                                          prismVerticalValue, prismVerticalAxis);
  return {
    'prism': resultantPrism,
    'prism_base': resultantBase
  };
}
```

### Complete Prism Mapping

| Eye-Office Field | DATEYE Field | Unit | Description |
|-----------------|--------------|------|-----------|
| `prismHorizontalValue` | - | prism diopters | Used for calculation |
| `prismHorizontalAxis` | - | degrees | Used for calculation |
| `prismVerticalValue` | - | prism diopters | Used for calculation |
| `prismVerticalAxis` | - | degrees | Used for calculation |
| `prismResultingValue` | `prism` | prism diopters | Calculated resultant |
| `prismResultingAxis` | `prism_base` | degrees | Calculated base direction |

## API Configuration

Unified configuration for both import modes:

```json
{
  "adapters": {
    "eye_office": {
      "import": {
        "mode": "automatic",
        "source": "api",
        "api": {
          "url": "https://eye-office.local:4450/v1",
          "apiKey": "encrypted:...",
          "username": "encrypted:...",
          "password": "encrypted:...",
          "crmExportId": 789,
          "syncInterval": 300
        },
        "data": {
          "visualAcuity": true,
          "prismValues": true,
          "objectiveRefraction": true,
          "subjectiveRefraction": true,
          "import_external": true,
          "import_historical": true
        }
      }
    }
  }
}
```

## API Integration Details

### Authentication Protocol

```http
# Session initialization
POST /v1/login
X-API-KEY: {api_key}
Content-Type: application/json
{
  "user": "{username}",
  "password": "{password}"
}
Response: { "session_id": "{session_id}" }

# Session maintenance
GET /v1/ping
X-API-KEY: {api_key}
Session-ID: {session_id}

# Session termination
GET /v1/logout
X-API-KEY: {api_key}
Session-ID: {session_id}
```

### CRM Filtering Implementation

Patient filtering via CRM criteria:

```http
# Discover Export criterion ID
GET /v1/masterdata/crmcriteria
Response: Tree structure containing { "name": "Export", "id": 789 }

# Query tagged patients
GET /v1/customer?crmcriteria=789&lastChangedGreaterThan=2024-01-01T00:00:00Z
```

### Patient Creation (Optional)

```http
POST /v1/customer
Content-Type: application/json
{
  "branch": 1,
  "firstname": "Max",
  "lastname": "Mustermann",
  "birthday": "2010-03-15"
}
```

### Delta Synchronization

Incremental sync implementation:

```typescript
async function deltaSync(lastSyncTime: DateTime) {
  // Retrieve cached export criterion
  const exportId = await getExportCriterionId();

  // Query modified patients
  const patients = await api.get('/customer', {
    crmcriteria: exportId,
    lastChangedGreaterThan: lastSyncTime.toISO(),
    pageSize: 100
  });

  // Fetch refraction history
  for (const patient of patients.data) {
    const refractions = await api.get('/refraction', {
      customerId: patient.id,
      latestDataOnly: false
    });
  }
}
```

### API Endpoint Reference

| Endpoint | Method | Purpose | Frequency |
|----------|--------|---------|-----------|
| `/v1/login` | POST | Session creation | Startup |
| `/v1/ping` | GET | Session maintenance | 5 minutes |
| `/v1/logout` | GET | Session termination | Shutdown |
| `/v1/masterdata/crmcriteria` | GET | Criterion discovery | Once |
| `/v1/customer` | GET | Patient query | Per sync |
| `/v1/refraction` | GET | Refraction retrieval | Per patient |
| `/v1/customer` | POST | Patient creation | Optional |

## Error Handling Strategy

| Error Scenario | Resolution |
|---------------|------------|
| Connection failure | Exponential backoff retry |
| Session expiration | Automatic re-authentication |
| Missing CRM criterion | Setup wizard activation |
| Missing required fields | Skip record, log error |
| Invalid date format | Default to current date |
| No refraction data | Import demographics only |

## Adapter Implementation

```dart
class EyeOfficeImportAdapter implements ImportAdapter {
  final EyeOfficeApiClient _apiClient;
  final int _crmExportId;

  @override
  String get id => 'eye_office';

  @override
  String get displayName => 'Eye-Office';

  Future<List<ParseResult>> importWithDelta(DateTime lastSync) async {
    // Query modified patients
    final patients = await _apiClient.getCustomers(
      crmcriteria: _crmExportId,
      lastChangedGreaterThan: lastSync,
    );

    final results = <ParseResult>[];

    for (final patient in patients) {
      // Retrieve refraction history
      final refractions = await _apiClient.getRefractions(
        customerId: patient.id,
      );

      // Map patient demographics
      final patientData = {
        'first_name': patient.firstname,
        'last_name': patient.lastname,
        'birth_date': patient.birthday,
        'gender': _mapGender(patient.sex),
      };

      // Extract measurements
      final measurements = <Measurement>[];
      if (refractions.isNotEmpty) {
        final latest = refractions.first;

        if (latest.rightEye != null) {
          measurements.add(_parseRefraction(latest.rightEye, 'right'));
        }

        if (latest.leftEye != null) {
          measurements.add(_parseRefraction(latest.leftEye, 'left'));
        }
      }

      results.add(ParseResult(
        externalPid: 'eo_${patient.id}',
        patientData: patientData,
        measurements: measurements,
        examDate: refractions.firstOrNull?.date ?? DateTime.now(),
      ));
    }

    return results;
  }

  Measurement _parseRefraction(EyeData data, String eye) {
    return Measurement.refraction(
      eye: eye,
      sphere: data.sphere,
      cylinder: data.cylinder,
      axis: data.axisCylinder,
      addition: data.addition,
      vertex: data.backVertexDistance,
      prism: _calculateResultantPrism(data),
      prism_base: _calculatePrismBase(data),
      va_cc: data.visusCc,
      refraction_type: 'subjective',
      condition: 'regular',
      data_source: 'device',
    );
  }
}
```

## Data Mapping

### Patient Demographics
```json
// Eye-Office API
{
  "id": 12345,
  "firstname": "Anna",
  "lastname": "Schmidt",
  "birthday": "2010-03-15",
  "sex": "female"
}
```

```dart
// DATEYE Format
Patient(
  externalId: "EYE-OFFICE-12345",
  firstName: "Anna",
  lastName: "Schmidt",
  birthDate: DateTime(2010, 3, 15),
  gender: Gender.female,
)
```

### Refraction Data
```json
// Eye-Office API
"refrRight": {
  "sphere": -2.25,
  "cylinder": -0.50,
  "axisCylinder": 90,
  "addition": 2.00,
  "visusCc": 1.0
}
```

```dart
// DATEYE Format
Measurement.refraction(
  eye: 'right',
  sphere: -2.25,
  cylinder: -0.50,
  axis: 90,
  addition: 2.00,
  va_cc: 1.0,
  refraction_type: 'subjective',
  condition: 'regular',
  data_source: 'device',
)
```

### Field Mappings

| Eye-Office Field | DATEYE Field | Notes |
|------------------|--------------|-------|
| `id` | `external_id` | Prefixed with "EYE-OFFICE-" |
| `firstname` | `first_name` | Direct mapping |
| `lastname` | `last_name` | Direct mapping |
| `birthday` | `birth_date` | Parse to DateTime |
| `sex` | `gender` | Normalize to enum |
| `sphere` | `refraction.sphere` | Direct mapping |
| `cylinder` | `refraction.cylinder` | Direct mapping |
| `axisCylinder` | `refraction.axis` | Direct mapping |
| `addition` | `refraction.addition` | Optional field |
| `visusCc` | `va_cc` | Corrected vision (part of refraction) |

## Testing Requirements

API-only import requires:
- Mock API responses per OpenAPI specification
- CRM criteria filter validation
- Delta synchronization behavior
- Session lifecycle management

## Current Limitations

Not currently imported:
- Objective refraction data
- Interpupillary distance
- Binocular vision measurements
- Spectacle lens orders
- Contact lens specifications

## Future Export Capability

Potential bidirectional synchronization:

```dart
class EyeOfficeExportAdapter implements ExportAdapter {
  // Patient creation via POST /v1/customer
  // Implementation pending requirements analysis
}
```

Outstanding questions:
- Eye-Office data reception capability
- Updateable field specifications
- Conflict resolution strategy

## Related Documentation

- [Adapter Development](../adapter-development.md)
- [Data Formats](../data-formats.md)
- Eye-Office API documentation in `api-reference/eye-office/`
