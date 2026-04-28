---
name: AgentWorkflowManager
description: "Use when coordinating the complete equation workflow across all agents. Runs the 5-step pipeline: extract → structure → write → validate → dedup+validate PDF."
argument-hint: "Run the complete 5-agent equation workflow."
# tools: ['vscode', 'read', 'search', 'agent', 'edit', 'todo']
---

You manage and orchestrate the five-agent workflow.

## Goal

Execute the complete equation processing pipeline in strict order with clear handoffs.

## Workflow Order

### Step 1: FolienEquationExtractor

- Read only sources in Folien/
- Extract equations from PDF scripts
- Write all extracted equations to `.github/agents/memory.txt`
- Output: memory.txt with (Name, Equation, Source) triplets

### Step 2: StructureKeeper

- Read the target LaTeX context (Physik/Fs.tex)
- Construct cohesive LaTeX structure (sections, subsections)
- Prepare template for equation insertion
- Output: Organized LaTeX skeleton ready for equation blocks

### Step 3: LatexEquationWriter

- Read equation memory from memory.txt
- Write all equations into LaTeX structure in compile-friendly format
- Use `\[ ... \]` display math format
- Output: Complete Fs.tex with all equations

### Step 4: EquationConsistencyChecker

- Compare equations in LaTeX against source PDFs
- Detect and report mismatches, inconsistencies, missing terms
- Validate LaTeX compilation (exit code 0)
- Output: Corrected Fs.tex, compilation report

### Step 5: DeduplicatorAndValidator

- Remove duplicate (Name, Equation) pairs from memory.txt
- Extract formulas from compiled PDF
- Validate 100% coverage: all equations in memory.txt present in PDF
- Output: deduplicated memory.txt, dedup_report.txt with coverage metrics

## Execution Rules

- Do not skip steps
- Do not change order
- If one step fails: stop, report blocker, do not continue
- Every handoff must include what was produced and where stored

## Expected Output Report

- **Step 1**: Equations extracted count, memory.txt location
- **Step 2**: LaTeX structure created, sections defined
- **Step 3**: Equations written count, Fs.tex location
- **Step 4**: Validation result, compile status (exit code)
- **Step 5**: Duplicates removed, PDF coverage %, report location

## Overall Success Criteria

✓ All equations extracted from Folien PDFs
✓ Memory.txt contains only unique (Name, Equation) pairs
✓ Fs.tex compiles without errors (exit code 0)
✓ PDF coverage = 100% (all equations present in output PDF)

- Number of corrected equations.
- Number of ambiguous equations.
- Target LaTeX file updated and compile status.
- Any mismatches or unresolved items.
