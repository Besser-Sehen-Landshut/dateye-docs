# Mediworks AL550 Import/Export Adapters

ImportAdapter and ExportAdapter implementations for Mediworks AL550 optical biometer.

## Overview

The AL550 adapters provide:
- **ImportAdapter**: Import measurement data from AL550 device
- **ExportAdapter**: Export patient registration to AL550 device

Supported measurements:
- Axial length with OCT technology
- Keratometry and topography
- Anterior segment biometry
- White-to-white and pupil measurements

## ImportAdapter Functionality

### File Format

AL550 exports data as JSON:

```json
{
  "DeviceModel": "AL550",
  "Version": "2.1.0",
  "PatientInfo": {
    "firstname": "Anna",
    "lastname": "Schmidt",
    "patientId": "0000000015",
    "gender": "F",
    "birthday": "2010-04-12"
  },
  "Cases": [{
    "CheckTime": "2024-08-15T10:30:00Z",
    "OD": {
      "AxialCase": {
        "Data": {
          "dataFilter": [23.67, 0.542, 3.12, 4.14],
          "snrData": [12.5, 8.2, 11.1, 9.8]
        }
      },
      "TopographyCase": {
        "Data": {
          "CorneaFront": {
            "K1": 43.11,
            "K2": 44.36,
            "Rf": 7.83,
            "Rs": 7.61,
            "AxisFlat": 172,
            "AxisSteep": 82,
            "Astig": 1.25
          }
        }
      },
      "WTWCase": {
        "Data": {
          "wtw": { "r": 5.9 },
          "pupil": { "r": 2.1 }
        }
      }
    },
    "OS": { /* Left eye data */ }
  }]
}
```

### Data Mapping

**Axial Measurements:**
```
dataFilter[0] → Axial length (mm)
dataFilter[1] → Corneal thickness (mm) 
dataFilter[2] → Anterior chamber depth (mm)
dataFilter[3] → Lens thickness (mm)
```

**Complete Field Mappings:**

| AL550 | DATEYE | Unit | Notes |
|-------|--------|------|-------|
| **Axial Length** ||||
| `AxialCase.Data.dataFilter[0]` | `axial_length.value_mm` | mm | |
| `AxialCase.Data.snrData[0]` | `axial_length.signal_noise` | - | Signal quality |
| **Anterior Chamber** ||||
| `AxialCase.Data.dataFilter[2]` | `anterior_chamber.acd` | mm | ACD value |
| **Lens** ||||
| `AxialCase.Data.dataFilter[3]` | `lens.thickness` | mm | Lens thickness |
| **Cornea** ||||
| `TopographyCase.Data.CorneaFront.Rf` | `cornea.k1_mm` | mm | Flat meridian |
| `TopographyCase.Data.CorneaFront.Rs` | `cornea.k2_mm` | mm | Steep meridian |
| `TopographyCase.Data.CorneaFront.AxisFlat` | `cornea.axis_k1` | degrees | |
| `TopographyCase.Data.CorneaFront.AxisSteep` | `cornea.axis_k2` | degrees | |
| `WTWCase.Data.wtw.r` | `cornea.corneal_diameter` | mm | × 2 (radius to diameter) |
| `AxialCase.Data.dataFilter[1]` | `cornea.corneal_thickness` | μm | × 1000 (mm to μm) |
| **Pupil** ||||
| `WTWCase.Data.pupil.r` | `pupil.diameter` | mm | × 2 (radius to diameter) |

## ExportAdapter Functionality

### CRITICAL: Patient Registration Only

**The AL550 ExportAdapter sends ONLY patient demographics to the device:**
- Patient ID, First name, Last name, Birth date, Gender
- **NO measurement data is exported** (AL550 cannot receive measurements)
- **Purpose**: Patient must be registered BEFORE measurement on device

This is a common misconception - the AL550 can export all its measurements but can only import patient registration data.

### Patient Registration

Patients must be registered before measurements:

```http
POST /setPatients
Content-Type: multipart/form-data

------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="patients.json"

[
  {
    "patientId": "0000000015",
    "firstname": "Anna",
    "lastname": "Schmidt",
    "gender": "F",
    "birthday": "2010-04-12",
    "refractiveSurgery": "NONE"
  }
]
------WebKitFormBoundary--
```

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/getPatients` | GET | Retrieve registered patients |
| `/setPatients` | POST | Register new patients |

Default URL: `http://<device-ip>:8080`

### Export Flow

1. Check existing patients - GET /getPatients
2. Compare with DATEYE - Find new patients
3. Prepare upload - Format patient data
4. Send to device - POST /setPatients
5. Log results - Track success/failure

### Gender Mapping

| DATEYE | AL550 |
|--------|-------|
| `male` | `M` |
| `female` | `F` |
| `other` | `F` |
| `unknown` | `F` |

## Configuration

```json
{
  "adapters": {
    "mediworks_al550": {
      "import": {
        "path": "/import/al550/",
        "delete_after_import": true,
        "quality": {
          "min_snr": 5.0
        }
      },
      "export": {
        "targets": [{
          "id": "al550_main",
          "name": "AL550 Hauptgerät",
          "host": "192.168.1.100",
          "port": 8080,
          "auto_export": true
        }]
      }
    }
  }
}
```

## Quality Validation

### SNR Thresholds
- Minimum: 5.0 for reliable measurements
- Warning: 2.0-5.0 (import with flag)
- Reject: < 2.0

### Range Validation

| Measurement | Normal | Extended | Action |
|-------------|--------|----------|--------|
| Axial Length | 22-26mm | 15-35mm | Flag if outside |
| Keratometry | 40-48D | 38-50D | Flag if outside |
| ACD | 2.5-4.0mm | 2.0-5.0mm | Flag if outside |
| Lens Thickness | 3.5-5.0mm | 3.0-6.0mm | Flag if outside |

## Error Handling

| Error | Import | Export |
|-------|--------|--------|
| Network timeout | N/A | Retry with backoff |
| Invalid JSON | Skip file | N/A |
| Missing required field | Import partial | Skip patient |
| Device offline | N/A | Queue for retry |
| Duplicate patient | N/A | Skip silently |

## Testing

Test files in `test/fixtures/mediworks-al550/`:
- `complete_exam.json` - Bilateral measurements
- `single_eye.json` - Monocular patient
- `low_quality.json` - Poor SNR values
- `patient_export.json` - Export format

## Limitations

The AL550 does not provide:
- Refraction data
- Visual acuity
- Subjective measurements
- IOL calculations (separate module)

## Troubleshooting

### Import Issues
- Check JSON structure
- Verify file permissions
- Review quality thresholds

### Export Issues
- Ping device IP address
- Check port 8080 is open
- Verify network connectivity
- Maximum 10,000 patients on device

## API Reference

Complete AL550 API documentation available in `api-reference/mediworks/`

## Related Documentation

- [Adapter Development](../adapter-development.md)
- [Data Formats](../data-formats.md)
- [AL550 API Documentation](../external-apis/mediworks/README.md)