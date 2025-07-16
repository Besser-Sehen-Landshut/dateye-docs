# DATEYE Documentation

Medical device integration platform using ImportAdapter/ExportAdapter architecture for offline data workflows between incompatible medical devices.

## Quick Navigation

- **Start Here**: [Current Development Tasks](implementation/current-tasks.md)
- **Architecture Overview**: [System Design](architecture.md)
- **Code Repository**: [github.com/Besser-Sehen-Landshut/dateye](https://github.com/Besser-Sehen-Landshut/dateye)

## Core Concepts

DATEYE uses separate adapter interfaces for medical device integration:
- **ImportAdapter**: Device/API → DATEYE (file parsing, API sync)
- **ExportAdapter**: DATEYE → Device/API (patient registration, data export)
- **Clean Architecture**: Core business logic separated from infrastructure
- **Offline-First**: No database, JSON file storage, no network dependencies

## Documentation Structure

### Architecture & Design
- `architecture.md` - System overview, design philosophy, data flow
- `data-formats.md` - JSON specifications, measurement types, validation rules
- `adapter-development.md` - Creating ImportAdapter/ExportAdapter implementations

### Implementation Guides
- `implementation/` - Step-by-step development tasks with technical details
- `implementation/current-tasks.md` - Active development priorities and implementation order
- `flutter-implementation.md` - Platform-specific UI development (Windows/macOS/Linux)

### Device Integration
- `adapters/` - Complete specifications for medical device integrations
- `adapters/topcon-myah.md` - XML file import (reference implementation)
- `adapters/mediworks-al550.md` - JSON import and HTTP export
- `adapters/eye-office.md` - REST API integration
- `adapters/zeiss-iolmaster.md` - DICOM import

### User Interface
- `ui-design/` - Flutter UI specifications and platform-native design system
- `ui-design/design-system.md` - Cross-platform components (Fluent/macOS/Yaru)
- `ui-design/dashboard/` - Main application screens
- `ui-design/connections/` - Import/Export workflow management

### Security & APIs
- `security/` - Patient data encryption and privacy protection
- `external-apis/` - Third-party API documentation and integration guides

## Key Files for Development

### Architecture Decisions
- `architecture.md` - Fundamental design patterns and constraints
- `data-formats.md` - Data structures and transformation rules
- `adapter-development.md` - Adapter interface contracts and implementation patterns

### Active Development
- `implementation/current-tasks.md` - Immediate development priorities
- `implementation/README.md` - Development status and task overview

### Flutter Implementation
- `flutter-implementation.md` - Platform-specific UI development
- `ui-design/design-system.md` - Component library and styling

## Repository Relationship

This documentation repository provides complete specifications for the Flutter application in the main code repository. All implementation details, architectural decisions, and interface specifications are maintained here for consistency and version control.
