# Improvement Prompt: Sharpen Arguments

**Objective**: Strengthen logical flow, make claims more precise, and add supporting evidence.

---

## Your Task

You are improving the **{SECTION_NAME}** section of a research paper.

**Focus**: Make arguments clearer, stronger, and more precise.

---

## Instructions

1. **Read the current section text** (provided below)
2. **Identify weak arguments**:
   - Vague or imprecise claims
   - Missing logical connections
   - Weak transitions between ideas
   - Claims without sufficient support
3. **Strengthen arguments**:
   - Make claims more specific and precise
   - Add logical connectors and transitions
   - Provide supporting evidence or reasoning
   - Clarify cause-effect relationships
4. **Remove fluff**:
   - Delete unnecessary hedging (unless scientifically appropriate)
   - Remove redundant statements
   - Cut vague language
5. **Output the improved section**

---

## Rules

- Maintain scientific accuracy (don't overstate)
- Preserve all experimental results and citations
- Keep LaTeX formatting intact
- Focus on logical flow and precision, not style

---

## Reference Quality

Look at these reference papers for examples of strong arguments:
{REFERENCE_PAPERS_LIST}

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

