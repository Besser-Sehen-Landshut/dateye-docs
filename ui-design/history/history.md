# History Screen

Complete record of all DATEYE operations and system activities.

## Purpose

The History screen provides comprehensive visibility into all system activities, not just today's events. It serves as the central location for troubleshooting, auditing, and manual export selection.

## Layout Structure

```
┌─────────────────────────────────────────────────────────┐
│                                           [_] [□] [x]   │
├─────────────────────────────────────────────────────────┤
│ [LOGO] Dashboard │ Connections │ History │ Settings │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  All Activities                       [Export Selected]  │
│                                                          │
│  [▼ Last 7 days    ] [▼ All Types  ] [Search...     ]  │
│                                                          │
│  ┌──┬─────────────────────────────────────────────────┐ │
│  │☐│ [2024-07-11 14:32] ✓ Transfer: MYAH → AL550      │ │
│  │ │ Schmidt_Anna_2024.xml - 3 measurements            │ │
│  │ │ Patient: Anna Schmidt (2010-03-15)               │ │
│  ├──┼─────────────────────────────────────────────────┤ │
│  │☐│ [2024-07-11 14:28] ✓ Transfer: Eye-Office → USB  │ │
│  │ │ Anna Schmidt, Hans Mueller - Auto Transfer       │ │
│  │ │ Target: Backup Drive - Success                   │ │
│  ├──┼─────────────────────────────────────────────────┤ │
│  │☐│ [2024-07-11 14:15] ⚠ Transfer: AL550 → Cloud     │ │
│  │ │ Connection timeout - Retry 1/3                    │ │
│  │ │ Next retry: 14:45                                │ │
│  ├──┼─────────────────────────────────────────────────┤ │
│  │☐│ [2024-07-11 14:10] ✓ Sync: Eye-Office API        │ │
│  │ │ 15 patients synchronized - Auto Sync             │ │
│  │ │ Duration: 2.3 seconds                            │ │
│  ├──┼─────────────────────────────────────────────────┤ │
│  │☐│ [2024-07-11 13:58] ✓ Transfer: IOLMaster → Core  │ │
│  │ │ bilateral_exam_2024.dcm - Manual Transfer        │ │
│  │ │ Patient: Lisa Meyer (1955-08-22)                 │ │
│  └──┴─────────────────────────────────────────────────┘ │
│                                                          │
│  Showing 89 of 1,247 events               [Load More]   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Visual Design

### Activity Timeline
- **Workflow Activities**: Clear "Source → Target" format for transfers
- **Regular Activities**: Clean white cards with hover effects
- **Enhanced Details**: Multi-line display with filenames, patient names
- **Visual Hierarchy**: Time → Type → Details → Metadata
- **Monospace Timestamps**: Better alignment and technical feel

### Tab Navigation
- **Logo placement**: DATEYE logo on the left side of tabs
- **Four main tabs**: Dashboard, Connections, History, Settings
- **Active tab**: Pill-style background with light blue tint (#0087BA at 10% opacity)
- **Icons**: Each tab has an icon for better recognition
- **Responsive behavior**:
  - **Desktop (> 1100px)**: Full logo + icons with complete text
  - **Tablet (768-1100px)**: Smaller logo + icons with shortened text
  - **Mobile (< 768px)**: Text only (no logo, no icons), optimized for readability
- **Consistent padding**: 32px left/right at all screen sizes

### Smart Filtering
- Filter chips show counts: "All (22)", "Transfers (12)", etc.
- Numbers update dynamically as activities complete
- Quick visual indication of activity distribution
- Helps prioritize attention (e.g., "Errors (2)" draws eye)

## Core Functions

### 1. Complete History
- All events stored in `history.ndjson`
- Infinite scroll with lazy loading
- No data expiry (except manual archiving)
- Complete audit trail for compliance

### 2. Advanced Filtering
```
Time Ranges:
- Today
- Last 7 days
- Last 30 days
- Last 3 months
- Custom range
- All time

Activity Types:
- All Activities
- Workflow Transfers
- Manual Operations
- System Events
- Errors Only
- Scheduled Tasks
```

### 3. Activity Details
Each activity shows:
- **Primary Info**: Type, source, target, status
- **Secondary Info**: Affected files/patients
- **Metadata**: Duration, retry count, error details
- **Expandable**: Click for complete JSON view

### 4. Manual Export Selection
```
1. Select activities via checkboxes
2. Click "Export Selected"
3. Choose target device/folder
4. Confirm export
5. Track in export queue
```

### 5. Search Capabilities
- Patient names (decrypted on-the-fly)
- Filenames
- Device/adapter names
- Error messages
- Activity IDs

## State Management

```typescript
interface HistoryState {
  // Filter state
  timeRange: 'today' | '7days' | '30days' | '3months' | 'all';
  activityType: 'all' | 'transfer' | 'manual' | 'system' | 'error';
  searchQuery: string;

  // Activity data
  activities: ActivityEntry[];
  totalCount: number;
  hasMore: boolean;
  isLoading: boolean;

  // Selection state
  selectedActivityIds: Set<string>;

  // UI state
  expandedActivityIds: Set<string>;
  scrollPosition: number;
}

interface ActivityEntry {
  id: string;
  timestamp: DateTime;
  type: 'transfer' | 'import' | 'export' | 'sync' | 'system';
  mode: 'automatic' | 'manual' | 'scheduled';
  status: 'success' | 'warning' | 'error' | 'pending';
  
  // Workflow context
  workflow?: {
    source: string;  // "MYAH", "Eye-Office"
    target: string;  // "AL550", "Backup"
    name: string;    // "MYAH → AL550"
  };

  // Legacy support
  adapter?: string;
  file?: string;
  target?: string;
  
  // Common data
  patientData?: {
    name: string;  // Decrypted for display
    birthDate: string;
    externalId: string;
  };
  measurementCount?: number;
  duration?: number;  // milliseconds
  error?: string;
  retryCount?: number;
  nextRetry?: DateTime;
}
```

## Responsive Behavior

- **< 1400px**: Patient details hidden, shown on expand
- **< 1200px**: Compact timestamps (time only)
- **< 1024px**: Single-line activities with expand button
- **Always**: Checkbox column maintained for selection

## Performance

### Optimization Strategies
- Virtual scrolling for large lists
- Lazy decrypt of patient names
- Debounced search (300ms)
- Cached filter results
- Progressive loading (50 activities at once)

### Loading States
```
Initial Load:
- Show skeleton rows
- Load first 50 activities
- Enable interaction immediately

Scroll Loading:
- Show "Loading..." indicator
- Fetch next 50 activities
- Seamlessly append to list
```

## User Flows

### Troubleshooting Flow
```
Error in Dashboard
  │
  ├─→ Click "History" tab
  │
  ├─→ Filter: "Errors Only"
  │
  ├─→ Find error activity
  │     │
  │     ├─→ Click to expand
  │     ├─→ Read error details
  │     └─→ Copy error for support
  │
  └─→ Take corrective action
```

### Manual Export Flow
```
History Tab
  │
  ├─→ Search for patient
  │
  ├─→ Select relevant activities
  │     │
  │     ├─→ Check multiple boxes
  │     └─→ "Export Selected" enabled
  │
  ├─→ Click "Export Selected"
  │     │
  │     ├─→ Target selection dialog
  │     ├─→ Choose device/folder
  │     └─→ Confirm export
  │
  └─→ Monitor in Dashboard
```

### Audit Review Flow
```
Compliance Request
  │
  ├─→ History Tab
  │
  ├─→ Set time range
  │
  ├─→ Search patient name
  │
  └─→ Export matching activities
        │
        ├─→ Select all results
        ├─→ Export as JSON/CSV
        └─→ Save for records
```

## Security Considerations

### Patient Name Display
- Names decrypted on-demand from `identity.enc`
- Never stored in UI state
- Cleared from memory after display
- Search operates on encrypted IDs first

### Activity Selection
- Maximum 100 activities selectable at once
- Confirmation required for bulk operations
- Export creates new log entries
- Original activities never modified

## Keyboard Shortcuts

- `Ctrl/Cmd + F`: Focus search field
- `Space`: Toggle selection on focused row
- `Ctrl/Cmd + A`: Select all visible
- `Escape`: Clear selection
- `Enter`: Expand/collapse focused activity

## Localization

All UI text localized:
- Time format respects system locale
- Status messages translated
- Error descriptions in user language
- Technical IDs remain English

## Success Metrics

- Find specific activity: < 5 seconds
- Export selected activities: < 3 clicks
- Browse through 1000 activities: < 100ms per page
- Search response time: < 300ms

## Related Documentation

- [Dashboard](../dashboard/dashboard.md) - Shows today's summary
- [Import & Export](../import-export/import-export.md) - Configure operations
- [Data Formats](../../data-formats.md) - Log file structure
