# ZEISS API Documentation

API specifications and data structures for ZEISS ophthalmic devices.

## Supported Devices

| Device | Model | Documentation |
|--------|-------|---------------|
| IOLMaster 700 | Swept-source OCT biometer | [DICOM API Reference](IOLMaster700Types.md) |
| IOLMaster 500 | Partial coherence interferometry | Planned |

## DICOM Integration

ZEISS devices export measurement data using DICOM standards.

### DICOM SOP Classes

- **Ophthalmic Axial Measurements Storage** - Axial length, ACD, lens thickness
- **Keratometry Measurements Storage** - Corneal curvature measurements  
- **Intraocular Lens Calculations Storage** - IOL power calculations
- **Ophthalmic Photography 8 Bit Image Storage** - Reference images
- **Encapsulated PDF Storage** - Measurement reports

### Data Flow
```
ZEISS Device → DICOM Export → DATEYE Import → Standardized Events
```

## IOLMaster 700 Specifications

### Available Measurements
- **Axial Length** - Swept-source OCT with segmental measurements
- **Keratometry** - Standard and Total Keratometry (licensed feature)
- **Anterior Chamber Depth** - High precision measurement
- **Lens Thickness** - Crystalline lens measurement
- **White-to-White** - Corneal diameter with offset measurements
- **Pupil Size** - Photopic conditions
- **IOL Calculations** - Multiple formulas (Haigis, SRK-T, Barrett)

### Quality Metrics
- Signal-to-noise ratios for axial measurements
- Standard deviations for composite values
- Quality indicators per measurement type
- Automatic validation flags

### Data Precision
- Axial Length: ±0.01 mm
- Keratometry: ±0.01 D
- Automatic reliability assessment

## DICOM Implementation Details

### Instance Structure
ZEISS creates multiple related DICOM instances per examination:
- **Performed Procedure Step ID** - Groups related measurements
- **Study Instance UID** - Links examination data
- **Cross-references** - Images reference measurement instances

### Private DICOM Tags
ZEISS uses private tags for:
- Extended quality metrics
- Additional measurement parameters
- Device-specific calculations
- Clinical patient information

## DATEYE Integration

### Import Process
1. Parse and validate DICOM structure
2. Extract biometric data by SOP Class
3. Process quality metrics and validation
4. Convert to DATEYE measurement schema
5. Maintain relationships between measurements

### Supported Workflows
- **Manual Import** - DICOM files in import folder
- **Batch Processing** - Multiple examinations per export

## Related Documentation

- [ZEISS IOLMaster Adapter](../../adapters/zeiss-iolmaster.md)
- [Data Formats](../../data-formats.md)
