#!/usr/bin/env python3
"""
DeduplicatorAndValidator Agent
Removes duplicate equations from memory.txt and validates PDF coverage.
"""

import re
import os
import shutil
import subprocess
from difflib import SequenceMatcher

MEMORY_FILE = ".github/agents/memory.txt"
PDF_FILE = "Physik/Fs.pdf"
BACKUP_FILE = f"{MEMORY_FILE}.backup"
REPORT_FILE = ".github/agents/dedup_report.txt"

class DeduplicatorAndValidator:
    def __init__(self):
        self.original_count = 0
        self.unique_count = 0
        self.duplicates_removed = 0
        self.formulas = []
        self.unique_formulas = {}
        self.pdf_formulas = []
        self.missing_from_pdf = []
        
    def normalize_equation(self, eq):
        """Normalize equation for comparison"""
        return re.sub(r'\s+', ' ', eq.strip().lower())
    
    def read_memory_file(self):
        """Read all formulas from memory.txt"""
        if not os.path.exists(MEMORY_FILE):
            print(f"✗ {MEMORY_FILE} nicht gefunden")
            return False
        
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        current_formula = {}
        for line in lines:
            if line.startswith("Name:"):
                if current_formula and 'Name' in current_formula and 'Equation' in current_formula:
                    self.formulas.append(current_formula)
                current_formula = {"Name": line.replace("Name:", "").strip()}
            elif line.startswith("Equation:"):
                current_formula["Equation"] = line.replace("Equation:", "").strip()
            elif line.startswith("Source:"):
                current_formula["Source"] = line.replace("Source:", "").strip()
        
        if current_formula and 'Name' in current_formula and 'Equation' in current_formula:
            self.formulas.append(current_formula)
        
        self.original_count = len(self.formulas)
        return True
    
    def deduplicate(self):
        """Remove duplicate formulas"""
        print("\n=== Schritt 1: Deduplizierung ===")
        print(f"Lese {self.original_count} Einträge aus {MEMORY_FILE}...")
        
        for formula in self.formulas:
            name = formula['Name']
            equation_norm = self.normalize_equation(formula['Equation'])
            
            # Create unique key
            key = (name.lower(), equation_norm)
            
            # Keep only first occurrence
            if key not in self.unique_formulas:
                self.unique_formulas[key] = formula
        
        self.unique_count = len(self.unique_formulas)
        self.duplicates_removed = self.original_count - self.unique_count
        
        print(f"✓ {self.original_count} Einträge → {self.unique_count} eindeutig")
        print(f"✓ {self.duplicates_removed} Dubletten gefunden und entfernt")
        
        return self.duplicates_removed > 0
    
    def write_deduplicated_memory(self):
        """Write deduplicated formulas back to memory.txt"""
        # Backup original
        if os.path.exists(MEMORY_FILE):
            shutil.copy(MEMORY_FILE, BACKUP_FILE)
            print(f"✓ Backup erstellt: {BACKUP_FILE}")
        
        # Write deduplicated
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            f.write("# Folien Equation Memory\n")
            f.write("# This file is used by FolienEquationExtractor.agent.md\n")
            f.write("# Deduplicated version\n\n")
            
            for (name, _), formula in sorted(self.unique_formulas.items()):
                f.write(f"Name: {formula['Name']}\n")
                f.write(f"Equation: {formula['Equation']}\n")
                if 'Source' in formula:
                    f.write(f"Source: {formula['Source']}\n")
                f.write("\n")
        
        print(f"✓ {MEMORY_FILE} aktualisiert ({self.unique_count} Formeln)")
    
    def extract_pdf_formulas(self):
        """Extract formulas from PDF"""
        print("\n=== Schritt 2: PDF-Extraktion ===")
        
        if not os.path.exists(PDF_FILE):
            print(f"⚠ {PDF_FILE} nicht gefunden - überspringe PDF-Validierung")
            return False
        
        try:
            # Extract text from PDF
            result = subprocess.run(
                ['pdftotext', PDF_FILE, '/tmp/fs_extracted.txt'],
                capture_output=True,
                timeout=10
            )
            
            if result.returncode != 0:
                print(f"⚠ pdftotext Fehler: {result.stderr.decode()}")
                return False
            
            # Read extracted text
            with open('/tmp/fs_extracted.txt', 'r', encoding='utf-8') as f:
                pdf_text = f.read()
            
            # Extract math sections (simple pattern: text between important keywords)
            # Look for formula-like patterns
            pdf_lines = pdf_text.split('\n')
            
            in_formula = False
            current_formula = []
            
            for line in pdf_lines:
                line = line.strip()
                if not line:
                    continue
                
                # Detect formula content (simplified heuristic)
                if any(x in line.lower() for x in ['fall', 'newton', 'lagrange', 'energie', 'kraft', 'beschleun', '=']):
                    if line and not line.startswith('*'):
                        self.pdf_formulas.append(line.lower())
            
            # Remove duplicates
            self.pdf_formulas = list(set(self.pdf_formulas))
            
            print(f"✓ PDF analysiert: {len(self.pdf_formulas)} Formeln/Linien gefunden")
            return True
        
        except Exception as e:
            print(f"✗ Fehler bei PDF-Extraktion: {e}")
            return False
    
    def validate_coverage(self):
        """Validate that formulas are in PDF"""
        print("\n=== Schritt 3: Validierung ===")
        
        self.missing_from_pdf = []
        
        for (name, eq_norm), formula in self.unique_formulas.items():
            eq_norm_lower = eq_norm.lower()
            
            # Check if any PDF line contains key parts of the equation
            found = False
            for pdf_line in self.pdf_formulas:
                # Simple check: does PDF contain key terms
                if any(term in pdf_line for term in eq_norm_lower.split()[:3]):
                    found = True
                    break
            
            if not found:
                self.missing_from_pdf.append({
                    'Name': formula['Name'],
                    'Equation': formula['Equation']
                })
        
        coverage = (self.unique_count - len(self.missing_from_pdf)) / self.unique_count * 100 if self.unique_count > 0 else 0
        
        print(f"✓ Vergleich durchgeführt:")
        print(f"  - Formeln in memory.txt: {self.unique_count}")
        print(f"  - Formeln in PDF: {len(self.pdf_formulas)}")
        print(f"  - Coverage: {coverage:.1f}%")
        
        if self.missing_from_pdf:
            print(f"\n⚠ {len(self.missing_from_pdf)} Formeln fehlen in PDF:")
            for formula in self.missing_from_pdf:
                print(f"  - {formula['Name']}")
        else:
            print(f"\n✓ Alle {self.unique_count} Formeln sind in der PDF vorhanden!")
    
    def write_report(self):
        """Write detailed report"""
        report = "=" * 60 + "\n"
        report += "DEDUPLICATOR & VALIDATOR REPORT\n"
        report += "=" * 60 + "\n\n"
        
        report += "1. DEDUPLIZIERUNGS-ERGEBNISSE:\n"
        report += f"   Original-Einträge: {self.original_count}\n"
        report += f"   Eindeutige Formeln: {self.unique_count}\n"
        report += f"   Entfernte Dubletten: {self.duplicates_removed}\n"
        report += f"   Memory-Datei aktualisiert: {'JA' if self.duplicates_removed > 0 else 'NEIN'}\n\n"
        
        report += "2. PDF-VALIDIERUNGS-ERGEBNISSE:\n"
        report += f"   Formeln in memory.txt: {self.unique_count}\n"
        report += f"   Formeln in PDF: {len(self.pdf_formulas)}\n"
        report += f"   Coverage: {(self.unique_count - len(self.missing_from_pdf)) / self.unique_count * 100 if self.unique_count > 0 else 0:.1f}%\n\n"
        
        if self.missing_from_pdf:
            report += "3. FEHLENDE FORMELN IN PDF:\n"
            for formula in self.missing_from_pdf:
                report += f"   - {formula['Name']}\n"
                report += f"     Eq: {formula['Equation'][:60]}...\n"
            report += "\n"
        else:
            report += "3. STATUS:\n"
            report += "   ✓ Alle Formeln sind in der PDF vorhanden!\n\n"
        
        report += "4. EMPFEHLUNGEN:\n"
        if self.duplicates_removed > 0:
            report += f"   - {self.duplicates_removed} Dubletten wurden entfernt\n"
            report += "   - Workflow erneut ausführen: make workflow\n"
        if self.missing_from_pdf:
            report += f"   - {len(self.missing_from_pdf)} fehlende Formeln müssen hinzugefügt werden\n"
        if self.duplicates_removed == 0 and not self.missing_from_pdf:
            report += "   ✓ Keine Aktionen erforderlich - alles ist in Ordnung\n"
        
        with open(REPORT_FILE, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n✓ Report gespeichert: {REPORT_FILE}")
        print("\n" + "=" * 60)
        print(report)
        print("=" * 60)

def main():
    print("=" * 60)
    print("DEDUPLICATOR & VALIDATOR AGENT")
    print("=" * 60)
    
    validator = DeduplicatorAndValidator()
    
    # Step 1: Read memory file
    if not validator.read_memory_file():
        return False
    
    # Step 2: Deduplicate
    has_duplicates = validator.deduplicate()
    
    # Step 3: Write deduplicated memory
    validator.write_deduplicated_memory()
    
    # Step 4: Extract PDF formulas
    validator.extract_pdf_formulas()
    
    # Step 5: Validate coverage
    validator.validate_coverage()
    
    # Step 6: Write report
    validator.write_report()
    
    return True

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
