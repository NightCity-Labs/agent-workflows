#!/usr/bin/env python3
"""
Gemini-based paper analyzer for improvement recommendations.
Analyzes full paper with context and provides section-by-section recommendations.
"""

import sys
import os
import argparse
from pathlib import Path
from typing import Optional

# Add ncl_agents to path
sys.path.insert(0, '/Users/cstein/code/ncl_agents/src')

from llm_lib.llm.manager import LLM


class PaperAnalyzer:
    """Analyze paper and provide improvement recommendations."""
    
    IMPROVEMENT_TYPES = {
        "align_sources": {
            "name": "Source Alignment",
            "focus": "Ensure all claims are grounded in KB/code/results. Verify accuracy."
        },
        "sharpen_arguments": {
            "name": "Argument Sharpening",
            "focus": "Strengthen logical flow, make claims more precise, add evidence."
        },
        "improve_style": {
            "name": "Writing Style",
            "focus": "Enhance clarity, conciseness, active voice, professional tone."
        },
        "restructure": {
            "name": "Structure & Organization",
            "focus": "Improve paragraph organization, transitions, logical flow."
        },
        "check_consistency": {
            "name": "Consistency",
            "focus": "Ensure notation, terminology, cross-references are consistent."
        }
    }
    
    def __init__(self, model: str = "vertex_ai/gemini-2.5-pro"):
        self.llm = LLM(model=model)
        self.model = model
    
    def analyze(
        self,
        paper_tex: str,
        improvement_type: str,
        kb_summary: Optional[str] = None,
        style_guide: Optional[str] = None,
        strategic_goals: Optional[str] = None
    ) -> str:
        """
        Analyze paper and provide improvement recommendations.
        
        Args:
            paper_tex: Full LaTeX paper content
            improvement_type: Type of improvement (align_sources, sharpen_arguments, etc.)
            kb_summary: Optional KB summary for context
            style_guide: Optional style guidelines from reference papers
            strategic_goals: Optional strategic assessment goals
        
        Returns:
            Markdown recommendations
        """
        if improvement_type not in self.IMPROVEMENT_TYPES:
            raise ValueError(f"Unknown improvement type: {improvement_type}")
        
        imp_info = self.IMPROVEMENT_TYPES[improvement_type]
        
        system_prompt = f"""You are an expert scientific writing editor for top-tier ML conferences.
You are analyzing a paper for: {imp_info['name']}

Focus: {imp_info['focus']}

Your goal: Help this paper reach NeurIPS spotlight/oral quality."""

        # Build context
        context_parts = []
        
        if strategic_goals:
            context_parts.append(f"STRATEGIC GOALS:\n{strategic_goals}\n")
        
        if style_guide:
            context_parts.append(f"STYLE GUIDELINES (from top papers):\n{style_guide}\n")
        
        if kb_summary:
            context_parts.append(f"KNOWLEDGE BASE SUMMARY:\n{kb_summary}\n")
        
        context = "\n".join(context_parts) if context_parts else ""
        
        user_prompt = f"""{context}

PAPER TO ANALYZE:
```latex
{paper_tex}
```

TASK: Analyze for {imp_info['name']}

Provide:

## Overall Assessment
Brief 2-3 sentence assessment of current state for this improvement dimension.

## Section-by-Section Recommendations

For each major section (Abstract, Introduction, Methods, Results, Discussion, Conclusion):

### [Section Name]

**Current Issues:**
- [Specific issue 1]
- [Specific issue 2]

**Recommendations:**
- [Specific actionable recommendation 1]
- [Specific actionable recommendation 2]

**Priority:** [High/Medium/Low]

Be specific and actionable. Focus only on {imp_info['name']}."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self.llm.chat(messages, temperature=0.3, max_tokens=4000)
        return response


def main():
    """CLI for paper analysis."""
    parser = argparse.ArgumentParser(description="Analyze paper for improvements")
    parser.add_argument("paper_file", help="LaTeX paper file")
    parser.add_argument(
        "--type",
        required=True,
        choices=list(PaperAnalyzer.IMPROVEMENT_TYPES.keys()),
        help="Type of improvement analysis"
    )
    parser.add_argument("--kb-summary", help="KB summary file")
    parser.add_argument("--style-guide", help="Style guide file")
    parser.add_argument("--strategic-goals", help="Strategic assessment file")
    parser.add_argument("--output", "-o", required=True, help="Output markdown file")
    parser.add_argument("--model", default="vertex_ai/gemini-2.5-pro", help="Model to use")
    
    args = parser.parse_args()
    
    # Read inputs
    paper_tex = Path(args.paper_file).read_text()
    kb_summary = Path(args.kb_summary).read_text() if args.kb_summary else None
    style_guide = Path(args.style_guide).read_text() if args.style_guide else None
    strategic_goals = Path(args.strategic_goals).read_text() if args.strategic_goals else None
    
    print(f"🔍 Analyzing paper for {args.type}...", file=sys.stderr)
    
    # Analyze
    analyzer = PaperAnalyzer(model=args.model)
    recommendations = analyzer.analyze(
        paper_tex,
        args.type,
        kb_summary=kb_summary,
        style_guide=style_guide,
        strategic_goals=strategic_goals
    )
    
    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(recommendations)
    
    print(f"✅ Recommendations written to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()

