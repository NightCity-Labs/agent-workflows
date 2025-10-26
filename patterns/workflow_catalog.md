# ML Paper Workflow Catalog (Detailed Draft)

Tags for feasibility:
- [Now]: Works with current cursor-agent (local files + --browser search)
- [Partial]: Achievable with search/generation; full automation needs extra tools/APIs
- [Needs extras]: Requires code execution, compilers, GPUs, queues, or external services

---

## Discovery & Scoping

### 1) Project → Knowledge Base Docs [Now]
- Goal: Create `00_INDEX.md`, `CONTENT.md`, `COMPLETE.md` for any project stage.
- Inputs: local code/docs (vaults, code/, Drive), online links (arXiv, GitHub, venues).
- Outputs: three files under `vaults/projects/science/[project_name]/` + dashboard updates.
- How to run:
  - Prompt: "Document [PROJECT] using workflow at kb_creation/ README. Include online links if published."
  - Flags: `--browser --model sonnet-4.5-thinking --output-format json -f`
- Notes: Strictly “write only what you actually found”; no personal info.

### 2) Idea → Hypotheses & Goals [Now]
- Goal: Turn a rough idea into clearly testable hypotheses and success criteria.
- Inputs: notes, related prior projects.
- Outputs: 1–2 paragraph hypothesis doc + measurable criteria.
- How to run: "From these notes, extract hypotheses and success metrics for experiments."
- Notes: Keep scope small; tie metrics to figures.

### 3) Related Work Search [Partial]
- Goal: Curate key papers with links and 1–2 line relevance notes.
- Inputs: seed papers/keywords.
- Outputs: `RELATED_WORK.md` with clusters and gaps.
- How to run: "Find related work for [TOPIC]; group by theme; include links."
- Needs: arXiv/Scholar/Semantic Scholar APIs for scale and de-dup.

---

## Theory & Planning

### 4) Theory → Figure Plan [Now]
- Goal: Map claims to figures; define variables, axes, expected trends.
- Inputs: hypotheses.
- Outputs: `FIGURE_PLAN.md` with figure-by-figure specs.
- How to run: "Propose figures to validate these hypotheses; define axes/data."

### 5) Assumptions → Math Formalization Checklist [Now]
- Goal: List assumptions, derive minimal equations/notations required.
- Outputs: `THEORY_CHECKLIST.md` with unresolved items.

### 6) Metrics & Eval Protocol [Now]
- Goal: Define primary/secondary metrics, datasets/splits, statistical tests.
- Outputs: `EVAL_PLAN.md` with acceptance thresholds.

---

## Experiment Design

### 7) Sim Design → Experiment Matrix [Now]
- Goal: Enumerate experiments (main + ablations + controls) with factors/levels.
- Outputs: `EXPERIMENT_MATRIX.md` (table of runs).

### 8) Sim Design → Code Skeleton [Partial]
- Goal: Create repo structure, config patterns, runners, logging hooks.
- Outputs: directory scaffold + templates.
- Needs: project scaffolding rules, language/runtime choices.

### 9) Dataset Plan [Partial]
- Goal: Source selection, preprocessing, splits, licensing.
- Outputs: `DATA_PLAN.md` + scripts outline.
- Needs: data access and storage policy.

---

## Implementation & Runs

### 10) Training/Experiment Script Drafting [Partial]
- Goal: Generate initial train/eval scripts with CLI/configs.
- Outputs: runnable stubs (subject to human edits).
- Needs: Python runtime, env, package install.

### 11) Hyperparameter Sweep Spec [Now]
- Goal: Define sweeps for key knobs; prioritize budget.
- Outputs: `SWEEP_SPEC.yaml` or markdown.

### 12) Main Sims → Controls & Applications Plan [Now]
- Goal: For each main result, list matched controls and simple application demos.
- Outputs: `CONTROLS_AND_APPS.md`.

### 13) Babysit Runs (Queue/Retry/Alerts) [Needs extras]
- Goal: Submit, monitor, and auto-recover jobs.
- Needs: SLURM/queue integration, log tailing, notification service.

### 14) Log Parsing & Run Registry [Needs extras]
- Goal: Centralize metrics; index runs with metadata.
- Needs: DB or flatfile registry; log parsers.

---

## Results & Analysis

### 15) Results → Plots/Tables Spec [Partial]
- Goal: Map metrics to plots/tables with styles and aggregation.
- Outputs: `PLOTS_AND_TABLES.md` (spec + code stubs optional).
- Needs: plotting lib if auto-generating.

### 16) Ablations Matrix [Now]
- Goal: Prioritize ablations that most test claims.
- Outputs: `ABLATIONS.md` with tiers.

### 17) Sanity Checks/Controls Mapping [Now]
- Goal: Checklist of must-pass sanity tests.
- Outputs: `SANITY_CHECKS.md`.

### 18) Error Analysis Prompts [Partial]
- Goal: Guide to diagnose failures and unexpected trends.
- Outputs: `ERROR_ANALYSIS.md`.

---

## Writing

### 19) Paper Outline from KB + Results [Now]
- Goal: Structured outline mapping figures to sections.
- Outputs: `OUTLINE.md`.

### 20) Section Drafting (Methods/Results/Limitations) [Now]
- Goal: First-pass text from outline + results.
- Outputs: `draft/sections/*.md` or .tex blocks.

### 21) Section Revision (Consistency/Fact Checks) [Partial]
- Goal: Tighten, remove contradictions, check numbers.
- Needs: browser for fact checks; style rules.

### 22) Figure Captions & Callouts [Now]
- Goal: Precise, informative captions; in-text callouts.
- Outputs: `captions.md`.

---

## Citations

### 23) Citation Harvest [Partial]
- Goal: Pull candidate refs (with links) from text/keywords.
- Needs: arXiv/Scholar/Semantic Scholar; de-dup.

### 24) Citation Verification → BibTeX [Partial]
- Goal: Resolve DOI, correct metadata, consistent fields.
- Outputs: `refs.bib` (validated).
- Needs: Crossref/DOI APIs; BibTeX lints.

### 25) Venue Style Formatting [Partial]
- Goal: Style compliance (abbr, fields, order).
- Outputs: formatted `.bib` + notes.

---

## Packaging & Submission

### 26) arXiv Packaging [Partial]
- Goal: Build submission tarball with valid sources and metadata.
- Outputs: `arxiv.tar.gz`, `ARXIV_METADATA.md`.
- What works now: collect files, prune aux, draft metadata, basic checks.
- Missing for full automation: TeX compile, image conversion, upload flow.

### 27) Venue Compliance Checklist [Now]
- Goal: Ensure anonymity, page limits, formatting.
- Outputs: `SUBMISSION_CHECKLIST.md`.

### 28) Rebuttal Drafting from Reviews [Now]
- Goal: Summarize critiques; point-by-point responses.
- Outputs: `REBUTTAL.md`.

### 29) Camera-Ready Diffs (latexdiff/git) [Partial]
- Goal: Produce change diffs.
- Needs: latexdiff + TeX; git tags.

---

## Reproducibility & Release

### 30) Code → Repro Package [Partial]
- Goal: Minimal install + run instructions; versioned env.
- Outputs: `INSTALL.md`, `requirements.txt` / `environment.yaml`.
- Needs: smoke tests.

### 31) Env Export (Conda/Docker) [Partial/Needs extras]
- Goal: Deterministic runtimes.
- Outputs: `Dockerfile` / `environment.yaml`.
- Needs: Docker/Conda.

### 32) Data Release Checklist [Now]
- Goal: License, docs, small sample, PII scrub.
- Outputs: `DATA_RELEASE.md`.

### 33) Colab Demo Scaffold [Partial]
- Goal: Simple runnable notebook for headline result.
- Outputs: `.ipynb` with badges.

### 34) Artifact Evaluation (AE) Bundle [Needs extras]
- Goal: Conference reproducibility package.
- Outputs: container, scripts, README_AE.
- Needs: container build, compute.

---

## Communication

### 35) Slide Deck Outline [Now]
- Outputs: `SLIDES_OUTLINE.md`.

### 36) Poster Skeleton [Now]
- Outputs: `POSTER_PLAN.md`.

### 37) Project Webpage / Blog Draft [Now]
- Outputs: page content with links and figures.

---

## Meta & Ops

### 38) Timeline Mining (git/file dates) [Now]
- Outputs: milestones, versions, dates.

### 39) Cross-Project Links Mapping [Now]
- Outputs: predecessors, follow-ups, internal wiki-links.

### 40) Dashboard Updates [Now]
- Outputs: entries in `all_projects` and `SCIENCE_ALL_PROJECTS`.

### 41) Task Board Generation [Now]
- Outputs: sprint plan tied to figures/results.

---

## How to Run (generic)
- Command pattern:
```
cursor-agent -p "[TASK] for [PROJECT]; follow workflow guidance in [PATH]; include links; no made-up info." \
  --browser --model sonnet-4.5-thinking --output-format json -f </dev/null
```
- Add author names to searches when relevant; prefer arXiv/GitHub/venue pages.
- Always separate content vs meta; facts vs speculation; if unknown, leave blank.

---

This catalog is a living document. Add or split workflows as we standardize runbooks.
