# DATEYE Documentation

Complete technical documentation for the DATEYE medical device integration platform.

## Overview

- [Architecture](architecture.md) - System design, technical principles, and requirements

## Implementation

- [Implementation Guide](implementation/README.md) - Current development tasks and priorities
- [Current Tasks](implementation/current-tasks.md) - Step-by-step implementation instructions

## Core Documentation

### Data Handling

- [Data Formats](data-formats.md) - Complete specification of file formats, data structures, and measurement types

### Development

- [Adapter Development](adapter-development.md) - Creating ImportAdapter and ExportAdapter implementations
- [Flutter Implementation](flutter-implementation.md) - Platform-native desktop application development

### Security

- [Encryption Implementation](security/encryption-planned.md) - Patient data protection strategy

## Device Adapters

### Overview
- [Adapter Index](adapters/README.md) - Complete list of supported devices

### Import/Export Adapters

- [Topcon MYAH](adapters/topcon-myah.md) - Myopia control device integration
- [ZEISS IOLMaster](adapters/zeiss-iolmaster.md) - Optical biometry integration
- [Eye-Office](adapters/eye-office.md) - Practice management system integration
- [Mediworks AL550](adapters/mediworks-al550.md) - Optical biometer integration

## External APIs

### Eye-Office
- [API Overview](external-apis/eye-office/README.md) - REST API documentation
- [API Specification](external-apis/eye-office/eye-office-api-1.yaml) - OpenAPI 3.0 specification

### Mediworks
- [API Overview](external-apis/mediworks/README.md) - AL550 integration documentation
- [Export File Format](external-apis/mediworks/AL550ExportFile-EN.md) - Detailed field descriptions
- [GET Patients Endpoint](external-apis/mediworks/getPatients-en.md) - Patient retrieval API
- [SET Patients Endpoint](external-apis/mediworks/setPatients-en.md) - Patient registration API

### ZEISS
- [API Overview](external-apis/zeiss/README.md) - DICOM integration documentation
- [IOLMaster 700 Types](external-apis/zeiss/IOLMaster700Types.md) - Complete DICOM structure reference

## User Interface Design

### Overview
- [UI Design Philosophy](ui-design/README.md) - Design principles and guidelines
- [Design System](ui-design/design-system.md) - Platform-native component specifications

### Screens

#### Dashboard
- [Dashboard Screen](ui-design/dashboard/dashboard.md) - Main status overview

#### Connections
- [Connections Overview](ui-design/connections/README.md) - Import/Export workflow management
- [Connections Screen](ui-design/connections/connections.md) - Detailed specifications

#### History
- [History Screen](ui-design/history/history.md) - Complete operation logs

#### Settings
- [Settings Screen](ui-design/settings/settings.md) - Application configuration

### Additional UI Components

- [Eye-Office Setup](ui-design/eye-office-setup/eye-office-setup.md) - API connection wizard
- [Eye-Office Sync Details](ui-design/eye-office-setup/eye-office-sync-details.md) - Synchronization dialogs
- [Identity Key Dialog](ui-design/identity-key-dialog/identity-key-dialog.md) - Encryption key notification

### Logo System
- [Logo Documentation](ui-design/logo/README.md) - Complete logo system and usage guidelines

## Maintenance

Run update script: `cd /update/ && ./update.sh`

---

Generated: 2025-01-13  
Update command: `cd /update/ && ./update.sh`
