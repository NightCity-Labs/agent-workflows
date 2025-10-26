# Improvement Prompt: Align with Source Material

**Objective**: Ensure all claims, results, and details in the section are accurately grounded in source material (KB, code, experimental results).

---

## Your Task

You are improving the **{SECTION_NAME}** section of a research paper.

**Focus**: Verify and strengthen alignment with source material.

---

## Instructions

1. **Read the current section text** (provided below)
2. **Read the source materials**:
   - Knowledge Base (KB): `{KB_PATH}/CONTENT.md`, `{KB_PATH}/COMPLETE.md`
   - Code repository: `{CODE_PATH}/`
   - Experimental results: `{CODE_PATH}/results/`, wandb logs
3. **Identify misalignments**:
   - Claims not supported by results
   - Missing experimental details
   - Incorrect numbers or statistics
   - Overstated conclusions
4. **Make corrections**:
   - Add missing details from source
   - Correct inaccuracies
   - Tone down unsupported claims
   - Add specific numbers/results where available
5. **Output the improved section**

---

## Rules

- Only make changes related to source alignment
- Do not change writing style or structure (that comes later)
- If a claim cannot be verified, flag it with `% TODO: verify claim`
- Preserve all LaTeX formatting
- Add citations to source material where appropriate

---

## Input Section

```latex
{SECTION_TEXT}
```

---

## Output Format

Return the improved section as LaTeX, followed by a brief change log:

```latex
% Improved section
{IMPROVED_SECTION_TEXT}
```

**Changes Made**:
- [Brief list of changes and reasoning]

