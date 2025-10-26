# Improvement Prompt: Restructure Section

**Objective**: Improve paragraph organization, logical flow, and section structure.

---

## Your Task

You are improving the **{SECTION_NAME}** section of a research paper.

**Focus**: Structural organization and logical flow.

---

## Instructions

1. **Read the current section text** (provided below)
2. **Analyze structure**:
   - Is the information in the right order?
   - Do paragraphs have clear topics?
   - Are transitions smooth?
   - Is there a logical progression?
3. **Restructure if needed**:
   - Reorder paragraphs for better flow
   - Split or merge paragraphs as appropriate
   - Add topic sentences
   - Improve transitions between paragraphs
   - Consider subsection organization
4. **Check against reference papers**:
   {REFERENCE_PAPERS_LIST}
   - How do they structure similar sections?
5. **Output the improved section**

---

## Structural Principles

- **Topic sentences**: Each paragraph should have a clear main point
- **Logical flow**: Ideas should build on each other
- **Transitions**: Clear connections between paragraphs
- **Hierarchy**: Use subsections if needed for clarity
- **Completeness**: All necessary information present

---

## Rules

- Do not change technical content
- Preserve all results, figures, and citations
- Keep LaTeX formatting intact
- Major restructuring should be justified

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
- [Brief list of structural changes and reasoning]

