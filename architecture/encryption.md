# Data Encryption in DATEYE

Implementation specification for patient data encryption and privacy protection.

## Overview

DATEYE implements data separation to achieve:
- **Privacy Protection**: Encrypted patient identities
- **Research Capability**: Anonymous measurement sharing
- **GDPR Compliance**: Personal data protection
- **Performance**: Fast measurement access

## Current Status

**NOT YET IMPLEMENTED** - Critical priority before production deployment.

Patient data is currently stored unencrypted. Implementation required before processing real patient data.

## Encryption Architecture

```
identity.enc (ENCRYPTED)          log.ndjson (PLAINTEXT)
├── Patient Names                 ├── Anonymous ID: pat_001
├── Birth Dates                   ├── Measurements
└── Contact Info                  └── Events
        ↓                                    ↓
   Encrypted with                    No personal data
   identity.key                      Only references
```

## Implementation Plan

### 1. Encryption Service

```dart
@singleton
class EncryptionService {
  static const _keyFileName = 'identity.key';
  late final Encrypter _encrypter;
  late final Key _key;
  
  Future<void> initialize() async {
    _key = await _loadOrGenerateKey();
    _encrypter = Encrypter(AES(_key, mode: AESMode.cbc));
  }
  
  String encryptPatient(Map<String, dynamic> patientData) {
    final plainText = jsonEncode(patientData);
    final iv = IV.fromSecureRandom(16);
    final encrypted = _encrypter.encrypt(plainText, iv: iv);
    
    // Store IV with encrypted data
    return jsonEncode({
      'iv': iv.base64,
      'data': encrypted.base64,
    });
  }
  
  Map<String, dynamic> decryptPatient(String encryptedJson) {
    final json = jsonDecode(encryptedJson);
    final iv = IV.fromBase64(json['iv']);
    final encrypted = Encrypted.fromBase64(json['data']);
    
    final decrypted = _encrypter.decrypt(encrypted, iv: iv);
    return jsonDecode(decrypted);
  }
}
```

### 2. Key Generation Implementation

```dart
Future<Key> _loadOrGenerateKey() async {
  final appDir = await getApplicationSupportDirectory();
  final keyFile = File('${appDir.path}/secure/$_keyFileName');
  
  if (await keyFile.exists()) {
    // Load existing key
    final keyHex = await keyFile.readAsString();
    return Key.fromBase16(keyHex.trim());
  }
  
  // Generate new key
  final key = Key.fromSecureRandom(32); // 256-bit
  await _showKeyBackupDialog(key);
  
  // Save after user confirms backup
  await keyFile.create(recursive: true);
  await keyFile.writeAsString(key.base16);
  
  // Set file permissions (Unix-like systems)
  if (Platform.isLinux || Platform.isMacOS) {
    await Process.run('chmod', ['600', keyFile.path]);
  }
  
  return key;
}
```

### 3. Key Backup Dialog

```dart
Future<void> _showKeyBackupDialog(Key key) async {
  // Create temporary file with key
  final desktop = await getDesktopDirectory();
  final tempFile = File('${desktop.path}/DATEYE-RECOVERY-KEY.txt');
  
  await tempFile.writeAsString('''
DATEYE Encryption Key
=====================
IMPORTANT: Back up this file externally then delete it.

Key: ${key.base16}

Created: ${DateTime.now().toIso8601String()}
Installation: ${await getInstallationId()}

WARNING: Without this key, patient data cannot be recovered.
''');

  // Show dialog
  await showDialog(
    context: context,
    barrierDismissible: false,
    builder: (context) => AlertDialog(
      title: Text('IMPORTANT: Back Up Encryption Key'),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text('Your encryption key has been created:'),
          Text(tempFile.path, style: TextStyle(fontFamily: 'monospace')),
          SizedBox(height: 16),
          Text('REQUIRED ACTIONS:', style: TextStyle(fontWeight: FontWeight.bold)),
          Text('1. Open the file'),
          Text('2. Copy the contents'),
          Text('3. Store securely (USB drive, safe)'),
          Text('4. Do NOT store in cloud/email/photos'),
        ],
      ),
      actions: [
        TextButton(
          onPressed: () => openFile(tempFile.path),
          child: Text('Open File'),
        ),
        ElevatedButton(
          onPressed: () async {
            Navigator.of(context).pop();
            // Delete after 48 hours
            Future.delayed(Duration(hours: 48), () async {
              if (await tempFile.exists()) {
                await tempFile.delete();
              }
            });
          },
          child: Text('I Have Backed Up The Key'),
        ),
      ],
    ),
  );
}
```

### 4. Data Storage Pattern

```dart
// Save patient with encryption
class PatientRepository {
  final EncryptionService _encryption;
  
  Future<void> savePatient(Patient patient) async {
    // Generate anonymous ID
    final secretId = 'pat_${DateTime.now().millisecondsSinceEpoch}';
    
    // Encrypt identity
    final identity = {
      'firstName': patient.firstName,
      'lastName': patient.lastName,
      'birthDate': patient.birthDate,
      'externalIds': patient.externalIds,
    };
    
    final encrypted = _encryption.encryptPatient(identity);
    
    // Save to identity.enc
    await _identityStorage.save(secretId, encrypted);
    
    // Return anonymous reference
    return secretId;
  }
}

// Log events with anonymous ID only
class EventLogger {
  Future<void> logImport(String secretPid, List<Measurement> measurements) async {
    await _database.insert(LogEntry(
      type: 'import',
      secretPid: secretPid,  // Only anonymous ID
      measurements: measurements,
      timestamp: DateTime.now(),
    ));
  }
}
```

## Security Considerations

### Protected Data
- Patient names, birth dates, addresses
- Personally identifiable information
- External IDs that could identify patients

### Unencrypted Data
- Measurements (anonymized)
- Event logs (anonymized)
- Device configurations
- Application settings

### Key Management Strategy

**Implementation approach:**
1. Automatic key generation on first start
2. Temporary file creation on desktop
3. User acknowledgment required for backup
4. Automatic deletion after 48 hours
5. Permanent storage in secure directory

**User responsibilities:**
- Backup recovery key externally
- Secure storage (physical media)
- Delete temporary file

### Recovery Process

Key recovery procedure:
1. Locate backup recovery key
2. Place in: `[AppData]/DATEYE/secure/identity.key`
3. Restart DATEYE
4. Patient data accessible

Without the key: **All patient data is permanently inaccessible.**

## Implementation Timeline

### Phase 1: Prototype (Current)
- No encryption
- Development/testing only
- No real patient data

### Phase 2: Pre-Production (Required)
- Encryption service implementation
- Key generation with backup flow
- Encrypted identity storage
- Data migration tool

### Phase 3: Production
- Mandatory encryption
- Audit logging
- Key rotation capability (future)

## Testing

```dart
test('patient data encryption', () async {
  final service = EncryptionService();
  await service.initialize();
  
  final patient = {
    'firstName': 'Test',
    'lastName': 'Patient',
    'birthDate': '2000-01-01',
  };
  
  final encrypted = service.encryptPatient(patient);
  
  // Verify no plaintext
  expect(encrypted.contains('Test'), false);
  expect(encrypted.contains('Patient'), false);
  
  // Verify decryption
  final decrypted = service.decryptPatient(encrypted);
  expect(decrypted['firstName'], 'Test');
});
```

## Compliance Implementation

This implementation addresses:
- **GDPR Article 32**: Technical protection measures
- **Pseudonymization**: Personal data separation
- **Data Portability**: Encrypted export capability
- **Right to Erasure**: Individual record deletion

## Related Documentation

- [Architecture](../architecture.md) - Security architecture
- [Data Formats](../data-formats.md) - File structure specifications
- [Deployment](../deployment.md) - Security configuration