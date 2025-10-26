#!/usr/bin/env python3
"""
Analyze reference papers to extract style guidelines.
One-time analysis, results are cached for reuse.
"""

import sys
import os
import argparse
from pathlib import Path

# Add ncl_agents to path
sys.path.insert(0, '/Users/cstein/code/ncl_agents/src')

from llm_lib.llm.manager import LLM


class ReferenceAnalyzer:
    """Extract style guidelines from reference papers."""
    
    def __init__(self, model: str = "vertex_ai/gemini-2.5-pro"):
        self.llm = LLM(model=model)
        self.model = model
    
    def analyze_references(self, reference_info: str) -> str:
        """
        Analyze reference papers and extract style guidelines.
        
        Args:
            reference_info: Information about reference papers (titles, abstracts, key points)
        
        Returns:
            Style guidelines as markdown text
        """
        system_prompt = """You are an expert in scientific writing, specializing in top-tier ML conference papers.
You analyze highly-cited papers to extract patterns that make them compelling and clear."""

        user_prompt = f"""Analyze these top-tier papers on activation functions and neural networks:

REFERENCE PAPERS:
{reference_info}

Extract a concise style guide (2-3 pages) covering:

1. **Writing Style Patterns**
   - Sentence structure and length
   - Use of active vs passive voice
   - Technical precision vs accessibility balance

2. **Argument Structure**
   - How they motivate the problem
   - How they present contributions
   - How they structure the narrative

3. **Results Presentation**
   - How they present experimental results
   - Use of figures and tables
   - How they discuss limitations

4. **What Makes Them Compelling**
   - Opening hooks
   - Clear problem statements
   - Strong conclusions

Output as markdown. Be specific with examples where possible."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self.llm.chat(messages, temperature=0.3, max_tokens=3000)
        return response


def main():
    """CLI for reference analysis."""
    parser = argparse.ArgumentParser(description="Analyze reference papers for style guidelines")
    parser.add_argument("--references-dir", required=True, help="Directory with reference papers")
    parser.add_argument("--output", "-o", required=True, help="Output markdown file")
    parser.add_argument("--model", default="vertex_ai/gemini-2.5-pro", help="Model to use")
    
    args = parser.parse_args()
    
    # For now, use the reference papers metadata file
    # In future, could extract text from PDFs
    ref_dir = Path(args.references_dir)
    ref_info_file = ref_dir / "REFERENCE_PAPERS.md"
    
    if ref_info_file.exists():
        reference_info = ref_info_file.read_text()
    else:
        # Fallback: list PDF files
        pdfs = list(ref_dir.glob("*.pdf"))
        reference_info = f"Reference papers:\n" + "\n".join([f"- {p.stem}" for p in pdfs])
    
    print(f"🔍 Analyzing reference papers...", file=sys.stderr)
    
    # Analyze
    analyzer = ReferenceAnalyzer(model=args.model)
    style_guide = analyzer.analyze_references(reference_info)
    
    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(style_guide)
    
    print(f"✅ Style guide written to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()

