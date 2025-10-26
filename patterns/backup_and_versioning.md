# Agent Workflow Backup & Versioning

**Version**: 1.0  
**Status**: Standard

---

## Overview

All agent workflow runs are backed up to Google Cloud Storage for:
- Historical comparison
- Debugging failed runs
- Performance analysis
- Workflow evolution tracking

---

## Run Identification

### Run ID Format

```
{workflow_type}_{YYYYMMDD}_{HHMMSS}
```

**Examples:**
- `paper_adaptive_20251026_212124`
- `kb_creation_20251026_204414`
- `paper_pipeline_20251026_205654`

### Run ID Components

- **workflow_type**: What workflow was run (paper_adaptive, kb_creation, etc.)
- **YYYYMMDD**: Date
- **HHMMSS**: Time (24-hour format)

---

## Local Storage Structure

```
/Users/cstein/code/{project}_agent/
├── logs/
│   ├── {run_id}/                    # One directory per run
│   │   ├── orchestrator.log         # Human-readable decisions
│   │   ├── orchestrator.jsonl       # Full agent output
│   │   ├── status.json             # Current state
│   │   └── step_*.jsonl            # Individual step logs (if any)
│   └── {another_run_id}/
├── paper/                           # Current output folder
├── paper_old_{timestamp}/           # Previous versions (if any)
└── backup_agent_runs.sh            # Backup script
```

---

## GCS Backup Structure

**Bucket:** `gs://ncl-agent-workflow-backups/{project}/`

```
gs://ncl-agent-workflow-backups/activation_function_agent/
├── runs/
│   ├── paper_adaptive_20251026_212124/
│   │   ├── orchestrator.log
│   │   ├── orchestrator.jsonl
│   │   └── status.json
│   ├── paper_pipeline_20251026_205654/
│   │   ├── orchestrator.log
│   │   └── step_*.jsonl
│   └── ...
├── outputs/
│   ├── paper_20251026_213045/       # Timestamped paper outputs
│   │   ├── main.pdf
│   │   ├── main.tex
│   │   └── figures/
│   └── paper_latest/                # Always points to most recent
│       ├── main.pdf
│       └── ...
└── manifests/
    └── run_manifest_20251026_213045.json  # Metadata about all runs
```

---

## Backup Script

### Location

`/Users/cstein/code/{project}_agent/backup_agent_runs.sh`

### Usage

```bash
# Manual backup
cd /Users/cstein/code/activation_function_agent
./backup_agent_runs.sh

# Check backup log
tail -f backup.log
```

### What Gets Backed Up

1. **All run directories** from `logs/`
   - Only backs up new runs (skips if already in GCS)
   - Preserves full directory structure

2. **Paper outputs** from `paper/`
   - Timestamped copy: `outputs/paper_{timestamp}/`
   - Latest copy: `outputs/paper_latest/`

3. **Run manifest** (JSON)
   - List of all runs with metadata
   - Status, decision count, size, GCS path

### Backup Frequency

**Manual:** Run after completing a workflow
**Automatic:** (Optional) Set up cron/launchd to run daily

---

## Run Manifest Format

```json
{
  "project": "activation_function_agent",
  "backup_timestamp": "2025-10-26T21:30:45Z",
  "runs": [
    {
      "run_id": "paper_adaptive_20251026_212124",
      "status": "completed",
      "decisions": 10,
      "size": "296K",
      "gcs_path": "gs://ncl-agent-workflow-backups/activation_function_agent/runs/paper_adaptive_20251026_212124/"
    },
    {
      "run_id": "paper_pipeline_20251026_205654",
      "status": "completed",
      "decisions": 0,
      "size": "691K",
      "gcs_path": "gs://ncl-agent-workflow-backups/activation_function_agent/runs/paper_pipeline_20251026_205654/"
    }
  ],
  "total_runs": 2
}
```

---

## Retrieving Backups

### List all runs

```bash
gcloud storage ls gs://ncl-agent-workflow-backups/activation_function_agent/runs/
```

### Download a specific run

```bash
gcloud storage cp -r \
  gs://ncl-agent-workflow-backups/activation_function_agent/runs/paper_adaptive_20251026_212124/ \
  ./restored_runs/
```

### Download latest paper output

```bash
gcloud storage cp -r \
  gs://ncl-agent-workflow-backups/activation_function_agent/outputs/paper_latest/ \
  ./paper_restored/
```

### View run manifest

```bash
gcloud storage cat \
  gs://ncl-agent-workflow-backups/activation_function_agent/manifests/run_manifest_20251026_213045.json
```

---

## Comparison Workflow

### Compare Two Runs

```bash
# Download both runs
gcloud storage cp -r gs://ncl-agent-workflow-backups/activation_function_agent/runs/paper_pipeline_20251026_205654/ ./run1/
gcloud storage cp -r gs://ncl-agent-workflow-backups/activation_function_agent/runs/paper_adaptive_20251026_212124/ ./run2/

# Compare orchestrator logs
diff run1/orchestrator.log run2/orchestrator.log

# Compare decisions
grep "\[DECIDE\]" run1/orchestrator.log > run1_decisions.txt
grep "\[DECIDE\]" run2/orchestrator.log > run2_decisions.txt
diff run1_decisions.txt run2_decisions.txt
```

### Compare PDF Outputs

```bash
# Download both PDFs
gcloud storage cp gs://ncl-agent-workflow-backups/activation_function_agent/outputs/paper_20251026_210000/main.pdf ./old.pdf
gcloud storage cp gs://ncl-agent-workflow-backups/activation_function_agent/outputs/paper_latest/main.pdf ./new.pdf

# Compare sizes
ls -lh old.pdf new.pdf

# Visual diff (requires diffpdf or similar)
diffpdf old.pdf new.pdf
```

---

## Retention Policy

### Local

- Keep all runs locally until manually deleted
- Recommended: Clean up after backing up to GCS

### GCS

- **Runs**: Keep indefinitely (small, valuable for analysis)
- **Outputs**: Keep timestamped for 90 days, latest indefinitely
- **Manifests**: Keep all

### Manual Cleanup

```bash
# Delete runs older than 90 days from GCS
CUTOFF=$(date -v-90d '+%Y%m%d' 2>/dev/null || date -d "90 days ago" '+%Y%m%d')
gcloud storage ls gs://ncl-agent-workflow-backups/activation_function_agent/runs/ | while read run; do
  run_date=$(basename "$run" | grep -oE '[0-9]{8}' | head -1)
  if [[ "$run_date" -lt "$CUTOFF" ]]; then
    echo "Would delete: $run"
    # gcloud storage rm -r "$run"  # Uncomment to actually delete
  fi
done
```

---

## Setup for New Projects

### 1. Create GCS Bucket (if needed)

```bash
gcloud storage buckets create gs://ncl-agent-workflow-backups \
  --location=us-central1 \
  --uniform-bucket-level-access
```

### 2. Copy Backup Script

```bash
cp /Users/cstein/code/activation_function_agent/backup_agent_runs.sh \
   /Users/cstein/code/{new_project}_agent/
   
# Update PROJECT_NAME in the script
sed -i '' 's/activation_function_agent/{new_project}_agent/g' \
  /Users/cstein/code/{new_project}_agent/backup_agent_runs.sh
```

### 3. Test Backup

```bash
cd /Users/cstein/code/{new_project}_agent
./backup_agent_runs.sh
```

---

## Integration with Workflows

### After Each Run

```bash
# At end of orchestrator script
echo "Backing up run to GCS..."
./backup_agent_runs.sh
```

### Automatic Backup

Add to orchestrator:

```bash
# After workflow completes
if [ -f "$BASE_DIR/backup_agent_runs.sh" ]; then
  log "📦 Backing up to GCS..."
  "$BASE_DIR/backup_agent_runs.sh" 2>&1 | tee -a "$LOG_FILE"
fi
```

---

## Benefits

1. **Historical Record**: Track how workflows evolve over time
2. **Debugging**: Compare failed vs successful runs
3. **Performance Analysis**: See decision patterns, timing
4. **Reproducibility**: Restore exact state of any run
5. **Comparison**: Diff outputs between workflow versions
6. **Safety**: Never lose work, even if local files deleted

---

## Related

- [[logging_structure|Logging Structure]]
- [[adaptive_orchestrator|Adaptive Orchestrator Pattern]]
- [[lessons_paper_pipeline|Lessons Learned]]

---

**Last Updated:** October 26, 2025

