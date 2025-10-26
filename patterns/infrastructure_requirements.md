# Infrastructure Requirements for ML Paper Workflows

Purpose: What is needed to move each workflow from [Partial]/[Needs extras] to [Now], with concrete tools, permissions, and integration notes.

---

## Isolation & Permissions (Non‑negotiable)
- Sandbox first: prefer Docker or restricted sandbox execution
- Path policy: whitelisted read/write paths per project; deny all else
- No destructive ops: disable delete/rename across trees; backups before edits
- Env policy: per-project conda env; never touch `base`
- Network policy: allowlist API domains (arXiv, Crossref, Semantic Scholar, GitHub, wandb)
- Credential policy: .env / keychain; no secrets in repos or logs
- Audit: append-only `META_LOG.md` with timestamps and actions

Tooling
- Docker: non-root user, bind mounts (project rw; datasets ro), no privileged
- Sandboxing: process/user limits; no sudo; resource ceilings
- FS guardrails: pre-flight path checks; atomic writes; timestamped backups
- Git guardrails: branch-only commits; no force-push
- DB guardrails: upsert-only; migrations blocked by default

---

## Baseline
- Cursor-agent with local file access and `--browser` web search
- Directory conventions: vaults/, code/, data/
- Git available for read (history mining)

Recommended shared config
- API keys (stored securely): Crossref, arXiv, Semantic Scholar
- Python env: 3.10+, pip/conda
- CLI helpers: ripgrep, jq, pandoc (optional)

---

## Search & Citations
- Related Work Search [Partial] → [Now]
  - Tools: arXiv API, Semantic Scholar API, Crossref API
  - Additions: de-dup logic, venue whitelist, author disambiguation
  - Permissions: network

- Citation Verification → BibTeX [Partial] → [Now]
  - Tools: Crossref/DOI resolvers, BibTeX linters
  - Additions: field normalization (authors, pages, year), DOI enforcement
  - Permissions: network

---

## Experiment Design & Implementation
- Sim Design → Code Skeleton [Partial] → [Now]
  - Tools: cookiecutter/scaffold scripts, repo templates
  - Additions: config pattern (YAML/JSON), logging hooks, seed control
  - Permissions: local writes; optional git init

- Training Script Drafting [Partial] → [Now]
  - Tools: Python runner; environment manager (conda/pip)
  - Additions: package install, datasets cache path, error handling
  - Permissions: execution; network for pip

- Hyperparameter Sweeps [Now] (spec) → execution
  - Tools: wandb/optuna/ray[tune] (optional)
  - Additions: job launcher, resume logic
  - Permissions: network; GPU/queue access if used

---

## Execution & Monitoring
- Babysit Runs [Needs extras] → [Now]
  - Tools: SLURM (sbatch/squeue), tmux/screen, custom supervisor
  - Additions: log tailing, heartbeats, auto-restart on failure
  - Permissions: cluster access; process control

- Log Parsing & Registry [Needs extras] → [Now]
  - Tools: MLFlow or simple SQLite/CSV registry; regex parsers
  - Additions: schema for metrics/artifacts; run linking to git hash
  - Permissions: local writes; optional server

---

## Results & Figures
- Plots/Tables Spec [Partial] → [Now] (auto-generate)
  - Tools: matplotlib/seaborn/plotly, pandas, numpy
  - Additions: plotting style module, save paths, tightlayout
  - Permissions: local writes; headless rendering

- Error Analysis Prompts [Partial] → [Now]
  - Tools: notebooks or scripted reports
  - Additions: canned analyses (outliers, failure modes)

---

## Writing & Packaging
- Section Revision [Partial] → [Now]
  - Tools: style checkers, citation cross-check scripts
  - Additions: consistency passes (term glossary), number validation hooks

- arXiv Packaging [Partial] → [Now]
  - Tools: TeX Live + latexmk, ghostscript/ImageMagick, latexdiff
  - Additions: source pruning, image conversion, banned-command scan
  - Permissions: execution; optional network for fonts

- Camera-Ready Diffs [Partial] → [Now]
  - Tools: latexdiff, git
  - Additions: tag previous version, produce PDF diff

---

## Reproducibility & Release
- Repro Package [Partial] → [Now]
  - Tools: pytest (smoke tests), Makefile, INSTALL.md generator
  - Additions: environment lock (requirements.txt / environment.yaml)

- Env Export (Conda/Docker) [Partial] → [Now]
  - Tools: conda, docker, docker-compose (optional)
  - Additions: base image policy, CUDA variants, cache strategy
  - Permissions: docker daemon; network for pulls

- Data Release [Now] (doc) → hosting
  - Tools: Zenodo/OSF/S3 (optional)
  - Additions: PII scrub scripts, license templates
  - Permissions: network; storage creds

- Artifact Evaluation (AE) Bundle [Needs extras] → [Now]
  - Tools: Docker/Apptainer, run scripts, checksum verification
  - Additions: lightweight dataset subset, fixed seeds, time caps
  - Permissions: container runtime; optional GPU

---

## Monitoring & Ops
- Job Monitoring & Alerts
  - Tools: simple cron + email/Slack webhook; or wandb alerts
  - Additions: log pattern triggers, ETA estimates
  - Permissions: network (webhooks)

- Provenance & Timeline Mining
  - Tools: git log parsers, file mtime scanners
  - Additions: milestone extraction rules; release tagging

---

## Security & Credentials
- Store API keys in `.env` or system keychain; never commit
- Separate prod/test credentials; least-privilege scope
- For automated uploads (arXiv/venues), use non-interactive tokens where supported

---

## Phased Upgrade Plan
1) Add citation APIs (Crossref, arXiv, Semantic Scholar)
2) Add TeX toolchain and diffing
3) Add execution (Python runner) + plotting stack
4) Add containerization (Docker) and minimal AE bundle scripts
5) Add queue/cluster integration and monitoring

With these, most [Partial]/[Needs extras] workflows become [Now].
