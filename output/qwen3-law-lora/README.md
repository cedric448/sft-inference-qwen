---
library_name: peft
license: other
base_model: /root/models/Qwen3.5-0.8B
tags:
- base_model:adapter:/root/models/Qwen3.5-0.8B
- llama-factory
- lora
- transformers
pipeline_tag: text-generation
model-index:
- name: qwen3-law-lora
  results: []
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

# qwen3-law-lora

This model is a fine-tuned version of [/root/models/Qwen3.5-0.8B](https://huggingface.co//root/models/Qwen3.5-0.8B) on the law_sft dataset.
It achieves the following results on the evaluation set:
- Loss: 0.5789

## Model description

More information needed

## Intended uses & limitations

More information needed

## Training and evaluation data

More information needed

## Training procedure

### Training hyperparameters

The following hyperparameters were used during training:
- learning_rate: 0.0001
- train_batch_size: 4
- eval_batch_size: 2
- seed: 42
- gradient_accumulation_steps: 4
- total_train_batch_size: 16
- optimizer: Use OptimizerNames.ADAMW_TORCH with betas=(0.9,0.999) and epsilon=1e-08 and optimizer_args=No additional optimizer arguments
- lr_scheduler_type: cosine
- lr_scheduler_warmup_steps: 0.1
- num_epochs: 3

### Training results

| Training Loss | Epoch  | Step | Validation Loss |
|:-------------:|:------:|:----:|:---------------:|
| 0.8172        | 0.4082 | 200  | 0.6900          |
| 0.7147        | 0.8163 | 400  | 0.6344          |
| 0.6301        | 1.2245 | 600  | 0.6079          |
| 0.6146        | 1.6327 | 800  | 0.5934          |
| 0.6185        | 2.0408 | 1000 | 0.5820          |
| 0.5320        | 2.4490 | 1200 | 0.5804          |
| 0.6158        | 2.8571 | 1400 | 0.5791          |


### Framework versions

- PEFT 0.18.1
- Transformers 5.2.0
- Pytorch 2.5.1+cu124
- Datasets 4.0.0
- Tokenizers 0.22.2