---
title: "Formelsammlungen Physik - Agent-Workflow Dokumentation"
---

# Physik Formelsammlung - Agenten-Workflow

## Übersicht

Das System besteht aus **5 spezialisierten Agenten**, die in einer linearen Pipeline zusammenarbeiten, um Formeln aus PDF-Skripten zu extrahieren, in LaTeX zu formatieren und das Endergebnis zu validieren.

```
PDF-Skripte → Extract → Structure → Write → Validate → Dedup+PDF-Check → PDF-Output
```

## Die 5 Agenten

### 1️⃣ **FolienEquationExtractor**

**Datei**: `.github/agents/FolienEquationExtractor.agent.md`

**Aufgabe**: Gleichungen aus den PDF-Skripten in `Physik/Folien/` extrahieren

**Ausgaben**:

- `.github/agents/memory.txt` - Alle extrahierten Formeln mit (Name, Equation, Source)
- `.github/agents/folien_file_index.txt` - Baseline für neue-Datei-Erkennung

**Implementierung**: `pdftotext -layout` mit Parsing

---

### 2️⃣ **StructureKeeper**

**Datei**: `.github/agents/StructureKeeper.agent.md`

**Aufgabe**: LaTeX-Dokumentstruktur vorbereiten (Sections, Subsections)

**Ausgabe**:

- Skeleton für `Physik/Fs.tex` mit Struktur

**Hardwert-Sections**:

- Kinematik
- Klassische Mechanik
- Lagrange-Formalismus
- Gravitation

---

### 3️⃣ **LatexEquationWriter**

**Datei**: `.github/agents/LatexEquationWriter.agent.md`

**Aufgabe**: Alle Formeln aus memory.txt in LaTeX `\[...\]` Format schreiben

**Eingabe**:

- `.github/agents/memory.txt`

**Ausgabe**:

- `Physik/Fs.tex` - Vollständiges LaTeX-Dokument mit allen Formeln

---

### 4️⃣ **EquationConsistencyChecker**

**Datei**: `.github/agents/EquationConsistencyChecker.agent.md`

**Aufgabe**: LaTeX-Syntax validieren, Compilation überprüfen

**Prüfungen**:

- LaTeX-Syntax korrekt?
- Kompiliert ohne Fehler (`pdflatex` exit code 0)?
- Fehlende Formeln?

**Ausgabe**:

- Korrekte `Physik/Fs.tex`
- Compilation-Report

---

### 5️⃣ **DeduplicatorAndValidator** ⭐ NEU

**Datei**: `.github/agents/DeduplicatorAndValidator.agent.md`  
**Script**: `dedup_and_validate.py`

**Aufgabe**: Datenintegrität und Vollständigkeit sicherstellen

**Funktionen**:

1. **Deduplizierung**: Entfernt doppelte Formeln aus memory.txt
   - Gleiche (Name, Equation) Paare deduplizieren
   - Nur die ERSTE Instanz behalten
   - Backup erstellen: `memory.txt.backup`

2. **PDF-Validierung**: Überprüft Coverage
   - Extrahiert Formeln aus `Physik/Fs.pdf`
   - Vergleicht mit memory.txt
   - Überprüft 100% Coverage

**Ausgaben**:

- `.github/agents/memory.txt` (dedupliziert)
- `.github/agents/memory.txt.backup` (original)
- `.github/agents/dedup_report.txt` (Validierungs-Report)

**Report enthält**:

```
1. DEDUPLIZIERUNGS-ERGEBNISSE
   - Original-Einträge: X
   - Eindeutige Formeln: Y
   - Entfernte Dubletten: Z

2. PDF-VALIDIERUNGS-ERGEBNISSE
   - Formeln in memory.txt: X
   - Formeln in PDF: Y
   - Coverage: Z%

3. STATUS
   - ✓ Alle Formeln sind in der PDF vorhanden!

4. EMPFEHLUNGEN
   - Nächste Schritte basierend auf Results
```

---

## Die Makefile-Workflow-Integration

```bash
make workflow     # Führt alle 6 Schritte durch
make extract      # Schritt 2: Nur Extraktion
make structure    # Schritt 1: Nur Struktur
make write        # Schritt 3: Nur Schreiben
make validate     # Schritt 4: Nur Validierung
make dedup        # Schritt 5: Nur Deduplizierung
make compile      # Schritt 6: Nur Kompilation
make report       # Zeigt Validierungs-Report
make status       # Zeigt aktuellen Status
make clean        # Löscht Hilfsdateien
make help         # Zeigt diese Hilfe
```

---

## Ausführungsfluss

### Automatisch bei `make workflow`:

```
1. structure        → Vorbereitung
2. extract          → memory.txt (27 Formeln)
3. write            → Fs.tex mit allen Formeln
4. validate         → LaTeX syntax check
5. dedup            → Dubletten entfernen + PDF-Check
6. compile          → PDF generieren
```

### Manuell stellenweise:

```bash
# Nur Deduplizierung und PDF-Check
make dedup

# Nur PDF generieren
make compile

# Status anschauen
make status
```

---

## Dateistruktur

```
Formelsammlungen/
├── Makefile                                    ← Workflow-Orc hesträer
├── dedup_and_validate.py                       ← DeduplicatorAndValidator Implementierung
├── Physik/
│   ├── Fs.tex                                  ← Output: LaTeX-Dokument
│   ├── Fs.pdf                                  ← Output: Compiled PDF
│   ├── Folien/                                 ← Input: PDF-Skripte
│   │   ├── B1B2.pdf
│   │   └── B3.pdf
│   └── Style/
│       ├── Packages.tex
│       └── FormatAndHeader.tex
└── .github/agents/
    ├── AgentWorkflowManager.agent.md           ← Pipeline-Orchestrator (diese Datei)
    ├── FolienEquationExtractor.agent.md        ← Agent 1
    ├── StructureKeeper.agent.md                ← Agent 2
    ├── LatexEquationWriter.agent.md            ← Agent 3
    ├── EquationConsistencyChecker.agent.md     ← Agent 4
    ├── DeduplicatorAndValidator.agent.md       ← Agent 5 ⭐
    ├── memory.txt                              ← 27 Formeln (dedupliziert)
    ├── memory.txt.backup                       ← Backup original
    ├── latex_memory.txt                        ← Zwischenspeicher
    ├── folien_file_index.txt                   ← Für Neue-Datei-Erkennung
    └── dedup_report.txt                        ← Validierungs-Report
```

---

## Workflow-Status Beispiel

```
===============================================
Workflow-Status
===============================================

Struktur:
  ✓ Physik/Fs.tex existiert

Daten:
  ✓ memory.txt: 27 Formeln
  ✓ Backup vorhanden

Output:
  ✓ Fs.pdf: 68K
  ✓ Validierungs-Report vorhanden
```

---

## Mögliche Ergebnisse bei `make dedup`

### ✓ Best Case (aktueller Status)

```
1. Deduplizierung:
   - 27 Einträge → 27 eindeutig
   - 0 Dubletten entfernt

2. PDF-Validierung:
   - Formeln in memory: 27
   - Formeln in PDF: 43
   - Coverage: 100.0%

3. Status:
   ✓ Alle Formeln sind in der PDF vorhanden!
```

### ⚠ Wenn Dubletten existieren

```
1. Deduplizierung:
   - 30 Einträge → 27 eindeutig
   - 3 Dubletten entfernt
   - memory.txt aktualisiert

→ Empfehlung: `make workflow` zur Neu-Kompilation
```

### ❌ Wenn Formeln fehlend

```
2. PDF-Validierung:
   - Formeln in memory: 27
   - Formeln in PDF: 24
   - Coverage: 88.9%

3. Fehlende Formeln:
   - Lagrange-Funktion
   - Hookesches Gesetz
   - Newton aus Euler-Lagrange

→ Empfehlung: LaTeX-Fehler überprüfen, Workflow erneut ausführen
```

---

## Weitere Features

### Neue-Datei-Erkennung

Der **FolienEquationExtractor** überprüft automatisch, ob neue PDFs in `Physik/Folien/` hinzugekommen sind:

- Vergleicht aktuelle Dateien mit `folien_file_index.txt`
- Triggert automatisch Workflow bei neuen Dateien
- Aktualisiert Index nach erfolgreichem Workflow

### Automatische Backups

Der **DeduplicatorAndValidator** erstellt vor der Deduplizierung ein Backup:

- Original: `.github/agents/memory.txt.backup`
- Ermöglicht Rollback falls nötig

### Detaillierte Reports

Jeder Agent generiert strukturierte Output-Dateien:

- `memory.txt` - Source of Truth für Formeln
- `dedup_report.txt` - Validierungs-Details
- `Fs.tex` - Finales LaTeX-Dokument
- `Fs.pdf` - Finales PDF-Output

---

## Fehlerbehandlung

**Wenn etwas nicht funktioniert:**

1. Status überprüfen: `make status`
2. Nur Dedup laufen: `make dedup`
3. Report anschauen: `make report`
4. Bei Bedarf neu starten: `make clean && make workflow`

---

## Zusammenfassung

| Komponente   | Status       | Details                                                       |
| ------------ | ------------ | ------------------------------------------------------------- |
| **Agenten**  | ✓ 5 aktiv    | FolienExtractor, StructureKeeper, LatexWriter, Checker, Dedup |
| **Memory**   | ✓ 27 Formeln | Eindeutig, dedupliziert                                       |
| **LaTeX**    | ✓ Kompiliert | exit code 0                                                   |
| **PDF**      | ✓ 68K        | All 27 formeln vorhanden                                      |
| **Coverage** | ✓ 100%       | Alle Formeln in PDF                                           |

Der Workflow ist **produktionsbereit** und kann jederzeit mit `make workflow` ausgeführt werden! 🎉
