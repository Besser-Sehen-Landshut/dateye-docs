# Eye-Office Sync Details

Extended UI specifications for Eye-Office API synchronization dialogs.

## Sync Details Dialog

Dialog displayed when viewing Eye-Office API sync source details:

```
┌─────────────────────────────────────────────────────────┐
│ Eye-Office API Sync                                [X]  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Status: Connected                                       │
│  Server: eye-office.local:4450                          │
│  User: dr.schmidt                                       │
│                                                          │
│  ─────────────────────────────────────────────────────  │
│                                                          │
│  Sync Statistics:                                        │
│  • Last sync: 2 minutes ago (14:32)                    │
│  • Next sync: in 3 minutes                             │
│  • Sync interval: Every 5 minutes                      │
│                                                          │
│  • Total patients with "Export" tag: 47                │
│  • Synced today: 47 patients                           │
│  • New since last sync: 3                              │
│  • Updates since last sync: 12                         │
│                                                          │
│  Data Settings:                                          │
│  ☑ Visual acuity (visusCc)                             │
│  ☑ Prism values                                        │
│  ☑ Objective refraction                                │
│  ☑ Subjective refraction                               │
│                                                          │
│  [Sync Now] [Pause] [Configure] [View Log] [Close]     │
└─────────────────────────────────────────────────────────┘
```

## Add Sync Source Dialog

Initial dialog for adding new automatic sync sources:

```
┌─────────────────────────────────────────────────────────┐
│ Add Automatic Sync Source                          [X]  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Source Type                                             │
│  ○ Eye-Office API                                       │
│  ○ Cloud Service (Future)                               │
│  ○ Network Device (Future)                              │
│                                                          │
│  [Continue] [Cancel]                                     │
└─────────────────────────────────────────────────────────┘
```

## Dialog Actions

### Sync Details Dialog
- **Sync Now** - Triggers immediate synchronization
- **Pause** - Temporarily disables automatic sync
- **Configure** - Opens Eye-Office API setup wizard
- **View Log** - Opens filtered event log for Eye-Office sync events
- **Close** - Returns to Import & Export screen

### Add Sync Source Dialog
- **Continue** - Proceeds to selected source type setup
- **Cancel** - Returns to Import & Export screen

## State Management

### Sync Status States
- Connected - Active connection, successful sync
- Disconnected - Unable to reach server
- Paused - User-initiated sync pause
- Error - Authentication or other error

### Statistics Update
- Real-time update when dialog is open
- Cached values when closed
- Refresh on "Sync Now" action

## Related Documentation

- [Eye-Office Setup](eye-office-setup.md) - Main setup wizard
- [Import & Export](../import-export/import-export.md) - Parent screen
- [Eye-Office Adapter](../../adapters/eye-office.md) - Technical implementation
