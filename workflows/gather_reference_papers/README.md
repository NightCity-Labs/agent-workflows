# Gather Reference Papers Workflow

**Purpose**: Find, download, and organize high-quality reference papers for benchmarking paper quality, style, and structure.

---

## Quick Start (Agent One-Pager)

```
Task: Gather reference papers for "[PROJECT NAME]" paper

Project Topic: [brief description]
Conference Target: [e.g., ICML, NeurIPS]
Output: /Users/cstein/code/[project_name]/paper/references/

Find 3-5 top-tier papers on similar topics:
1. Search online for highly-cited papers (arxiv, Google Scholar)
2. Prioritize: top venues (NeurIPS, ICML, ICLR), high citations, recent (last 5-7 years)
3. Download PDFs to references/ folder
4. Create REFERENCE_PAPERS.md with metadata and download commands
5. Verify PDFs downloaded correctly (check file sizes > 100KB)

Selection Criteria:
- Similar topic or methodology
- Top-tier venue (NeurIPS, ICML, ICLR, JMLR)
- High citation count (>500 for older papers, >100 for recent)
- Excellent writing and presentation quality
- Clear structure and argumentation

Rules:
- Download actual PDFs, not HTML redirects (use curl -L)
- Include arxiv links and venue information
- Document why each paper was selected
- Verify file integrity (check sizes)
```

---

## Inputs

- **Project Topic**: Brief description of the research area
- **Conference Target**: Target venue for submission (e.g., ICML, NeurIPS)
- **KB Documentation**: `/Users/cstein/vaults/projects/science/[project_name]/` (for understanding project scope)

---

## Outputs

- **References Directory**: `/Users/cstein/code/[project_name]/paper/references/`
  - PDFs of selected papers (e.g., `swish_2017.pdf`, `gelu_2016.pdf`)
  - `REFERENCE_PAPERS.md`: Metadata and rationale for each paper

---

## Reference Paper Selection

### Primary References (3-5 papers)
Papers directly related to your topic:
- Same research area
- Similar methodology
- Key prior work you're building on

### Secondary References (optional, 2-3 papers)
Papers exemplifying excellent writing:
- May not be same topic
- Chosen for clarity, structure, presentation
- Often highly-cited landmark papers

---

## REFERENCE_PAPERS.md Template

```markdown
# Reference Papers for Quality Benchmarking

High-quality papers for style, structure, and quality reference.

---

## Primary References ([Topic Area])

### 1. [Paper Title]
- **Authors**: [Author list]
- **Venue**: [Conference/Journal Year]
- **URL**: [arxiv or conference link]
- **PDF**: [direct PDF link]
- **Citations**: ~[number]
- **Why**: [1-2 sentence rationale]
- **Download**: `curl -L -o [filename].pdf [pdf_url]`

[Repeat for each paper]

---

## Download All

```bash
cd /Users/cstein/code/[project_name]/paper/references/

# Primary references
curl -L -o paper1.pdf [url1]
curl -L -o paper2.pdf [url2]
...
```

---

## Usage in Improvement Workflow

These papers serve as benchmarks for:
- **Writing style**: Clarity, conciseness, technical precision
- **Structure**: How to organize sections
- **Argumentation**: How to present and support claims
- **Figures**: Quality and presentation standards
- **Experimental design**: Comprehensive evaluation strategies
```

---

## Search Strategy

### 1. Identify Key Papers
- Search arxiv.org, Google Scholar, Papers with Code
- Use project-specific keywords + "neural networks" / "machine learning"
- Look for survey papers or highly-cited foundational work

### 2. Evaluate Quality
- Check citation count (use Google Scholar)
- Verify venue prestige (NeurIPS, ICML, ICLR > regional conferences)
- Skim abstract and introduction for clarity
- Check if paper is well-structured

### 3. Download PDFs
```bash
# Use curl with -L flag to follow redirects
curl -L -o paper_name.pdf "https://arxiv.org/pdf/XXXX.XXXXX"

# Verify download
ls -lh paper_name.pdf  # Should be > 100KB
```

### 4. Document Selection
For each paper, document:
- Why it was selected
- What aspect it exemplifies (style, structure, content)
- How it relates to your project

---

## Common Sources

### arXiv
- **URL Pattern**: `https://arxiv.org/pdf/XXXX.XXXXX`
- **Download**: `curl -L -o paper.pdf "https://arxiv.org/pdf/XXXX.XXXXX"`

### Conference Proceedings (Open Access)
- NeurIPS: `https://proceedings.neurips.cc/`
- ICML: `https://proceedings.mlr.press/`
- ICLR: `https://openreview.net/`

### Papers with Code
- **URL**: `https://paperswithcode.com/`
- Good for finding highly-cited papers with code

---

## Verification

After downloading, verify:
```bash
cd paper/references/

# Check file sizes (should be > 100KB for real PDFs)
ls -lh *.pdf

# Count pages (optional, requires pdfinfo)
for f in *.pdf; do
    echo "$f: $(pdfinfo "$f" 2>/dev/null | grep Pages | awk '{print $2}') pages"
done
```

---

## Integration with Improvement Workflow

Reference papers are used in:
- `improve_style.md` prompt: "Match the writing style of these reference papers"
- `restructure.md` prompt: "Consider how reference papers structure similar sections"
- `sharpen_arguments.md` prompt: "Use reference papers as examples of strong argumentation"

Agent reads these papers to understand quality standards and best practices.

---

## Example: Activation Functions Project

**Topic**: Novel activation functions for neural networks

**Primary References**:
1. Swish (Ramachandran et al., NeurIPS 2017) - Learned activation function
2. GELU (Hendrycks & Gimpel, 2016) - Gaussian error linear units
3. Mish (Misra, 2019) - Self-regularized activation

**Why These**:
- Directly relevant to activation function research
- Comprehensive experimental evaluation
- Clear presentation of motivation and results
- High impact (Swish: 3000+ citations, GELU: widely adopted in BERT/GPT)

---

## Logging

- Progress log: `logs/{run_id}/orchestrator.log`
- Format: `[TIMESTAMP] [PHASE] message`
- Phases: SEARCH, EVALUATE, DOWNLOAD, VERIFY, DONE

---

## Safety

- Only download from trusted sources (arxiv, conference proceedings)
- Verify file integrity (check sizes, test opening PDFs)
- Respect copyright (only use for personal research/benchmarking)

