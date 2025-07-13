# Connections Screen

Import/Export workflow management interface for medical device integration.

## Concept

**ImportAdapter/ExportAdapter Architecture:** DATEYE uses separate adapter interfaces for medical device integration. Users configure import sources and export targets independently, then create logical connections between them.

**Example Workflows:**
- MYAH files → DATEYE (ImportAdapter for file processing)
- DATEYE → AL550 device (ExportAdapter for patient registration)
- Eye-Office API → DATEYE (ImportAdapter for practice management sync)
- DATEYE → File backup (ExportAdapter for data archiving)

## Layout Structure

### Main View - Active Connections

```
┌─────────────────────────────────────────────────────────┐
│                                           [_] [□] [x]   │
├─────────────────────────────────────────────────────────┤
│ [LOGO] Dashboard │ Connections │ History │ Settings     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Import & Export Connections           [New Connection] │
│  ──────────────────────────────────────────────────────  │
│                                                          │
│  Active Import Sources                                   │
│  ┌─────────────────────────────────────────────────┐   │
│  │ 📁 MYAH Files → DATEYE                     ✓   │   │
│  │   Watch folder: C:\Import\MYAH                 │   │
│  │   Status: 3 files imported today               │   │
│  │   [Configure] [Pause]                          │   │
│  │                                                 │   │
│  │ 🔗 Eye-Office API → DATEYE                ⏸   │   │
│  │   Sync every 5 minutes                         │   │
│  │   Status: Paused (API maintenance)             │   │
│  │   [Configure] [Resume]                          │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
│  Active Export Targets                                   │
│  ┌─────────────────────────────────────────────────┐   │
│  │ DATEYE → 📟 AL550 Device               ✓   │   │
│  │   Patient registration enabled                  │   │
│  │   Status: 2 patients exported 1 hour ago       │   │
│  │   [Configure] [Test Connection]                 │   │
│  │                                                 │   │
│  │ DATEYE → 💾 File Backup                   ✓   │   │
│  │   Daily backup to external drive               │   │
│  │   Status: Last backup completed 6 hours ago    │   │
│  │   [Configure] [Run Now]                         │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
│  Manual Operations                                       │
│  ┌─────────────────────────────────────────────────┐   │
│  │ [Import Files] [Export Data] [Batch Processing] │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Empty State - No Connections

```
┌─────────────────────────────────────────────────────────┐
│  No import sources or export targets configured         │
│                                                          │
│  Set up data workflows between your medical devices.    │
│  Configure import sources and export targets separately.│
│                                                          │
│  Examples:                                               │
│  • Import: MYAH Files → DATEYE (File monitoring)       │
│  • Export: DATEYE → AL550 Device (Patient registration)│
│  • Import: Eye-Office API → DATEYE (Scheduled sync)    │
│                                                          │
│                    [New Connection]                      │
└─────────────────────────────────────────────────────────┘
```

## New Connection Dialog

### Import Source Configuration

```
┌───────────────────────────────────────────────────────────────────────┐
│ Configure Import Source                                           [X] │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Select Import Adapter:                                               │
│  ┌─────────────────────────────────────────────────┐                 │
│  │ ◉ 📁 MYAH Files                                 │                 │
│  │   Import XML files from Topcon MYAH device     │                 │
│  │   Source: File system monitoring               │                 │
│  └─────────────────────────────────────────────────┘                 │
│                                                                       │
│  ┌─────────────────────────────────────────────────┐                 │
│  │ ○ 🔗 Eye-Office API                             │                 │
│  │   Import patient data via REST API             │                 │
│  │   Source: Practice management system           │                 │
│  └─────────────────────────────────────────────────┘                 │
│                                                                       │
│  ┌─────────────────────────────────────────────────┐                 │
│  │ ○ 📂 Manual File Import                         │                 │
│  │   One-time file import                         │                 │
│  │   Source: User file selection                  │                 │
│  └─────────────────────────────────────────────────┘                 │
│                                                                       │
│  ─────────────────────────────────────────────────────────────────  │
│                                                                       │
│  📁 MYAH Files Configuration                                         │
│                                                                       │
│  Watch Folder: [C:\Import\MYAH\           ] [Browse]                 │
│  File Pattern: [*.xml                     ]                          │
│  Processing:   ☑ Delete files after import                          │
│                ☑ Create backup copies                               │
│                                                                       │
│                                   [Test] [Save Import Source]        │
└───────────────────────────────────────────────────────────────────────┘
```

### Export Target Configuration

```
┌───────────────────────────────────────────────────────────────────────┐
│ Configure Export Target                                           [X] │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Select Export Adapter:                                               │
│  ┌─────────────────────────────────────────────────┐                 │
│  │ ◉ 📟 AL550 Device                               │                 │
│  │   Export patient data to optical biometer      │                 │
│  │   Target: HTTP API (192.168.1.100)            │                 │
│  └─────────────────────────────────────────────────┘                 │
│                                                                       │
│  ┌─────────────────────────────────────────────────┐                 │
│  │ ○ 💾 File Export                                │                 │
│  │   Export data to JSON/CSV files               │                 │
│  │   Target: File system                          │                 │
│  └─────────────────────────────────────────────────┘                 │
│                                                                       │
│  ┌─────────────────────────────────────────────────┐                 │
│  │ ○ ☁️ Myopia.cloud                               │                 │
│  │   Export anonymized data for analytics         │                 │
│  │   Target: Cloud platform                       │                 │
│  └─────────────────────────────────────────────────┘                 │
│                                                                       │
│  ─────────────────────────────────────────────────────────────────  │
│                                                                       │
│  📟 AL550 Device Configuration                                       │
│                                                                       │
│  Device IP:    [192.168.1.100        ]                              │
│  Port:         [8080                 ]                              │
│  Export Mode:  ◉ Auto-export  ○ Manual only                         │
│  Data Filter:  ☑ New patients only                                  │
│                ☑ Include patient demographics                       │
│                                                                       │
│                                   [Test] [Save Export Target]        │
└───────────────────────────────────────────────────────────────────────┘
```

### Key Simplifications

**Separate Configuration:**
- **Import Sources** configured independently
- **Export Targets** configured independently
- **Logical Connections** created through workflow management

**Adapter-Specific Forms:**
- Each ImportAdapter has custom configuration UI
- Each ExportAdapter has custom configuration UI
- Type-safe validation in adapter implementations

**Clear Data Flow:**
- Import: Device/API → DATEYE
- Export: DATEYE → Device/File/Cloud
- Manual operations available for one-time tasks

## Available Import Adapters

### File-Based Import

| Adapter | Configuration | Data Source |
|---------|---------------|-------------|
| **MYAH Files** | Watch folder, file patterns | XML files from Topcon MYAH |
| **IOLMaster Files** | DICOM folder monitoring | DICOM files from ZEISS devices |
| **Manual Import** | File browser | User-selected files |

### API-Based Import

| Adapter | Configuration | Data Source |
|---------|---------------|-------------|
| **Eye-Office API** | REST endpoint, credentials | Practice management system |
| **Cloud Import** | API credentials, sync schedule | Cloud platforms |

## Available Export Adapters

### Device Export

| Adapter | Configuration | Target |
|---------|---------------|--------|
| **AL550 Device** | IP address, patient filter | HTTP API for patient registration |
| **Eye-Office Export** | API credentials | Practice management system |

### File/Cloud Export

| Adapter | Configuration | Target |
|---------|---------------|--------|
| **File Export** | Output folder, format (JSON/CSV) | Local file system |
| **Myopia.cloud** | API credentials, anonymization | Cloud analytics platform |

## Connection Management

### Import Source States

```typescript
enum ImportSourceStatus {
  active,      // Monitoring and processing files/API
  paused,      // User-paused
  error,       // Connection/processing error  
  disabled,    // User-disabled
}
```

### Export Target States

```typescript
enum ExportTargetStatus {
  active,      // Ready to receive exports
  testing,     // Connection test in progress
  error,       // Connection/export error
  disabled,    // User-disabled
}
```

### Status Indicators

- 🟢 **Active**: Processing data successfully
- 🟡 **Warning**: Minor issues, auto-retrying
- 🔴 **Error**: Manual intervention required
- ⏸️ **Paused**: User-paused or scheduled downtime

### Connection Actions

```
[Configure] - Modify adapter configuration
[Test] - Validate connection/configuration
[Pause/Resume] - Toggle active state
[View Data] - Browse imported/exported data
[Delete] - Remove import source or export target
```

## State Management

```typescript
interface ConnectionsState {
  // Import sources
  importSources: ImportSource[];
  
  // Export targets  
  exportTargets: ExportTarget[];
  
  // Manual operations
  isImporting: boolean;
  isExporting: boolean;
  
  // Discovery
  availableAdapters: AdapterInfo[];
}

interface ImportSource {
  id: string;
  adapterId: string;           // 'topcon_myah', 'eye_office_api'
  name: string;                // User-friendly name
  config: Map<string, dynamic>; // Adapter-specific configuration
  status: ImportSourceStatus;
  lastImport?: DateTime;
  statistics: ImportStatistics;
}

interface ExportTarget {
  id: string;
  adapterId: string;           // 'al550_export', 'file_export'
  name: string;                // User-friendly name
  config: Map<string, dynamic>; // Adapter-specific configuration
  status: ExportTargetStatus;
  lastExport?: DateTime;
  statistics: ExportStatistics;
}
```

## Error Handling & Recovery

### Import Errors

**File Processing Issues:**
```
🔴 MYAH Import Error
   Failed to parse patient_001.xml (Invalid XML format)
   
   [Skip File] [Retry] [View Details]
```

**API Connection Issues:**
```
🔴 Eye-Office API Error
   Connection timeout (https://eye-office.local:4450)
   
   [Test Connection] [Edit Configuration] [Retry]
```

### Export Errors

**Device Offline:**
```
🔴 AL550 Export Error
   Device unreachable (192.168.1.100:8080)
   
   [Test Connection] [Edit Configuration] [Queue for Retry]
```

**Data Validation:**
```
🟡 Export Warning
   2 patients skipped (missing required fields)
   8 patients exported successfully
   
   [View Details] [Export Failed Items] [Continue]
```

## Responsive Behavior

- **< 1400px**: Hide detailed statistics
- **< 1200px**: Stack import/export sections vertically
- **< 1024px**: Simplified connection cards
- **< 768px**: Mobile-optimized layout with tabs

## Performance Optimization

### Import Processing
- Stream processing for large files
- Parallel processing for multiple sources
- Progress indicators for long imports

### Export Operations
- Batch operations for multiple patients
- Retry mechanisms with exponential backoff
- Progress tracking for network operations

## Future Enhancements

### Advanced Import Features
```
Conditional import: "Only new patients since last sync"
Data transformation: Custom field mapping
Multi-format support: DICOM, HL7, CSV
```

### Advanced Export Features
```
Scheduled exports: "Daily backup at 2 AM"
Conditional exports: "Only patients with recent exams"
Multi-target exports: Send to multiple destinations
```

## Success Metrics

- Import configuration time: < 3 minutes for file sources
- Export setup time: < 5 minutes for network devices
- Error recovery rate: > 85% automatic resolution
- Data processing reliability: > 99% success rate

## Related Documentation

- [ImportAdapter Development](../adapter-development.md) - Implementing import adapters
- [ExportAdapter Development](../adapter-development.md) - Implementing export adapters
- [Dashboard](../dashboard/dashboard.md) - Import/export status overview
- [History](../history/history.md) - Complete operation logs
