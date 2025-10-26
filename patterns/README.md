# Workflow Development - General Principles

**Purpose**: Core lessons for creating AI agent workflows

---

## Isolation & Safety (Critical)
- Default read-first, write-minimal; no deletions
- Writes confined to whitelisted project paths only (KB folder, project repo, outputs)
- No sudo or system changes; no edits outside whitelists
- Per-project conda env; never modify `base`
- wandb scoped per project; never delete runs
- Log DB is upsert-only; append logs, no destructive ops
- Prefer Docker/sandbox: mount project paths rw, datasets ro
- Keep an audit `META_LOG.md` of actions
- See `execution_safety.md` for full policy

---

## Design Philosophy

### Principle-Based, Not Prescriptive
- Specify **what** to do, not **how** to do it
- Give agents initiative and flexibility
- Avoid step-by-step instructions

### Less Is More
- One-page specs preferred
- No word counts, time estimates, or detailed checklists
- Clear outputs, flexible process

---

## What Doesn't Work

❌ **Detailed templates** → Agents fill placeholders with made-up info  
❌ **Prescriptive steps** → Agents follow blindly, no initiative  
❌ **Multiple reference files** → Confusion, inconsistency  
❌ **Word/time targets** → Padding, irrelevant for AI  
❌ **Examples as templates** → Agents copy structure instead of learning

---

## What Works

✅ **Clear prohibitions** → "No made-up info" works better than "verify all info"  
✅ **Explicit outputs** → Name exact files to create  
✅ **Real examples to study** → Show finished work, not templates  
✅ **Flexible search** → List places to look, encourage finding more  
✅ **Web search enabled** → Use `--browser` flag when needed

---

## Universal Rules

1. **Only write what you actually found**
   - No placeholders, no assumptions, no made-up connections
   - If you don't know, don't write it

2. **Search comprehensively**
   - Look in obvious places, then adjacent places
   - Search online: arxiv, github, conference pages, Google Scholar
   - Include author name in searches for better results
   - Use web search when appropriate (--browser flag)
   - Read everything: papers, code, logs, READMEs

3. **Respect privacy**
   - No personal contact info unless citing publications
   - No internal emails, private notes

4. **Maintain separation**
   - Content (what) vs Meta (how organized)
   - Science vs Process
   - Facts vs Speculation

5. **Do NOT improvise or change scope**
   - If a resource is unavailable (SSH fails, env missing, permission denied), ABORT
   - Do NOT switch compute targets, create unauthorized infrastructure, or work around errors
   - Retry once; if still failing, ABORT with clear reason
   - Log abort to DB/Redis and exit cleanly

---

## Running Workflows

### Standard cursor-agent invocation:
```bash
cursor-agent -p "[TASK] using workflow at [PATH]" \
  --browser \
  --model sonnet-4.5-thinking \
  --output-format json \
  -f </dev/null
```

### Progress logging (required)
- Maintain an append-only progress log per run: `/Users/cstein/code/[agent_repo]/logs/{run_id}.log`
- Line format: `[YYYY-MM-DDTHH:MM:SSZ] [run_id] [PHASE] message`
- PHASE values: PLAN, START, STEP, INFO, WARN, DONE, FAIL
- Write at plan creation, before/after each step, and on completion/failure

### Flags:
- `--browser`: Enable web search
- `--model sonnet-4.5-thinking`: Use thinking model
- `--output-format json`: Structured output
- `-f </dev/null`: Non-interactive

---

## Testing New Workflows

1. **Create minimal spec** (one page)
2. **Test on real project** (not toy example)
3. **Check for hallucination** (made-up info, wrong connections)
4. **Refine prohibitions** (add explicit "don't do X")
5. **Test again** (different project type)

---

## Workflow Structure

```
/workflows/
  [workflow_name]/
    README.md              # One-page spec
    TEMPLATE_CHECKLIST.md  # Optional minimal checklist
  meta/
    README.md              # This file (general principles)
    execution_safety.md    # System safety & isolation policy
    [workflow]_development.md  # Specific workflow lessons
```

---

## Key Insight

**Agents need constraints, not instructions.**

Tell them what not to do, what to produce, and let them figure out how.

---

*Living document. Update as we learn from new workflows.*

