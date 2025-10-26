# Knowledge Base Creation Workflow

**Purpose**: Document research projects (active, completed, archived)  
**Version**: 1.0  
**Created**: October 2025  
**Status**: Production-ready

---

## What This Is

Reusable workflow for creating comprehensive documentation for any research project at any stage.

---

## Quick Start (Agent One-Pager)

Run this with initiative. Prefer breadth-first search, escalate depth only when needed. If sources are missing, search broadly, note gaps, and proceed.

```
Task: Create KB docs for "[PROJECT NAME]"

Output folder: /Users/cstein/vaults/projects/science/[project_name]/
Files: 00_INDEX.md, CONTENT.md, COMPLETE.md

Gather comprehensively:
- Search: Google Drive `/work/drafts/`, `/work/projects/`, vaults, `/code/`
- Try aliases, adjacent dirs, related names
- Search online for publication info (arxiv, conference pages, github)
- If published, include links to arxiv, conference page, github repo
- Read everything you find: papers, code, READMEs, tex files, logs

CONTENT.md - what the project is about:
- Read the actual artifacts
- Write what you learned: problem, idea, how it works, what happened
- No structure requirements, just explain clearly

COMPLETE.md - project organization:
- Where files are, what's in them
- Timeline from what you found (git logs, file dates, paper versions)
- How it connects to other work
- No structure requirements, just document what exists

00_INDEX.md - brief entry point:
- Short overview
- Links to [[CONTENT]] and [[COMPLETE]]

Update dashboards:
- all_projects/README.md
- SCIENCE_ALL_PROJECTS.md

Rules:
- Only write what you actually found
- If you don't know, don't write it
- No templates, no placeholders, no made-up connections
- No author, institution, or contact info (unless citing specific publications)

Progress log (required):
- Append to `/Users/cstein/code/activation_function_agent/logs/{run_id}.log` while running
- Line format: `[YYYY-MM-DDTHH:MM:SSZ] [run_id] [PHASE] message`
- PHASE: PLAN, START, STEP, INFO, WARN, DONE, FAIL
```

---

## Files in This Workflow

**[[README.md]] (this file)**
- One-page agent spec (authoritative)

**[[TEMPLATE_CHECKLIST.md]]**
- Optional progress tracker

---

## What Gets Created

For each project, you'll have:

```
/vaults/projects/science/[project_name]/
├── 00_INDEX.md          # Quick overview & navigation (1-2 pages)
├── CONTENT.md            # Scientific content summary (~7-10k words)
├── COMPLETE.md           # Meta documentation (~10-20k words)
└── README.md             # Folder structure guide
```

**Plus**: Integration with main dashboards and cross-references

---

## The 4-Step Process

1. **Gather** → Find key artifacts (paper/code/slides/data)
2. **Core Substance** → Summarize the essence from whatever artifact exists
3. **Meta** → Document organization/timeline/locations/lessons
4. **Integrate** → Create folder and link everything

---

## When to Use This Workflow

Use for any project you want organized and documented:
- Active projects (capture current state, evolve docs as you go)
- Completed projects (archive and reference)
- Exploratory work (document what exists now)
- Code-first, paper-first, or experiment-first projects

---

## Quality Standards

This workflow produces:
- ✅ Comprehensive scientific content summaries
- ✅ Complete project meta-documentation
- ✅ Clear navigation and organization
- ✅ Working cross-references
- ✅ Integration with knowledge base
- ✅ Reusable templates for future projects

---

## Examples

Documented Projects:
- `/vaults/projects/science/nonlinear_hebb/`
- `/vaults/projects/science/second_order_invariance/`

