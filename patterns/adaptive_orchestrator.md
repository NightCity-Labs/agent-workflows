# Adaptive Orchestrator Pattern

**Version**: 1.0  
**Status**: Standard

---

## Core Principle

Orchestrator is a **decision loop**, not a fixed script.

```
while not done:
    1. EVALUATE current state
    2. DECIDE next action
    3. EXECUTE action
    4. LOG results
```

---

## Orchestrator Agent Prompt Template

```
You are an adaptive orchestrator for {GOAL}.

GOAL: {specific goal, e.g., "Create ICML PDF from KB documentation"}

RESOURCES:
- Input: {input paths}
- Output: {output paths}
- Available workflows: {list of workflow paths}

CURRENT STATE:
{what files exist, what's been done, what issues were found}

YOUR JOB:
1. Evaluate current state
2. Decide next action:
   - Run a workflow
   - Fix an issue
   - Verify output
   - Declare done
3. Execute the action
4. Update state and repeat

DECISION RULES:
- Check outputs after each step
- If something is wrong, fix it (don't just continue)
- If a workflow fails, try alternative approach
- If stuck after 3 attempts, abort with clear reason
- Log every decision to {log_path}

AVAILABLE ACTIONS:
- run_workflow: Execute a workflow from {workflows_dir}
- fix_issue: Direct fix (e.g., uncomment figures, fix paths)
- verify: Check output quality
- abort: Stop with reason
- done: Mark complete

STATE TRACKING:
Update {status_json} after each action with:
- What was done
- What exists now
- What issues remain
- Next planned action

SAFETY:
- Read-only: {source_paths}
- Write-only: {output_paths}
- All actions logged
- Follow execution_safety.md abort policy

Now evaluate the current state and decide your first action.
```

---

## Example Decision Flow

**Goal:** Create ICML PDF from KB

**Loop 1:**
- EVAL: No files exist
- DECIDE: Run kb_to_outline
- EXECUTE: outline.md created
- LOG: outline exists (15K)

**Loop 2:**
- EVAL: outline exists, no LaTeX
- DECIDE: Run outline_to_draft
- EXECUTE: main.tex created but figures commented out
- LOG: main.tex exists but incomplete

**Loop 3:**
- EVAL: main.tex has commented figures
- DECIDE: Run prepare_figures first, then fix LaTeX
- EXECUTE: figures copied, paths fixed in main.tex
- LOG: main.tex updated with correct paths

**Loop 4:**
- EVAL: main.tex ready, no PDF
- DECIDE: Run compile_latex
- EXECUTE: PDF created
- LOG: main.pdf exists (257K, 9 pages)

**Loop 5:**
- EVAL: PDF exists, check quality
- DECIDE: Verify PDF has figures
- EXECUTE: Check shows no figures in PDF
- LOG: Issue detected - figures still missing

**Loop 6:**
- EVAL: Figures in folder but not in PDF
- DECIDE: Fix - uncomment includegraphics in main.tex
- EXECUTE: LaTeX updated
- LOG: main.tex fixed

**Loop 7:**
- EVAL: LaTeX fixed, need recompile
- DECIDE: Run compile_latex again
- EXECUTE: PDF regenerated
- LOG: main.pdf updated

**Loop 8:**
- EVAL: PDF has figures, looks complete
- DECIDE: done
- LOG: Pipeline complete

---

## Implementation

Single cursor-agent call with full context, runs decision loop internally.

**NOT:** Separate orchestrator script calling multiple agents

**YES:** One agent that decides and acts iteratively

---

## Advantages

- Adapts to problems
- Can fix issues mid-pipeline
- No rigid step order
- Learns from previous actions
- Can try alternatives if something fails

---

## Logging

Every decision logged:
```
[timestamp] [EVAL] {current state}
[timestamp] [DECIDE] {chosen action and why}
[timestamp] [EXECUTE] {what happened}
[timestamp] [RESULT] {outcome}
```

---

## When to Use

Use adaptive orchestrator when:
- Multi-step process with dependencies
- Output quality matters
- Steps might fail or produce incomplete results
- Need to verify and fix issues
- Goal is clear but path is flexible

Don't use when:
- Single simple task
- Fixed deterministic sequence
- No quality checks needed

