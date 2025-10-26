#!/usr/bin/env python3
"""
Gemini-based section improver for research papers.
Uses Vertex AI Gemini API via LiteLLM for high-quality rewriting.
"""

import sys
import os
import argparse
from pathlib import Path
from typing import Optional

# Add ncl_agents to path
sys.path.insert(0, '/Users/cstein/code/ncl_agents/src')

from llm_lib.llm.manager import LLM


class GeminiSectionImprover:
    """Improve research paper sections using Gemini API."""
    
    def __init__(self, model: str = "vertex_ai/gemini-2.5-pro"):
        self.llm = LLM(model=model)
        self.model = model
    
    def improve_section(
        self,
        section_text: str,
        improvement_type: str,
        context: Optional[dict] = None
    ) -> str:
        """
        Improve a section with a specific improvement type.
        
        Args:
            section_text: The LaTeX section text to improve
            improvement_type: Type of improvement (align_sources, sharpen_arguments, 
                            improve_style, restructure, check_consistency)
            context: Optional context (KB path, reference papers, etc.)
        
        Returns:
            Improved section text
        """
        system_prompt = self._get_system_prompt(improvement_type)
        user_prompt = self._get_user_prompt(section_text, improvement_type, context)
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        # Lower temperature for more focused improvements
        temperature = 0.3 if improvement_type in ["align_sources", "check_consistency"] else 0.5
        
        response = self.llm.chat(messages, temperature=temperature, max_tokens=4000)
        return response
    
    def _get_system_prompt(self, improvement_type: str) -> str:
        """Get system prompt for specific improvement type."""
        
        base_prompt = """You are an expert scientific writing editor specializing in machine learning research papers.
You help improve papers for top-tier venues like NeurIPS, ICML, and ICLR.

Your improvements should:
- Maintain all technical content and accuracy
- Preserve LaTeX formatting
- Keep the academic tone professional
- Follow best practices for scientific writing"""
        
        type_specific = {
            "align_sources": """
Focus: Ensure all claims are grounded in source material.
- Verify claims can be supported
- Flag unsupported statements
- Add specific numbers/results where available
- Maintain scientific rigor""",
            
            "sharpen_arguments": """
Focus: Strengthen logical flow and precision.
- Make claims more specific and precise
- Add logical connectors
- Clarify cause-effect relationships
- Remove vague language""",
            
            "improve_style": """
Focus: Enhance clarity and readability.
- Use active voice where appropriate
- Improve sentence variety and flow
- Simplify complex sentences
- Use precise technical language
- Match the style of top-tier papers""",
            
            "restructure": """
Focus: Improve organization and flow.
- Reorder for better logical progression
- Add topic sentences
- Improve transitions
- Ensure clear paragraph structure""",
            
            "check_consistency": """
Focus: Ensure consistency across the paper.
- Check notation consistency
- Verify terminology usage
- Ensure cross-references work
- Align with paper conventions"""
        }
        
        return base_prompt + "\n" + type_specific.get(improvement_type, "")
    
    def _get_user_prompt(
        self,
        section_text: str,
        improvement_type: str,
        context: Optional[dict]
    ) -> str:
        """Generate user prompt with section and context."""
        
        prompt = f"""Improve the following research paper section.

Improvement Type: {improvement_type}

"""
        
        if context:
            if "kb_summary" in context:
                prompt += f"""Source Material Summary:
{context['kb_summary']}

"""
            if "reference_style" in context:
                prompt += f"""Reference Paper Style Notes:
{context['reference_style']}

"""
        
        prompt += f"""Section to Improve:
```latex
{section_text}
```

Instructions:
1. Apply the {improvement_type} improvement focus
2. Preserve all LaTeX formatting (equations, citations, figures)
3. Maintain technical accuracy
4. Output ONLY the improved LaTeX section, no explanations

Improved Section:"""
        
        return prompt


def main():
    """CLI for testing section improvement."""
    parser = argparse.ArgumentParser(description="Improve paper sections with Gemini API")
    parser.add_argument("section_file", help="File containing section text")
    parser.add_argument(
        "--type",
        choices=["align_sources", "sharpen_arguments", "improve_style", "restructure", "check_consistency"],
        default="improve_style",
        help="Type of improvement to apply"
    )
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    parser.add_argument("--model", default="vertex_ai/gemini-2.5-pro", help="Model to use")
    
    args = parser.parse_args()
    
    # Read section text
    section_text = Path(args.section_file).read_text()
    
    print(f"🔄 Improving section with Gemini ({args.type})...", file=sys.stderr)
    
    # Improve section
    improver = GeminiSectionImprover(model=args.model)
    improved = improver.improve_section(section_text, args.type)
    
    # Output
    if args.output:
        Path(args.output).write_text(improved)
        print(f"✅ Improved section written to {args.output}", file=sys.stderr)
    else:
        print("\n" + "=" * 80, file=sys.stderr)
        print("IMPROVED SECTION:", file=sys.stderr)
        print("=" * 80, file=sys.stderr)
        print(improved)


if __name__ == "__main__":
    main()

