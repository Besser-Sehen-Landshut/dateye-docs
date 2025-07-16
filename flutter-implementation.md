# Flutter Implementation Guide

Platform-native desktop application development using Flutter.

## Platform Strategy

- **Windows**: Fluent UI (Priority 1)
- **macOS**: macOS UI (Priority 2)
- **Linux**: Yaru (Priority 3)

## Project Structure

```
lib/
├── core/                    # Business logic
├── infrastructure/          # Technical implementation
│   └── adapters/           # Device adapters
├── presentation/           # UI layer
│   ├── windows/            # Fluent UI
│   ├── macos/              # macOS UI
│   ├── linux/              # Yaru
│   └── shared/             # Shared logic
│       └── bloc/           # State management
└── main.dart               # Platform detection
```

## Platform-Aware Entry Point

```dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await initializeCore();
  
  if (Platform.isWindows) {
    runApp(WindowsDateyeApp());
  } else if (Platform.isMacOS) {
    runApp(MacOSDateyeApp());
  } else if (Platform.isLinux) {
    runApp(LinuxDateyeApp());
  }
}
```

## Windows Implementation

```dart
class WindowsDateyeApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return FluentApp(
      title: 'DATEYE',
      theme: FluentThemeData(
        accentColor: Colors.teal,
        fontFamily: 'Segoe UI',
      ),
      home: WindowsShell(),
    );
  }
}

// Navigation with top pane
NavigationView(
  pane: NavigationPane(
    displayMode: PaneDisplayMode.top,
    items: [
      PaneItem(icon: Icon(FluentIcons.home), title: Text('Dashboard')),
      PaneItem(icon: Icon(FluentIcons.sync), title: Text('Import & Export')),
      PaneItem(icon: Icon(FluentIcons.event_info), title: Text('Event Log')),
    ],
  ),
);
```

## macOS Implementation

```dart
class MacOSDateyeApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MacosApp(
      title: 'DATEYE',
      theme: MacosThemeData.light().copyWith(
        primaryColor: CupertinoColors.systemTeal,
      ),
      home: MacOSShell(),
    );
  }
}

// Sidebar navigation
MacosWindow(
  sidebar: Sidebar(
    items: [
      SidebarItem(
        leading: MacosIcon(CupertinoIcons.home),
        label: Text('Dashboard'),
      ),
    ],
  ),
);
```

## Shared State Management

```dart
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

## Platform-Aware Dialogs

```dart
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
              child: Text('Cancel'),
              onPressed: () => Navigator.pop(context, false),
            ),
            fluent.FilledButton(
              child: Text('Confirm'),
              onPressed: () => Navigator.pop(context, true),
            ),
          ],
        ),
      );
    } else if (Platform.isMacOS) {
      return showMacosAlertDialog<bool>(
        context: context,
        builder: (context) => MacosAlertDialog(
          title: Text(title),
          message: Text(content),
          primaryButton: PushButton(
            child: Text('Confirm'),
            onPressed: () => Navigator.pop(context, true),
          ),
          secondaryButton: PushButton(
            child: Text('Cancel'),
            onPressed: () => Navigator.pop(context, false),
          ),
        ),
      );
    } else {
      // Linux - standard Material
      return showDialog<bool>(
        context: context,
        builder: (context) => AlertDialog(
          title: Text(title),
          content: Text(content),
          actions: [
            TextButton(
              child: Text('Cancel'),
              onPressed: () => Navigator.pop(context, false),
            ),
            TextButton(
              child: Text('Confirm'),
              onPressed: () => Navigator.pop(context, true),
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
  flutter_bloc: ^8.1.0
  freezed_annotation: ^2.4.0
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

dev_dependencies:
  build_runner: ^2.4.0
  freezed: ^2.4.0
  injectable_generator: ^2.4.0
```

## Build Commands

```bash
# Windows
flutter build windows --release

# macOS
flutter build macos --release

# Linux
flutter build linux --release
```

## Testing Strategy

```dart
// Platform-specific UI test
testWidgets('Windows Dashboard shows navigation', (tester) async {
  await tester.pumpWidget(FluentApp(home: WindowsDashboardScreen()));
  expect(find.byType(NavigationView), findsOneWidget);
});

// Shared logic test
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

## Guidelines

1. Use `Platform.isX` for runtime checks
2. Keep business logic in core layer
3. Follow platform design conventions
4. Test on all target platforms

## Related Documentation

- [Architecture](architecture.md) - System architecture
- [Design System](ui-design/design-system.md) - Platform-specific UI
- [Adapter Development](adapter-development.md) - Device integration