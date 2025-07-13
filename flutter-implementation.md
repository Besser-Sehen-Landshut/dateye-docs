# Flutter Implementation Guide

Platform-native desktop application development using Flutter framework.

## Platform-Native UI Strategy

DATEYE implements native UI components for each platform to ensure professional, familiar user experiences:
- **Windows**: Fluent UI (Microsoft design system)
- **macOS**: macOS UI (Apple design language)
- **Linux**: Yaru (Ubuntu/GNOME design)

Implementation priority: Windows → macOS → Linux

## Project Structure

```
lib/
├── core/                    # Business logic (platform-independent)
│   ├── models/             # Data models
│   ├── services/           # Business services
│   └── repositories/       # Data repositories
│
├── infrastructure/          # Technical implementation
│   ├── adapters/           # Device adapters
│   │   ├── import/
│   │   └── export/
│   ├── storage/            # File/data persistence
│   └── platform/           # Platform-specific services
│
├── presentation/            # UI layer (platform-specific)
│   ├── windows/            # Windows UI (Fluent UI)
│   │   ├── app.dart
│   │   ├── screens/
│   │   ├── widgets/
│   │   └── theme/
│   ├── macos/              # macOS UI (macOS UI)
│   │   ├── app.dart
│   │   ├── screens/
│   │   ├── widgets/
│   │   └── theme/
│   ├── linux/              # Linux UI (Yaru)
│   │   ├── app.dart
│   │   ├── screens/
│   │   ├── widgets/
│   │   └── theme/
│   └── shared/             # Shared UI logic
│       ├── bloc/           # State management
│       ├── routing/        # Navigation
│       └── l10n/           # Localization
│
└── main.dart               # Platform-aware entry point
```

## Platform-Aware Entry Point

```dart
// main.dart
import 'dart:io';
import 'package:fluent_ui/fluent_ui.dart' as fluent;
import 'package:macos_ui/macos_ui.dart';
import 'package:yaru/yaru.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize core services
  await initializeCore();
  
  // Launch platform-specific app
  if (Platform.isWindows) {
    runApp(WindowsDateyeApp());
  } else if (Platform.isMacOS) {
    runApp(MacOSDateyeApp());
  } else if (Platform.isLinux) {
    runApp(LinuxDateyeApp());
  }
}
```

## Windows Implementation (Priority 1)

### Dependencies
```yaml
dependencies:
  fluent_ui: ^4.7.0
  system_tray: ^2.0.0
  windows_taskbar: ^1.1.0
```

### App Structure
```dart
// presentation/windows/app.dart
import 'package:fluent_ui/fluent_ui.dart';

class WindowsDateyeApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return FluentApp(
      title: 'DATEYE',
      theme: FluentThemeData(
        accentColor: Colors.teal,
        visualDensity: VisualDensity.standard,
        fontFamily: 'Segoe UI',
      ),
      darkTheme: FluentThemeData(
        brightness: Brightness.dark,
        accentColor: Colors.teal,
      ),
      home: WindowsShell(),
      localizationsDelegates: [
        FluentLocalizations.delegate,
        ...AppLocalizations.localizationsDelegates,
      ],
    );
  }
}
```

### Navigation Shell
```dart
// presentation/windows/screens/shell.dart
class WindowsShell extends StatefulWidget {
  @override
  _WindowsShellState createState() => _WindowsShellState();
}

class _WindowsShellState extends State<WindowsShell> {
  int _index = 0;
  
  @override
  Widget build(BuildContext context) {
    return NavigationView(
      appBar: NavigationAppBar(
        automaticallyImplyLeading: false,
        title: const Text('DATEYE'),
        actions: Row(
          mainAxisAlignment: MainAxisAlignment.end,
          children: [
            IconButton(
              icon: const Icon(FluentIcons.settings),
              onPressed: () => _navigateToSettings(),
            ),
          ],
        ),
      ),
      pane: NavigationPane(
        selected: _index,
        onChanged: (i) => setState(() => _index = i),
        displayMode: PaneDisplayMode.top,
        items: [
          PaneItem(
            icon: const Icon(FluentIcons.home),
            title: const Text('Dashboard'),
            body: const DashboardScreen(),
          ),
          PaneItem(
            icon: const Icon(FluentIcons.sync),
            title: const Text('Import & Export'),
            body: const ImportExportScreen(),
          ),
          PaneItem(
            icon: const Icon(FluentIcons.event_info),
            title: const Text('Event Log'),
            body: const EventLogScreen(),
          ),
        ],
      ),
    );
  }
}
```

### Windows-Specific Features
```dart
// System Tray Integration
class WindowsSystemTray {
  static Future<void> initialize() async {
    final SystemTray systemTray = SystemTray();
    
    await systemTray.initSystemTray(
      title: 'DATEYE',
      iconPath: 'assets/icons/tray_icon.ico',
    );
    
    final Menu menu = Menu()
      ..buildFrom([
        MenuItemLabel(
          label: 'Show',
          onClicked: (_) => _showWindow(),
        ),
        MenuSeparator(),
        MenuItemLabel(
          label: 'Import Files...',
          onClicked: (_) => _quickImport(),
        ),
        MenuSeparator(),
        MenuItemLabel(
          label: 'Exit',
          onClicked: (_) => _exitApp(),
        ),
      ]);
    
    await systemTray.setContextMenu(menu);
  }
}
```

## macOS Implementation (Priority 2)

### Dependencies
```yaml
dependencies:
  macos_ui: ^2.0.0
  macos_window_utils: ^1.0.0
```

### App Structure
```dart
// presentation/macos/app.dart
import 'package:macos_ui/macos_ui.dart';

class MacOSDateyeApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MacosApp(
      title: 'DATEYE',
      theme: MacosThemeData.light().copyWith(
        primaryColor: CupertinoColors.systemTeal,
      ),
      darkTheme: MacosThemeData.dark().copyWith(
        primaryColor: CupertinoColors.systemTeal,
      ),
      home: MacOSShell(),
      localizationsDelegates: [
        ...AppLocalizations.localizationsDelegates,
      ],
    );
  }
}
```

### macOS Window with Sidebar
```dart
// presentation/macos/screens/shell.dart
class MacOSShell extends StatefulWidget {
  @override
  _MacOSShellState createState() => _MacOSShellState();
}

class _MacOSShellState extends State<MacOSShell> {
  int _pageIndex = 0;
  
  @override
  Widget build(BuildContext context) {
    return PlatformMenuBar(
      menus: createMenus(),
      child: MacosWindow(
        sidebar: Sidebar(
          minWidth: 200,
          builder: (context, scrollController) {
            return SidebarItems(
              currentIndex: _pageIndex,
              onChanged: (i) => setState(() => _pageIndex = i),
              items: [
                const SidebarItem(
                  leading: MacosIcon(CupertinoIcons.home),
                  label: Text('Dashboard'),
                ),
                const SidebarItem(
                  leading: MacosIcon(CupertinoIcons.arrow_2_circlepath),
                  label: Text('Import & Export'),
                ),
                const SidebarItem(
                  leading: MacosIcon(CupertinoIcons.list_bullet),
                  label: Text('Event Log'),
                ),
              ],
            );
          },
          bottom: MacosListTile(
            leading: const MacosIcon(CupertinoIcons.settings),
            title: const Text('Settings'),
            onClick: () => _navigateToSettings(),
          ),
        ),
        child: IndexedStack(
          index: _pageIndex,
          children: const [
            DashboardScreen(),
            ImportExportScreen(),
            EventLogScreen(),
          ],
        ),
      ),
    );
  }
}
```

## Linux Implementation (Priority 3)

### Dependencies
```yaml
dependencies:
  yaru: ^1.0.0
  yaru_icons: ^2.0.0
```

### App Structure
```dart
// presentation/linux/app.dart
import 'package:yaru/yaru.dart';

class LinuxDateyeApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return YaruTheme(
      builder: (context, yaru, child) {
        return MaterialApp(
          title: 'DATEYE',
          theme: yaru.theme,
          darkTheme: yaru.darkTheme,
          home: LinuxShell(),
          localizationsDelegates: [
            ...AppLocalizations.localizationsDelegates,
          ],
        );
      },
    );
  }
}
```

### Linux Navigation
```dart
// presentation/linux/screens/shell.dart
class LinuxShell extends StatefulWidget {
  @override
  _LinuxShellState createState() => _LinuxShellState();
}

class _LinuxShellState extends State<LinuxShell> {
  int _selectedIndex = 0;
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('DATEYE'),
        actions: [
          IconButton(
            icon: const Icon(YaruIcons.settings),
            onPressed: () => _navigateToSettings(),
          ),
        ],
      ),
      body: Row(
        children: [
          NavigationRail(
            selectedIndex: _selectedIndex,
            onDestinationSelected: (i) => setState(() => _selectedIndex = i),
            labelType: NavigationRailLabelType.all,
            destinations: const [
              NavigationRailDestination(
                icon: Icon(YaruIcons.home),
                label: Text('Dashboard'),
              ),
              NavigationRailDestination(
                icon: Icon(YaruIcons.sync),
                label: Text('Import & Export'),
              ),
              NavigationRailDestination(
                icon: Icon(YaruIcons.format_list_bulleted),
                label: Text('Event Log'),
              ),
            ],
          ),
          const VerticalDivider(thickness: 1, width: 1),
          Expanded(
            child: IndexedStack(
              index: _selectedIndex,
              children: const [
                DashboardScreen(),
                ImportExportScreen(),
                EventLogScreen(),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
```

## Shared State Management

All platforms utilize unified BLoC/Cubit state management:

```dart
// presentation/shared/bloc/import/import_cubit.dart
class ImportCubit extends Cubit<ImportState> {
  final ImportService _importService;
  
  ImportCubit(this._importService) : super(ImportState.initial());
  
  Future<void> importFile(String path) async {
    emit(state.copyWith(isProcessing: true));
    
    try {
      final result = await _importService.processFile(path);
      emit(state.copyWith(
        isProcessing: false,
        lastImportResult: result,
      ));
    } catch (e) {
      emit(state.copyWith(
        isProcessing: false,
        error: e.toString(),
      ));
    }
  }
}
```

## Platform-Aware Components

### Dialog Implementation
```dart
// presentation/shared/widgets/platform_dialog.dart
class PlatformDialog {
  static Future<bool?> showConfirmation({
    required BuildContext context,
    required String title,
    required String content,
  }) {
    if (Platform.isWindows) {
      return fluent.showDialog<bool>(
        context: context,
        builder: (context) => fluent.ContentDialog(
          title: Text(title),
          content: Text(content),
          actions: [
            fluent.Button(
              child: const Text('Cancel'),
              onPressed: () => Navigator.of(context).pop(false),
            ),
            fluent.FilledButton(
              child: const Text('Confirm'),
              onPressed: () => Navigator.of(context).pop(true),
            ),
          ],
        ),
      );
    } else if (Platform.isMacOS) {
      return showMacosAlertDialog<bool>(
        context: context,
        builder: (context) => MacosAlertDialog(
          appIcon: const FlutterLogo(size: 56),
          title: Text(title),
          message: Text(content),
          primaryButton: PushButton(
            controlSize: ControlSize.large,
            onPressed: () => Navigator.of(context).pop(true),
            child: const Text('Confirm'),
          ),
          secondaryButton: PushButton(
            controlSize: ControlSize.large,
            onPressed: () => Navigator.of(context).pop(false),
            child: const Text('Cancel'),
          ),
        ),
      );
    } else {
      // Linux (Yaru/Material)
      return showDialog<bool>(
        context: context,
        builder: (context) => AlertDialog(
          title: Text(title),
          content: Text(content),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(false),
              child: const Text('Cancel'),
            ),
            TextButton(
              onPressed: () => Navigator.of(context).pop(true),
              child: const Text('Confirm'),
            ),
          ],
        ),
      );
    }
  }
}
```

## Dependencies

```yaml
dependencies:
  # Core
  flutter:
    sdk: flutter
  flutter_bloc: ^8.1.0
  freezed_annotation: ^2.4.0
  json_annotation: ^4.8.0
  get_it: ^7.6.0
  injectable: ^2.3.0
  
  # Platform UI
  fluent_ui: ^4.7.0          # Windows
  macos_ui: ^2.0.0           # macOS  
  yaru: ^1.0.0               # Linux
  
  # Platform Integration
  window_manager: ^0.3.0
  system_tray: ^2.0.0
  path_provider: ^2.1.0
  
  # Functionality
  watcher: ^1.1.0
  encrypt: ^5.0.0
  dio: ^5.3.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  build_runner: ^2.4.0
  freezed: ^2.4.0
  json_serializable: ^6.7.0
  injectable_generator: ^2.4.0
```

## Testing Strategy

### Platform-Specific Testing
```dart
// test/windows/dashboard_screen_test.dart
testWidgets('Windows Dashboard shows correct navigation', (tester) async {
  await tester.pumpWidget(
    FluentApp(
      home: WindowsDashboardScreen(),
    ),
  );
  
  expect(find.byType(NavigationView), findsOneWidget);
  expect(find.byIcon(FluentIcons.home), findsOneWidget);
});
```

### Shared Logic Testing
```dart
// test/shared/bloc/import_cubit_test.dart
blocTest<ImportCubit, ImportState>(
  'emits success when import completes',
  build: () => ImportCubit(mockImportService),
  act: (cubit) => cubit.importFile('test.xml'),
  expect: () => [
    ImportState(isProcessing: true),
    ImportState(isProcessing: false, lastResult: success),
  ],
);
```

## Build and Deployment

### Windows Build
```bash
flutter build windows --release
# Output: build/windows/runner/Release/
```

### macOS Build
```bash
flutter build macos --release
# Output: build/macos/Build/Products/Release/DATEYE.app
```

### Linux Build
```bash
flutter build linux --release
# Output: build/linux/x64/release/bundle/
```

## Responsive Design Considerations

Window size adaptation for desktop environments:

```dart
class ResponsiveBuilder extends StatelessWidget {
  final Widget Function(BuildContext, BoxConstraints) builder;
  
  const ResponsiveBuilder({required this.builder});
  
  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        // Provide different layouts based on window size
        return builder(context, constraints);
      },
    );
  }
}
```

## Implementation Guidelines

1. **Platform Detection**: Use `Platform.isX` for runtime platform checks
2. **Conditional Imports**: Implement conditional imports for platform-specific code
3. **Business Logic Separation**: Maintain all business logic in the core layer
4. **Design Guidelines**: Follow platform-specific design conventions
5. **Cross-Platform Testing**: Test on all target platforms before release

## Related Documentation

- [Architecture](architecture.md) - System architecture overview
- [Design System](ui-design/design-system.md) - Platform-aware design specifications
- [Adapter Development](adapter-development.md) - Device adapter implementation
- [Data Formats](data-formats.md) - JSON structure specifications