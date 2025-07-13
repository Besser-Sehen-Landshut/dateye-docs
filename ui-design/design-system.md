# DATEYE Design System

Platform-native design system for professional medical software.

## Platform-Native Approach

DATEYE uses native UI components for each platform to ensure a familiar, professional user experience:

1. **Windows**: Fluent UI (Windows 11 Design Language)
2. **macOS**: macOS UI (Apple Human Interface Guidelines)
3. **Linux**: Yaru (Ubuntu/GNOME Design System)

This strategy ensures:
- Familiar operation for users on their platform
- Native performance and behavior
- Compliance with platform guidelines
- Professional medical quality

## Platform-Specific Design Systems

### Windows (Fluent Design)

The Windows implementation uses Microsoft's Fluent Design System:

```dart
// Windows Theme Configuration
FluentThemeData(
  accentColor: Color(0xFF0087BA), // DATEYE Blue
  brightness: Brightness.light,
  visualDensity: VisualDensity.standard,
  
  // Fluent-specific elements
  micaBackgroundColor: Color(0xFFF3F3F3),
  acrylicBackgroundColor: Color(0xCC3F3F3F),
  
  // Typography
  typography: Typography.raw(
    display: TextStyle(fontSize: 68, fontWeight: FontWeight.w600),
    titleLarge: TextStyle(fontSize: 28, fontWeight: FontWeight.w600),
    title: TextStyle(fontSize: 20, fontWeight: FontWeight.w600),
    body: TextStyle(fontSize: 14),
    caption: TextStyle(fontSize: 12),
  ),
);
```

**Fluent Core Components:**
- NavigationView with Top/Left-Pane options
- CommandBar for actions
- ContentDialog for alerts
- Acrylic/Mica materials for depth
- Reveal highlight effects

### macOS (Human Interface)

The macOS implementation follows Apple's design language:

```dart
// macOS Theme Configuration
MacosThemeData.light().copyWith(
  primaryColor: Color(0xFF0087BA), // DATEYE Blue
  
  // macOS-specific colors
  canvasColor: CupertinoColors.systemBackground,
  controlBackgroundColor: CupertinoColors.secondarySystemBackground,
  dividerColor: CupertinoColors.separator,
  
  // Typography
  typography: MacosTypography(
    largeTitle: TextStyle(fontSize: 26, fontWeight: FontWeight.w400),
    title1: TextStyle(fontSize: 22, fontWeight: FontWeight.w400),
    title2: TextStyle(fontSize: 17, fontWeight: FontWeight.w600),
    headline: TextStyle(fontSize: 14, fontWeight: FontWeight.w600),
    body: TextStyle(fontSize: 13),
    caption1: TextStyle(fontSize: 10),
  ),
);
```

**macOS Core Components:**
- MacosWindow with unified toolbar
- Sidebar navigation
- MacosAlertDialog
- Push/Help buttons
- SF Symbols icons

### Linux (Yaru Design)

The Linux implementation uses Ubuntu's Yaru design:

```dart
// Yaru Theme Configuration
YaruThemeData(
  variant: YaruVariant.prussianGreen, // Closest DATEYE blue variant
  useMaterial3: true,
  
  // Extension for custom colors
  extensions: [
    YaruColors(
      primary: Color(0xFF0087BA), // DATEYE Blue
      success: Color(0xFF16A34A),
      warning: Color(0xFFEA580C),
      error: Color(0xFFDC2626),
    ),
  ],
);
```

**Yaru Core Components:**
- HeaderBar with integrated controls
- NavigationRail for sidebar
- Yaru icons and indicators
- GNOME-style dialogs
- Rounded corners and shadows

## Unified Brand Identity

While respecting platform conventions, DATEYE maintains brand consistency through:

### Brand Colors
```dart
// Cross-platform semantic colors
class DateyeColors {
  // Brand colors from logo
  static const datGray = Color(0xFFB0B0B0);  // Gray (69% opacity in logo)
  static const eyeBlue = Color(0xFF0087BA);  // Light blue

  // Primary brand color (used as accent)
  static const primary = Color(0xFF0087BA);

  // Status colors
  static const active = Color(0xFF16A34A);   // Green - System running
  static const import = Color(0xFF0087BA);   // Blue - Data coming in
  static const export = Color(0xFFEA580C);   // Orange - Data going out

  // Semantic colors (adapted to platform conventions)
  static const success = Color(0xFF16A34A);
  static const warning = Color(0xFFEA580C);
  static const error = Color(0xFFDC2626);
  static const info = Color(0xFF0EA5E9);
}
```

### Typography Scale
Each platform uses its native font but follows consistent sizes:

| Level | Windows (Segoe UI) | macOS (SF Pro) | Linux (Ubuntu) |
|-------|-------------------|----------------|----------------|
| Display | 68pt | - | 40pt |
| Title Large | 28pt | 26pt | 32pt |
| Title | 20pt | 22pt | 24pt |
| Headline | 14pt | 17pt | 18pt |
| Body | 14pt | 13pt | 14pt |
| Caption | 12pt | 10pt | 12pt |

### Spacing System
Universal 8px grid across all platforms:
```dart
class DateyeSpacing {
  static const double xs = 4;   // 0.5 grid units
  static const double sm = 8;   // 1 grid unit
  static const double md = 16;  // 2 grid units
  static const double lg = 24;  // 3 grid units
  static const double xl = 32;  // 4 grid units
  static const double xxl = 48; // 6 grid units
}
```

## Platform-Aware Components

### Cross-Platform Button Component

```dart
class DateyeButton extends StatelessWidget {
  final String label;
  final VoidCallback onPressed;
  final bool isPrimary;

  const DateyeButton({
    required this.label,
    required this.onPressed,
    this.isPrimary = false,
  });

  @override
  Widget build(BuildContext context) {
    if (Platform.isWindows) {
      return isPrimary
        ? fluent.FilledButton(
            onPressed: onPressed,
            child: Text(label),
          )
        : fluent.Button(
            onPressed: onPressed,
            child: Text(label),
          );
    } else if (Platform.isMacOS) {
      return isPrimary
        ? PushButton(
            buttonSize: ButtonSize.large,
            onPressed: onPressed,
            child: Text(label),
          )
        : MacosTextButton(
            onPressed: onPressed,
            child: Text(label),
          );
    } else {
      // Linux (Material/Yaru)
      return isPrimary
        ? ElevatedButton(
            onPressed: onPressed,
            child: Text(label),
          )
        : TextButton(
            onPressed: onPressed,
            child: Text(label),
          );
    }
  }
}
```

### Platform Dialogs

```dart
class DateyeDialog {
  static Future<bool?> showConfirmation({
    required BuildContext context,
    required String title,
    required String message,
  }) {
    if (Platform.isWindows) {
      return fluent.showDialog<bool>(
        context: context,
        builder: (_) => fluent.ContentDialog(
          title: Text(title),
          content: Text(message),
          actions: [
            fluent.Button(
              child: const Text('Cancel'),
              onPressed: () => Navigator.pop(context, false),
            ),
            fluent.FilledButton(
              child: const Text('Confirm'),
              onPressed: () => Navigator.pop(context, true),
            ),
          ],
        ),
      );
    } else if (Platform.isMacOS) {
      return showMacosAlertDialog<bool>(
        context: context,
        builder: (_) => MacosAlertDialog(
          appIcon: const FlutterLogo(size: 56),
          title: Text(title),
          message: Text(message),
          primaryButton: PushButton(
            buttonSize: ButtonSize.large,
            child: const Text('Confirm'),
            onPressed: () => Navigator.pop(context, true),
          ),
          secondaryButton: MacosTextButton(
            child: const Text('Cancel'),
            onPressed: () => Navigator.pop(context, false),
          ),
        ),
      );
    } else {
      // Linux
      return showDialog<bool>(
        context: context,
        builder: (_) => AlertDialog(
          title: Text(title),
          content: Text(message),
          actions: [
            TextButton(
              child: const Text('Cancel'),
              onPressed: () => Navigator.pop(context, false),
            ),
            TextButton(
              child: const Text('Confirm'),
              onPressed: () => Navigator.pop(context, true),
            ),
          ],
        ),
      );
    }
  }
}
```

## Layout Patterns

### Dashboard Layout
Each platform uses its native navigation pattern:

**Windows**: NavigationView with Top Pane
```dart
NavigationView(
  pane: NavigationPane(
    displayMode: PaneDisplayMode.top,
    items: [...],
  ),
)
```

**macOS**: Sidebar Navigation
```dart
MacosWindow(
  sidebar: Sidebar(
    items: [...],
  ),
)
```

**Linux**: NavigationRail
```dart
Scaffold(
  body: Row(
    children: [
      NavigationRail(...),
      Expanded(child: content),
    ],
  ),
)
```

## Component States

### Interactive States
Consistent across all platforms:
- **Default**: Base appearance
- **Hover**: Subtle highlighting (desktop only)
- **Pressed**: Visual feedback
- **Focused**: Keyboard navigation indicator
- **Disabled**: Reduced opacity

### Loading States
```dart
// Platform-aware progress indicator
class DateyeProgress extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    if (Platform.isWindows) {
      return const fluent.ProgressRing();
    } else if (Platform.isMacOS) {
      return const MacosProgressCircle();
    } else {
      return const CircularProgressIndicator();
    }
  }
}
```

## Theming Strategy

### Light Mode (Standard)
All platforms deliver Light Mode optimized for medical environments:
- High contrast for readability
- Reduced eye strain for long sessions
- Professional appearance

### Dark Mode (Future)
Prepared for v2 implementation:
```dart
// Theme detection
final brightness = MediaQuery.of(context).platformBrightness;
final isDark = brightness == Brightness.dark;
```

## Responsive Design

### Window Size Breakpoints
```dart
class Breakpoints {
  static const double mobile = 600;   // Minimum supported
  static const double tablet = 900;   // Compact layout
  static const double desktop = 1200; // Standard layout
  static const double wide = 1800;    // Extended layout
}
```

### Adaptive Layouts
```dart
class AdaptiveLayout extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final width = MediaQuery.of(context).size.width;
    
    if (width < Breakpoints.tablet) {
      return CompactLayout();
    } else if (width < Breakpoints.desktop) {
      return StandardLayout();
    } else {
      return WideLayout();
    }
  }
}
```

## Accessibility

### Platform-Specific Requirements

**Windows**:
- Narrator screenreader support
- High contrast mode detection
- Keyboard navigation with F6/Tab

**macOS**:
- VoiceOver support
- Reduce transparency option
- Full keyboard access

**Linux**:
- Orca screenreader support
- High contrast themes
- Focus indicators

### Universal Accessibility
```dart
// Semantic labels for all platforms
Semantics(
  label: 'Import patient data',
  button: true,
  child: DateyeButton(...),
)
```

## Icon Strategy

### Platform Icons
- **Windows**: Fluent Icons
- **macOS**: SF Symbols
- **Linux**: Yaru Icons

### Icon System - Font Awesome 5

DATEYE uses Font Awesome 5 as primary icon system for cross-platform consistency.

#### Font Awesome 5 Rationale
- Consistent design - Unified style across all icons
- Comprehensive library - Over 7,000 icons available (Pro version)
- Professional - Proven in medical and enterprise applications
- Scalable - Vector-based, perfect at all sizes
- Documentation - Excellent docs and community support

#### Icon Categories in DATEYE

| Category | Font Awesome Class | Size | Usage | Color |
|-----------|-------------------|--------|------------|--------|
| Status | `fas fa-*` | 24px | System status indicators | Context-dependent |
| Navigation | `fas fa-*` | 20px | Main navigation | Standard |
| Activity | `fas fa-*` | 14px | Event log icons | Context-dependent |
| Meta | `fas fa-*` | 12px | Additional information | Gray |

#### Used Icons

```css
/* Status Icons */
.fa-check          /* System active - Green */
.fa-download       /* Import Queue - Blue/Teal */
.fa-upload         /* Export Queue - Orange */

/* Activity Icons */
.fa-download       /* Import events - Blue/Teal */
.fa-upload         /* Export events - Orange */
.fa-exclamation-circle  /* Error - Red */

/* Navigation */
.fa-arrows-alt-v   /* Import & Export */
.fa-history        /* Event Log */
.fa-cog            /* Settings */

/* Meta Icons */
.fa-folder         /* Folders/Files */
.fa-check-circle   /* Success */
.fa-users          /* Multiple patients */
.fa-user           /* Single patient */
.fa-plug           /* Network/Device */
.fa-cloud          /* Cloud export */
.fa-chart-bar      /* Statistics */
.fa-ruler          /* Measurements */
.fa-glasses        /* Refraction */
.fa-exclamation-triangle /* Warning */
.fa-redo           /* Retry/Refresh */
```

#### Integration

```html
<!-- Font Awesome 5 Pro (Production) -->
<link rel="stylesheet" href="https://pro.fontawesome.com/releases/v5.15.4/css/all.css" 
      integrity="YOUR-INTEGRITY-KEY" 
      crossorigin="anonymous">

<!-- Font Awesome 5 Free (Development) -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
```

#### Icon Styles

```css
/* Base styles for all icons */
.status-icon i,
.activity-icon i,
.nav-button i,
.activity-meta i {
    display: inline-block;
    vertical-align: middle;
    line-height: 1;
}

/* Sizes by category */
.status-icon i { font-size: 24px; }
.nav-button i { font-size: 20px; }
.activity-icon i { font-size: 14px; }
.activity-meta i { 
    font-size: 12px;
    opacity: 0.7;
}
```

### Fallback Icons
For consistency when platform icons are unavailable:
```dart
class DateyeIcons {
  static IconData get home {
    if (Platform.isWindows) return FluentIcons.home;
    if (Platform.isMacOS) return CupertinoIcons.home;
    return YaruIcons.home;
  }
}
```

## Implementation Guidelines

### 1. Platform Detection
Always check platform at runtime:
```dart
if (Platform.isWindows) {
  // Windows-specific code
} else if (Platform.isMacOS) {
  // macOS-specific code
} else if (Platform.isLinux) {
  // Linux-specific code
}
```

### 2. Conditional Imports
Use conditional imports for smaller bundle size:
```dart
// platform_button.dart
export 'platform_button_stub.dart'
  if (dart.library.io) 'platform_button_io.dart'
  if (dart.library.html) 'platform_button_web.dart';
```

### 3. Testing Strategy
Test on all platforms:
```bash
# Windows
flutter test --platform windows

# macOS
flutter test --platform macos

# Linux
flutter test --platform linux
```

## Performance Considerations

### Platform-Specific Optimizations

**Windows**:
- Use native win32 APIs where beneficial
- Utilize DirectX rendering

**macOS**:
- Metal rendering backend
- Native macOS animations

**Linux**:
- GTK rendering optimizations
- Wayland/X11 compatibility

### Universal Performance Tips
1. Lazy load heavy components
2. Use const constructors
3. Minimize rebuilds with proper state management
4. Profile separately on each platform

## Design Checklist

Before implementing a new component:

- [ ] Design exists for all three platforms
- [ ] Follows platform conventions
- [ ] Maintains DATEYE brand identity
- [ ] Accessible on all platforms
- [ ] Responsive to window sizes
- [ ] Tested with platform-specific tools
- [ ] Performance profiled
- [ ] Documentation complete

## Resources

### Platform Guidelines
- [Fluent Design System](https://www.microsoft.com/design/fluent/)
- [Human Interface Guidelines](https://developer.apple.com/design/)
- [GNOME Human Interface Guidelines](https://developer.gnome.org/hig/)

### Flutter Packages
- [fluent_ui Documentation](https://pub.dev/packages/fluent_ui)
- [macos_ui Documentation](https://pub.dev/packages/macos_ui)
- [yaru Documentation](https://pub.dev/packages/yaru)

## Related Documentation

- [Flutter Implementation](../flutter-implementation.md) - Technical implementation
- [UI Design](README.md) - General design philosophy
- [Architecture](../architecture.md) - System architecture
