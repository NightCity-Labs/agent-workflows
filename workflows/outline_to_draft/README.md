# Outline to Draft Workflow

**Purpose**: Generate LaTeX manuscript from paper outline  
**Version**: 1.0  
**Status**: Production-ready

---

## What This Does

Takes a paper outline and KB docs, generates complete LaTeX manuscript in specified conference format.

---

## Inputs

- `outline_path`: Path to outline.md
- `kb_folder`: Path to KB folder (for detailed content)
- `output_folder`: Where to write LaTeX files
- `format`: Conference format (icml, neurips, iclr, etc.)

---

## Outputs

- `main.tex`: Complete LaTeX manuscript
- `references.bib`: Bibliography (if citations found)
- `icml2025.sty` (or other format files): Downloaded template

---

## Agent Instructions

```
Task: Generate LaTeX manuscript from outline

Input outline: {outline_path}
KB folder: {kb_folder}
Output: {output_folder}/
Format: {format}

Steps:
1. Download LaTeX template for {format}
   - Search online for official template
   - Save .sty, .cls files to output folder

2. Read outline.md - get structure
3. Read KB docs - get detailed content

4. Write main.tex:
   - Use {format} document class
   - Create sections from outline
   - Write prose for each section using KB content
   - Convert theory/equations to LaTeX math
   - Insert \includegraphics for figures (paths from outline)
   - Add \cite commands for any references

5. Write references.bib:
   - Extract any citations from KB or outline
   - Format as BibTeX entries
   - Search online if needed to complete entries

Content guidelines:
- Introduction: Clear problem statement, contribution, results preview
- Methods: Enough detail to reproduce
- Results: Highlight key findings, refer to figures
- Discussion: Interpret results, acknowledge limitations
- Write clearly, avoid jargon, define notation
- Equations: Use proper LaTeX math environments
- Figures: Use \begin{figure}...\end{figure} with captions

Rules:
- Only cite work actually mentioned in KB
- Don't make up results or experiments
- If something is unclear, note it as [TODO: clarify X]
- Keep draft focused (8-10 pages target for conference)

Progress log: {log_path}
Format: [YYYY-MM-DDTHH:MM:SSZ] [run_id] [PHASE] message
```

---

## Safety

- Read-only: outline, KB folder
- Write-only: output_folder
- Network: allowed for template download, citation lookup (with --browser)
- No deletions

---

## Example Usage

```bash
cursor-agent --browser -p "Run outline_to_draft workflow.
Outline: /Users/cstein/code/activation_function_agent/paper/outline.md
KB: /Users/cstein/vaults/projects/science/activation_function/
Output: /Users/cstein/code/activation_function_agent/paper/
Format: icml
Follow /Users/cstein/vaults/projects/agents/workflows/outline_to_draft/README.md"
```

