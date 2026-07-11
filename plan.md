# Finance FAQ Assistant Fine-Tuning Plan (Qwen + Unsloth)

## 1. Project Goal
Build a domain-specific Finance FAQ Assistant using a 3-stage fine-tuning workflow:
1. Non-instruction fine-tuning on raw finance text
2. Instruction fine-tuning (SFT) on finance Q&A pairs
3. Preference alignment (DPO) with chosen vs rejected answers

Final model should outperform the base model on correctness, domain accuracy, clarity, safety, and helpfulness.

## 2. Assignment Requirements Mapping
- Domain: Finance FAQ Assistant
- Base model family: Qwen from Hugging Face (recommended in assignment)
- Minimum data targets:
  - Raw non-instruction text: >= 50 finance paragraphs
  - Instruction dataset: >= 100 instruction-response examples
  - Preference dataset: >= 50 prompt/chosen/rejected examples
- Required outputs:
  - notebooks/non_instruction_finetuning.ipynb
  - notebooks/instruction_finetuning.ipynb
  - notebooks/dpo_alignment.ipynb
  - reports/base_model_evaluation.md
  - reports/sft_model_comparison.md
  - reports/final_evaluation.md
  - reports/fine_tuning_explanation.md
  - src/inference.py
  - README.md

## 3. Model Strategy (Qwen)
Primary choice: Qwen2.5-1.5B-Instruct (HF)
Fallback (lower VRAM): Qwen2.5-0.5B-Instruct

Reason:
- Strong small-model performance for instruction following
- Good fit for Unsloth LoRA/QLoRA workflows
- Practical for assignment timeline and local experimentation

## 4. Data Plan
### 4.1 Non-instruction data
Source candidates:
- Existing finance text in data/raw and data/processed
- Public finance policy/FAQ content with valid licenses
- Cleaned synthetic finance paragraphs (manually verified)

Actions:
1. Clean duplicates, broken lines, and boilerplate
2. Normalize formatting (currency, date patterns, acronyms)
3. Chunk text for causal LM training
4. Save final corpus to data/non_instruction_data.txt

Acceptance check:
- At least 50 high-quality finance paragraphs

### 4.2 Instruction dataset (SFT)
Format: JSONL with fields instruction and response

Actions:
1. Define taxonomy of finance intents:
   - account services
   - cards and payments
   - fees and charges
   - loans and EMI
   - KYC and compliance
   - fraud and dispute support
2. Generate >=100 pairs
3. Enforce response style guide:
   - factual and domain-specific
   - safe and non-speculative
   - concise and actionable
4. Validate schema and remove low-quality items
5. Save as data/instruction_dataset.jsonl

Acceptance check:
- At least 100 clean examples, no malformed JSONL rows

### 4.3 Preference dataset (DPO)
Format: JSONL with prompt, chosen, rejected

Actions:
1. Create >=50 prompts from same finance intent taxonomy
2. Create chosen responses that are correct and professional
3. Create rejected responses that are generic, incomplete, unsafe, or wrong
4. Validate schema and quality
5. Save as data/preference_dataset.jsonl

Acceptance check:
- At least 50 clean preference triples

## 5. Training Plan
### Stage 1: Non-instruction FT
Notebook: notebooks/non_instruction_finetuning.ipynb

Include:
1. Load and inspect raw corpus
2. Text cleaning + chunking
3. Load Qwen base with Unsloth
4. Apply LoRA or QLoRA
5. Train on raw corpus
6. Save adapter/model
7. Run post-training probe prompts

### Stage 2: Instruction FT (SFT)
Notebook: notebooks/instruction_finetuning.ipynb

Include:
1. Load instruction dataset
2. Convert to chat/instruction format expected by tokenizer
3. Load Stage-1 adapter/model as initialization
4. Apply LoRA/QLoRA and train
5. Save SFT adapter/model
6. Run inference on 10 evaluation questions

### Stage 3: DPO alignment
Notebook: notebooks/dpo_alignment.ipynb

Include:
1. Load SFT model
2. Load preference dataset
3. Format prompt/chosen/rejected
4. Configure DPO trainer
5. Train and save DPO model
6. Run inference on same 10 questions

## 6. Suggested Hyperparameter Baseline
Note: tune based on GPU memory.

- LoRA rank (r): 16
- LoRA alpha: 32
- LoRA dropout: 0.05
- Learning rate (SFT): 2e-4
- Learning rate (DPO): 5e-6 to 1e-5
- Per-device batch size: 2 to 4
- Gradient accumulation: 4 to 8
- Sequence length: 1024 (or 2048 if memory allows)
- Precision: bf16 (preferred) or fp16
- Quantization: 4-bit QLoRA for low VRAM setup

These values must be reported in reports/fine_tuning_explanation.md.

## 7. Evaluation Plan
### 7.1 Base model test
Create 10 finance-specific questions and capture:
- Base answer
- Problem in answer (generic/wrong/unsafe/etc.)

Output: reports/base_model_evaluation.md

### 7.2 SFT comparison
Reuse same 10 questions and compare:
- Base answer
- SFT answer
- Which is better and why

Output: reports/sft_model_comparison.md

### 7.3 Final comparison (Base vs SFT vs DPO)
Reuse same 10 questions and compare all three stages:
- Base
- SFT
- DPO
- Best answer + reason

Output: reports/final_evaluation.md

Evaluation criteria to score each answer:
- Correctness
- Domain accuracy
- Helpfulness
- Safety
- Tone/professionalism
- Clarity
- Hallucination reduction

## 8. Inference App Plan
File: src/inference.py

Requirements:
1. Load tokenizer + final DPO-aligned adapter/model
2. Expose generate_answer(question)
3. Simple CLI loop for user questions
4. Handle empty input and exit commands
5. Keep generation settings deterministic for demo (e.g., low temperature)

## 9. Execution Schedule (today to submission)
Current date considered: 2026-07-05
Submission deadline: 2026-07-11
Demo day: 2026-07-12

Day 1 (Jul 5):
- Finalize domain scope and data sources
- Prepare non-instruction corpus (>=50 paragraphs)
- Draft 10 evaluation questions

Day 2 (Jul 6):
- Complete Stage-1 notebook and save adapter
- Run quick probes and log observations

Day 3 (Jul 7):
- Build instruction dataset (>=100)
- Complete base model evaluation report

Day 4 (Jul 8):
- Complete SFT notebook
- Generate SFT outputs for 10 questions
- Write SFT comparison report

Day 5 (Jul 9):
- Build preference dataset (>=50)
- Complete DPO notebook

Day 6 (Jul 10):
- Final evaluation report (Base vs SFT vs DPO)
- Write fine_tuning_explanation report
- Build src/inference.py

Day 7 (Jul 11):
- README cleanup, screenshots/logs, final QA pass
- Ensure folder structure and all deliverables are present
- Submit repository link

## 10. Risks and Mitigations
- VRAM limits:
  - Use Qwen2.5-0.5B + 4-bit QLoRA + smaller batch size
- Data quality issues:
  - Manual sampling checks and schema validators
- Overly generic responses:
  - Increase instruction diversity and preference quality
- Hallucination or unsafe answers:
  - Add safety-focused examples in SFT and DPO data

## 11. Definition of Done Checklist
- [ ] Domain and business problem clearly stated (finance FAQ)
- [ ] Non-instruction dataset complete (>=50 paragraphs)
- [ ] Instruction dataset complete (>=100 JSONL examples)
- [ ] Preference dataset complete (>=50 JSONL examples)
- [ ] 3 notebooks completed and runnable
- [ ] Base evaluation report completed
- [ ] SFT comparison report completed
- [ ] Final comparison report completed
- [ ] Fine-tuning explanation report completed
- [ ] Inference script completed
- [ ] README completed with all required sections
- [ ] Repository matches expected structure
