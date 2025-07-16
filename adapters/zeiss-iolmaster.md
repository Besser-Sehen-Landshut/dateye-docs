# ZEISS IOLMaster ImportAdapter

ImportAdapter for ZEISS IOLMaster 500 and 700 optical biometers.

## Overview

The IOLMaster ImportAdapter supports both models:
- IOLMaster 500: Partial coherence interferometry biometer
- IOLMaster 700: Swept-source OCT biometer

Supported measurements:
- Axial length (optical)
- Keratometry (anterior cornea)
- Anterior chamber depth
- White-to-white distance

## IOLMaster 500

### File Format

Supports two export formats:

#### DICOM Format (Preferred)
- Standard DICOM biometry module
- Patient demographics in header
- Measurements in specific tags

#### XML Format (Legacy)
```xml
<IOLMaster500Export>
  <Patient>
    <ID>123456</ID>
    <FirstName>Hans</FirstName>
    <LastName>Mueller</LastName>
    <BirthDate>1950-03-15</BirthDate>
    <Sex>M</Sex>
  </Patient>
  <Examination Date="2024-01-15">
    <OD>
      <AxialLength>23.45</AxialLength>
      <SNR>12.8</SNR>
      <MeasurementCount>5</MeasurementCount>
      <StandardDeviation>0.02</StandardDeviation>
      <K1>43.25</K1>
      <K1Axis>178</K1Axis>
      <K2>44.50</K2>
      <K2Axis>88</K2Axis>
      <ACD>3.15</ACD>
      <WTW>11.9</WTW>
    </OD>
    <OS>
      <!-- Left eye data -->
    </OS>
  </Examination>
</IOLMaster500Export>
```

### DICOM Tags

| Tag | Field | DATEYE | Unit |
|-----|-------|--------|------|
| (0022,0030) | Axial Length | `axial_length.value_mm` | mm |
| (0022,0031) | Keratometry | `cornea.k1_mm`, `cornea.k2_mm` | mm |
| (0022,0032) | ACD | `acd.value` | mm |
| (0022,0033) | White-to-White | `cornea.corneal_diameter` | mm |
| - | Central corneal thickness | `cornea.corneal_thickness` | μm |
| - | Signal-to-noise | `axial_length.signal_noise` | - |
| - | Measurement count | `axial_length.measurements` | - |

### Quality Requirements

- Minimum SNR: 2.0
- Measurement count: ≥ 5
- Standard deviation: < 0.05mm

## IOLMaster 700

### Additional Capabilities

The 700 model provides:
- Swept-source OCT imaging
- Total keratometry (anterior + posterior)
- Lens thickness measurement
- Fixation check
- Reference images for toric IOLs

### DICOM Structure

Multiple instances per exam:
```
Study Instance UID
├── Axial Measurements (1.2.840.10008.5.1.4.1.1.78.7)
├── Keratometry (1.2.840.10008.5.1.4.1.1.78.3)
├── IOL Calculations (1.2.840.10008.5.1.4.1.1.78.8)
└── Reference Images (1.2.840.10008.5.1.4.1.1.77.1.5.1)
```

### Additional Measurements

| Measurement | DATEYE Field | Notes |
|-------------|--------------|-------|
| Central corneal thickness | `cornea.corneal_thickness` | From OCT |
| Lens thickness | `lens_thickness.value` | Direct measurement |
| Total keratometry | `cornea.type = "total"` | Licensed feature |
| Posterior K values | `cornea.posterior_k1_d` | If available |

## Configuration

```json
{
  "adapters": {
    "zeiss_iolmaster": {
      "import_path": "/import/iolmaster/",
      "formats": {
        "dicom": true,
        "xml": true
      },
      "quality": {
        "500": {
          "min_snr": 2.0,
          "min_measurements": 5
        },
        "700": {
          "min_snr": 8.0,
          "fixation_threshold": "fair"
        }
      }
    }
  }
}
```

## Model Detection

The adapter automatically detects the model:

```dart
String _detectModel(Map data) {
  // IOLMaster 700 specific features
  if (data.containsKey('TotalKeratometry') || 
      data.containsKey('SweptSourceOCT')) {
    return 'iolmaster_700';
  }
  
  // Check software version
  final version = data['SoftwareVersion'];
  if (version?.startsWith('7.') ?? false) {
    return 'iolmaster_500';
  }
  
  return 'iolmaster_unknown';
}
```

## Error Handling

| Error | Handling |
|-------|----------|
| Invalid DICOM | Try XML parser |
| Missing patient ID | Use exam date + initials |
| Low SNR | Import with warning |
| Incomplete exam | Import available data |

## Range Validation

| Measurement | IOLMaster 500 | IOLMaster 700 |
|-------------|---------------|---------------|
| Axial Length | 15-35mm | 15-35mm |
| Signal Noise | >2.0 | >8.0 |
| Keratometry | 37-52D | 38-52D |
| ACD | 2.0-5.0mm | 2.0-5.0mm |
| Lens Thickness | N/A | 3.0-6.0mm |

## Testing

Test files in `test/fixtures/zeiss-iolmaster/`:
- `iol500_dicom.dcm` - Standard DICOM export
- `iol500_xml.xml` - Legacy XML format
- `iol700_multiinstance.dcm` - Multiple DICOM files
- `iol700_total_k.dcm` - With total keratometry

## Limitations

### IOLMaster 500
- No lens thickness
- No posterior cornea
- Anterior keratometry only

### Both Models
- No refraction data
- No visual acuity
- No pupil measurements (photopic only)

## DICOM Specifics

### Character Encoding
```dart
String _parsePersonName(String? dicomName) {
  // DICOM format: Last^First^Middle
  final parts = dicomName?.split('^') ?? [];
  return parts.isNotEmpty ? parts[0] : '';
}
```

### Date Parsing
```dart
String _parseDicomDate(String? dicomDate) {
  // DICOM format: YYYYMMDD
  if (dicomDate?.length == 8) {
    return '${dicomDate!.substring(0,4)}-'
           '${dicomDate.substring(4,6)}-'
           '${dicomDate.substring(6,8)}';
  }
  return '';
}
```

## Related Documentation

- [Adapter Development](../adapter-development.md)
- [Data Formats](../data-formats.md)
- [ZEISS API Documentation](../external-apis/zeiss/README.md)