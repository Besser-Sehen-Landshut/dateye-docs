# AL550ExportFile 字段说明

## 对象: AL550ExportFile

- **DeviceModel** (`string`): 设备型号。
- **Version** (`string`): 设备软件版本。

### Calibration (校准数据)

- **anchor** (锚点数据)

  - **x**, **y** (`integer`): 标定的环中心的 X 和 Y 坐标。
  - **r1**, **r2**, **r3** (`integer`): 辅助识别环的三个半径参数。
- **motorCenter** (电机中心位置)

  - **x**, **y**, **z** (`integer`): 对准中心时的 X、Y、Z 坐标。
- **octParas** (OCT 参数)

  - **zerostart1**, **zerostart2** (`integer`): 零位起始位置。
  - **topopos1**, **topopos2**, **octpos1**, **octpos2** (`integer`): 角膜地形和OCT拍摄位置。
  - **imagescale** (`integer`): 图像缩放比例。
  - **imageshowlabel** (`integer`): 图像显示标签（0 或 1）。
  - **rulmean**, **frethres** (`integer`): 标尺信号的均值和频域上的阈值。
  - **halfwavelength1**, **halfwavelength2** (`float`): 两个半波长值。
  - **signaloffset1**, **signaloffset2**, **signaloffset3**, **signaloffset4**, **signaloffset5**, **signaloffset6** (`integer`): 六个信号偏移值。
  - **ruldividepos** (`integer`): 标尺信号分割位置。
  - **signaloffset** (`integer`): 基础信号偏移量。
  - **threcorneapos1**, **threcorneapos2** (`integer`): 角膜位置阈值。
  - **threcorneathick1**, **threcorneathick2** (`integer`): 角膜厚度阈值。
  - **threacdepth1**, **threacdepth2** (`integer`): 前房深度阈值。
  - **threlensthick1**, **threlensthick2** (`integer`): 晶状体厚度阈值。
  - **threretinapos1**, **threretinapos2** (`integer`): 视网膜位置阈值。
  - **threcornea1**, **threcornea2** (`integer`): 角膜参数。
  - **threretina2lensb1**, **threretina2lensb2** (`integer`): 视网膜到晶状体后面距离。
  - **threretina2lensf1**, **threretina2lensf2** (`integer`): 视网膜到晶状体前面距离。
  - **threretina2corneaf1**, **threretina2corneaf2** (`integer`): 视网膜到角膜距离。
  - **refractiveindex0**, **refractiveindex1**, **refractiveindex2**, **refractiveindex3** (`array of float`): 四个不同眼睛结构的折射率数组。
  - **CCT_offset** (`float`): 角膜中央厚度偏移量。
- **rendercfg** (渲染配置)

  - **w**, **h** (`integer`): 渲染宽高。
  - **x**, **y** (`integer`): 渲染位置坐标。
  - **flip** (翻转配置)
    - **x**, **y** (`integer`): x、y 轴翻转配置。
- **cam_lamp** (相机和灯光配置)

  - **fixedLight** (固定灯光配置)
    - **brightness** (`integer`): 固定灯光亮度。
  - **axislength** (轴长配置)
    - **cam** (相机设置)
      - **rgain**, **ggain**, **bgain** (`integer`): 红、绿、蓝增益。
      - **blacklevel** (`float`): 黑电平。
      - **gamma** (`float`): Gamma 值。
    - **lamp** (灯光设置)
      - **infrared**, **red**, **green** (`boolean`): 红外、红光和绿光开关。
      - **ir_lightness** (`float`): 红外光亮度。
      - **center_ring_lightness**, **middle_ring_lightness**, **outer_ring_lightness** (`float`): 灯光中心、中间和外环亮度。
- **Laser** (激光位置)

  - **x**, **y** (`integer`): 激光的 X 和 Y 坐标。
- **focusThreshold** (聚焦阈值)

  - **axisLength**, **topography** (`integer`): 轴长和地形聚焦阈值。
- **dstPath** (`string`): 图像目标路径。
- **CAMERA_pixelsize** (`float`): 相机像素大小。
- **coarse**, **fine**, **ir**, **green** (`string`): 四种模型文件的路径。
- **pupil**, **wtw** (`string`): 瞳孔和白到白文件路径。
- **initX**, **initY**, **initZ** (`integer`): 初始位置 X、Y、Z 坐标。
- **maxFrontPos**, **maxBackPos** (`integer`): 最大前、后位置。
- **PZ_Motor_A**, **PZ_Motor_B** (`integer`): 电机参数。
- **AE** (`integer`): 自动曝光值。
- **cam_lamp_1** (备选灯光配置，与 `cam_lamp` 配置相同结构)。
- **focusThreshold_new** (新的聚焦阈值)

  - **axisLength**, **topography** (`integer`): 新的轴长和地形聚焦阈值。
- **isNew** (`boolean`): 是否为新版本。

### Patients (患者信息)

- **PatientInfo** (患者基本信息)

  - **_id**, **_rev** (`string`): 数据库唯一标识符。
  - **firstname**, **lastname** (`string`): 患者姓名。
  - **patientId** (`integer`): 患者编号。
  - **gender** (`string`): 性别 ("M" 或 "F")。
  - **birthday** (`string`): 出生日期。
  - **address**, **phone**, **email** (`string`): 联系信息。
  - **refractiveSurgery** (`string`): 屈光手术类型。
  - **age** (`integer`): 患者年龄。
  - **status** (`string`): 状态（如 "checked"）。
  - **pid** (`integer`): 患者 ID 编码。
  - **checkTime**, **createTime**, **updateTime** (`integer`): 检查、创建、更新时间（UNIX 时间戳）。
  - **isDeleted** (`boolean`): 是否已删除。
- **Cases** (检查记录)

  - **CheckTime** (`string`): 检查时间。
  - **OD**, **OS** (右眼、左眼数据)
    - **EyeType** (`string`): 眼别 ("Right" 或 "Left")。
    - **CheckType** (`string`): 检查类型。
    - **TopographyCase** (地形数据)

      - **Data**
        - **QS** (质量评分)
          - **OffsetX**, **OffsetY**, **OffsetZ** (`integer`): 偏移量。
          - **AreaU**, **AreaD**, **AreaA** (`float`): 区域测量。
          - **HeightU**, **HeightD** (`integer`): 高度值。
          - **TearN**, **TearA** (`integer`): 泪液参数。
        - **CorneaFront** (角膜前表面数据)
          - **K1**, **K2**, **Km**, **Kmax** (`float`): 角膜曲率。
          - **Astig** (`float`): 散光。
          - **AxisFlat**, **AxisSteep** (`integer`): 平坦轴和陡峭轴。
          - **Rf**, **Rs**, **Rh**, **Rv**, **Rm** (`float`): 曲率半径。
          - **Rper**, **RminX**, **RminY**, **Rmin** (`float`): 半径相关参数。
          - **SRI**, **SAI**, **IS** (`float`): 角膜不对称指数。
    - **AxialCase** (眼轴数据)

      - **Data**
        - **data** 包含具体OCT测量值
          - **value** (`array of float`): 测量值。
          - **fixed** (`integer`): 保留的小数位数。
          - **scale** (`integer`): 单位换算比例。
        - **dataFilter** (筛选后的OCT数据，格式同data)
        - **chartData** (`array`): 图表数据数组。
        - **positionData** (`array of integer`): 各层识别位置的横纵坐标。
        - **snrData** (`array of float`): 用于筛选和显示的信噪比数据。
        - **thresholdData** (`array of float`): 用于筛选的阈值数据。
    - **WTWCase** (白到白距离数据)

      - **Data**
        - **pupil** (瞳孔数据)
          - **x**, **y** (`float`): 瞳孔中心的 X 和 Y 坐标。
          - **r** (`float`): 瞳孔半径。
        - **wtw** (白到白数据)
          - **x**, **y** (`float`): 白到白中心的 X 和 Y 坐标。
          - **r** (`float`): 白到白半径。
        - **center** (中心位置)
          - **x**, **y** (`integer`): 中心 X 和 Y 坐标。
        - **kapa** (`object`): Kappa 角坐标
          - **x**, **y** (`float`): Kappa 角的 X 和 Y 值。
        - **alpha** (`object`): Alpha 角坐标
          - **x**, **y** (`float`): Alpha 角的 X 和 Y 值。
        - **imageurl** (`string`): 瞳孔图像的 URL。
    - **Map** (地形图数据)

      - **Data**
        - **CornealHeight** (角膜高度数据)

          - **Cols**, **Rows** (`integer`): 数据网格的列数和行数。
          - **InvalidDataValue** (`integer`): 标记无效数据的值。
          - **WorldCoords** (世界坐标范围)
            - **Low** (`object`): 最低 X 和 Y 坐标。
              - **X**, **Y** (`float`): X 和 Y 的最小值。
            - **High** (`object`): 最高 X 和 Y 坐标。
              - **X**, **Y** (`float`): X 和 Y 的最大值。
          - **MinimumValue**, **MaximumValue** (`string`): 数据的最小值和最大值。
          - **Data** (`string`): 角膜高度具体数据。
        - **SagitalCurvatureFront** (矢状曲率数据)

          - **Cols**, **Rows** (`integer`): 数据网格的列数和行数。
          - **InvalidDataValue** (`integer`): 标记无效数据的值。
          - **WorldCoords** (世界坐标范围)
            - **Low** (`object`): 最低 X 和 Y 坐标。
              - **X**, **Y** (`float`): X 和 Y 的最小值。
            - **High** (`object`): 最高 X 和 Y 坐标。
              - **X**, **Y** (`float`): X 和 Y 的最大值。
          - **MinimumValue**, **MaximumValue** (`string`): 数据的最小值和最大值。
          - **Data** (`string`): 矢状曲率具体数据。
