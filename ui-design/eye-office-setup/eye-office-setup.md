# Eye-Office API Setup

Step-by-step guide for setting up Eye-Office REST API integration.

## Purpose

This guide walks through setting up the Eye-Office API connection, including CRM criteria configuration and initial synchronization.

## Prerequisites

### In Eye-Office Administration
1. **CRM Criterion "Export"**
   - Navigation: Administration → CRM Criteria
   - Create new criterion named "Export" (capital E)
   - Choose distinctive color (e.g., green #00FF00)
   - Save changes

2. **Mark patients for export**
   - Open each patient record to be synchronized
   - Check "Export" in the CRM criteria section
   - Save patient

### From Eye-Office Support
- API key for your installation
- API endpoint URL (typically port 4450)

## Setup Flow

### 1. Initial Connection

```
┌─────────────────────────────────────────────────────────┐
│ Eye-Office API Setup                          Step 1/3   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Connect DATEYE to your Eye-Office installation         │
│                                                          │
│  Server URL                                              │
│  ┌─────────────────────────────────────────────────┐   │
│  │ https://eye-office.local               :4450    │   │
│  └─────────────────────────────────────────────────┘   │
│  Example: https://eye-office.local:4450                 │
│                                                          │
│  API Key                                                 │
│  ┌─────────────────────────────────────────────────┐   │
│  │ ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●        [Show]    │   │
│  └─────────────────────────────────────────────────┘   │
│  Get this from Eye-Office support                       │
│                                                          │
│  Eye-Office Username                                     │
│  ┌─────────────────────────────────────────────────┐   │
│  │ dr.schmidt                                      │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
│  Eye-Office Password                                     │
│  ┌─────────────────────────────────────────────────┐   │
│  │ ●●●●●●●●●●●●                         [Show]    │   │
│  └─────────────────────────────────────────────────┘   │
│  Use your regular Eye-Office login                      │
│                                                          │
│             [Back] [Test Connection]                     │
└─────────────────────────────────────────────────────────┘
```

### 2. Connection Test & CRM Detection

#### Success Case
```
┌─────────────────────────────────────────────────────────┐
│ Eye-Office API Setup                          Step 2/3   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Testing Connection...                                   │
│                                                          │
│  ✅ Server reachable                                     │
│  ✅ API key valid                                        │
│  ✅ Login successful                                     │
│  ✅ "Export" criterion found (ID: 789)                   │
│                                                          │
│  Connection successful!                                  │
│                                                          │
│                              [Continue]                  │
└─────────────────────────────────────────────────────────┘
```

#### Missing CRM Criterion
```
┌─────────────────────────────────────────────────────────┐
│ Eye-Office API Setup                          Step 2/3   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Testing Connection...                                   │
│                                                          │
│  ✅ Server reachable                                     │
│  ✅ API key valid                                        │
│  ✅ Login successful                                     │
│  ⚠️  No "Export" CRM criterion found                     │
│                                                          │
│  ─────────────────────────────────────────────────────  │
│                                                          │
│  Please create it in Eye-Office:                        │
│  1. Open Eye-Office Administration                      │
│  2. Navigate to: CRM Criteria                           │
│  3. Create new criterion named "Export"                 │
│  4. Save and return here                                │
│                                                          │
│  [📄 Print Instructions] [Retry] [Cancel]               │
└─────────────────────────────────────────────────────────┘
```

### 3. Configuration Complete

```
┌─────────────────────────────────────────────────────────┐
│ Eye-Office API Setup                          Step 3/3   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ✅ Setup Complete!                                      │
│                                                          │
│  Connection Details:                                     │
│  • Server: eye-office.local                             │
│  • User: dr.schmidt                                     │
│  • Export criterion ID: 789                             │
│                                                          │
│  Sync Settings:                                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │ ☑ Enable automatic sync                         │   │
│  │                                                 │   │
│  │ Sync interval:  [▼ Every 5 minutes    ]        │   │
│  │                                                 │   │
│  │ ☑ Import visual acuity (visusCc)               │   │
│  │ ☑ Import prism values                          │   │
│  │ ☑ Import objective refraction                  │   │
│  │ ☑ Import subjective refraction                 │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
│  Found 47 patients marked with "Export"                 │
│                                                          │
│                              [Start Initial Sync]        │
└─────────────────────────────────────────────────────────┘
```

## Import & Export Screen Integration

### New Tab for Eye-Office API

Eye-Office appears as an option in both manual and automatic import:

```
┌─────────────────────────────────────────────────────────┐
│ ← Dashboard    Import & Export                           │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────────────┬──────────────────────┐        │
│  │ Import              │ Export                │        │
│  └─────────────────────┴──────────────────────┘        │
│                                                          │
│  Automatic Sync Sources                                  │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Eye-Office API      eye-office.local         ✓ │   │
│  │    Every 5 minutes • Export tag filter         │   │
│  │    Last: 47 patients synced 2 min ago         │   │
│  │                                                 │   │
│  │                    [+ Add Sync Source]          │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
│  Watch Folders                                           │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Topcon MYAH         C:\Import\MYAH           ✓ │   │
│  │    Topcon MYAH • Keep files                    │   │
│  │    Last: 1 file imported 1 hour ago           │   │
│  │                                                 │   │
│  │ AL550               D:\AL550\Export          ⏸ │   │
│  │    Mediworks AL550 • Disabled                  │   │
│  │    Last: No imports yet                       │   │
│  │                                                 │   │
│  │                        [+ Add Watch Folder]     │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
│  Recent Imports                                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │ ✅ 14:32 - Anna Schmidt                         │   │
│  │    Updated: Refraction, Visual Acuity           │   │
│  │                                                 │   │
│  │ ✅ 14:28 - Max Weber                           │   │
│  │    New patient with 3 refractions               │   │
│  │                                                 │   │
│  │ ✅ 14:15 - Lisa Meyer                          │   │
│  │    Updated: Visual Acuity only                  │   │
│  │                                                 │   │
│  │ ⚠️  14:10 - Import Warning                      │   │
│  │    3 patients missing "Export" tag              │   │
│  │    [View Details]                               │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Eye-Office Instructions Dialog

Accessible via [Configure] Button:

```
┌─────────────────────────────────────────────────────────┐
│ Eye-Office Configuration                            [X]  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Current Setup:                                          │
│  • Server: eye-office.local                             │
│  • Export criterion ID: 789                             │
│  • Sync interval: 5 minutes                             │
│                                                          │
│  ─────────────────────────────────────────────────────  │
│                                                          │
│  To export patients from Eye-Office:                    │
│                                                          │
│  1. In Eye-Office patient record:                       │
│     • Open CRM criteria section                         │
│     • Check "Export" checkbox                           │
│     • Save patient                                      │
│                                                          │
│  2. Only marked patients will sync to DATEYE            │
│                                                          │
│  3. Changes sync automatically every 5 minutes          │
│                                                          │
│  [🖨️ Print Instructions] [Change Settings] [Close]      │
└─────────────────────────────────────────────────────────┘
```

### Missing Export Tag Warning

```
┌─────────────────────────────────────────────────────────┐
│ Patients Without Export Tag                         [X]  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  The following patients were updated in Eye-Office      │
│  but don't have the "Export" tag:                      │
│                                                          │
│  • Mueller, Hans (ID: 12345)                           │
│  • Fischer, Eva (ID: 12346)                            │
│  • Weber, Klaus (ID: 12347)                            │
│                                                          │
│  To include them in DATEYE:                            │
│  1. Open each patient in Eye-Office                    │
│  2. Add "Export" to CRM criteria                       │
│  3. Save patient                                        │
│  4. They'll sync on next interval                      │
│                                                          │
│                              [OK]                        │
└─────────────────────────────────────────────────────────┘
```

## State Flow

### Setup States

```typescript
enum SetupState {
  Initial,        // Show connection form
  Testing,        // Test connection
  MissingCRM,     // Export criterion not found
  Ready,          // All checks passed
  Syncing         // Initial sync running
}
```

### Runtime States

```typescript
interface EyeOfficeApiState {
  connection: {
    status: 'connected' | 'disconnected' | 'error';
    lastPing: DateTime;
    sessionId?: string;
  };

  sync: {
    isRunning: boolean;
    lastSync: DateTime;
    nextSync: DateTime;
    patientCount: number;
    newCount: number;
  };

  config: {
    url: string;
    username: string;
    crmExportId: number;
    syncInterval: number;
    importOptions: {
      visualAcuity: boolean;
      prismValues: boolean;
      objectiveRefraction: boolean;
      subjectiveRefraction: boolean;
    };
  };
}
```

## Error Handling

### Connection Error

```
┌─────────────────────────────────────────────────────────┐
│ Connection Error                                    [X]  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ❌ Could not connect to Eye-Office                      │
│                                                          │
│  Error: Connection timeout (eye-office.local:4450)      │
│                                                          │
│  Possible causes:                                        │
│  • Eye-Office server not running                        │
│  • Firewall blocking port 4450                          │
│  • Incorrect server URL                                 │
│  • Network connectivity issue                           │
│                                                          │
│  [Retry] [Edit Settings] [Cancel]                       │
└─────────────────────────────────────────────────────────┘
```

### Authentication Error

```
┌─────────────────────────────────────────────────────────┐
│ Authentication Failed                               [X]  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ❌ Invalid credentials                                   │
│                                                          │
│  Please verify:                                          │
│  • Username is correct                                  │
│  • Password is current                                  │
│  • User has API access rights                           │
│  • Account is not locked                                │
│                                                          │
│  Contact Eye-Office administrator if needed             │
│                                                          │
│                    [Edit Credentials] [Cancel]           │
└─────────────────────────────────────────────────────────┘
```

## Dashboard Integration

The main dashboard shows Eye-Office sync status:

```
Recent Activity
───────────────────────────────────────────
[14:32] ✓ API Import: 3 patients from Eye-Office
[14:28] ✓ Export: 2 patients → AL550
[14:15] ⚠ Eye-Office: 3 patients missing Export tag
```

## Security Considerations

1. **Credential Storage**
   - Username/password encrypted in `identity.enc`
   - API key encrypted with system key
   - Session ID only in memory

2. **Network Security**
   - HTTPS required for API connection
   - Certificate validation enabled
   - No credentials in logs

3. **Access Control**
   - Uses existing Eye-Office user permissions
   - Read-only access sufficient
   - No admin rights required

## Success Metrics

- Setup completion < 5 minutes
- No failed syncs due to configuration
- Clear error messages for troubleshooting
- Minimal Eye-Office admin intervention

## Related Documentation

- [Eye-Office Adapter](../../adapters/eye-office.md) - Technical Details
- [Import & Export](../import-export/import-export.md) - Main UI
- [Data Formats](../../data-formats.md) - JSON Structures
