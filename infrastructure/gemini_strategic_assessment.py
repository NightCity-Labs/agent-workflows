#!/usr/bin/env python3
"""
Strategic assessment of paper quality and improvement goals.
High-level analysis focused on NeurIPS acceptance and impact.
"""

import sys
import os
import argparse
from pathlib import Path

# Add ncl_agents to path
sys.path.insert(0, '/Users/cstein/code/ncl_agents/src')

from llm_lib.llm.manager import LLM


class StrategicAssessor:
    """Provide strategic assessment of paper quality and goals."""
    
    def __init__(self, model: str = "vertex_ai/gemini-2.5-pro"):
        self.llm = LLM(model=model)
        self.model = model
    
    def assess(self, paper_tex: str) -> str:
        """
        Provide strategic assessment of paper.
        
        Args:
            paper_tex: Full LaTeX paper content
        
        Returns:
            Strategic assessment as markdown
        """
        system_prompt = """You are a NeurIPS area chair with deep expertise in machine learning.
Your goal: Identify what would make this paper a spotlight or oral presentation.

Think about:
- What makes papers memorable at NeurIPS?
- What gets people excited in talks?
- What drives high citation counts?
- What makes reviewers advocate for acceptance?"""

        user_prompt = f"""Assess this paper strategically for NeurIPS submission.

PAPER:
```latex
{paper_tex}
```

Provide a strategic assessment covering:

## Current Positioning
- What is this paper's current strength?
- Where does it stand vs typical NeurIPS papers?
- Estimated current outcome: reject/poster/spotlight/oral?

## Path to Spotlight/Oral
- What would make this a spotlight?
- What would make this an oral?
- What's the gap between current state and those goals?

## Key Leverage Points
- What 2-3 improvements would have highest impact?
- What's currently holding it back most?
- What's the low-hanging fruit?

## Impact Potential
- What's the potential citation impact?
- What communities would care about this?
- What follow-up work could it enable?

## Recommended Strategy
- Should we aim for spotlight or be content with poster?
- What's the priority order for improvements?
- What should we NOT change (already strong)?

Be honest and strategic. Think like an area chair deciding between 100 papers."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self.llm.chat(messages, temperature=0.4, max_tokens=2000)
        return response


def main():
    """CLI for strategic assessment."""
    parser = argparse.ArgumentParser(description="Strategic assessment of paper quality")
    parser.add_argument("paper_file", help="LaTeX paper file")
    parser.add_argument("--output", "-o", required=True, help="Output markdown file")
    parser.add_argument("--model", default="vertex_ai/gemini-2.5-pro", help="Model to use")
    
    args = parser.parse_args()
    
    # Read paper
    paper_tex = Path(args.paper_file).read_text()
    
    print(f"🎯 Performing strategic assessment...", file=sys.stderr)
    
    # Assess
    assessor = StrategicAssessor(model=args.model)
    assessment = assessor.assess(paper_tex)
    
    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(assessment)
    
    print(f"✅ Strategic assessment written to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()

