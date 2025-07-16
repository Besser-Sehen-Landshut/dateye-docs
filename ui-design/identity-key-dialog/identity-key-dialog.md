# Identity Key Dialog

First-time notification about the automatically generated identity key.

## Purpose

DATEYE uses a device-specific identity key for encrypting and decrypting sensitive patient data (`patients.enc`, `search.enc`). To ensure complete transparency and recovery options, the application shows this key the first time it is generated.

## Dialog Layout

```
╭────────────────────────────────────────────────────────────╮
│      Your Identity Key Has Been Created                    │
│                                                            │
│  This key is required to decrypt encrypted patient        │
│  records.                                                  │
│                                                            │
│  Storage location:                                         │
│   C:\Users\%USER%\AppData\Local\DATEYE\identity.key       │
│                                                            │
│  For security, we recommend:                              │
│   • Making a backup copy of this file                     │
│   • Printing the key and storing it securely              │
│                                                            │
│  Identity Key:                                             │
│  ┌────────────────────────────────────────────────────┐   │
│  │ 9c82-fdd1-7ae9-42b7-ae13-ff22b1a9129e             │   │
│  └────────────────────────────────────────────────────┘   │
│                                                            │
│   IMPORTANT: Without this key, your data will be        │
│     permanently inaccessible!                              │
│                                                            │
│ [ Open Folder ]   [ Print ]                    [ OK ]     │
╰────────────────────────────────────────────────────────────╯
```

## Visual Design

The identity key dialog is a modal window that appears centered on screen with:

### Dialog Structure
- Clean white background with shadow
- Clear header with title
- Well-organized content sections
- Action buttons at the bottom

### Key Display
- Key displayed in highlighted box
- Monospace font for easy reading
- Blue background for attention
- Auto-select on click for easy copying

### Visual Hierarchy
1. **Title** - Clear statement of what happened
2. **Explanation** - Why this is important
3. **Storage location** - Where the key is stored
4. **Recommendations** - What to do next
5. **The key** - Most important element, visually prominent
6. **Warning** - Critical information highlighted
7. **Actions** - Clear next steps

### Warning Area
- Warning icon for attention
- Contrasting background
- Bold text for emphasis

## Core Functions

### 1. When it appears
- **First startup only** - after key generation
- Never appears again unless key is deleted
- Modal dialog - must be acknowledged

### 2. User Actions

| Button | Action |
|--------|--------|
| **Open Folder** | Opens file explorer to `identity.key` location |
| **Print** | Opens system print dialog with key info |
| **OK** | Closes dialog and continues to dashboard |

### 3. Key Properties
- Automatically generated (UUID v4)
- Stored as plain text file
- Not in system keychain (portable)
- Required for patient data decryption

## Security Considerations

### What the key protects
- `patients.enc` - Encrypted patient identities
- `search.enc` - Search index with names
- Separation of personal data from measurements

### Key Storage
- Local filesystem only
- User-specific app directory
- No cloud synchronization
- No automatic backup

### If the key is lost
- New key generated on next startup
- Previous encrypted data becomes inaccessible
- Measurements remain (anonymous)
- Patient assignment permanently lost

## Platform-Specific Paths

**Windows:**
```
C:\Users\%USERNAME%\AppData\Local\DATEYE\identity.key
```

**macOS:**
```
~/Library/Application Support/DATEYE/identity.key
```

**Linux:**
```
~/.config/DATEYE/identity.key
```

## Localization

All UI text uses the application's i18n system:
- Immediate language switching
- No hardcoded strings
- Fallback to English if keys are missing

Example translation keys:
```typescript
const translations = {
  title: "Your Identity Key Has Been Created",
  description: "This key is required to decrypt encrypted patient records.",
  recommendations: "For security, we recommend:",
  recommendationBackup: "Making a backup copy of this file",
  recommendationPrint: "Printing the key and storing it securely",
  warning: "IMPORTANT: Without this key, your data will be permanently inaccessible!",
  openFolder: "Open Folder",
  print: "Print",
  ok: "OK"
};
```

## Success Metrics

- User acknowledges dialog: 100%
- Backup action performed: > 80%
- Key recovery success rate: > 95%
- Support tickets for lost keys: < 5%