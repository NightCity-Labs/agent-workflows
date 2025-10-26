#!/usr/bin/env python3
"""
Gemini-based paper quality evaluator.
Provides structured assessment for research papers targeting top-tier venues.
"""

import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Add ncl_agents to path
sys.path.insert(0, '/Users/cstein/code/ncl_agents/src')

from llm_lib.llm.manager import LLM


class PaperEvaluator:
    """Evaluate research paper quality with structured scores."""
    
    def __init__(self, model: str = "vertex_ai/gemini-2.5-pro"):
        self.llm = LLM(model=model)
        self.model = model
    
    def evaluate(
        self,
        paper_tex: str,
        version: str,
        run_id: str
    ) -> Dict[str, Any]:
        """
        Evaluate paper quality with structured scores.
        
        Args:
            paper_tex: Full LaTeX paper content
            version: Version identifier (e.g., "v2", "v3")
            run_id: Unique run identifier
        
        Returns:
            Structured evaluation dictionary
        """
        system_prompt = """You are a senior area chair for NeurIPS/ICML with 15+ years of experience.
You evaluate papers with the goal of identifying top-tier contributions worthy of spotlight/oral presentations.

Your evaluation must be:
- Rigorous and honest
- Calibrated to top-tier venue standards (NeurIPS, ICML, ICLR)
- Focused on both technical quality and presentation
- Constructive and actionable

Provide scores on a 1-10 scale where:
- 1-3: Reject
- 4-5: Weak reject
- 6-7: Weak accept (poster)
- 8-9: Accept (spotlight candidate)
- 10: Strong accept (oral candidate)"""

        user_prompt = f"""Evaluate this research paper for submission to a top-tier ML conference (NeurIPS/ICML).

PAPER (LaTeX):
```latex
{paper_tex}
```

Provide a structured evaluation in JSON format with the following fields:

{{
  "scores": {{
    "overall_quality": <float 1-10>,
    "acceptance_probability": <float 0-1>,
    "novelty": <float 1-10>,
    "clarity": <float 1-10>,
    "rigor": <float 1-10>,
    "impact": <float 1-10>,
    "writing_quality": <float 1-10>,
    "experimental_validation": <float 1-10>
  }},
  "estimated_venue": "<NeurIPS reject/poster/spotlight/oral>",
  "key_strengths": ["<strength 1>", "<strength 2>", ...],
  "key_weaknesses": ["<weakness 1>", "<weakness 2>", ...],
  "detailed_feedback": "<2-3 paragraph assessment>",
  "recommendation": "<1-2 sentence recommendation for authors>"
}}

Be honest and calibrated to real NeurIPS standards. Most papers are posters (6-7), few are spotlights (8-9), very few are orals (10).

Output ONLY the JSON, no other text."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        # Get evaluation from Gemini
        response = self.llm.chat(messages, temperature=0.2, max_tokens=2000)
        
        # Parse JSON response
        try:
            # Extract JSON from response (handle markdown code blocks)
            response_clean = response.strip()
            if response_clean.startswith("```json"):
                response_clean = response_clean[7:]
            if response_clean.startswith("```"):
                response_clean = response_clean[3:]
            if response_clean.endswith("```"):
                response_clean = response_clean[:-3]
            
            evaluation = json.loads(response_clean.strip())
        except json.JSONDecodeError as e:
            print(f"Warning: Failed to parse JSON response: {e}", file=sys.stderr)
            print(f"Raw response: {response}", file=sys.stderr)
            # Return minimal structure
            evaluation = {
                "scores": {"overall_quality": 0.0},
                "error": "Failed to parse evaluation",
                "raw_response": response
            }
        
        # Add metadata
        evaluation["run_id"] = run_id
        evaluation["version"] = version
        evaluation["timestamp"] = datetime.utcnow().isoformat() + "Z"
        evaluation["model"] = self.model
        
        return evaluation


def main():
    """CLI for paper evaluation."""
    parser = argparse.ArgumentParser(description="Evaluate paper quality with Gemini")
    parser.add_argument("paper_file", help="LaTeX paper file")
    parser.add_argument("--version", required=True, help="Version identifier (e.g., v2, v3)")
    parser.add_argument("--run-id", required=True, help="Unique run identifier")
    parser.add_argument("--output", "-o", required=True, help="Output JSON file")
    parser.add_argument("--model", default="vertex_ai/gemini-2.5-pro", help="Model to use")
    
    args = parser.parse_args()
    
    # Read paper
    paper_tex = Path(args.paper_file).read_text()
    
    print(f"🔍 Evaluating paper (version {args.version})...", file=sys.stderr)
    
    # Evaluate
    evaluator = PaperEvaluator(model=args.model)
    evaluation = evaluator.evaluate(paper_tex, args.version, args.run_id)
    
    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(evaluation, indent=2))
    
    print(f"✅ Evaluation written to {args.output}", file=sys.stderr)
    print(f"\n📊 Summary:", file=sys.stderr)
    print(f"   Overall Quality: {evaluation['scores']['overall_quality']:.1f}/10", file=sys.stderr)
    print(f"   Accept Probability: {evaluation['scores']['acceptance_probability']:.0%}", file=sys.stderr)
    print(f"   Estimated Venue: {evaluation['estimated_venue']}", file=sys.stderr)


if __name__ == "__main__":
    main()

