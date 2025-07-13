# DATEYE Documentation

**Professional medical device integration platform documentation**

[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://github.com/Besser-Sehen-Landshut/dateye-docs)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Comprehensive documentation for the DATEYE medical device integration platform. This repository contains all technical documentation, API specifications, and implementation guides.

## 🎯 Documentation Overview

DATEYE is an offline-first desktop application for seamless data transfer between incompatible medical devices, eliminating manual data entry while maintaining complete patient privacy and audit compliance.

**Main Repository**: [DATEYE Flutter Application](https://github.com/Besser-Sehen-Landshut/dateye)

## 📚 Table of Contents

### 🚀 **Getting Started**
- **[System Architecture](architecture.md)** - Technical architecture, security, and design patterns
- **[Deployment Guide](deployment.md)** - Installation, configuration, and maintenance
- **[Executive Summary](executive-summary.md)** - Business overview and project status

### 🔌 **Device Integration**
- **[Adapter Development](adapter-development.md)** - Creating ImportAdapter and ExportAdapter implementations
- **[Data Formats](data-formats.md)** - NDJSON specifications and data models
- **[Supported Devices](adapters/)** - Complete device integration documentation
  - [Topcon MYAH](adapters/topcon-myah.md) - Myopia control biometer
  - [ZEISS IOLMaster](adapters/zeiss-iolmaster.md) - Optical biometry devices  
  - [Eye-Office](adapters/eye-office.md) - Practice management system API
  - [Mediworks AL550](adapters/mediworks-al550.md) - Bidirectional biometer integration

### 🎨 **User Interface**
- **[UI Design System](ui-design/design-system.md)** - Platform-native design specifications
- **[Screen Documentation](ui-design/)** - Complete UI/UX specifications
  - [Dashboard](ui-design/dashboard/dashboard.md) - Real-time status overview
  - [Connections](ui-design/connections/connections.md) - Workflow management
  - [History](ui-design/history/history.md) - Activity audit trail
  - [Settings](ui-design/settings/settings.md) - Configuration interface
- **[Brand Assets](ui-design/logo/)** - Logo system and usage guidelines

### 🔧 **Technical Reference**
- **[Flutter Implementation](flutter-implementation.md)** - UI architecture and cross-platform development
- **[Architecture Deep Dive](architecture/)** - Detailed technical specifications
  - [Dependency Injection](architecture/dependency-injection.md)
  - [Encryption System](architecture/encryption.md)
  - [Project Structure](architecture/project-structure.md)
  - [State Management](architecture/state-management.md)

### 📡 **External APIs**
- **[Eye-Office API](external-apis/eye-office/)** - Practice management REST API
- **[Mediworks AL550 API](external-apis/mediworks/)** - Biometer HTTP interface
- **[ZEISS API](external-apis/zeiss/)** - DICOM specifications and data structures

## 🏥 **For Medical Practices**

### Quick Start Guides
- **[Installation Guide](deployment.md#installation)** - Step-by-step setup for clinical environments
- **[User Training](deployment.md#user-guide)** - Operation procedures for medical staff
- **[Troubleshooting](deployment.md#troubleshooting)** - Common issues and solutions

### Supported Workflows
- **Biometry Integration**: Topcon MYAH → AL550 patient registration
- **Practice Management**: Eye-Office API synchronization
- **Data Backup**: Automated file export and archiving
- **Audit Compliance**: Complete transaction logging

## 👨‍💻 **For Developers**

### Implementation Guides
- **[Getting Started](../README.md#quick-start)** - Development environment setup
- **[Architecture Overview](architecture.md)** - ImportAdapter/ExportAdapter pattern
- **[Adding Devices](adapter-development.md)** - Step-by-step device integration
- **[API Reference](external-apis/)** - Complete API specifications

### Code Examples
```dart
// ImportAdapter example
@Named('your_device')
@Singleton(as: ImportAdapter)  
class YourDeviceImportAdapter implements ImportAdapter {
  @override
  Future<ImportedDataFileModel> parse(String filePath) async {
    // Device-specific parsing logic
  }
}

// ExportAdapter example  
@Named('your_export')
@Singleton(as: IExportAdapter)
class YourExportAdapter implements IExportAdapter {
  @override
  Future<Either<Failure, ExportResult>> export({
    required ExportableDataFile data,
    required ExportTarget target,
  }) async {
    // Device-specific export logic
  }
}
```

## 🔒 **Security & Compliance**

### Data Protection
- **Local-Only Storage**: No cloud dependencies for core functionality
- **Planned Encryption**: AES-256 implementation for patient data
- **Audit Trails**: Complete transaction logging for compliance
- **GDPR Compliance**: Privacy by design with data separation

### Medical Standards
- **Device Validation**: Testing with real medical device data
- **Error Handling**: Robust error recovery for clinical environments  
- **Data Integrity**: Comprehensive validation and quality checks
- **Offline Operation**: Zero network dependency for reliability

## 📊 **Project Status**

### ✅ **Production Ready**
- Core ImportAdapter/ExportAdapter architecture
- Topcon MYAH import implementation
- AL550 export implementation  
- NDJSON storage system
- Flutter UI framework

### 🚧 **In Development**
- Additional export adapters (File Export, Myopia.cloud)
- Eye-Office API integration
- End-to-end testing suite
- UI workflow management

### 📋 **Planned**
- Patient data encryption (AES-256)
- ZEISS IOLMaster support
- Advanced device integrations
- Platform optimization

## 🤝 **Contributing to Documentation**

We welcome documentation improvements! 

### How to Contribute
1. Fork this repository
2. Create a documentation branch: `git checkout -b docs/your-improvement`
3. Make your changes following our [style guide](CONTRIBUTING.md)
4. Submit a pull request

### Documentation Standards
- **Clear Structure**: Logical organization for different user types
- **Practical Examples**: Code snippets and real-world scenarios
- **Medical Context**: Consider clinical workflows and requirements
- **Accessibility**: Clear language and comprehensive explanations

## 📞 **Support**

- **Issues**: [Main Repository Issues](https://github.com/Besser-Sehen-Landshut/dateye/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Besser-Sehen-Landshut/dateye/discussions)
- **Documentation Issues**: [Docs Repository Issues](https://github.com/Besser-Sehen-Landshut/dateye-docs/issues)

## 📄 **License**

This documentation is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**DATEYE Documentation** - Comprehensive guides for professional medical device integration.
