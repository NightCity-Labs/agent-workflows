# Execution Safety Policy for Agents

Purpose: Prevent disruption to the system. Define exactly what agents may read, write, execute, and network, and how to do so safely.

---

## Operating Mode
- Default: read-first, write-minimal, no deletion.
- All writes: confined to whitelisted project paths (below). Create files; avoid editing in-place where possible; back up before edits.
- No elevated privileges: never use sudo; do not change system settings.

## Path Whitelists (per project)
- Read (broad):
  - `/Users/cstein/vaults/` (except private folders if flagged)
  - `/Users/cstein/code/`
  - Project-related Google Drive mounts (read-only)
- Write (strict, create-or-append only):
  - `vaults/projects/science/[project_name]/` (KB docs, links)
  - `code/[project_repo]/` (new files or additive edits only; prefer PR/branch when git-enabled)
  - `code/[project_repo]/outputs/`, `artifacts/`, `figures/` (new artifacts)
- Prohibited:
  - Any path outside the above (e.g., `/System`, `/Library`, home dotfiles)
  - Mass file operations (rename/move/delete trees)

## File Operations
- Creation: allowed only inside write whitelist.
- Edits: prefer additive edits; if editing existing files, make timestamped backup in the same folder before change.
- Deletion: forbidden. If cleanup is needed, mark for human review.
- Large files: do not duplicate datasets; reference paths; write checksums if needed.

## Environment Management
- Conda: create/use per-project env `miniconda3/envs/[project_slug]` only.
  - No changes to `base` env.
  - Pin versions in `environment.yaml` or `requirements.txt` saved in the project repo.
- Pip: install only into the project env; no `--user`, no system site-packages.
- Jupyter: kernels bound to the project env.

## Execution & Compute
- Python execution: only within the project env and project repo.
- Long runs: use supervised processes (tmux/screen) or cluster queue; do not leave orphaned processes.
- Resource limits: respect GPU/CPU quotas; no `nproc`/`ulimit` modifications.

## Docker/Sandbox (preferred when available)
- Run containers as non-root; no privileged mode.
- Mounts:
  - Read-write: project repo and project KB folder only
  - Read-only: datasets, shared libs
  - Block everything else by default
- Network: allowlisted domains (arXiv, Crossref, GitHub, conference sites, Weights & Biases) as needed.

## Network & Credentials
- Web search: use `--browser` flag; do not scrape aggressively; rate-limit.
- APIs: Crossref, arXiv, Semantic Scholar, wandb — keys stored securely; never hardcode in repos.
- Prohibit uploading private data. Redact secrets from logs.

## Tracking & Logging
- Weights & Biases:
  - Set `WANDB_PROJECT=[project_slug]`, `WANDB_ENTITY=[entity]`.
  - Log metrics/artifacts; never delete runs or artifacts.
- Log DB (if used): upsert-only; append logs; never destructive updates.
- Keep an audit log in `vaults/projects/science/[project_name]/META_LOG.md` summarizing actions.

## Git Hygiene (if git write is enabled)
- No force-push; no history rewrites on shared branches.
- Create feature branches: `agent/[short-task]`.
- Commit messages: clear, scoped, reference task.

## Destructive Actions: Explicitly Forbidden
- `rm -rf` outside temp folders; any recursive delete.
- `sudo`, system service changes, kernel or driver changes.
- Modifying `/System`, `/Library`, global configs, or browser profiles.
- Killing unrelated processes.

## Human-in-the-Loop Checkpoints
- Before first write in a new path, confirm whitelist membership.
- Before editing existing files, create backups and record in `META_LOG.md`.
- Before any environment or container build, write the plan and get explicit approval if outside norms.

---

## Abort Policy (Critical)

**Do NOT improvise. Do NOT change scope.**

If the specified task cannot be completed as instructed:
1. **STOP immediately** - do not switch targets, create unauthorized infra, or work around errors
2. **Log abort** - write to SQLite/Redis with status "aborted" and error message
3. **Report clearly** - state what failed, why, and what was attempted
4. **Exit cleanly** - non-zero status, final progress log line with [FAIL]

**Prohibited actions when blocked:**
- Switching compute targets (e.g., SSH fails → do NOT run locally)
- Creating infrastructure without permission (conda env, Redis, services)
- Working around missing resources (env, DB, packages)
- Proceeding on permission errors (file writes, conda, sudo)
- Continuing after repeated failures (retry once max)

**Valid abort reasons:**
- SSH/network unreachable
- Missing dependencies
- Permission denied
- Resource unavailable
- Timeout exceeded
- Safety violation
- Repeated failures

---

This policy applies to all workflows. If a workflow needs broader access, document the exception, justify it, and add a narrow-timeboxed allowance with explicit approval.
