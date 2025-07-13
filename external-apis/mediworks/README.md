# Mediworks AL550 API Documentation

API documentation for Mediworks AL550 biometer integration.

## Documentation Files

### English Documentation
- `getPatients-en.md` - GET endpoint for retrieving patient list
- `setPatients-en.md` - POST endpoint for patient registration
- `AL550ExportFile-EN.md` - Export file format specification
- `Explanation of the Interface.docx` - Integration overview

### Chinese Documentation
- `getPatients-zh.md` - GET患者列表接口
- `setPatients-zh.md` - POST患者注册接口
- `AL550ExportFile-ZH.md` - 导出文件格式说明

### Technical Resources
- `AL550ExportFile.json` - Example export file
- `caseData.xml` - Sample case data format

## API Reference

### Connection
```
Base URL: http://<device_ip>:<port>
Default Port: 8080
Authentication: None (trusted local network)
```

### Endpoints
```http
GET  /getPatients    # Retrieve all registered patients
POST /setPatients    # Register new patients for measurement
```

## Data Flow

### Patient Registration (DATEYE → AL550)
1. Export patient demographics from DATEYE
2. POST to `/setPatients` endpoint
3. Patient available for measurement on device

### Measurement Import (AL550 → DATEYE)
1. Perform measurements on AL550
2. Export as JSON file from device
3. Import file into DATEYE

## Data Model

### Key Identifiers
- `patientId` - AL550 internal patient identifier
- `pid` - System-generated unique ID
- `Cases` - Container for examination data
- `OD`/`OS` - Right eye / Left eye data structures

### File Format
Complete specification available in `AL550ExportFile-EN.md`. JSON structure includes:
- Patient demographics
- Multiple examination cases
- Detailed measurement data per eye
- Quality metrics and metadata

## Related Documentation

- [Mediworks AL550 Adapter](../../adapters/mediworks-al550.md)
- [Data Formats](../../data-formats.md)
