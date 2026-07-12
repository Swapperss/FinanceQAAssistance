# ============================================================
# 3. Global configuration
# ============================================================
# Keep all important parameters in one place.
# This makes the notebook easier to debug, reproduce, and productionize.

from dataclasses import asdict, dataclass


@dataclass
class Config:
    # Folder and file names used during finance-domain corpus preparation.
    raw_data_dir: str = "data/raw"
    non_instruction_dir: str = "data/non_instruction_dataset"
    instruction_dir: str = "data/instruction_dataset"
    preferred_raw_csv_filename: str = "complaints-2026-07-04_02_07.csv"
    raw_csv_pattern: str = "complaints-*.csv"
    source_text_column: str = "Consumer complaint narrative"
    raw_text_filename: str = "raw_extracted_text.txt"
    non_instruction_filename: str = "non_instruction_data.txt"
    hf_dataset_dirname: str = "hf_non_instruction_dataset"
    instruction_dataset_filename: str = "finance_instruction_dataset.jsonl"
    instruction_hf_dataset_dirname: str = "hf_finance_instruction_dataset"

    # Base causal language model for non-instruction fine-tuning.
    model_name: str = "Qwen/Qwen2.5-0.5B"

    # Directories where training outputs will be saved.
    output_dir: str = "artifacts/non_instruction_output"
    adapter_dir: str = "artifacts/non_instruction_adapter"
    instruction_output_dir: str = "artifacts/instruction_output"
    instruction_adapter_dir: str = "artifacts/instruction_adapter"

    # Data filtering and split settings.
    min_chars_per_paragraph: int = 80
    block_size: int = 512
    test_size: float = 0.10
    seed: int = 42

    # LoRA settings.
    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05

    # Training settings.
    num_train_epochs: float = 3.0
    per_device_train_batch_size: int = 1
    per_device_eval_batch_size: int = 1
    gradient_accumulation_steps: int = 8
    learning_rate: float = 2e-4
    warmup_ratio: float = 0.03
    weight_decay: float = 0.01
    logging_steps: int = 1
    logging_first_step: bool = True
    eval_steps: int = 10
    save_steps: int = 25
    save_total_limit: int = 2
    max_steps: int = -1

    def to_dict(self) -> dict:
        return asdict(self)