# Lessons Learned: Paper Pipeline Development

**Date**: 2025-10-26  
**Project**: activation_function KB → ICML PDF  
**Status**: Success (after iteration)

---

## What We Built

1. **KB creation workflow** - Document research projects
2. **Paper pipeline** - KB → ICML PDF with figures
3. **Modular workflows** - kb_to_outline, outline_to_draft, prepare_figures, compile_latex
4. **Adaptive orchestrator** - Decision loop pattern

---

## What Went Wrong (First Attempt)

### Issue 1: Rigid Sequential Pipeline

**Problem:**
- Created 4 workflows that must run in fixed order: 1→2→3→4
- Step 2 (draft) ran before Step 3 (figures)
- Draft agent didn't know what figures would be named
- Commented out all `\includegraphics` with wrong paths
- Step 3 copied figures but LaTeX was already written

**Root cause:** No feedback between steps, no adaptation

**Symptom:** PDF compiled but had NO figures (all commented out)

### Issue 2: Scattered Logs

**Problem:**
- Pipeline log in one place
- Step logs in another
- Progress logs supposed to go somewhere else
- Hard to track what happened

**Root cause:** No logging standard defined upfront

### Issue 3: No Quality Checks

**Problem:**
- Orchestrator just ran steps blindly
- Didn't check if outputs were correct
- Declared success even though PDF was incomplete

**Root cause:** No evaluation between steps

---

## What We Fixed

### Fix 1: Adaptive Orchestrator Pattern

**Solution:** Decision loop instead of fixed script

```
while not done:
    EVALUATE current state
    DECIDE next action
    EXECUTE action
    LOG result
```

**Benefits:**
- Can run workflows in any order
- Can fix issues mid-pipeline
- Can verify outputs
- Adapts to actual state

**Result:** PDF with figures, correct paths, complete output

### Fix 2: Unified Logging Structure

**Solution:** All logs in `logs/{run_id}/`

```
logs/paper_adaptive_20251026_212124/
├── orchestrator.log      # Human-readable decisions
├── orchestrator.jsonl    # Full agent output
└── status.json          # Current state
```

**Benefits:**
- Easy to find all logs for a run
- Clear what happened when
- Can monitor live progress

### Fix 3: Evaluation After Each Action

**Solution:** Orchestrator checks output quality

```
[EVAL] Checking final output quality
[EVAL] Final state check:
- main.pdf: EXISTS, 567KB, 7 pages
- Figures: 8 figures present in PDF
- Compilation: SUCCESSFUL
```

**Benefits:**
- Catches issues before continuing
- Can fix problems
- Knows when actually done

---

## Key Insights

### 1. Agent Initiative > Rigid Steps

**Don't:** Create detailed step-by-step instructions
**Do:** Give goal, resources, rules - let agent decide

The adaptive orchestrator figured out the right order and dependencies itself.

### 2. Evaluate, Don't Assume

**Don't:** Run step → assume success → continue
**Do:** Run step → check output → decide next action

The first pipeline assumed everything worked. The adaptive one verified.

### 3. Modular Workflows Are Still Useful

**Keep:** Individual workflow specs (kb_to_outline, etc.)
**Change:** How they're orchestrated (adaptive vs fixed)

The workflows themselves were fine. The rigid orchestration was the problem.

### 4. Logging Is Critical

**Must have:**
- All logs in one place
- Clear timestamps
- Decision rationale
- Current state

Without good logs, impossible to debug or understand what happened.

---

## Workflow Design Principles (Updated)

### When to Use Adaptive Orchestrator

✅ Multi-step process with dependencies
✅ Output quality matters
✅ Steps might fail or produce incomplete results  
✅ Need to verify and fix issues
✅ Goal is clear but path is flexible

### When to Use Fixed Pipeline

✅ Simple deterministic sequence
✅ Steps are independent
✅ No quality checks needed
✅ Fast iteration more important than robustness

### When to Use Single Agent

✅ One clear task
✅ No complex dependencies
✅ Agent can handle everything in one call

---

## Metrics

### First Attempt (Rigid Pipeline)
- Time: ~13 minutes
- Result: PDF with NO figures (commented out)
- Logs: Scattered across 3 locations
- Quality: Incomplete

### Second Attempt (Adaptive Orchestrator)
- Time: ~7 minutes
- Result: PDF with 8 figures, complete
- Logs: All in `logs/{run_id}/`
- Quality: Ready for review

**Adaptive was faster AND better.**

---

## Next Steps

### Improvements to Make

1. **Add more evaluation checks:**
   - Figure count matches outline
   - PDF page count in expected range
   - No compilation warnings
   - Bibliography complete

2. **Add repair workflows:**
   - fix_latex_figures: Uncomment and fix paths
   - fix_compilation: Parse errors and fix
   - improve_formatting: Adjust spacing, layout

3. **Make workflows more robust:**
   - Better error messages
   - Clearer abort conditions
   - More examples in specs

4. **Test on other projects:**
   - bootstrap_sgd
   - crossregularization
   - Different paper formats (NeurIPS, ICLR)

### Patterns to Reuse

- ✅ Adaptive orchestrator pattern
- ✅ Unified logging structure
- ✅ Evaluation between actions
- ✅ Modular workflow specs
- ✅ Decision loop with state tracking

---

## Conclusion

**The key lesson:** Give agents goals and let them decide how to achieve them, rather than forcing rigid step sequences.

The adaptive orchestrator pattern works because:
- Agents can see the full context
- They can adapt to actual state
- They can fix issues
- They know when they're actually done

This is the pattern to use for all complex multi-step workflows going forward.

