# Eye-Office API Documentation

API specification for Eye-Office practice management software integration.

## Files

- `eye-office-api-1.yaml` - OpenAPI 3.0 specification with CRM criteria support
- `Eye-Office API V0_1-3.pdf` - Complete API documentation

## API Overview

Eye-Office provides a REST API for accessing patient and refraction data from their practice management system. The API uses session-based authentication with existing Eye-Office user credentials.

## Authentication

All requests require:
- Header: `X-API-KEY` - Provided by Eye-Office support
- Header: `Session-ID` - Obtained from login endpoint

### Session Management
```http
POST /v1/login          # Authenticate and obtain session
GET  /v1/ping           # Keep session alive (5-minute intervals)
GET  /v1/logout         # End session
```

## Core Endpoints

### Patient Management
```http
GET  /v1/customer           # List patients with optional CRM filtering
GET  /v1/customer/{id}      # Get specific patient details
POST /v1/customer           # Create new patient
```

Query parameters:
- `crmcriteria` - Filter by CRM criterion ID
- `lastChangedGreaterThan` - Delta synchronization support

### Refraction Data
```http
GET  /v1/refraction         # Get patient refraction history
GET  /v1/refraction/{id}    # Get specific refraction
```

Query parameters:
- `customerId` - Required patient identifier
- `latestDataOnly` - Return only current prescription

### CRM Criteria
```http
GET  /v1/masterdata/crmcriteria    # Get all CRM criteria for filtering
```

## Data Models

### Customer (Patient)
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
        "visusSc": 0.5,
        "visusCc": 1.0,
        "prismHorizontalValue": 0,
        "prismVerticalValue": 0
      }
    }
  }
}
```

### Key Fields
- `internalData.refraction` - Contains trusted refraction values
- `useForOrder` - Boolean flag indicating current prescription
- Visual acuity values: `visusSc` (without correction), `visusCc` (with correction)
- Complete prism data: horizontal, vertical, and resulting values

## Integration Notes

Eye-Office serves as a data source for:
1. Patient demographics
2. Historical refraction data
3. Practice management synchronization

Delta synchronization is supported via the `lastChangedGreaterThan` parameter for efficient updates.

## Related Documentation

- [Eye-Office Adapter Implementation](../../adapters/eye-office.md)
- [Data Formats](../../data-formats.md)
