# ZEISS IOLMaster 700 DICOM API Reference

Complete DICOM structure reference for IOLMaster 700 integration

## Overview

The IOLMaster 700 exports comprehensive biometric measurement data using standard DICOM Information Object Definitions (IODs). This document provides the complete structure reference for DATEYE integration.

## DICOM SOP Classes

### Measurement SOP Classes

| SOP Class | UID | Purpose |
|-----------|-----|---------|
| Ophthalmic Axial Measurements Storage | 1.2.840.10008.5.1.4.1.1.78.7 | Axial length, ACD, lens thickness |
| Keratometry Measurements Storage | 1.2.840.10008.5.1.4.1.1.78.3 | Corneal curvature measurements |
| Intraocular Lens Calculations Storage | 1.2.840.10008.5.1.4.1.1.78.8 | IOL power calculations |

### Image SOP Classes

| SOP Class | UID | Purpose |
|-----------|-----|---------|
| Ophthalmic Photography 8 Bit Image Storage | 1.2.840.10008.5.1.4.1.1.77.1.5.1 | Scleral, white-to-white images |
| Multi-frame Grayscale Byte Secondary Capture | 1.2.840.10008.5.1.4.1.1.7.2 | Quality control images |
| Encapsulated PDF Storage | 1.2.840.10008.5.1.4.1.1.104.1 | Measurement reports |

## Ophthalmic Axial Measurements IOD

### Core Measurement Structure

```typescript
interface OphthalmicAxialMeasurements {
  // Device identification
  ophthalmicAxialMeasurementsDeviceType: "OPTICAL";
  
  // Anterior chamber depth definition
  anteriorChamberDepthDefinition: "Front Of Cornea To Front Of Lens";
  
  // Right eye measurements (if measured)
  ophthalmicAxialMeasurementsRightEye?: {
    lensStatus: LensStatus;
    vitreousStatus: VitreousStatus;
    pupilDilated?: "YES" | "NO";
    ophthalmicAxialLengthMeasurements: AxialLengthMeasurement[];
    opticalSelectedOphthalmicAxialLength?: SelectedAxialLength[];
  };
  
  // Left eye measurements (if measured)
  ophthalmicAxialMeasurementsLeftEye?: {
    // Same structure as right eye
  };
}
```

### Axial Length Measurement Types

```typescript
interface AxialLengthMeasurement {
  ophthalmicAxialLengthMeasurementsType: "TOTAL LENGTH" | "SEGMENTAL LENGTH";
  
  // For total length measurements
  ophthalmicAxialLengthMeasurementsTotalLength?: {
    ophthalmicAxialLength: number; // mm
    ophthalmicAxialLengthMeasurementModified: "YES" | "NO";
    referencedOphthalmicAxialLengthMeasurementQCImage: ImageReference;
    opticalOphthalmicAxialLengthMeasurements: {
      ophthalmicAxialLengthDataSource: DataSource;
      ophthalmicAxialLengthDataSourceDescription: string;
    };
  }[];
  
  // For segmental measurements
  ophthalmicAxialLengthMeasurementsSegmentalLength?: {
    ophthalmicAxialLength: number; // mm
    ophthalmicAxialLengthMeasurementModified: "YES" | "NO";
    ophthalmicAxialLengthMeasurementsSegmentName: SegmentName;
    opticalOphthalmicAxialLengthMeasurements: {
      ophthalmicAxialLengthDataSource: DataSource;
      ophthalmicAxialLengthDataSourceDescription: string;
    };
  }[];
}
```

### Segment Names (Standard)

```typescript
type SegmentName = 
  | "T-AA200"   // Cornea
  | "T-AA050"   // Anterior Chamber  
  | "111778"    // Single or Anterior Lens
  | "IOLM_AQD"; // Aqueous Depth (private)
```

### Quality Metrics

```typescript
interface QualityMetric {
  conceptNameCode: QualityMetricType;
  numericValue: number;
  measurementUnitsCode: {
    codeValue: "1";
    codingSchemeDesignator: "UCUM";
    codeMeaning: "no units";
  };
}

type QualityMetricType = 
  | "111786"      // Standard Deviation of measurements used
  | "IOLM_QUALITY"; // IOLMaster Quality Metric (private)
```

### Selected Axial Length (Composite Results)

```typescript
interface SelectedAxialLength {
  ophthalmicAxialLengthMeasurementsType: "TOTAL LENGTH" | "SEGMENTAL LENGTH";
  
  selectedTotalOphthalmicAxialLength?: {
    ophthalmicAxialLength: number; // mm (composite value)
    referencedOphthalmicAxialLengthMeasurementQCImage: ImageReference;
    ophthalmicAxialLengthQualityMetric: QualityMetric;
  };
  
  selectedSegmentalOphthalmicAxialLength?: {
    ophthalmicAxialLengthMeasurementsSegmentName: SegmentName;
    ophthalmicAxialLength: number; // mm (composite value)
    referencedOphthalmicAxialLengthMeasurementQCImage: ImageReference;
    ophthalmicAxialLengthQualityMetric: QualityMetric;
  }[];
}
```

## Keratometry Measurements IOD

### Core Structure

```typescript
interface KeratometryMeasurements {
  // Right eye keratometry (if measured)
  keratometryRightEye?: {
    steepKeratometricAxis: {
      radiusOfCurvature: number; // mm
      keratometricPower: number;  // diopters
      keratometricAxis: number;   // degrees
    };
    flatKeratometricAxis: {
      radiusOfCurvature: number; // mm
      keratometricPower: number;  // diopters  
      keratometricAxis: number;   // degrees
    };
  };
  
  // Left eye keratometry (if measured)
  keratometryLeftEye?: {
    // Same structure as right eye
  };
}
```

### Extended Keratometry (Private Extensions)

```typescript
interface ExtendedKeratometry {
  // Quality information for each eye
  iolmasterKeratometryQualityRightEye?: {
    extendedSteepKeratometricAxis?: {
      standardDeviationOfKeratometryMeasurement?: number; // mm
    };
    extendedFlatKeratometricAxis?: {
      standardDeviationOfKeratometryMeasurement?: number; // mm
    };
    iolmasterQualityIndicator?: "SUCCESSFUL" | "WARNING" | "FAILED" | "NONE";
    standardDeviationOfSphericalEquivalent?: number; // mm
    referencedKeratometryMeasurementQCImage: {
      referencedSOPClassUID: "1.2.840.10008.5.1.4.1.1.7.2";
      referencedSOPInstanceUID: string;
    };
  };
  
  // Posterior cornea surface measurements (requires license)
  iolmasterPosteriorCorneaSurfaceRightEye?: {
    steepPosteriorCorneaSurface?: {
      posteriorRadiusOfCurvature?: number; // mm
      posteriorKeratometricPower?: number;  // diopters
      posteriorKeratometricAxis?: number;   // degrees
      standardDeviationOfKeratometryMeasurement?: number; // mm
    };
    flatPosteriorCorneaSurface?: {
      posteriorRadiusOfCurvature?: number; // mm
      posteriorKeratometricPower?: number;  // diopters
      posteriorKeratometricAxis?: number;   // degrees
      standardDeviationOfKeratometryMeasurement?: number; // mm
    };
    iolmasterQualityIndicator?: "SUCCESSFUL" | "WARNING" | "FAILED" | "NONE";
    standardDeviationOfSphericalEquivalent?: number; // mm
    indexOfRefractionOfTheCornea: number;
    indexOfRefractionOfTheAqueousHumor: number;
  };
  
  // Total keratometry measurements (requires license)
  iolmasterTotalKeratometryRightEye?: {
    steepTotalKeratometry: {
      totalKeratometryRadiusOfCurvature: number; // mm
      totalKeratometryPower: number; // diopters
      totalKeratometryAxis: number;  // degrees
      standardDeviationOfTotalKeratometry?: number; // mm
    };
    flatTotalKeratometry: {
      totalKeratometryRadiusOfCurvature: number; // mm
      totalKeratometryPower: number; // diopters
      totalKeratometryAxis: number;  // degrees
      standardDeviationOfTotalKeratometry?: number; // mm
    };
    iolmasterQualityIndicator?: "SUCCESSFUL" | "WARNING" | "FAILED" | "NONE";
    standardDeviationOfTotalKeratometrySphericalEquivalent?: number; // mm
  };
}
```

## Intraocular Lens Calculations IOD

### Core Structure

```typescript
interface IntraocularLensCalculations {
  // Right eye calculations (if performed)
  intraocularLensCalculationsRightEye?: {
    targetRefraction: number; // diopters
    refractiveProcedureOccurred?: "YES" | "NO";
    refractiveSurgeryType?: RefractiveSurgeryType[];
    refractiveErrorBeforeRefractiveSurgery?: RefractiveErrorType;
    
    // Measurement inputs used for calculation
    cornealSize?: {
      cornealSize: number; // mm (horizontal diameter)
      sourceOfCornealSizeData: DataSource;
    };
    lensThickness?: {
      lensThickness: number; // mm
      sourceOfLensThicknessData: DataSource;
    };
    anteriorChamberDepth?: {
      anteriorChamberDepth: number; // mm
      sourceOfAnteriorChamberDepthData: DataSource;
    };
    refractiveState?: {
      sphericalLensPower: number; // diopters
      cylinderLensPower: number;  // diopters
      cylinderAxis: number;       // degrees
      sourceOfRefractiveMeasurements: DataSource;
    };
    
    // Keratometry data used
    steepKeratometricAxis: KeratometricAxis;
    flatKeratometricAxis: KeratometricAxis;
    keratometryMeasurementType: "111754"; // Auto Keratometry
    keratopterIndex: number;
    
    // Alternative cornea measurements
    corneaMeasurements?: {
      steepCornealAxis: CornealAxis;
      flatCornealAxis: CornealAxis;
      corneaMeasurementMethod: CornealMeasurementMethod;
      keratopterIndex: number;
      refractiveIndexOfCornea?: number;     // For posterior measurements
      refractiveIndexOfAqueousHumor?: number; // For posterior measurements
      sourceOfCorneaMeasurementData: DataSource;
    };
    
    // Calculation details
    iolFormulaCode: IOLFormula;
    ophthalmicAxialLength: {
      ophthalmicAxialLength: number; // mm
      ophthalmicAxialLengthSelectionMethod: SelectionMethod;
      sourceOfOphthalmicAxialLength: DataSource;
    };
    surgicallyInducedAstigmatism?: {
      cylinderPower: number; // diopters
      cylinderAxis: number;  // degrees
    };
    
    // IOL specifications
    iolManufacturer: string;
    implantName: string;
    typeOfOpticalCorrection: "SPHERICAL" | "TORIC";
    lensConstant: LensConstant[];
    
    // Calculation results
    iolPower: IOLPowerResult[];
    iolPowerForExactEmmetropia?: number; // diopters
    toricIOLPowerForExactEmmetropia?: ToricPower;
    iolPowerForExactTargetRefraction?: number; // diopters (typically empty)
    toricIOLPowerForExactTargetRefraction?: ToricPower;
    calculationComment?: CalculationComment[];
  };
  
  // Left eye calculations (if performed)
  intraocularLensCalculationsLeftEye?: {
    // Same structure as right eye
  };
}
```

### IOL Calculation Results

```typescript
interface IOLPowerResult {
  iolPower: number; // diopters (spherical equivalent for toric)
  toricIOLPower?: {
    spherePower?: number;  // diopters (optional)
    cylinderPower: number; // diopters
    cylinderAxis: number;  // degrees
  };
  predictedRefractiveError: number; // diopters
  predictedToricError?: {
    spherePower?: number;  // diopters (optional)
    cylinderPower: number; // diopters
    cylinderAxis: number;  // degrees
  };
  implantPartNumber?: string;
  preSelectedForImplantation: "YES" | "NO"; // Only one should be "YES"
}
```

### IOL Formulas

```typescript
type IOLFormula = 
  | "111760"          // Haigis
  | "111761"          // Haigis-L
  | "111762"          // Holladay 1
  | "111763"          // Holladay 2
  | "111764"          // Hoffer Q
  | "111767"          // SRK-T
  | "111860"          // Haigis Toric
  | "111861"          // Haigis-L Toric
  | "111862"          // Barrett Toric
  | "111863"          // Barrett True-K
  | "111864"          // Barrett True-K Toric
  | "111865"          // Barrett Universal II
  | "IOLM_BRRTT_TKT"  // Barrett TK Toric (private)
  | "IOLM_BRRTT_TKUII" // Barrett TK Universal II (private)
  | "IOLM_BRRTT_TKTK"  // Barrett TK True-K (private)
  | "IOLM_BRRTT_TKTKT"; // Barrett TK True-K Toric (private)
```

### Lens Constants

```typescript
interface LensConstant {
  conceptNameCode: LensConstantType;
  numericValue: string; // Encoded as string in DICOM
}

type LensConstantType = 
  | "F-048FA"  // A-Constant
  | "111768"   // ACD Constant
  | "111769"   // Haigis a0
  | "111770"   // Haigis a1
  | "111771"   // Haigis a2
  | "111772"   // Hoffer pACD Constant
  | "111773"   // Surgeon Factor
  | "111866"   // Barrett Lens Factor
  | "111867";  // Barrett Design Factor
```

## Ophthalmic Photography IOD

### Scleral Reference Images

```typescript
interface ScleralImage {
  imageType: "ORIGINAL\\PRIMARY\\\\SCLERA";
  imageLaterality: "R" | "L";
  acquisitionContext: {
    toricAcquisitionQuality?: {
      valueType: "NUMERIC";
      numericValue: number; // Range 0.0-1.0
      measurementUnits: "1"; // No units
    };
    acquisitionExposureTime?: {
      valueType: "NUMERIC";
      numericValue: number; // milliseconds
      measurementUnits: "ms";
    };
    acquisitionIllumination?: {
      valueType: "NUMERIC";
      numericValue: number; // Range 0-255
      measurementUnits: "1"; // No units
    };
    referenceImageEvaluationData?: {
      valueType: "TEXT";
      textValue: string;
    };
    // Pixel dimensions
    pixelWidth: {
      valueType: "NUMERIC";
      numericValue: number; // millimeters
      measurementUnits: "mm";
    };
    pixelHeight: {
      valueType: "NUMERIC";
      numericValue: number; // millimeters
      measurementUnits: "mm";
    };
    // Limbus detection
    limbusCenterX: {
      valueType: "NUMERIC";
      numericValue: number; // pixels
      measurementUnits: "pixels";
    };
    limbusCenterY: {
      valueType: "NUMERIC";
      numericValue: number; // pixels
      measurementUnits: "pixels";
    };
    limbusRadius: {
      valueType: "NUMERIC";
      numericValue: number; // millimeters
      measurementUnits: "mm";
    };
    // Eyelid detection (polynomial coefficients)
    lowerLidCoeffA: number;
    lowerLidCoeffB: number;
    lowerLidCoeffC: number;
    upperLidCoeffA: number;
    upperLidCoeffB: number;
    upperLidCoeffC: number;
    scleraQuality: "SUCCESSFUL" | "WARNING" | "FAILED" | "NONE";
  };
}
```

### White-to-White Images

```typescript
interface WhiteToWhiteImage {
  imageType: "ORIGINAL\\PRIMARY\\\\WHITE_TO_WHITE";
  imageLaterality: "R" | "L";
  acquisitionContext: {
    wtwDiameter: {
      valueType: "NUMERIC";
      numericValue: number; // millimeters
      measurementUnits: "mm";
    };
    wtwFpX: {
      valueType: "NUMERIC";
      numericValue: number; // millimeters offset
      measurementUnits: "mm";
    };
    wtwFpY: {
      valueType: "NUMERIC";
      numericValue: number; // millimeters offset
      measurementUnits: "mm";
    };
    pupilDiameter: {
      valueType: "NUMERIC";
      numericValue: number; // millimeters
      measurementUnits: "mm";
    };
    pupilFpX: {
      valueType: "NUMERIC";
      numericValue: number; // millimeters offset
      measurementUnits: "mm";
    };
    pupilFpY: {
      valueType: "NUMERIC";
      numericValue: number; // millimeters offset
      measurementUnits: "mm";
    };
    positionFpX: {
      valueType: "NUMERIC";
      numericValue: number; // pixels
      measurementUnits: "pixels";
    };
    positionFpY: {
      valueType: "NUMERIC";
      numericValue: number; // pixels
      measurementUnits: "pixels";
    };
    wtwQuality: "SUCCESSFUL" | "WARNING" | "FAILED" | "NONE";
  };
}
```

## Quality Control Images

### Multi-frame Secondary Capture Images

```typescript
interface QualityControlImage {
  imageType: "DERIVED\\PRIMARY\\\\OAM_QUALITY" | "DERIVED\\PRIMARY\\\\KER_QUALITY";
  qualityControlImage: "YES";
  referencedInstance: {
    referencedSOPClassUID: string; // References measurement SOP Class
    referencedSOPInstanceUID: string;
    purposeOfReference: "MEASUREMENTS"; // Private code
  };
  numberOfFrames: number;
  frameIncrementPointer: "(0018,2002)"; // Frame Label Vector
  frameLabelVector: string[]; // Frame numbers as labels
}
```

## Common Data Types

### Data Source Types

```typescript
type DataSource = 
  | "111780"         // Measurement From This Device
  | "113857"         // Manual Entry
  | "IOLM_SCAN_000"  // Measurement at scan angle 0° (private)
  | "IOLM_SCAN_030"  // Measurement at scan angle 30° (private)
  | "IOLM_SCAN_090"  // Measurement at scan angle 90° (private)
  | "IOLM_SCAN_240"  // Measurement at scan angle 240° (private)
  | "IOLM_SCAN_300"  // Measurement at scan angle 300° (private)
  | "IOLM_SCAN_330"  // Measurement at scan angle 330° (private)
  | "IOLM_COMPOSITE"; // Calculated composite result (private)
```

### Lens Status Types

```typescript
type LensStatus = 
  | "DA-73410"           // Aphakic
  | "R-2073F"            // Phakic
  | "A-040F7"            // Phakic IOL
  | "F-02087"            // Piggyback IOL
  | "DA-73460"           // Pseudophakia
  | "PGGYBCK_SILICON"    // Piggyback Silicone IOL (private)
  | "PSDPHKC_SILICON"    // Pseudophakic Silicone (private)
  | "PSDPHKC_PMMA";      // Pseudophakic PMMA (private)
```

### Vitreous Status Types

```typescript
type VitreousStatus = 
  | "DA-7930D"  // Post-Vitrectomy
  | "F-035FD"   // Silicone Oil
  | "T-AA092";  // Vitreous Only
```

### Refractive Surgery Types

```typescript
type RefractiveSurgeryType = 
  | "P1-A3102"  // RK (Radial Keratotomy)
  | "P1-A3835"  // PRK
  | "P0-0526F"  // LASIK
  | "P1-A3846"; // LASEK
```

### Refractive Error Types

```typescript
type RefractiveErrorType = 
  | "DA-74120"  // Myopia
  | "DA-74110"; // Hyperopia
```

## Instance Relationships

All instances from a single IOLMaster 700 examination are linked through:

### Shared Identifiers

```typescript
interface SharedIdentifiers {
  // Links all instances from one examination
  performedProcedureStepID: string;
  performedProcedureStepStartDate: string; // YYYYMMDD
  performedProcedureStepStartTime: string; // HHMMSS
  performedProcedureStepDescription: "Ophthalmic Biometry Measurement";
  
  // Patient and study identifiers
  studyInstanceUID: string;
  patientID: string;
  patientsName: string;
}
```

### Instance Cross-References

```typescript
interface InstanceReferences {
  // From Encapsulated PDF to other instances
  sourceInstanceSequence: {
    referencedSOPClassUID: string;
    referencedSOPInstanceUID: string;
  }[];
  
  // From Quality Control Images to Measurements
  referencedInstance: {
    referencedSOPClassUID: string;
    referencedSOPInstanceUID: string;
    purposeOfReference: "MEASUREMENTS";
  };
  
  // From Measurements to Quality Control Images
  referencedOphthalmicAxialLengthMeasurementQCImage?: {
    referencedSOPClassUID: "1.2.840.10008.5.1.4.1.1.7.2";
    referencedSOPInstanceUID: string;
    referencedFrameNumber: number;
  };
}
```

## Private Extensions

IOLMaster 700 uses several private tag groups for extended functionality:

### Private Tag Groups

| Group | Creator | Purpose |
|-------|---------|---------|
| (771B,00xx) | "99CZM" | PDF measurement values |
| (1201,00xx) | "99CZM_IOLMaster_ExtendedKeratometryMeasurements" | Extended keratometry |
| (1203,00xx) | "99CZM_IOLMaster_ClinicalPatientInformation" | Clinical data |
| (1205,00xx) | "99CZM_IOLMaster_ExtendedOphthalmicAxialMeasurements" | Extended axial measurements |
| (2201,00xx) | "99CZM_NIM_INTERNAL_01" | Internal metadata |

These private tags provide additional measurement details and quality metrics not available in standard DICOM tags.

## Related Documentation

- [IOLMaster 700 Import Adapter](../Import/ZeissIOLMaster700.md) – Implementation details
- [DICOM Integration Guide](../../Operations/Integration.md) – Setup and configuration
- [Measurement Types](../../API/Events.md) – DATEYE measurement schema
- [Import Adapter API](../ImportAPI.md) – Adapter interface specification
