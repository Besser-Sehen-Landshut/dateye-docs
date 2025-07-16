# Dashboard Screen

> Passive status view when DATEYE UI is opened

## Purpose

The dashboard provides a read-only overview of DATEYE's background operations. It appears only when users manually open the UI from the system tray or when attention is required. DATEYE runs silently in the background by default.

## Layout Structure

```
┌─────────────────────────────────────────────────────────┐
│                                           [_] [□] [x]   │
├─────────────────────────────────────────────────────────┤
│ [LOGO] Dashboard │ Connections │ History │ Settings │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Today's Activity    12 imports • 8 exports • 2 errors │
│                                                          │
│                        [All (22)] [Imports (12)]        │
│                        [Exports (8)] [Errors (2)]       │
│  ───────────────────────────────────────────────────    │
│  [NOW] Importing: MYAH Files (2/3 files) ••○        │
│  [14:32] Import: MYAH → DATEYE - Schmidt_Anna_2024.xml  │
│           Mueller_Hans.xml, Weber_Lisa.xml               │
│  [14:28] Export: DATEYE → AL550 - Anna Schmidt, Hans Mueller │
│  [14:15] Export failed: DATEYE → AL550 - Connection timeout │
│  [14:10] Import: Eye-Office → DATEYE - 15 patients imported │
│  [13:58] Import: IOLMaster → DATEYE - bilateral_exam.dcm │
│  [13:45] Import error: Unknown format - 3 files         │
│  [13:40] Import: Eye-Office → DATEYE - 2 batch files    │
│  [13:35] Export: DATEYE → Cloud - 3 patients            │
│  [13:30] Import: AL550 → DATEYE - Hans Mueller          │
│                                                          │
├─────────────────────────────────────────────────────────┤
│ System running • Last sync: 2 min ago         v2.0.0    │
└─────────────────────────────────────────────────────────┘
```

### Active Process Display

**Subtle Design:**
- Light blue background (8% opacity) instead of bold card
- Animated progress dots instead of progress bar
- Subtle pulse effect on icon (no rotation)
- Smaller visual footprint
- Still clearly distinguishable with "[NOW]" timestamp

## Visual Design

### Activity Timeline

- **Active Process**: Subtle blue-tinted background with animated dots
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
  - **Tablet (768-1100px)**: Smaller logo + icons with shortened text ("Connections" → "Connect")
  - **Mobile (< 768px)**: Text only (no logo, no icons), optimized for readability
- **Consistent padding**: 32px left/right at all screen sizes
- Easy switching between main functions
- Settings integrated as fourth tab (no separate icon)

### Minimal Footer

- System status on the left
- Version info on the right
- Clean single-line design
- No navigation buttons (moved to tabs)

### Smart Filtering

- Filter chips show counts: "All (22)", "Import (12)", etc.
- Numbers update dynamically as activities complete
- Quick visual indication of activity distribution
- Helps prioritize attention (e.g., "Errors (2)" draws eye)

###  Interactive Mockup

**[View Windows Fluent UI Dashboard Mockup](dashboard-fluent-ui.html)**

The interactive mockup demonstrates:
- **Logo and tab navigation** in single row for space efficiency
- **Larger logo** (180×36px) for strong brand visibility
- **Responsive navigation** with three distinct breakpoints:
  - **Desktop (>1100px)**: Full logo + icon tabs with complete text
  - **Tablet (768-1100px)**: Smaller logo + icon tabs with shortened "Import" text
  - **Mobile (<768px)**: Text-only navigation (no logo/icons) for optimal readability
- **Four tabs**: Dashboard, Connections, History, Settings
- **Consistent 32px padding** maintained across all window sizes
- Timeline showing all today's activities
- **Mini-statistics** in header (hidden on screens < 1200px)
- **Smart filtering** with activity counts
- Subtle active process indicator with pulse effect
- Fluent Design reveal effects and animations
- Live data simulation with progress dots
- Minimal footer with status
- Auto-scrolling for longer activity lists

##  Key Features

### 1. Active Process Display
- **Subtle Indicator**: Light blue background (8% opacity)
- **"[NOW]" Timestamp**: Indicates ongoing process
- **Progress Dots**: Visual progress indicator (••○ = 2/3)
- **Auto-hide**: Disappears when process completes
- **Animated Icon**: Subtle pulse effect shows activity

### 2. Today's Activity Timeline
- All events from today (filtered from log.ndjson)
- **Mini-statistics**: Quick summary in header (X imports • Y exports • Z errors)
- Chronological order (newest first)
- **Enhanced details**: Shows filenames, patient names, or counts inline
- No interaction - just information display
- Older events accessible via "History" tab

**Example entries with details:**
```
[14:32] ✓ Import: Topcon MYAH - Schmidt_Anna_2024.xml, Mueller_Hans.xml, Weber_Lisa.xml
[14:28] ✓ Export: AL550 - Anna Schmidt, Hans Mueller
[14:15] ⚠ Export failed → AL550 - Connection timeout (Retry 1/3)
[14:10] ✓ Import: Eye-Office API - 15 patients synced
[13:58] ✓ Import: ZEISS IOLMaster - bilateral_exam_2024.dcm
```

### 3. Tab Navigation
- Four main sections easily accessible
- Dashboard always visible as default
- Import & Export for configuration
- History for full activity record
- Settings for app configuration
- DATEYE logo on the left for branding
- No hidden navigation - everything visible

### 4. Version Display
- Right-aligned in footer
- **Interactive**: Click for About or Update dialog
- **Red text** when update available (shows urgency)
- Subtle hover effect

### 5. Settings Access
- Integrated as fourth tab
- Same level as other main functions
- Direct navigation without extra clicks
- Consistent with main app flow

### 6. When Dashboard Appears
- User opens from system tray
- Critical error needs attention
- First launch after installation
- Manual app launch

##  State Management

```typescript
interface DashboardState {
  // Active processes (only one at a time)
  activeProcess: {
    id: string;
    type: 'import' | 'export' | null;
    source: string;  // e.g., "Topcon MYAH", "AL550"
    progress?: {
      current: number;
      total: number;
      unit: string;  // "files" or "patients"
    };
    startedAt: DateTime;
  } | null;

  // Recent completed activities
  recentActivity: ActivityItem[];

  // Filter state
  filter: 'all' | 'import' | 'export' | 'errors';

  // Activity counts
  counts: {
    total: number;
    imports: number;
    exports: number;
    errors: number;
  };

  // Version info
  version: {
    current: string;
    updateAvailable?: string;
    updateCheckedAt: DateTime;
  };
}

interface ActivityItem {
  id: string;
  timestamp: DateTime;
  type: 'import' | 'export' | 'error';
  status: 'success' | 'warning' | 'error';
  source: string;  // Device/adapter name
  details: string; // What happened
  items?: string[]; // Filenames or patient names
  count?: number;  // Number of items processed
  error?: string;  // Error details for warnings/errors
}
```

### Process Completion Flow

```typescript
// When a process completes:
function onProcessComplete(process: ActiveProcess) {
  // 1. Remove from active
  state.activeProcess = null;

  // 2. Create completed activity with timestamp
  const completedActivity: ActivityItem = {
    ...process,
    timestamp: DateTime.now(),
    status: 'success'
  };

  // 3. Add to top of recent activities
  state.recentActivity.unshift(completedActivity);

  // 4. Trim to keep only last 50 activities
  state.recentActivity = state.recentActivity.slice(0, 50);
}
```

## Responsive Behavior

- **< 1280px**: Cards stack vertically
- **< 1200px**: Activity statistics hidden
- **< 1100px**: Tab text shortened ("Import & Export" → "Import")
- **< 1024px**: Simplified activity items
- **< 768px**: Icon-only navigation with tooltips
- **Always**: Minimum 1024px recommended

## Performance

- Shows all of today's activities (no fixed limit)
- Auto-scrolls if needed (with subtle scrollbar)
- Updates every 2 seconds when visible
- Pauses updates when minimized
- Smooth transitions when activities complete

## User Flow

### Activity Timeline Flow

```
System starts process
  │
  ├─→ Active Process card appears (pinned)
  │     │
  │     ├─→ Shows "[NOW]" timestamp
  │     ├─→ Animated icon (subtle pulse)
  │     ├─→ Live progress updates
  │     └─→ Progress dots animation
  │
  ├─→ Process completes
  │     │
  │     ├─→ Card transitions to regular activity
  │     ├─→ Gets real timestamp
  │     └─→ Moves into timeline
  │
  └─→ Timeline updates
        │
        ├─→ New activity at top
        ├─→ Others shift down
        └─→ Oldest falls off (>50)
```

### Navigation Flow

```
Dashboard Tab (Active)
  │
  ├─→ User clicks "Import & Export"
  │     └─→ Navigate to Import & Export screen
  │
  ├─→ User clicks "History"
  │     └─→ Navigate to full History
  │
  └─→ User clicks "Settings"
        └─→ Navigate to Settings screen
```

**Key Principle**: DATEYE runs silently in the system tray. The UI is only opened when needed.

## Success Metrics

- Time to understand system state: < 2 seconds
- Minimal resource usage when open
- Clear indication when action needed
- Easy return to system tray
