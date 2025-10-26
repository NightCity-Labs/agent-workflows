# Agent Workflows

General-purpose agent workflow system for ML paper development.

---

## What This Is

Reusable workflow system that can be applied to any ML research project to:
- Document projects (KB creation)
- Generate paper drafts
- Prepare figures
- Compile LaTeX

**This is the general system.** For project-specific instances, see:
- `activation_function_agent` - Example project using these workflows

---

## Structure

```
agent-workflows/
├── workflows/              # Reusable workflow specs
│   ├── kb_creation/
│   ├── outline_to_draft/
│   ├── prepare_figures/
│   └── compile_latex/
├── patterns/               # Orchestration patterns
│   ├── adaptive_orchestrator.md
│   ├── logging_structure.md
│   ├── backup_and_versioning.md
│   └── lessons_paper_pipeline.md
├── infrastructure/         # Shared infrastructure code
│   ├── agent_workflow_logger.py
│   ├── agent_status_server.py
│   └── backup_agent_runs.sh
└── docs/                   # General documentation
```

---

## Usage

### For a New Project

1. **Create project repo** (e.g., `my_project_agent`)

2. **Copy orchestrator template:**
```bash
cp agent-workflows/patterns/adaptive_orchestrator_template.sh my_project_agent/orchestrator.sh
```

3. **Configure for your project:**
   - Set project paths
   - Set KB location
   - Set source code location

4. **Run:**
```bash
cd my_project_agent
./orchestrator.sh
```

---

## Workflows

### KB Creation
Document a research project from code/papers/notes.

**Input**: Project code folder  
**Output**: KB documentation (00_INDEX.md, CONTENT.md, COMPLETE.md)

### Outline to Draft
Generate LaTeX manuscript from KB.

**Input**: KB folder, conference format  
**Output**: main.tex, references.bib

### Prepare Figures
Copy and organize figures for paper.

**Input**: Source figures, outline  
**Output**: Organized figures folder

### Compile LaTeX
Compile LaTeX to PDF.

**Input**: LaTeX files  
**Output**: PDF

---

## Patterns

### Adaptive Orchestrator
Decision loop that evaluates state and adapts.

**Use when**: Multi-step process with quality checks needed

### Logging Structure
Unified logging: all logs in `logs/{run_id}/`

### Backup & Versioning
Three-tier: Git (local) + GitHub (remote) + GCS (archive)

---

## Infrastructure

### Workflow Logger
SQLite-based logging for workflow runs.

### Status Server
Redis-backed live status monitoring.

### Backup Script
Automated GCS backup for all runs.

---

## Examples

See project repos using this system:
- `activation_function_agent` - Paper pipeline for activation function project

---

## Documentation

- `/workflows/` - Individual workflow specs
- `/patterns/` - Orchestration patterns and best practices
- `/docs/` - General guides

---

**Created**: October 26, 2025  
**Status**: Production-ready  
**License**: MIT

