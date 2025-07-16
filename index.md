# DATEYE Documentation

Complete technical documentation for the DATEYE medical device integration platform.

## Overview

DATEYE is an offline-first desktop application that enables seamless data transfer between incompatible medical devices. The system uses an ImportAdapter/ExportAdapter pattern to integrate various ophthalmologic devices and practice management systems.

## Core Architecture

- **[Architecture](architecture.md)** - System design and component overview
- **[Data Formats](data-formats.md)** - File formats, data structures, and specifications
- **[Adapter Development](adapter-development.md)** - Creating device adapters

## Implementation Guides

- **[Flutter Implementation](flutter-implementation.md)** - Platform-native desktop development
- **[Current Development Tasks](implementation/current-tasks.md)** - Priority implementation tasks

## Device Adapters

- **[Adapter Overview](adapters/README.md)** - Summary of all supported devices
- **[Topcon MYAH](adapters/topcon-myah.md)** - Myopia control device integration

## UI Design

- **[Design System](ui-design/design-system.md)** - Platform-native UI components
- **[Dashboard](ui-design/dashboard/dashboard.md)** - Main application interface
- **[Connections](ui-design/connections/connections.md)** - Import/Export workflow management

## System Status

**Current State**: ~70% complete
- ✅ ImportAdapter system with Topcon MYAH implementation
- ✅ Core data models and storage
- ✅ Flutter UI framework
- ❌ ExportAdapter system (critical missing component)
- ❌ Patient data encryption

**Priority**: Complete export functionality - see [Current Tasks](implementation/current-tasks.md)

## Key Principles

1. **Offline-First**: No database, no services, no network dependencies
2. **Transparent Operations**: All actions logged and auditable
3. **Privacy-First**: Patient data encrypted with local keys
4. **Adapter Pattern**: Extensible device integration

## Getting Started

For developers joining the project:

1. Review [Architecture](architecture.md) for system design
2. Check [Current Tasks](implementation/current-tasks.md) for immediate priorities
3. Examine [Topcon MYAH Adapter](adapters/topcon-myah.md) as reference implementation
4. Follow [Flutter Implementation](flutter-implementation.md) for platform setup

## Documentation Maintenance

This documentation is automatically synchronized between:
- Local development: `/docs/`
- GitHub repository: `dateye-docs`

Updates should be made locally and synchronized using the update scripts.

---

**Version**: 1.0  
**Last Updated**: 2025-01-13  
**Maintained by**: DATEYE Development Team