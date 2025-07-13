# DATEYE Documentation Workflow

Entwickler-Checkliste für Dokumentations-Updates.

## 📝 **Neue Dokumentationsdatei hinzufügen**

### Schritt 1: Datei erstellen
```bash
# Beispiel: Neue Adapter-Dokumentation
touch docs/adapters/new-device.md
# Inhalt schreiben...
```

### Schritt 2: In index.md verlinken
Datei in passender Sektion von `docs/index.md` hinzufügen:
```markdown
### [New Device](adapters/new-device.md)
Beschreibung des neuen Adapters
```

### Schritt 3: Konsistenz prüfen
```bash
dateye
# oder nur Konsistenz-Check:
cd docs/Update && python3 check_consistency.py
```

### Schritt 4: Bei Fehlern korrigieren
Falls Konsistenz-Check fehlschlägt:
- Broken Links: Datei erstellen oder Link entfernen
- Missing Links: Fehlende Dateien zu index.md hinzufügen

## 🔍 **Nur Konsistenz prüfen (ohne Summary update)**

```bash
cd /Users/culfin/Documents/Projekte/Dateye/docs/Update
python3 check_consistency.py
```

## 📊 **Was wird automatisch geprüft**

### ✅ **Broken Links**
- Links in index.md, aber Datei existiert nicht
- Führt zu Fehler und stoppt Update

### ⚠️ **Missing Links** 
- .md Datei existiert, aber nicht in index.md verlinkt
- Führt zu Warnung und stoppt Update

### 🚫 **Ausgeschlossen von Prüfung**
- `docs/Update/` - Update-Scripts
- `README.md` - Speziell behandelt
- `*/README.md` - Verzeichnis-READMEs

## 🛠️ **Typische Workflow-Probleme**

### Problem: "Missing Links" Warnung
```
⚠️  MISSING LINKS (file exists but not in index.md):
   • ui-design/new-screen/new-screen.md
```

**Lösung:**
```bash
# 1. Öffne index.md
# 2. Füge unter passender Sektion hinzu:
- [New Screen](ui-design/new-screen/new-screen.md) - Beschreibung
# 3. Teste erneut:
dateye
```

### Problem: "Broken Links" Fehler
```
❌ BROKEN LINKS (in index.md but file doesn't exist):
   • adapters/missing-device.md
```

**Lösungen:**
```bash
# Option A: Datei erstellen
touch docs/adapters/missing-device.md

# Option B: Link aus index.md entfernen
# (in docs/index.md die entsprechende Zeile löschen)

# Teste erneut:
dateye
```

## 🎯 **Best Practices**

1. **Immer dateye vor Git Commit ausführen**
2. **Dokumentation parallel zur Code-Entwicklung schreiben**
3. **Sinnvolle Dateinamen verwenden (kebab-case)**
4. **Logische Verzeichnisstrukturen beibehalten**
5. **README.md in Unterverzeichnissen für Übersichten nutzen**

## 🔧 **Troubleshooting**

### Script-Berechtigung fehlt
```bash
chmod +x /Users/culfin/Documents/Projekte/Dateye/docs/Update/update.sh
chmod +x /Users/culfin/Documents/Projekte/Dateye/docs/Update/check_consistency.py
```

### Python-Module fehlen
```bash
# Normalerweise nur Standard-Library, aber falls Probleme:
python3 -c "import pathlib, re; print('OK')"
```

### dateye Command funktioniert nicht
```bash
# Prüfe Alias:
alias | grep dateye

# Falls nicht vorhanden:
echo 'alias dateye="cd /Users/culfin/Documents/Projekte/Dateye/docs/Update && ./update.sh"' >> ~/.zshrc
source ~/.zshrc
```

---

**Nach jedem Dokumentations-Update:** `dateye` ausführen! ✨
