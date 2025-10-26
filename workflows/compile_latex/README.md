# Compile LaTeX Workflow

**Purpose**: Compile LaTeX to PDF  
**Version**: 1.0  
**Status**: Production-ready

---

## What This Does

Compiles LaTeX manuscript to PDF, handles bibliography, fixes common errors.

---

## Inputs

- `paper_folder`: Path to folder with main.tex

---

## Outputs

- `main.pdf`: Compiled PDF
- `compile.log`: Compilation log with any errors/warnings

---

## Agent Instructions

```
Task: Compile LaTeX manuscript to PDF

Paper folder: {paper_folder}
Main file: {paper_folder}/main.tex

Steps:
1. Check LaTeX installation:
   - pdflatex available
   - bibtex available
   - Required packages installed

2. Compile sequence:
   ```bash
   cd {paper_folder}
   pdflatex main.tex
   bibtex main  # if references.bib exists
   pdflatex main.tex
   pdflatex main.tex  # second pass for references
   ```

3. Check for errors:
   - Read main.log
   - If errors, try to fix common issues:
     * Missing packages → note what to install
     * Missing figures → check paths
     * LaTeX syntax errors → fix if simple
   - Retry compilation after fixes

4. Verify output:
   - main.pdf exists
   - Check page count (reasonable for conference)
   - Note any warnings (overfull boxes, missing refs, etc.)

5. Write compile.log:
   - Success/failure status
   - Any errors encountered and fixes applied
   - Warnings to review
   - PDF stats (pages, size)

Rules:
- Don't modify main.tex unless fixing compilation errors
- If error is unclear, ABORT with clear message
- Log all compilation attempts

Progress log: {log_path}
Format: [YYYY-MM-DDTHH:MM:SSZ] [run_id] [PHASE] message
```

---

## Safety

- Read-only: LaTeX source files
- Write: PDF, auxiliary files (.aux, .log, .bbl, etc.)
- Can modify main.tex ONLY to fix compilation errors
- No deletions of source files

---

## Example Usage

```bash
cursor-agent -p "Run compile_latex workflow.
Paper folder: /Users/cstein/code/activation_function_agent/paper/
Follow /Users/cstein/vaults/projects/agents/workflows/compile_latex/README.md"
```

