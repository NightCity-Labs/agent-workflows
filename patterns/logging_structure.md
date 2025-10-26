# Agent Workflow Logging Structure

**Version**: 1.0  
**Status**: Standard

---

## Log Organization

All logs go to: `/Users/cstein/code/{project}_agent/logs/`

### Naming Convention

```
{run_id}/
├── orchestrator.log          # Main orchestrator decisions and status
├── orchestrator.jsonl        # Full orchestrator agent output (stream-json)
├── step_{name}.log          # Human-readable step summary
├── step_{name}.jsonl        # Full step agent output (stream-json)
└── status.json              # Current state for monitoring
```

### Run ID Format

`{workflow}_{YYYYMMDD}_{HHMMSS}`

Example: `paper_pipeline_20251026_205654`

---

## Log Types

### 1. Orchestrator Log (orchestrator.log)
Human-readable decisions and state changes:
```
[2025-10-26T20:56:54Z] [INIT] Starting paper pipeline
[2025-10-26T20:56:55Z] [EVAL] Current state: no outline exists
[2025-10-26T20:56:55Z] [DECIDE] Run kb_to_outline workflow
[2025-10-26T20:59:10Z] [EVAL] outline.md created (15K)
[2025-10-26T20:59:10Z] [DECIDE] Run outline_to_draft workflow
...
```

### 2. Step Logs (step_{name}.jsonl)
Full cursor-agent streaming JSON output for detailed debugging.

### 3. Status File (status.json)
Current state for live monitoring:
```json
{
  "run_id": "paper_pipeline_20251026_205654",
  "status": "running",
  "current_step": "outline_to_draft",
  "steps_completed": ["kb_to_outline"],
  "steps_pending": ["prepare_figures", "compile_latex"],
  "last_update": "2025-10-26T21:00:00Z",
  "outputs": {
    "outline.md": {"exists": true, "size": 15360},
    "main.tex": {"exists": false}
  },
  "issues": []
}
```

---

## Log Retention

- Keep all logs for completed runs
- Logs are read-only after run completes
- Use run_id to correlate all logs for a single execution

---

## Access Patterns

**Monitor live progress:**
```bash
tail -f logs/{run_id}/orchestrator.log
cat logs/{run_id}/status.json
```

**Debug step failure:**
```bash
cat logs/{run_id}/step_outline_to_draft.jsonl | jq -r 'select(.type == "assistant") | .message.content[0].text'
```

**Review all decisions:**
```bash
grep DECIDE logs/{run_id}/orchestrator.log
```

