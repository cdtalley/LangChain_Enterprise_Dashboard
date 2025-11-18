"""
Advanced Context Engineering
============================
LLM context engineering with prompt templates, few-shot learning, and optimization.
Demonstrates advanced LLM context engineering skills.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PromptTemplate:
    """Reusable prompt template with variable substitution"""
    
    def __init__(self, template: str, variables: List[str]):
        self.template = template
        self.variables = variables
    
    def format(self, **kwargs) -> str:
        """Format template with provided variables"""
        try:
            return self.template.format(**kwargs)
        except KeyError as e:
            logger.error(f"Missing variable in template: {e}")
            raise


class FewShotExample:
    """Few-shot learning example"""
    
    def __init__(self, input_text: str, output_text: str, explanation: Optional[str] = None):
        self.input = input_text
        self.output = output_text
        self.explanation = explanation
    
    def to_dict(self) -> Dict[str, str]:
        return {
            "input": self.input,
            "output": self.output,
            "explanation": self.explanation
        }


class ContextEngineer:
    """
    Advanced Context Engineering for LLMs
    
    Features:
    - Prompt templates
    - Few-shot learning
    - Context window optimization
    - Chain-of-thought prompting
    """
    
    def __init__(self):
        self.templates = {}
        self.few_shot_examples = {}
        logger.info("Context Engineer initialized")
    
    def create_template(
        self,
        name: str,
        template: str,
        variables: List[str]
    ) -> PromptTemplate:
        """Create and store a prompt template"""
        prompt_template = PromptTemplate(template, variables)
        self.templates[name] = prompt_template
        logger.info(f"Template '{name}' created")
        return prompt_template
    
    def build_few_shot_prompt(
        self,
        examples: List[FewShotExample],
        task_description: str,
        user_input: str
    ) -> str:
        """Build few-shot learning prompt"""
        prompt_parts = [task_description, "\n\nExamples:\n"]
        
        for i, example in enumerate(examples, 1):
            prompt_parts.append(f"Example {i}:")
            prompt_parts.append(f"Input: {example.input}")
            prompt_parts.append(f"Output: {example.output}")
            if example.explanation:
                prompt_parts.append(f"Explanation: {example.explanation}")
            prompt_parts.append("")
        
        prompt_parts.append("Now solve this:")
        prompt_parts.append(f"Input: {user_input}")
        prompt_parts.append("Output:")
        
        return "\n".join(prompt_parts)
    
    def build_chain_of_thought_prompt(
        self,
        question: str,
        reasoning_steps: Optional[List[str]] = None
    ) -> str:
        """Build chain-of-thought reasoning prompt"""
        prompt = f"""Let's think step by step.

Question: {question}

"""
        
        if reasoning_steps:
            prompt += "Reasoning steps:\n"
            for i, step in enumerate(reasoning_steps, 1):
                prompt += f"{i}. {step}\n"
            prompt += "\n"
        
        prompt += """Let's work through this step by step:

1. First, I need to understand what is being asked.
2. Then, I'll identify the key information needed.
3. Next, I'll work through the solution.
4. Finally, I'll provide the answer.

"""
        
        prompt += f"Question: {question}\n\nAnswer:"
        
        return prompt
    
    def optimize_context_window(
        self,
        text: str,
        max_tokens: int,
        preserve_sections: Optional[List[str]] = None
    ) -> str:
        """Optimize context window by truncating less important parts"""
        # Simple implementation - in production, use more sophisticated methods
        words = text.split()
        max_words = max_tokens // 2  # Rough estimate: 2 words per token
        
        if len(words) <= max_words:
            return text
        
        # If we need to preserve sections, keep those first
        if preserve_sections:
            preserved_text = ""
            remaining_text = text
            
            for section in preserve_sections:
                if section in remaining_text:
                    idx = remaining_text.find(section)
                    preserved_text += remaining_text[:idx + len(section)]
                    remaining_text = remaining_text[idx + len(section):]
            
            # Truncate remaining text
            remaining_words = remaining_text.split()
            if len(remaining_words) > max_words - len(preserved_text.split()):
                remaining_words = remaining_words[:max_words - len(preserved_text.split())]
            
            return preserved_text + " " + " ".join(remaining_words)
        
        # Otherwise, truncate from the end
        return " ".join(words[:max_words])
    
    def create_rag_prompt(
        self,
        query: str,
        context: str,
        system_instruction: Optional[str] = None
    ) -> str:
        """Create optimized RAG prompt"""
        if system_instruction:
            prompt = f"{system_instruction}\n\n"
        else:
            prompt = "You are a helpful assistant. Use the following context to answer the question.\n\n"
        
        prompt += f"Context:\n{context}\n\n"
        prompt += f"Question: {query}\n\n"
        prompt += "Answer:"
        
        return prompt
    
    def create_structured_extraction_prompt(
        self,
        document_text: str,
        schema: Dict[str, str],
        examples: Optional[List[FewShotExample]] = None
    ) -> str:
        """Create prompt for structured data extraction"""
        prompt = "Extract structured information from the following document.\n\n"
        
        if examples:
            prompt += "Examples:\n"
            for example in examples:
                prompt += f"Input: {example.input}\n"
                prompt += f"Output: {json.dumps(json.loads(example.output), indent=2)}\n\n"
        
        prompt += "Schema:\n"
        for field, description in schema.items():
            prompt += f"- {field}: {description}\n"
        
        prompt += f"\n\nDocument:\n{document_text[:2000]}\n\n"
        prompt += "Extract the information as JSON matching the schema:"
        
        return prompt


# Pre-built templates for common use cases
CONTRACT_EXTRACTION_TEMPLATE = """Extract key information from this contract document.

Focus on:
- Parties involved
- Dates (start, end, important milestones)
- Financial terms (amounts, payment schedules)
- Key obligations and responsibilities
- Termination conditions

Document:
{document_text}

Return as structured JSON."""


LEASE_ANALYSIS_TEMPLATE = """Analyze this lease agreement and extract:

1. Parties: Lessor and Lessee names
2. Property: Address and description
3. Term: Start date, end date, duration
4. Financial: Monthly rent, security deposit, fees
5. Terms: Renewal options, maintenance responsibilities, restrictions

Lease Document:
{lease_text}

Provide a structured analysis."""

