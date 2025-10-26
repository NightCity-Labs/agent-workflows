# Paper Improvement Workflow

**Purpose**: Iteratively improve a paper draft through section-by-section refinement with multiple improvement dimensions.

---

## Quick Start (Agent One-Pager)

```
Task: Improve paper draft for "[PROJECT NAME]"

Input: /Users/cstein/code/[project_name]/paper/main.tex
Reference Papers: /Users/cstein/code/[project_name]/paper/references/
Output: /Users/cstein/code/[project_name]/paper/main_v2.tex

Improvement Strategy:
- Section-by-section iteration (not whole paper at once)
- Multiple improvement dimensions per section
- Use reference papers for quality/style benchmarks
- Deterministic loop: for each section, for each improvement type

Improvement Dimensions (apply in order):
1. Align with source material (KB, code, results)
2. Sharpen arguments and claims
3. Improve writing style and clarity
4. Restructure for logical flow
5. Check consistency with other sections

Rules:
- Never delete content without justification
- Preserve all experimental results and figures
- Maintain LaTeX compilation compatibility
- Log all changes with reasoning
```

---

## Architecture

### Deterministic Iteration Loop

```
FOR each section in [Abstract, Intro, Methods, Results, Discussion, Conclusion]:
    FOR each improvement_type in improvement_dimensions:
        1. Extract section from main.tex
        2. Load improvement prompt from library
        3. Load reference papers context
        4. Apply improvement (cursor-agent call)
        5. Evaluate improvement (quality check)
        6. Accept or reject changes
        7. Log decision and reasoning
    END FOR
END FOR
```

### Improvement Dimensions

Each dimension has a specific prompt template in the prompt library:

1. **Source Alignment** (`prompts/align_sources.md`)
   - Check claims against KB/code/results
   - Add missing experimental details
   - Remove unsupported claims

2. **Argument Sharpening** (`prompts/sharpen_arguments.md`)
   - Strengthen logical flow
   - Make claims more precise
   - Add supporting evidence

3. **Writing Style** (`prompts/improve_style.md`)
   - Clarity and conciseness
   - Active voice
   - Technical precision
   - Match reference paper style

4. **Restructuring** (`prompts/restructure.md`)
   - Improve paragraph organization
   - Better transitions
   - Logical section flow

5. **Consistency** (`prompts/check_consistency.md`)
   - Notation consistency
   - Cross-reference accuracy
   - Terminology alignment

---

## Inputs

- **Current Draft**: `/Users/cstein/code/[project_name]/paper/main.tex`
- **KB Documentation**: `/Users/cstein/vaults/projects/science/[project_name]/`
- **Reference Papers**: `/Users/cstein/code/[project_name]/paper/references/*.pdf`
- **Improvement Prompts**: `/Users/cstein/code/agent-workflows/workflows/improve_paper/prompts/`
- **Configuration**: `/Users/cstein/code/[project_name]/paper/improvement_config.json`

---

## Outputs

- **Improved Draft**: `/Users/cstein/code/[project_name]/paper/main_v{N}.tex`
- **Change Log**: `/Users/cstein/code/[project_name]/paper/improvements_v{N}.md`
  - Section-by-section changes
  - Improvement type applied
  - Reasoning for each change
  - Accept/reject decisions
- **Diff Report**: `/Users/cstein/code/[project_name]/paper/diff_v{N-1}_to_v{N}.html`

---

## Configuration File

`improvement_config.json`:
```json
{
  "sections": ["abstract", "introduction", "methods", "results", "discussion", "conclusion"],
  "improvement_dimensions": [
    "align_sources",
    "sharpen_arguments",
    "improve_style",
    "restructure",
    "check_consistency"
  ],
  "max_iterations_per_section": 1,
  "reference_papers": [
    "references/swish_neurips2017.pdf",
    "references/gelu_arxiv2016.pdf"
  ],
  "evaluation_criteria": {
    "min_quality_score": 7,
    "require_compilation": true,
    "max_length_increase": 0.2
  }
}
```

---

## Reference Papers

Store high-quality reference papers in `paper/references/`:
- Top NeurIPS/ICML papers on similar topics
- Papers with excellent writing/structure
- Used for style/quality benchmarking

Agent reads these to understand:
- How top papers structure arguments
- Writing style and tone
- Figure presentation
- Mathematical notation conventions

---

## Evaluation Loop

After each improvement iteration:

1. **Compilation Check**: Does LaTeX still compile?
2. **Quality Assessment**: Is the section better? (agent evaluates)
3. **Length Check**: Did it grow too much?
4. **Consistency Check**: Does it fit with other sections?

If evaluation fails → reject changes, log reason, continue.

---

## Logging

- Progress log: `logs/{run_id}/improvement_orchestrator.log`
- Change decisions: `logs/{run_id}/improvement_decisions.jsonl`
- Format: `[TIMESTAMP] [SECTION] [IMPROVEMENT_TYPE] [ACCEPT|REJECT] reasoning`

---

## Safety

- Original draft is never modified (always create v{N})
- All changes are logged and reversible
- Compilation tested after each section
- Human review before finalizing

