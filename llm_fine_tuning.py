"""
LLM Fine-Tuning with LoRA, QLoRA, and PEFT
===========================================
Production-ready fine-tuning implementation for open-source LLMs.
Demonstrates advanced Gen AI expertise required for Senior Data Scientist role.
"""

import torch
import numpy as np
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum
import logging
from pathlib import Path
import json

try:
    from transformers import (
        AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer,
        BitsAndBytesConfig, DataCollatorForLanguageModeling
    )
    from peft import LoraConfig, get_peft_model, TaskType, PeftModel
    from datasets import Dataset
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logging.warning("transformers/peft not available. Install with: pip install transformers peft bitsandbytes")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FineTuningMethod(Enum):
    """Fine-tuning methods"""
    FULL = "full"
    LORA = "lora"
    QLORA = "qlora"
    PEFT = "peft"


@dataclass
class FineTuningConfig:
    """Configuration for fine-tuning"""
    model_name: str
    method: FineTuningMethod
    output_dir: str
    num_epochs: int = 3
    batch_size: int = 4
    learning_rate: float = 2e-4
    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.1
    target_modules: Optional[List[str]] = None
    use_4bit: bool = True
    bnb_4bit_compute_dtype: str = "float16"
    bnb_4bit_quant_type: str = "nf4"
    max_length: int = 512


class LLMFineTuner:
    """
    Production-ready LLM fine-tuning with LoRA, QLoRA, and PEFT
    
    Features:
    - LoRA (Low-Rank Adaptation)
    - QLoRA (Quantized LoRA)
    - PEFT (Parameter-Efficient Fine-Tuning)
    - Model quantization
    - Gradient checkpointing
    - Mixed precision training
    """
    
    def __init__(self, config: FineTuningConfig):
        if not TRANSFORMERS_AVAILABLE:
            raise ImportError("transformers and peft required for fine-tuning")
        
        self.config = config
        self.model = None
        self.tokenizer = None
        self.peft_model = None
        
    def load_base_model(self) -> Tuple[Any, Any]:
        """Load base model and tokenizer with quantization if needed"""
        logger.info(f"Loading base model: {self.config.model_name}")
        
        if self.config.method == FineTuningMethod.QLORA:
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=self.config.use_4bit,
                bnb_4bit_quant_type=self.config.bnb_4bit_quant_type,
                bnb_4bit_compute_dtype=getattr(torch, self.config.bnb_4bit_compute_dtype),
                bnb_4bit_use_double_quant=True
            )
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.config.model_name,
                quantization_config=bnb_config,
                device_map="auto",
                trust_remote_code=True
            )
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                self.config.model_name,
                torch_dtype=torch.float16 if self.config.use_4bit else torch.float32,
                device_map="auto"
            )
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.model_name)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        logger.info("Base model loaded successfully")
        return self.model, self.tokenizer
    
    def setup_peft(self) -> Any:
        """Setup PEFT/LoRA configuration"""
        if self.config.method == FineTuningMethod.FULL:
            return self.model
        
        target_modules = self.config.target_modules or self._get_default_target_modules()
        
        lora_config = LoraConfig(
            r=self.config.lora_r,
            lora_alpha=self.config.lora_alpha,
            target_modules=target_modules,
            lora_dropout=self.config.lora_dropout,
            bias="none",
            task_type=TaskType.CAUSAL_LM
        )
        
        self.peft_model = get_peft_model(self.model, lora_config)
        self.peft_model.print_trainable_parameters()
        
        logger.info(f"PEFT/LoRA configured: {self.config.method.value}")
        return self.peft_model
    
    def _get_default_target_modules(self) -> List[str]:
        """Get default target modules based on model architecture"""
        model_lower = self.config.model_name.lower()
        
        if "llama" in model_lower or "mistral" in model_lower:
            return ["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
        elif "gpt" in model_lower:
            return ["c_attn", "c_proj", "c_fc"]
        else:
            return ["query", "value", "key", "dense"]
    
    def prepare_dataset(self, texts: List[str], max_length: Optional[int] = None) -> Dataset:
        """Prepare dataset for training"""
        max_len = max_length or self.config.max_length
        
        def tokenize_function(examples):
            return self.tokenizer(
                examples["text"],
                truncation=True,
                max_length=max_len,
                padding="max_length"
            )
        
        dataset = Dataset.from_dict({"text": texts})
        tokenized_dataset = dataset.map(tokenize_function, batched=True)
        
        return tokenized_dataset
    
    def train(
        self,
        train_dataset: Dataset,
        eval_dataset: Optional[Dataset] = None
    ) -> Dict[str, Any]:
        """Train the model"""
        if self.model is None:
            self.load_base_model()
        
        if self.peft_model is None and self.config.method != FineTuningMethod.FULL:
            self.setup_peft()
        
        model_to_train = self.peft_model if self.peft_model else self.model
        
        training_args = TrainingArguments(
            output_dir=self.config.output_dir,
            num_train_epochs=self.config.num_epochs,
            per_device_train_batch_size=self.config.batch_size,
            per_device_eval_batch_size=self.config.batch_size,
            learning_rate=self.config.learning_rate,
            fp16=self.config.use_4bit,
            logging_steps=10,
            save_steps=100,
            evaluation_strategy="epoch" if eval_dataset else "no",
            save_total_limit=3,
            load_best_model_at_end=True if eval_dataset else False,
            gradient_checkpointing=True,
            optim="paged_adamw_32bit" if self.config.method == FineTuningMethod.QLORA else "adamw_torch"
        )
        
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False
        )
        
        trainer = Trainer(
            model=model_to_train,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            data_collator=data_collator
        )
        
        logger.info("Starting training...")
        train_result = trainer.train()
        
        trainer.save_model()
        self.tokenizer.save_pretrained(self.config.output_dir)
        
        metrics = {
            "train_loss": train_result.training_loss,
            "train_runtime": train_result.metrics.get("train_runtime", 0),
            "train_samples_per_second": train_result.metrics.get("train_samples_per_second", 0)
        }
        
        logger.info(f"Training complete. Metrics: {metrics}")
        return metrics
    
    def save_model(self, path: Optional[str] = None) -> str:
        """Save fine-tuned model"""
        save_path = path or self.config.output_dir
        
        if self.peft_model:
            self.peft_model.save_pretrained(save_path)
        else:
            self.model.save_pretrained(save_path)
        
        self.tokenizer.save_pretrained(save_path)
        
        config_path = Path(save_path) / "finetuning_config.json"
        with open(config_path, 'w') as f:
            json.dump({
                "model_name": self.config.model_name,
                "method": self.config.method.value,
                "lora_r": self.config.lora_r,
                "lora_alpha": self.config.lora_alpha
            }, f, indent=2)
        
        logger.info(f"Model saved to {save_path}")
        return save_path
    
    def load_finetuned_model(self, path: str) -> Tuple[Any, Any]:
        """Load fine-tuned model"""
        if self.config.method == FineTuningMethod.FULL:
            self.model = AutoModelForCausalLM.from_pretrained(path)
        else:
            base_model = AutoModelForCausalLM.from_pretrained(
                self.config.model_name,
                device_map="auto"
            )
            self.peft_model = PeftModel.from_pretrained(base_model, path)
            self.model = self.peft_model
        
        self.tokenizer = AutoTokenizer.from_pretrained(path)
        logger.info(f"Fine-tuned model loaded from {path}")
        return self.model, self.tokenizer
    
    def generate(self, prompt: str, max_new_tokens: int = 100, temperature: float = 0.7) -> str:
        """Generate text with fine-tuned model"""
        if self.model is None:
            raise ValueError("Model not loaded. Call load_base_model() or load_finetuned_model() first.")
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text[len(prompt):].strip()


def create_finetuning_config(
    model_name: str = "microsoft/DialoGPT-medium",
    method: str = "lora",
    output_dir: str = "./finetuned_models"
) -> FineTuningConfig:
    """Create fine-tuning configuration"""
    return FineTuningConfig(
        model_name=model_name,
        method=FineTuningMethod(method.lower()),
        output_dir=output_dir,
        num_epochs=3,
        batch_size=4,
        learning_rate=2e-4,
        lora_r=16,
        lora_alpha=32,
        lora_dropout=0.1
    )

