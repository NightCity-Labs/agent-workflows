# Prepare Figures Workflow

**Purpose**: Copy and organize figures for paper  
**Version**: 1.0  
**Status**: Production-ready

---

## What This Does

Copies figures from source project to paper folder, ensures proper formatting, creates captions file.

---

## Inputs

- `outline_path`: Path to outline.md (contains figure list)
- `source_figures`: Path to source figures folder
- `output_folder`: Where to copy figures

---

## Outputs

- `figures/`: Folder with copied figures
- `figure_captions.txt`: Captions for each figure

---

## Agent Instructions

```
Task: Prepare figures for paper

Outline: {outline_path}
Source: {source_figures}
Output: {output_folder}/figures/

Steps:
1. Read outline.md - get figure list with source paths

2. For each figure:
   - Verify it exists in source
   - Copy to {output_folder}/figures/
   - Rename if needed (fig1.pdf, fig2.pdf, etc.)
   - Check format (PDF/PNG preferred for LaTeX)
   - If not PDF/PNG, note conversion needed

3. Create figure_captions.txt:
   For each figure:
   - Filename
   - Proposed caption from outline
   - Which section it belongs to

4. Check figure quality:
   - Readable labels/axes
   - Appropriate resolution
   - Note any issues (too small, unclear, etc.)

Rules:
- Only copy figures listed in outline
- Preserve original files in source (read-only)
- If figure doesn't exist, note it as missing
- Don't modify figures (no cropping, editing)

Progress log: {log_path}
Format: [YYYY-MM-DDTHH:MM:SSZ] [run_id] [PHASE] message
```

---

## Safety

- Read-only: outline, source_figures
- Write-only: output_folder/figures/
- No deletions from source
- No figure modification

---

## Example Usage

```bash
cursor-agent -p "Run prepare_figures workflow.
Outline: /Users/cstein/code/activation_function_agent/paper/outline.md
Source: /Users/cstein/code/activation_function/figures/
Output: /Users/cstein/code/activation_function_agent/paper/
Follow /Users/cstein/vaults/projects/agents/workflows/prepare_figures/README.md"
```

