"""
Context Engineering Example
==========================
Demonstrates advanced LLM context engineering techniques.
"""

from context_engineering import ContextEngineer, FewShotExample

def example_few_shot_learning():
    """Example of few-shot learning for contract analysis"""
    
    engineer = ContextEngineer()
    
    # Create few-shot examples
    examples = [
        FewShotExample(
            input_text="Lease term: Jan 1, 2024 to Dec 31, 2026. Monthly rent: $5,000.",
            output_text='{"lease_start": "2024-01-01", "lease_end": "2026-12-31", "monthly_rent": 5000}',
            explanation="Extracted dates and rent amount"
        ),
        FewShotExample(
            input_text="Contract between ABC Corp and XYZ Inc. Value: $100,000. Term: 2 years.",
            output_text='{"parties": ["ABC Corp", "XYZ Inc"], "value": 100000, "term_years": 2}',
            explanation="Extracted parties, value, and term"
        )
    ]
    
    # Build few-shot prompt
    task_description = "Extract structured information from contract/lease documents."
    user_input = "Lease between Property Co and Tenant LLC. Rent: $3,500/month. Term: 3 years starting Jan 2025."
    
    prompt = engineer.build_few_shot_prompt(examples, task_description, user_input)
    
    print("📝 Few-Shot Learning Example")
    print("=" * 50)
    print(prompt)


def example_chain_of_thought():
    """Example of chain-of-thought reasoning"""
    
    engineer = ContextEngineer()
    
    question = "What is the total cost of a 3-year lease with $5,000 monthly rent and a $10,000 security deposit?"
    
    reasoning_steps = [
        "Calculate monthly rent over 3 years: 36 months × $5,000",
        "Add one-time security deposit: $10,000",
        "Sum both amounts for total cost"
    ]
    
    prompt = engineer.build_chain_of_thought_prompt(question, reasoning_steps)
    
    print("\n🧠 Chain-of-Thought Example")
    print("=" * 50)
    print(prompt)


def example_rag_optimization():
    """Example of optimized RAG prompt"""
    
    engineer = ContextEngineer()
    
    query = "What are the key terms of the lease?"
    context = """
    LEASE AGREEMENT
    Property: 123 Main St
    Term: 3 years
    Rent: $5,000/month
    Deposit: $10,000
    """
    
    system_instruction = "You are a legal document analyst. Extract and summarize key information accurately."
    
    prompt = engineer.create_rag_prompt(query, context, system_instruction)
    
    print("\n🔍 RAG Prompt Optimization Example")
    print("=" * 50)
    print(prompt)


def example_context_window_optimization():
    """Example of context window optimization"""
    
    engineer = ContextEngineer()
    
    long_text = " ".join([f"Sentence {i} with some content." for i in range(1000)])
    
    # Optimize to fit within token limit
    optimized = engineer.optimize_context_window(
        long_text,
        max_tokens=100,
        preserve_sections=["Important section: This must be kept"]
    )
    
    print("\n⚡ Context Window Optimization")
    print("=" * 50)
    print(f"Original length: {len(long_text)} chars")
    print(f"Optimized length: {len(optimized)} chars")
    print(f"Reduction: {len(long_text) - len(optimized)} chars")


if __name__ == "__main__":
    example_few_shot_learning()
    example_chain_of_thought()
    example_rag_optimization()
    example_context_window_optimization()

