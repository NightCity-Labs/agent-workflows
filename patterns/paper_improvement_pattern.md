# Paper Improvement Pattern

**Purpose**: Systematically improve research paper drafts through iterative, section-by-section refinement with multiple improvement dimensions.

---

## 🎯 Core Principles

- **Section-by-Section**: Improve one section at a time, not the whole paper at once
- **Multiple Dimensions**: Apply different types of improvements (content, style, structure, consistency)
- **Deterministic Loop**: Predictable iteration order for reproducibility
- **Quality Benchmarking**: Use reference papers to set standards
- **Incremental Versioning**: v1 → v2 → v3, each preserved and backed up
- **Evaluation Loop**: Test compilation and quality after each change

---

## 🔄 The Improvement Loop

```
FOR each section in [Abstract, Intro, Methods, Results, Discussion, Conclusion]:
    FOR each improvement_type in [align_sources, sharpen_arguments, improve_style, restructure, check_consistency]:
        1. Extract section from current draft
        2. Load improvement prompt from library
        3. Load reference papers and source materials
        4. Apply improvement (cursor-agent call)
        5. Evaluate improvement (compilation, quality check)
        6. Accept or reject changes
        7. Log decision and reasoning
    END FOR
END FOR
```

---

## 📚 Improvement Dimensions

### 1. Align with Sources
**Goal**: Ensure all claims are grounded in KB, code, and experimental results.

**Actions**:
- Verify claims against source data
- Add missing experimental details
- Correct inaccuracies
- Remove unsupported claims

**Prompt**: `prompts/align_sources.md`

### 2. Sharpen Arguments
**Goal**: Strengthen logical flow and make claims more precise.

**Actions**:
- Make claims specific and precise
- Add logical connectors
- Provide supporting evidence
- Clarify cause-effect relationships

**Prompt**: `prompts/sharpen_arguments.md`

### 3. Improve Style
**Goal**: Enhance clarity, conciseness, and readability.

**Actions**:
- Use active voice
- Improve sentence variety
- Simplify complex sentences
- Use precise technical language
- Match top-tier paper style

**Prompt**: `prompts/improve_style.md`

### 4. Restructure
**Goal**: Improve organization and logical flow.

**Actions**:
- Reorder paragraphs for better flow
- Split or merge paragraphs
- Add topic sentences
- Improve transitions

**Prompt**: `prompts/restructure.md`

### 5. Check Consistency
**Goal**: Ensure notation, terminology, and cross-references are consistent.

**Actions**:
- Align notation across sections
- Use consistent terminology
- Fix broken references
- Resolve contradictions

**Prompt**: `prompts/check_consistency.md`

---

## 📁 File Structure

```
project/
├── paper/
│   ├── main.tex                    # v1 (original)
│   ├── main_v2.tex                 # v2 (improved)
│   ├── main.pdf / main_v2.pdf      # Compiled PDFs
│   ├── improvement_config.json     # Configuration
│   ├── improvements_v2.md          # Change log
│   └── references/                 # Benchmark papers
│       ├── swish_2017.pdf
│       ├── gelu_2016.pdf
│       └── mish_2019.pdf
├── logs/
│   └── improve_v2_YYYYMMDD_HHMMSS/
│       ├── orchestrator.log        # Human-readable log
│       ├── orchestrator.jsonl      # Machine-readable log
│       └── status.json             # Real-time status
└── improve_paper_orchestrator.sh   # Main script
```

---

## ⚙️ Configuration

`improvement_config.json`:
```json
{
  "version": 2,
  "base_version": 1,
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
    "references/swish_2017.pdf",
    "references/gelu_2016.pdf",
    "references/mish_2019.pdf"
  ],
  "evaluation_criteria": {
    "min_quality_score": 7,
    "require_compilation": true,
    "max_length_increase_pct": 20
  }
}
```

---

## 🔍 Reference Papers

Store high-quality papers in `paper/references/` for:
- **Style benchmarking**: How top papers write
- **Structure reference**: How to organize sections
- **Quality standards**: What excellence looks like

**Selection criteria**:
- Top-tier venues (NeurIPS, ICML, ICLR)
- Similar topic or methodology
- Excellent writing and presentation
- High citation count

---

## 🛡️ Safety & Versioning

### Version Control
- Original draft never modified (always create new version)
- Each improvement run creates a new git branch: `improve/v{N}_{run_id}`
- All changes logged and reversible

### Quality Checks
- LaTeX compilation tested after each section
- Changes rejected if compilation fails
- Length increase monitored (max 20%)
- Human review before finalizing

### Backup
- Git branches for version control
- GitHub for remote backup
- GCS for long-term archive
- All logs and outputs preserved

---

## 📊 Evaluation

After each improvement iteration:

1. **Compilation Check**: Does LaTeX still compile?
2. **Quality Assessment**: Is the section better? (agent evaluates)
3. **Length Check**: Did it grow too much?
4. **Consistency Check**: Does it fit with other sections?

If any check fails → reject changes, log reason, continue.

---

## 🚀 Usage

```bash
# Generate initial draft (v1)
./adaptive_paper_orchestrator.sh

# Improve to v2
./improve_paper_orchestrator.sh

# Review changes
git diff main..improve/v2_YYYYMMDD_HHMMSS -- paper/

# Push to GitHub
git push origin improve/v2_YYYYMMDD_HHMMSS

# Merge if satisfied
git checkout main && git merge improve/v2_YYYYMMDD_HHMMSS
```

---

## 💡 Lessons Learned

### Why Section-by-Section?
- More focused improvements
- Easier to evaluate changes
- Prevents overwhelming the agent
- Better error isolation

### Why Multiple Dimensions?
- Each dimension requires different focus
- Trying to do everything at once produces mediocre results
- Deterministic order ensures consistency

### Why Reference Papers?
- Provides concrete quality standards
- Helps agent understand "good writing"
- Reduces hallucination of style preferences

### Why Evaluation Loop?
- Catches compilation errors early
- Prevents accumulation of bad changes
- Maintains paper quality throughout

---

## 🔗 Related Patterns

- [[adaptive_orchestrator.md]]: Decision loop pattern
- [[logging_structure.md]]: Unified logging
- [[backup_and_versioning.md]]: Git + GCS backup
- [[execution_safety.md]]: Safety boundaries

---

**Last Updated**: October 26, 2025

