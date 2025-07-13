# DATEYE Documentation

Comprehensive documentation for the DATEYE medical device integration platform.

## Quick Navigation

- **🚀 [Getting Started](../README.md)** - Project overview and quick start guide
- **👨‍💻 [Technical Guide](../development/TECHNICAL-GUIDE.md)** - Complete setup, implementation, and troubleshooting
- **🏗️ [System Architecture](architecture.md)** - Technical architecture, security, and file storage
- **📋 [Executive Summary](executive-summary.md)** - Business overview and system requirements

## Core Documentation

### System Design
- [**Architecture Overview**](architecture.md) - System design, patterns, and technology stack
- [**Data Formats**](data-formats.md) - NDJSON specifications and data models
- [**Adapter Development**](adapter-development.md) - Creating medical device integrations

### Implementation Guides
- [**Flutter Implementation**](flutter-implementation.md) - UI architecture and cross-platform development
- [**Architecture Deep Dive**](architecture/) - Detailed technical specifications
  - [Dependency Injection](architecture/dependency-injection.md)
  - [Encryption Implementation](architecture/encryption.md)
  - [Project Structure](architecture/project-structure.md)
  - [State Management](architecture/state-management.md)

### Operations
- [**Executive Summary**](executive-summary.md) - Business overview, system requirements, and project status
- [**Technical Implementation**](../development/TECHNICAL-GUIDE.md) - Installation, deployment, and maintenance procedures

## UI/UX Documentation

### Design System
- [**UI Design Overview**](ui-design/README.md) - Design philosophy and platform-native approach
- [**Design System**](ui-design/design-system.md) - Colors, typography, and component specifications

### Screen Specifications
- [**Dashboard**](ui-design/dashboard/dashboard.md) - Real-time status overview
- [**Connections**](ui-design/connections/connections.md) - Source → Target workflow management
- [**History**](ui-design/history/history.md) - Complete operation audit trail
- [**Settings**](ui-design/settings/settings.md) - Application configuration

### Specialized Interfaces
- [**Eye-Office Setup**](ui-design/eye-office-setup/eye-office-setup.md) - API integration wizard
- [**Eye-Office Sync Details**](ui-design/eye-office-setup/eye-office-sync-details.md) - Extended sync UI specifications
- [**Identity Key Dialog**](ui-design/identity-key-dialog/identity-key-dialog.md) - Encryption key management

### Brand Assets
- [**Logo System**](ui-design/logo/README.md) - Logo specifications and usage guidelines

## Device Integration

### Import Adapters (Data Sources)
- [**Topcon MYAH**](adapters/topcon-myah.md) - Myopia control biometer
- [**ZEISS IOLMaster**](adapters/zeiss-iolmaster.md) - Optical biometry devices
- [**Eye-Office**](adapters/eye-office.md) - Practice management system API

### Export Adapters (Data Targets)
- [**Mediworks AL550**](adapters/mediworks-al550.md) - Optical biometer with bidirectional capability

## External API Reference

### Device APIs
- [**Eye-Office API**](external-apis/eye-office/README.md) - Practice management REST API
- [**Mediworks AL550 API**](external-apis/mediworks/README.md) - Biometer HTTP interface
  - [Export File Format](external-apis/mediworks/AL550ExportFile-EN.md) - JSON export specification
  - [Get Patients API](external-apis/mediworks/getPatients-en.md) - Patient retrieval endpoint
  - [Set Patients API](external-apis/mediworks/setPatients-en.md) - Patient registration endpoint
- [**ZEISS API**](external-apis/zeiss/README.md) - DICOM specifications and data structures
  - [IOLMaster 700 Types](external-apis/zeiss/IOLMaster700Types.md) - DICOM data structures and SOP classes

## Development Resources

### Active Development
- [**Current Status**](../development/README.md) - Implementation progress and remaining tasks
- [**Technical Guide**](../development/TECHNICAL-GUIDE.md) - Detailed technical implementation analysis
- [**Implementation Roadmap**](../development/IMPLEMENTATION-ROADMAP.md) - Step-by-step development plan
- [**Developer Quick Reference**](../development/DEVELOPER-QUICK-REFERENCE.md) - Essential implementation guide

## Implementation Status

### ✅ Production Ready
- **Core Architecture**: Clean Architecture with ImportAdapter pattern implemented
- **Import Pipeline**: Complete with Topcon MYAH reference implementation
- **Storage Framework**: NDJSON file structure and database abstraction defined
- **UI Framework**: Flutter with platform-native components infrastructure

### ❌ Needs Implementation
- **Export Architecture**: Complete IExportAdapter pattern implementation
- **Export Adapters**: AL550, File Export, Myopia.cloud integrations
- **End-to-End Pipeline**: Import → Storage → Export workflow
- **UI Workflow Management**: Source → Target configuration interface
- **Testing Infrastructure**: End-to-end validation suite

### 📋 Roadmap
- **Patient Data Encryption**: AES-256 implementation for production security
- **Advanced Device Support**: Eye-Office API, ZEISS IOLMaster DICOM
- **Platform Optimization**: Native Windows, macOS, Linux experiences

## Documentation Principles

This documentation follows these principles:

- **User-Centric**: Clear navigation for different roles (users, developers, administrators)
- **Implementation-Focused**: Practical guides with concrete examples
- **Architecture-Driven**: Technical decisions explained with rationale
- **Maintenance-Friendly**: Modular structure supporting independent updates

## Quick Reference Links

| Role | Primary Documentation | Secondary Resources |
|------|---------------------|-------------------|
| **Medical Practice** | [Executive Summary](executive-summary.md) | [Technical Guide](../development/TECHNICAL-GUIDE.md) |
| **Software Developer** | [Technical Guide](../development/TECHNICAL-GUIDE.md) | [Architecture](architecture.md), [Adapter Development](adapter-development.md) |
| **System Administrator** | [Technical Guide](../development/TECHNICAL-GUIDE.md) | [Architecture](architecture.md), [Security](architecture/encryption.md) |
| **Project Manager** | [Executive Summary](executive-summary.md) | [Development Status](../development/README.md) |

---

**DATEYE** - Professional medical device integration through proven ImportAdapter/ExportAdapter architecture
