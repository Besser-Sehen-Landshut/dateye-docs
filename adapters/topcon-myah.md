# Topcon MYAH ImportAdapter

ImportAdapter for Topcon MYAH myopia control device.

## Overview

The MYAH ImportAdapter processes the following measurement data:
- Axial length (optical biometry)
- Keratometry and corneal topography
- Pupillometry
- Anterior chamber measurements
- Growth tracking data

## File Format

MYAH exports data as XML files:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<MYAH>
  <DeviceInfo>
    <Model>MYAH</Model>
    <Version>1.3.0</Version>
    <ExportDate>2024-03-15T14:30:00</ExportDate>
  </DeviceInfo>
  
  <Patient>
    <ID>1066587</ID>
    <FirstName>Anna</FirstName>
    <LastName>Schmidt</LastName>
    <BirthDate>2012-05-02</BirthDate>
    <Sex>Female</Sex>
  </Patient>
  
  <Measurement>
    <Eye>OD</Eye>
    <Date>2024-03-15</Date>
    <Time>14:25:30</Time>
    
    <AxialLength>24.52</AxialLength>
    <AxialLengthSNR>12.5</AxialLengthSNR>
    
    <FlatK>7.89</FlatK>
    <FlatAngle>178</FlatAngle>
    <SteepK>7.72</SteepK>
    <SteepAngle>88</SteepAngle>
    
    <HWTW>11.8</HWTW>
    <PupilDiameter>4.2</PupilDiameter>
    <ACD>3.21</ACD>
    <LT>3.65</LT>
    <CCT>542</CCT>
    <QualityScore>9</QualityScore>
  </Measurement>
</MYAH>
```

## Import Methods

### File-based Transfer
- Export from MYAH device to USB/network
- Configure source path in DATEYE

### Watch Folder
- Configure network path: `\\MYAH-PC\Exports\`
- Automatic transfer on file detection

## Field Mappings

### Patient Demographics

| MYAH | DATEYE | Notes |
|------|--------|-------|
| `Patient/ID` | `external_pid` | Prefixed with "MYAH-" |
| `Patient/FirstName` | `first_name` | |
| `Patient/LastName` | `last_name` | |
| `Patient/BirthDate` | `birth_date` | YYYY-MM-DD |
| `Patient/Sex` | `gender` | Male/Female → male/female |

### Measurements

| MYAH | DATEYE | Unit | Description |
|------|--------|------|-------------|
| `AxialLength` | `axial_length.value` | mm | Eye length |
| `AxialLengthSNR` | `axial_length.snr` | - | Signal quality |
| `FlatK` | `cornea.k1_mm` | mm | Flat meridian |
| `SteepK` | `cornea.k2_mm` | mm | Steep meridian |
| `FlatAngle` | `cornea.axis_k1` | ° | 0-180 |
| `SteepAngle` | `cornea.axis_k2` | ° | 0-180 |
| `HWTW` | `white_to_white.horizontal` | mm | Corneal diameter |
| `PupilDiameter` | `pupil.photopic` | mm | Pupil size |
| `ACD` | `acd.value` | mm | Anterior chamber |
| `LT` | `lens_thickness.value` | mm | Lens thickness |
| `CCT` | `cornea.central_thickness` | μm | Corneal thickness |

### Calculated Values

The adapter calculates keratometry in diopters:
```dart
// Standard keratometer index
const KERATOMETER_INDEX = 337.5;
k1_d = KERATOMETER_INDEX / k1_mm;
k2_d = KERATOMETER_INDEX / k2_mm;
astigmatism = abs(k2_d - k1_d);
```

## Quality Validation

### Signal Quality
- Minimum SNR: 5.0 for axial length
- Warning if SNR 2.0-5.0
- Reject if SNR < 2.0

### Range Validation

| Measurement | Normal | Warning | Reject |
|-------------|--------|---------|--------|
| Axial Length | 22-26mm | 20-30mm | <18 or >32mm |
| Keratometry | 40-48D | 38-50D | <35 or >55D |
| Pupil | 3-6mm | 2-8mm | <1.5 or >9mm |
| ACD | 2.5-4.0mm | 2.0-5.0mm | <1.5 or >5.5mm |

## Configuration

```json
{
  "adapters": {
    "topcon_myah": {
      "import_path": "/import/myah/",
      "delete_after_import": true,
      "quality": {
        "min_snr": 5.0,
        "min_quality_score": 7
      },
      "validation": {
        "require_both_eyes": false
      }
    }
  }
}
```

## Adapter Implementation

```dart
class TopconMyahAdapter extends DataAdapter {
  @override
  String get id => 'topcon_myah';
  
  @override
  Future<ParseResult?> parseFile(File file) async {
    if (!file.path.endsWith('.xml')) return null;
    
    final document = XmlDocument.parse(await file.readAsString());
    final root = document.rootElement;
    
    if (root.name.local != 'MYAH') return null;
    
    // Extract patient
    final patient = _parsePatient(root.findElements('Patient').first);
    
    // Extract measurements
    final measurements = <Measurement>[];
    
    for (final meas in root.findElements('Measurement')) {
      final eye = meas.findElements('Eye').first.text == 'OD' ? 'right' : 'left';
      final date = meas.findElements('Date').first.text;
      
      // Axial length
      measurements.add(Measurement('axial_length', {
        'eye': eye,
        'value': double.parse(meas.findElements('AxialLength').first.text),
        'snr': double.parse(meas.findElements('AxialLengthSNR').first.text),
        'measured_at': '${date}T${meas.findElements('Time').first.text}Z',
      }));
      
      // Keratometry
      final k1mm = double.parse(meas.findElements('FlatK').first.text);
      final k2mm = double.parse(meas.findElements('SteepK').first.text);
      
      measurements.add(Measurement('cornea', {
        'eye': eye,
        'k1_mm': k1mm,
        'k2_mm': k2mm,
        'k1_d': 337.5 / k1mm,
        'k2_d': 337.5 / k2mm,
        'axis_k1': int.parse(meas.findElements('FlatAngle').first.text),
        'axis_k2': int.parse(meas.findElements('SteepAngle').first.text),
        'astigmatism': (337.5 / k2mm - 337.5 / k1mm).abs(),
      }));
    }
    
    return ParseResult(
      externalPid: 'MYAH-${patient['id']}',
      patientData: patient,
      measurements: measurements,
      examDate: DateTime.parse(date),
    );
  }
}
```

## Error Handling

| Error | Handling |
|-------|----------|
| Invalid XML | Reject file, log error |
| Missing patient ID | Generate from name+birthdate |
| Out of range values | Import with warning flag |
| Low SNR (<5.0) | Import with quality warning |
| Very low SNR (<2.0) | Skip measurement |

## Unit Conversions

All keratometry values stored in both formats:
- Millimeters (device native)
- Diopters (calculated using 337.5 index)

## Character Encoding

- Files use UTF-8 encoding
- Handles special characters (ä, ö, ü, ß)
- Patient names preserved exactly

## Limitations

The MYAH does not provide:
- Refraction data (requires separate device)
- Visual acuity measurements
- Subjective measurements
- OCT images (only numerical results)

## Testing

Test files in `test/fixtures/topcon-myah/`:
- `valid_export.xml` - Complete bilateral exam
- `single_eye.xml` - Only one eye measured
- `low_quality.xml` - Poor SNR values
- `german_chars.xml` - Special characters

## Troubleshooting

### Files Not Importing
- Check XML structure (must have `<MYAH>` root)
- Verify file permissions
- Check for XML syntax errors

### Missing Measurements
- Some values are optional (LT, CCT)
- Check device software version
- Verify export settings on device

## Related Documentation

- [Adapter Development](../adapter-development.md)
- [Data Formats](../data-formats.md)
- [Keratometry Conversion](../data-formats.md#unit-conversions)
