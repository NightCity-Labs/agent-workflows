# Improvement Prompt: Improve Writing Style

**Objective**: Enhance clarity, conciseness, and readability while matching the style of top-tier papers.

---

## Your Task

You are improving the **{SECTION_NAME}** section of a research paper.

**Focus**: Writing quality, clarity, and style.

---

## Instructions

1. **Read the current section text** (provided below)
2. **Read reference papers** for style benchmarking:
   {REFERENCE_PAPERS_LIST}
3. **Improve writing**:
   - Use active voice where appropriate
   - Improve sentence variety and flow
   - Simplify complex sentences
   - Use precise technical language
   - Remove jargon where simpler terms work
   - Improve paragraph transitions
4. **Match conference style**:
   - ICML writing conventions
   - Concise but complete
   - Technical precision
5. **Output the improved section**

---

## Style Guidelines

- **Clarity**: Every sentence should be immediately understandable
- **Conciseness**: No unnecessary words
- **Precision**: Technical terms used correctly
- **Flow**: Smooth transitions between ideas
- **Tone**: Professional, confident but not arrogant

---

## Rules

- Do not change technical content or results
- Preserve all citations and references
- Keep LaTeX formatting intact
- Maintain section structure

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

