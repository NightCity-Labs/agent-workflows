# KB Creation Workflow - Development Notes

**Created**: October 2025  
**Purpose**: Document how this workflow was created and lessons learned

---

## How This Workflow Was Created

### Initial Task
Document two completed research projects (nonlinear Hebb, second order invariance) by:
- Finding papers, code, presentations
- Creating summary and complete documentation
- Organizing in vault folders
- Linking to dashboards

### Development Process

1. **Started with detailed instructions** (9 files, very prescriptive)
   - Problem: Too much detail, agents followed templates blindly
   - Result: Hallucinated info, made-up connections, wrong formats

2. **Simplified to principles** (removed 7 files, kept 2)
   - Removed: Step-by-step guides, examples, checklists with detail
   - Kept: One-page spec (README.md), minimal checklist
   - Focus: What to do, not how to do it

3. **Tested and refined** (3 projects: crossregularization, bootstrap_sgd)
   - Fixed: Template following, hallucination, personal info
   - Added: Web search capability (--browser flag), publication links
   - Removed: README.md generation, author/institution fields

---

## Key Lessons

### What Doesn't Work
- ❌ Detailed step-by-step instructions → agents follow blindly
- ❌ Word count targets → agents pad with fluff
- ❌ Prescriptive templates → agents fill placeholders with made-up info
- ❌ Time estimates → irrelevant for AI agents
- ❌ Multiple reference files → agents get confused

### What Works
- ✅ Principle-based instructions (what, not how)
- ✅ Explicit prohibitions (no made-up info, no personal details)
- ✅ Real examples to study (nonlinear_hebb, second_order_invariance)
- ✅ Clear file outputs (00_INDEX.md, CONTENT.md, COMPLETE.md)
- ✅ Web search with --browser flag

### Critical Rules
- Only write what you actually found
- No templates, no placeholders, no made-up connections
- No author/institution/contact info (unless citing publications)
- Search online for publication info and include links
- Use wiki-link format: [[CONTENT]] not [[CONTENT.md]]

---

## How to Run

### Basic Usage

```bash
cd /Users/cstein
cursor-agent -p "Document the [PROJECT_NAME] project using the workflow at \
/Users/cstein/vaults/projects/agents/workflows/kb_creation/. \
Follow the README one-pager." \
--browser --model sonnet-4.5-thinking --output-format json -f </dev/null
```

### Flags
- `--browser`: Enable web search (required for finding publications)
- `--model sonnet-4.5-thinking`: Use thinking model (better quality)
- `--output-format json`: Get structured output
- `-f`: Force allow commands
- `</dev/null`: Non-interactive mode

### What It Does
1. Searches for project in code/, Google Drive, vaults
2. Reads papers, code, READMEs
3. Searches online for publications (with --browser)
4. Creates 3 files in `/vaults/projects/science/[project_name]/`:
   - `00_INDEX.md` - Brief overview + navigation
   - `CONTENT.md` - Scientific substance
   - `COMPLETE.md` - Project organization
5. Updates dashboards

### Post-Processing
Check for and remove:
- Personal info (author, institution, email)
- Made-up related projects
- Wrong publication info
- Template artifacts

---

## Workflow Files

### `/workflows/kb_creation/README.md`
One-page spec with:
- Task description
- 4 steps (Gather, Core Substance, Meta, Integrate)
- Rules (no templates, no made-up info, no personal details)

### `/workflows/kb_creation/TEMPLATE_CHECKLIST.md`
Optional minimal checklist (rarely used)

### `/workflows/meta/` (this folder)
Development notes and lessons learned

---

## Evolution Summary

**v1**: 9 files, detailed instructions, time estimates
- Result: Template following, hallucination

**v2**: 2 files, principle-based, no time estimates  
- Result: Better but still some issues

**v3**: Added web search, explicit prohibitions
- Result: Works well, minimal post-processing needed

---

## Future Improvements

Consider:
- Auto-detect project type (paper/code/experiment)
- Better handling of multi-paper projects
- Automatic related project detection (from actual citations)
- Integration with citation managers

---

*This workflow evolved through trial and error. The key insight: less prescription, more principle.*

