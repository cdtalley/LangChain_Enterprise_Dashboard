"""
LLM Fine-Tuning Example
========================
Demonstrates LoRA, QLoRA, and PEFT fine-tuning.
"""

from llm_fine_tuning import LLMFineTuner, FineTuningConfig, FineTuningMethod

def example_lora_finetuning():
    """Example of LoRA fine-tuning"""
    
    config = FineTuningConfig(
        model_name="microsoft/DialoGPT-medium",
        method=FineTuningMethod.LORA,
        output_dir="./finetuned_models/lora_dialogpt",
        num_epochs=3,
        batch_size=4,
        learning_rate=2e-4,
        lora_r=16,
        lora_alpha=32
    )
    
    tuner = LLMFineTuner(config)
    
    # Load base model
    model, tokenizer = tuner.load_base_model()
    
    # Setup LoRA
    peft_model = tuner.setup_peft()
    
    # Prepare dataset
    training_texts = [
        "Hello, how can I help you?",
        "What is the weather today?",
        "Tell me about machine learning.",
        # Add more training examples
    ]
    
    train_dataset = tuner.prepare_dataset(training_texts)
    
    # Train
    metrics = tuner.train(train_dataset)
    print(f"Training metrics: {metrics}")
    
    # Save model
    tuner.save_model()
    
    print("✅ LoRA fine-tuning complete!")


def example_qlora_finetuning():
    """Example of QLoRA fine-tuning (quantized)"""
    
    config = FineTuningConfig(
        model_name="microsoft/DialoGPT-medium",
        method=FineTuningMethod.QLORA,
        output_dir="./finetuned_models/qlora_dialogpt",
        num_epochs=2,
        batch_size=2,
        learning_rate=2e-4,
        use_4bit=True
    )
    
    tuner = LLMFineTuner(config)
    model, tokenizer = tuner.load_base_model()
    peft_model = tuner.setup_peft()
    
    print("✅ QLoRA setup complete (quantized for memory efficiency)")


if __name__ == "__main__":
    print("🚀 LLM Fine-Tuning Examples")
    print("=" * 50)
    
    try:
        example_lora_finetuning()
    except Exception as e:
        print(f"⚠️ Fine-tuning requires GPU and transformers/peft: {e}")
        print("This demonstrates the implementation pattern.")

