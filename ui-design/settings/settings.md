# Settings Screen

Simple configuration for DATEYE's runtime behavior.

## Purpose

The Settings screen provides essential configuration options for DATEYE. Following the philosophy of simplicity, it contains only necessary settings. Import/Export configuration has dedicated screens accessible from here.

## Layout Structure

```
┌─────────────────────────────────────────────────────────┐
│                                           [_] [□] [x]   │
├─────────────────────────────────────────────────────────┤
│ [LOGO] Dashboard │ Connections │ History │ Settings │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  General Settings                                        │
│  ──────────────────────────────────────────────────────  │
│                                                          │
│  Language                                                │
│  [▼ English              ]                               │
│     German                                               │
│                                                          │
│  Startup                                                 │
│  ☑ Start with system                                    │
│  ☑ Start minimized to tray                              │
│                                                          │
│  Data Management                                         │
│  ┌─────────────────────┐  ┌─────────────────────┐      │
│  │   Import Settings   │  │   Export Settings   │      │
│  │   Configure folders │  │   Manage targets    │      │
│  └─────────────────────┘  └─────────────────────┘      │
│                                                          │
│  ─────────────────────────────────────────────────────  │
│                                                          │
│  About DATEYE                                            │
│  Version 1.0.0                                           │
│  © 2024 DATEYE · MIT License                            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Visual Design

### Layout Principles
- Single column, no sidebar needed
- Clear sections with horizontal dividers
- Immediate saving (no Save/Cancel buttons)
- Cards for navigation to sub-settings

### Visual Elements
- **Dropdown**: Standard system dropdown for language
- **Checkboxes**: Simple toggles for startup options
- **Cards**: Clickable areas for import/export settings
- **About**: Subtle footer area

## Settings Structure

### General Settings

#### Language Selection
```
- English (Default)
- German
- System Default (future)
```
Changes apply immediately throughout the UI.

#### Startup Options
```
☑ Start with system
  - Adds DATEYE to OS startup
  - Platform-specific implementation

☑ Start minimized to tray
  - Opens directly in system tray
  - No window shown at startup
```

#### Data Management Links
Two cards that navigate to dedicated screens:
- **Import Settings**: Configure watch folders and adapters
- **Export Settings**: Manage export targets and devices

### About Section
```
Version: 1.0.0
License: MIT License
Copyright: © 2024 DATEYE
```

## Core Functions

### 1. Auto-Save
- All changes saved immediately
- No Save/Cancel workflow
- Visual feedback on change (subtle animation)

### 2. Live Updates
- Language change immediate
- No restart required
- File watcher detects external changes

### 3. Platform-Aware
- Startup options adapt to OS
- Correct terminology per platform
- Native system integration

## State Management

```typescript
interface SettingsState {
  // Core settings
  language: 'en' | 'de' | 'system';
  startWithSystem: boolean;
  startMinimized: boolean;
  
  // Runtime state
  isLoading: boolean;
  lastSaved: DateTime;
}

// Separate state for sub-screens
interface ImportSettingsState { ... }
interface ExportSettingsState { ... }
```

## Storage

Settings are stored as JSON in platform-specific locations:

**File**: `settings.json`

**Locations**:
- Windows: `%APPDATA%/DATEYE/settings.json`
- macOS: `~/Library/Application Support/DATEYE/settings.json`
- Linux: `~/.config/DATEYE/settings.json`

**Format**:
```json
{
  "language": "en",
  "startup": {
    "autostart": true,
    "minimizeOnLaunch": true
  },
  "version": "1.0.0"
}
```

## Future Extensions (v2+)

If actually needed:
- Notification settings
- Theme selection (if requested)
- Advanced/Debug settings:
  - Log level (Info/Debug/Verbose)
  - Performance options
  - Cache management
- Backup/Restore settings
- Cloud sync settings

## Keyboard Navigation

- `Tab`: Navigate between controls
- `Space`: Toggle checkboxes
- `Enter`: Activate cards/buttons
- `↑↓`: Navigate dropdown options

## Localization

All text uses the app's i18n system:
- Immediate language switching
- No hardcoded strings
- Fallback to English if keys missing

## Responsive Behavior

- Minimum width: 600px
- Maximum width: 800px (centered)
- Scales appropriately on larger screens

## Testing Considerations

1. **Language switching**: Verify all UI updates
2. **Startup registration**: Test per platform
3. **File watching**: External changes should reflect
4. **Navigation**: Cards should route correctly
5. **Auto-save**: Changes persist immediately

## Related Screens

- [Import & Export](../import-export/import-export.md) - Detailed data management
- [Dashboard](../dashboard/dashboard.md) - Return to main view
