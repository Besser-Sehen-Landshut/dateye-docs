# AL550ExportFile Field Descriptions

## Object: AL550ExportFile

- **DeviceModel** (`string`): Device model.
- **Version** (`string`): Device software version.

### Calibration Data

- **anchor** (Anchor Data)

  - **x**, **y** (`integer`): X and Y coordinates of the calibrated ring center.
  - **r1**, **r2**, **r3** (`integer`): Three radius parameters for auxiliary ring identification.
- **motorCenter** (Motor Center Position)

  - **x**, **y**, **z** (`integer`): X, Y, Z coordinates when centered.
- **octParas** (OCT Parameters)

  - **zerostart1**, **zerostart2** (`integer`): Zero-start positions.
  - **topopos1**, **topopos2**, **octpos1**, **octpos2** (`integer`): Corneal topography and OCT capture positions.
  - **imagescale** (`integer`): Image scale ratio.
  - **imageshowlabel** (`integer`): Image display label (0 or 1).
  - **rulmean**, **frethres** (`integer`): Mean value and frequency threshold of ruler signal.
  - **halfwavelength1**, **halfwavelength2** (`float`): Two half-wavelength values.
  - **signaloffset1**, **signaloffset2**, **signaloffset3**, **signaloffset4**, **signaloffset5**, **signaloffset6** (`integer`): Six signal offset values.
  - **ruldividepos** (`integer`): Ruler signal division position.
  - **signaloffset** (`integer`): Base signal offset.
  - **threcorneapos1**, **threcorneapos2** (`integer`): Corneal position thresholds.
  - **threcorneathick1**, **threcorneathick2** (`integer`): Corneal thickness thresholds.
  - **threacdepth1**, **threacdepth2** (`integer`): Anterior chamber depth thresholds.
  - **threlensthick1**, **threlensthick2** (`integer`): Lens thickness thresholds.
  - **threretinapos1**, **threretinapos2** (`integer`): Retina position thresholds.
  - **threcornea1**, **threcornea2** (`integer`): Corneal parameters.
  - **threretina2lensb1**, **threretina2lensb2** (`integer`): Retina-to-lens-back distance.
  - **threretina2lensf1**, **threretina2lensf2** (`integer`): Retina-to-lens-front distance.
  - **threretina2corneaf1**, **threretina2corneaf2** (`integer`): Retina-to-cornea distance.
  - **refractiveindex0**, **refractiveindex1**, **refractiveindex2**, **refractiveindex3** (`array of float`): Array of refractive indices for four different eye structures.
  - **CCT_offset** (`float`): Corneal central thickness offset.
- **rendercfg** (Rendering Configuration)

  - **w**, **h** (`integer`): Rendering width and height.
  - **x**, **y** (`integer`): Rendering position coordinates.
  - **flip** (Flip Configuration)
    - **x**, **y** (`integer`): Flip configuration for x and y axes.
- **cam_lamp** (Camera and Lamp Configuration)

  - **fixedLight** (Fixed Light Configuration)
    - **brightness** (`integer`): Brightness of the fixed light.
  - **axislength** (Axis Length Configuration)
    - **cam** (Camera Settings)
      - **rgain**, **ggain**, **bgain** (`integer`): Red, green, blue gain.
      - **blacklevel** (`float`): Black level.
      - **gamma** (`float`): Gamma value.
    - **lamp** (Lamp Settings)
      - **infrared**, **red**, **green** (`boolean`): Switches for infrared, red, and green lights.
      - **ir_lightness** (`float`): Infrared light brightness.
      - **center_ring_lightness**, **middle_ring_lightness**, **outer_ring_lightness** (`float`): Brightness of center, middle, and outer ring lights.
- **Laser** (Laser Position)

  - **x**, **y** (`integer`): X and Y coordinates of the laser.
- **focusThreshold** (Focus Threshold)

  - **axisLength**, **topography** (`integer`): Focus threshold for axis length and topography.
- **dstPath** (`string`): Image destination path.
- **CAMERA_pixelsize** (`float`): Camera pixel size.
- **coarse**, **fine**, **ir**, **green** (`string`): Paths for four model files.
- **pupil**, **wtw** (`string`): File paths for pupil and white-to-white.
- **initX**, **initY**, **initZ** (`integer`): Initial position coordinates X, Y, Z.
- **maxFrontPos**, **maxBackPos** (`integer`): Maximum front and back positions.
- **PZ_Motor_A**, **PZ_Motor_B** (`integer`): Motor parameters.
- **AE** (`integer`): Auto-exposure value.
- **cam_lamp_1** (Alternative Lamp Configuration, same structure as `cam_lamp`).
- **focusThreshold_new** (New Focus Threshold)

  - **axisLength**, **topography** (`integer`): New focus threshold for axis length and topography.
- **isNew** (`boolean`): Indicates if it is a new version.

### Patients

- **PatientInfo** (Basic patient information)

  - **_id**, **_rev** (`string`): Unique identifier in the database.
  - **firstname**, **lastname** (`string`): Patient's first and last name.
  - **patientId** (`integer`): Patient ID number.
  - **gender** (`string`): Gender ("M" or "F").
  - **birthday** (`string`): Birth date.
  - **address**, **phone**, **email** (`string`): Contact information.
  - **refractiveSurgery** (`string`): Type of refractive surgery.
  - **age** (`integer`): Patient age.
  - **status** (`string`): Status (e.g., "checked").
  - **pid** (`integer`): Patient ID code.
  - **checkTime**, **createTime**, **updateTime** (`integer`): Check, creation, and update time (UNIX timestamp).
  - **isDeleted** (`boolean`): Indicates if the record is deleted.

- **Cases** (Examination records)

  - **CheckTime** (`string`): Time of examination.
  - **OD**, **OS** (Data for the right and left eye)
    - **EyeType** (`string`): Eye type ("Right" or "Left").
    - **CheckType** (`string`): Type of examination.
    - **TopographyCase** (Topography data)

      - **Data**
        - **QS** (Quality Score)
          - **OffsetX**, **OffsetY**, **OffsetZ** (`integer`): Offset values.
          - **AreaU**, **AreaD**, **AreaA** (`float`): Area measurements.
          - **HeightU**, **HeightD** (`integer`): Height values.
          - **TearN**, **TearA** (`integer`): Tear parameters.
        - **CorneaFront** (Corneal front surface data)
          - **K1**, **K2**, **Km**, **Kmax** (`float`): Corneal curvature values.
          - **Astig** (`float`): Astigmatism.
          - **AxisFlat**, **AxisSteep** (`integer`): Flat and steep axis.
          - **Rf**, **Rs**, **Rh**, **Rv**, **Rm** (`float`): Radius of curvature parameters.
          - **Rper**, **RminX**, **RminY**, **Rmin** (`float`): Radius-related parameters.
          - **SRI**, **SAI**, **IS** (`float`): Corneal asymmetry indices.

    - **AxialCase** (Axial data)

      - **Data**
        - **data** contains specific OCT measurements
          - **value** (`array of float`): Measurement values.
          - **fixed** (`integer`): Number of decimal places.
          - **scale** (`integer`): Unit conversion scale.
        - **dataFilter** (Filtered OCT data, same format as `data`)
        - **chartData** (`array`): Array of chart data.
        - **positionData** (`array of integer`): Coordinates for each layer's recognized position.
        - **snrData** (`array of float`): SNR data used for filtering and display.
        - **thresholdData** (`array of float`): Threshold data used for filtering.

    - **WTWCase** (White-to-white data)

      - **Data**
        - **pupil** (Pupil data)
          - **x**, **y** (`float`): X and Y coordinates of pupil center.
          - **r** (`float`): Pupil radius.
        - **wtw** (White-to-white data)
          - **x**, **y** (`float`): X and Y coordinates of WTW center.
          - **r** (`float`): WTW radius.
        - **center** (Center position)
          - **x**, **y** (`integer`): Center X and Y coordinates.
        - **kapa** (`object`): Kappa angle coordinates
          - **x**, **y** (`float`): X and Y values of the Kappa angle.
        - **alpha** (`object`): Alpha angle coordinates
          - **x**, **y** (`float`): X and Y values of the Alpha angle.
        - **imageurl** (`string`): URL of the pupil image.

    - **Map** (Topography map data)

      - **Data**
        - **CornealHeight** (Corneal height data)

          - **Cols**, **Rows** (`integer`): Number of columns and rows in the data grid.
          - **InvalidDataValue** (`integer`): Value marking invalid data.
          - **WorldCoords** (World coordinate range)
            - **Low** (`object`): Lowest X and Y coordinates.
              - **X**, **Y** (`float`): Minimum X and Y values.
            - **High** (`object`): Highest X and Y coordinates.
              - **X**, **Y** (`float`): Maximum X and Y values.
          - **MinimumValue**, **MaximumValue** (`string`): Minimum and maximum values in the data.
          - **Data** (`string`): Specific corneal height data.

        - **SagitalCurvatureFront** (Sagittal curvature data)

          - **Cols**, **Rows** (`integer`): Number of columns and rows in the data grid.
          - **InvalidDataValue** (`integer`): Value marking invalid data.
          - **WorldCoords** (World coordinate range)
            - **Low** (`object`): Lowest X and Y coordinates.
              - **X**, **Y** (`float`): Minimum X and Y values.
            - **High** (`object`): Highest X and Y coordinates.
              - **X**, **Y** (`float`): Maximum X and Y values.
          - **MinimumValue**, **MaximumValue** (`string`): Minimum and maximum values in the data.
          - **Data** (`string`): Specific sagittal curvature data.
