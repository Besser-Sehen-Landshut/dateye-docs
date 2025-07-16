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
│   Server reachable                                     │
│   API key valid                                        │
│   Login successful                                     │
│   "Export" criterion found (ID: 789)                   │
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
│   Server reachable                                     │
│   API key valid                                        │
│   Login successful                                     │
│    No "Export" CRM criterion found                     │
│                                                          │
│  ─────────────────────────────────────────────────────  │
│                                                          │
│  Please create it in Eye-Office:                        │
│  1. Open Eye-Office Administration                      │
│  2. Navigate to: CRM Criteria                           │
│  3. Create new criterion named "Export"                 │
│  4. Save and return here                                │
│                                                          │
│  [ Print Instructions] [Retry] [Cancel]               │
└─────────────────────────────────────────────────────────┘
```

### 3. Configuration Complete

```
┌─────────────────────────────────────────────────────────┐
│ Eye-Office API Setup                          Step 3/3   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   Setup Complete!                                      │
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

## Related Documentation

- [Eye-Office Adapter](../../adapters/eye-office.md) - Technical Details
- [Import & Export](../import-export/import-export.md) - Main UI
- [Data Formats](../../data-formats.md) - JSON Structures