# Improvement Prompt: Check Consistency

**Objective**: Ensure notation, terminology, and cross-references are consistent across the paper.

---

## Your Task

You are improving the **{SECTION_NAME}** section of a research paper.

**Focus**: Consistency with other sections and internal coherence.

---

## Instructions

1. **Read the current section text** (provided below)
2. **Read other sections** for context:
   {OTHER_SECTIONS_PATHS}
3. **Check consistency**:
   - **Notation**: Are symbols used consistently?
   - **Terminology**: Are terms defined and used consistently?
   - **Cross-references**: Do figure/table/equation references work?
   - **Claims**: Do claims align with other sections?
   - **Definitions**: Are definitions consistent?
4. **Fix inconsistencies**:
   - Align notation with rest of paper
   - Use consistent terminology
   - Fix broken references
   - Resolve contradictions
5. **Output the improved section**

---

## Consistency Checks

- [ ] Mathematical notation matches other sections
- [ ] Terminology is consistent (e.g., "activation function" vs "nonlinearity")
- [ ] Figure/table/equation references are correct
- [ ] Claims don't contradict other sections
- [ ] Abbreviations defined on first use
- [ ] Citation style consistent

---

## Rules

- Do not change content unnecessarily
- Preserve technical accuracy
- Keep LaTeX formatting intact
- Flag unresolvable inconsistencies with `% TODO: check consistency`

---

## Input Section

```latex
{SECTION_TEXT}
```

---

## Other Sections Context

{OTHER_SECTIONS_SUMMARY}

---

## Output Format

Return the improved section as LaTeX, followed by a brief change log:

```latex
% Improved section
{IMPROVED_SECTION_TEXT}
```

**Changes Made**:
- [Brief list of consistency fixes and reasoning]

