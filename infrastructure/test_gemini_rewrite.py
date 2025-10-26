#!/usr/bin/env python3
"""
Test script for Gemini API calls via LiteLLM for paragraph rewriting.
Uses the ncl_agents llm_lib infrastructure.
"""

import sys
import os

# Add ncl_agents to path
sys.path.insert(0, '/Users/cstein/code/ncl_agents/src')

from llm_lib.llm.manager import LLM

def rewrite_paragraph(paragraph: str, model: str = "vertex_ai/gemini-2.5-pro") -> str:
    """
    Rewrite a paragraph to improve clarity and style.
    
    Args:
        paragraph: The original paragraph text
        model: The model to use (default: vertex_ai/gemini-2.5-pro)
    
    Returns:
        The rewritten paragraph
    """
    llm = LLM(model=model)
    
    messages = [
        {
            "role": "system",
            "content": """You are an expert scientific writing editor. 
Your task is to rewrite paragraphs to improve:
- Clarity and conciseness
- Technical precision
- Logical flow
- Active voice where appropriate
- Professional academic tone

Preserve all technical content and meaning. Only improve the writing quality."""
        },
        {
            "role": "user",
            "content": f"""Please rewrite the following paragraph to improve its clarity and style while preserving all technical content:

{paragraph}

Provide only the rewritten paragraph, no explanations."""
        }
    ]
    
    response = llm.chat(messages, temperature=0.3, max_tokens=2000)
    return response


def main():
    """Test the rewriting function with a sample paragraph."""
    
    # Sample paragraph from a research paper (typical academic writing that could be improved)
    sample_paragraph = """
    The activation function is a very important component of neural networks that has been studied 
    extensively in recent years. It is used to introduce non-linearity into the network which allows 
    it to learn complex patterns. There are many different activation functions that have been proposed, 
    such as ReLU, sigmoid, and tanh. Each of these functions has its own advantages and disadvantages 
    that need to be considered when designing a neural network. In this work, we propose a new activation 
    function that combines the benefits of existing functions while addressing their limitations.
    """
    
    print("=" * 80)
    print("GEMINI API REWRITING TEST")
    print("=" * 80)
    print("\n📝 Original Paragraph:")
    print("-" * 80)
    print(sample_paragraph.strip())
    print()
    
    print("🔄 Calling Gemini API via LiteLLM...")
    print()
    
    try:
        rewritten = rewrite_paragraph(sample_paragraph)
        
        print("✅ Rewritten Paragraph:")
        print("-" * 80)
        print(rewritten.strip())
        print()
        
        print("=" * 80)
        print("✅ SUCCESS: Gemini API call completed")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print()
        print("Troubleshooting:")
        print("1. Check GOOGLE_APPLICATION_CREDENTIALS env var is set")
        print("2. Check GCP project has Vertex AI API enabled")
        print("3. Check service account has Vertex AI permissions")
        sys.exit(1)


if __name__ == "__main__":
    main()

