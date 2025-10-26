#!/bin/bash
# Gemini-based Paper Improvement Orchestrator
# Uses Gemini API for analysis/evaluation and cursor-agent for implementation

set -e

# ============================================================================
# CONFIGURATION
# ============================================================================

if [ $# -lt 2 ]; then
    echo "Usage: $0 <project_dir> <input_version>"
    echo "Example: $0 /Users/cstein/code/activation_function_agent v2"
    exit 1
fi

PROJECT_DIR="$1"
INPUT_VERSION="$2"
OUTPUT_VERSION="v$((${INPUT_VERSION#v} + 1))"

PAPER_DIR="$PROJECT_DIR/paper"
INPUT_PAPER="$PAPER_DIR/main_${INPUT_VERSION}.tex"
OUTPUT_PAPER="$PAPER_DIR/main_${OUTPUT_VERSION}.tex"

# Generate unique run ID
RUN_ID="improve_${OUTPUT_VERSION}_$(date '+%Y%m%d_%H%M%S')"
LOG_DIR="$PROJECT_DIR/logs/$RUN_ID"
mkdir -p "$LOG_DIR"

ORCH_LOG="$LOG_DIR/orchestrator.log"

# Gemini scripts location
GEMINI_DIR="/Users/cstein/code/agent-workflows/infrastructure"

# ============================================================================
# LOGGING
# ============================================================================

log() {
    local phase=$1
    shift
    local msg="$@"
    local timestamp=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
    echo "[$timestamp] [$phase] $msg" | tee -a "$ORCH_LOG"
}

# ============================================================================
# INITIALIZATION
# ============================================================================

log "START" "Gemini improvement orchestrator: ${INPUT_VERSION} → ${OUTPUT_VERSION}"
log "INFO" "Input: $INPUT_PAPER"
log "INFO" "Output: $OUTPUT_PAPER"
log "INFO" "Run ID: $RUN_ID"

# Create new git branch
cd "$PROJECT_DIR"
BRANCH_NAME="improve/${OUTPUT_VERSION}_${RUN_ID}"
log "INFO" "Creating git branch: $BRANCH_NAME"
git checkout -b "$BRANCH_NAME" 2>&1 | tee -a "$ORCH_LOG"

# Copy input to output
cp "$INPUT_PAPER" "$OUTPUT_PAPER"
log "INFO" "Copied ${INPUT_VERSION} to ${OUTPUT_VERSION} for improvement"

# ============================================================================
# PHASE 1: STRATEGIC ASSESSMENT
# ============================================================================

log "PHASE1" "Strategic assessment (Gemini)"

python3 "$GEMINI_DIR/gemini_strategic_assessment.py" \
    "$INPUT_PAPER" \
    --output "$LOG_DIR/strategic_assessment.md" \
    2>&1 | tee -a "$ORCH_LOG"

log "INFO" "Strategic assessment complete"

# ============================================================================
# PHASE 2: REFERENCE ANALYSIS (cached if exists)
# ============================================================================

STYLE_GUIDE="$PAPER_DIR/reference_style_guide.md"

if [ ! -f "$STYLE_GUIDE" ]; then
    log "PHASE2" "Analyzing reference papers (one-time, Gemini)"
    
    python3 "$GEMINI_DIR/gemini_analyze_references.py" \
        --references-dir "$PAPER_DIR/references" \
        --output "$STYLE_GUIDE" \
        2>&1 | tee -a "$ORCH_LOG"
    
    log "INFO" "Reference analysis complete (cached for future runs)"
else
    log "PHASE2" "Using cached reference style guide"
fi

# ============================================================================
# PHASE 3: IMPROVEMENT RECOMMENDATIONS (Gemini)
# ============================================================================

log "PHASE3" "Generating improvement recommendations (Gemini)"

# Optional: Create KB summary if not exists
KB_SUMMARY="$LOG_DIR/kb_summary.txt"
if [ -d "/Users/cstein/vaults/projects/science/activation_function" ]; then
    cat /Users/cstein/vaults/projects/science/activation_function/CONTENT.md \
        /Users/cstein/vaults/projects/science/activation_function/COMPLETE.md \
        | head -200 > "$KB_SUMMARY"
fi

# Generate recommendations for each improvement type
for imp_type in align_sources sharpen_arguments improve_style restructure check_consistency; do
    log "ANALYZE" "Analyzing for: $imp_type"
    
    python3 "$GEMINI_DIR/gemini_paper_analyzer.py" \
        "$OUTPUT_PAPER" \
        --type "$imp_type" \
        --kb-summary "$KB_SUMMARY" \
        --style-guide "$STYLE_GUIDE" \
        --strategic-goals "$LOG_DIR/strategic_assessment.md" \
        --output "$LOG_DIR/recommendations_${imp_type}.md" \
        2>&1 | tee -a "$ORCH_LOG"
done

log "INFO" "All recommendations generated"

# ============================================================================
# PHASE 4: APPLY IMPROVEMENTS (cursor-agent)
# ============================================================================

log "PHASE4" "Applying improvements (cursor-agent)"

# Create master prompt for cursor-agent
CURSOR_PROMPT="$LOG_DIR/cursor_improvement_prompt.md"

cat > "$CURSOR_PROMPT" <<EOF
EXECUTE THIS TASK IMMEDIATELY. DO NOT ASK FOR CONFIRMATION.

You are an expert LaTeX editor. Your task is to apply improvement recommendations to a research paper.

## WHAT YOU MUST DO NOW:

1. Read these 5 recommendation files:
   - $LOG_DIR/recommendations_align_sources.md
   - $LOG_DIR/recommendations_sharpen_arguments.md
   - $LOG_DIR/recommendations_improve_style.md
   - $LOG_DIR/recommendations_restructure.md
   - $LOG_DIR/recommendations_check_consistency.md

2. Edit this file to apply ALL recommendations: $OUTPUT_PAPER

3. The input file for reference is: $INPUT_PAPER

## CRITICAL RULES:

- EDIT $OUTPUT_PAPER DIRECTLY - do not just read it
- Apply EVERY recommendation from ALL 5 files
- Maintain valid LaTeX syntax
- Preserve all \\includegraphics, \\cite, and equations
- Make substantial changes - the diff should show many modifications
- Work section by section through the entire paper

START IMMEDIATELY. Read the first recommendation file now.
EOF

# Replace placeholders
sed -i '' "s|INPUT_VERSION|${INPUT_VERSION}|g" "$CURSOR_PROMPT"
sed -i '' "s|OUTPUT_VERSION|${OUTPUT_VERSION}|g" "$CURSOR_PROMPT"
sed -i '' "s|OUTPUT_PAPER|${OUTPUT_PAPER}|g" "$CURSOR_PROMPT"

log "EXECUTE" "Running cursor-agent to apply improvements"

cd "$PROJECT_DIR"

cursor-agent \
    --model sonnet-4.5-thinking \
    --print \
    --output-format stream-json \
    "$CURSOR_PROMPT" \
    < /dev/null \
    > "$LOG_DIR/cursor_agent.jsonl" 2>&1

log "INFO" "cursor-agent completed"

# Check if changes were made
CHANGES=$(diff "$INPUT_PAPER" "$OUTPUT_PAPER" | wc -l)
log "INFO" "Changes made: $CHANGES lines different"

if [ "$CHANGES" -eq 0 ]; then
    log "ERROR" "cursor-agent made NO changes! v2 and v3 are identical"
    log "ERROR" "Check $LOG_DIR/cursor_agent.jsonl for details"
    exit 1
fi

# Show summary of changes
log "CHANGES" "Showing first 30 lines of diff:"
diff "$INPUT_PAPER" "$OUTPUT_PAPER" | head -30 | tee -a "$ORCH_LOG"

# ============================================================================
# PHASE 5: COMPILE PDF
# ============================================================================

log "COMPILE" "Compiling ${OUTPUT_VERSION} to PDF"

cd "$PAPER_DIR"

pdflatex -interaction=nonstopmode "main_${OUTPUT_VERSION}.tex" > "$LOG_DIR/compile.log" 2>&1
bibtex "main_${OUTPUT_VERSION}" >> "$LOG_DIR/compile.log" 2>&1 || true
pdflatex -interaction=nonstopmode "main_${OUTPUT_VERSION}.tex" >> "$LOG_DIR/compile.log" 2>&1
pdflatex -interaction=nonstopmode "main_${OUTPUT_VERSION}.tex" >> "$LOG_DIR/compile.log" 2>&1

if [ -f "main_${OUTPUT_VERSION}.pdf" ]; then
    PDF_SIZE=$(ls -lh "main_${OUTPUT_VERSION}.pdf" | awk '{print $5}')
    PDF_PAGES=$(pdfinfo "main_${OUTPUT_VERSION}.pdf" 2>/dev/null | grep Pages | awk '{print $2}' || echo "?")
    log "DONE" "PDF generated: ${PDF_SIZE}, ${PDF_PAGES} pages"
else
    log "ERROR" "PDF generation failed"
    exit 1
fi

cd "$PROJECT_DIR"

# ============================================================================
# PHASE 6: FINAL EVALUATION (Gemini)
# ============================================================================

log "EVALUATE" "Final quality evaluation (Gemini)"

python3 "$GEMINI_DIR/gemini_paper_evaluator.py" \
    "$OUTPUT_PAPER" \
    --version "$OUTPUT_VERSION" \
    --run-id "$RUN_ID" \
    --output "$LOG_DIR/evaluation.json" \
    2>&1 | tee -a "$ORCH_LOG"

log "INFO" "Evaluation complete"

# Display evaluation summary
if [ -f "$LOG_DIR/evaluation.json" ]; then
    # Check if evaluation failed
    ERROR=$(jq -r '.error // empty' "$LOG_DIR/evaluation.json" 2>/dev/null)
    if [ -n "$ERROR" ]; then
        log "ERROR" "Evaluation failed: $ERROR"
        QUALITY="FAILED"
        ACCEPT_PROB="FAILED"
        VENUE="FAILED"
    else
        QUALITY=$(jq -r '.scores.overall_quality' "$LOG_DIR/evaluation.json" 2>/dev/null || echo "?")
        ACCEPT_PROB=$(jq -r '.scores.acceptance_probability' "$LOG_DIR/evaluation.json" 2>/dev/null || echo "?")
        VENUE=$(jq -r '.estimated_venue' "$LOG_DIR/evaluation.json" 2>/dev/null || echo "?")
        
        log "EVAL" "Quality: $QUALITY/10, Accept Prob: $ACCEPT_PROB, Venue: $VENUE"
    fi
else
    log "ERROR" "Evaluation file not found"
    QUALITY="MISSING"
    ACCEPT_PROB="MISSING"
    VENUE="MISSING"
fi

# ============================================================================
# GIT COMMIT & BACKUP
# ============================================================================

log "GIT" "Committing ${OUTPUT_VERSION} to branch $BRANCH_NAME"

git add paper/ logs/"$RUN_ID"/
git commit -m "Paper improvement: ${INPUT_VERSION} → ${OUTPUT_VERSION}

Run: $RUN_ID
PDF: ${PDF_SIZE}, ${PDF_PAGES} pages
Quality: ${QUALITY}/10
Logs: logs/$RUN_ID/
Branch: $BRANCH_NAME" 2>&1 | tee -a "$ORCH_LOG"

log "BACKUP" "Running GCS backup"
if [ -f "$PROJECT_DIR/backup_agent_runs.sh" ]; then
    "$PROJECT_DIR/backup_agent_runs.sh" 2>&1 | tail -5 | tee -a "$ORCH_LOG" || log "WARN" "Backup failed (non-critical)"
else
    log "WARN" "Backup script not found, skipping"
fi

# ============================================================================
# COMPLETION
# ============================================================================

log "DONE" "Paper improvement complete"

# Print summary to stdout (not just log file)
echo ""
echo "============================================"
echo "WORKFLOW SUMMARY"
echo "============================================"
echo "Changes: $CHANGES lines modified"
echo "PDF: ${PDF_SIZE}, ${PDF_PAGES} pages"
echo "Quality: ${QUALITY}/10"
echo "Accept Prob: ${ACCEPT_PROB}"
echo "Venue: ${VENUE}"
echo "============================================"
echo ""

echo ""
echo "============================================"
echo "Paper Improvement Complete!"
echo "============================================"
echo "Version: ${INPUT_VERSION} → ${OUTPUT_VERSION}"
echo "PDF: $PAPER_DIR/main_${OUTPUT_VERSION}.pdf (${PDF_SIZE}, ${PDF_PAGES} pages)"
echo "Quality: ${QUALITY}/10"
echo "Accept Probability: ${ACCEPT_PROB}"
echo "Estimated Venue: ${VENUE}"
echo "Logs: $LOG_DIR/"
echo "Branch: $BRANCH_NAME"
echo ""
echo "Next steps:"
echo "  1. Review: git diff main..${BRANCH_NAME} -- paper/"
echo "  2. Check evaluation: cat $LOG_DIR/evaluation.json"
echo "  3. Push: git push origin ${BRANCH_NAME}"
echo "============================================"

