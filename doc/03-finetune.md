# 微调指南

## 环境准备

### 1. 系统要求

- Python 3.11+
- NVIDIA GPU（16GB+ VRAM，推荐 L40/A100）
- CUDA 12.x

### 2. 安装依赖

```bash
# 克隆 LLaMA-Factory
git clone https://github.com/hiyouga/LLaMA-Factory.git /root/LLaMA-Factory
cd /root/LLaMA-Factory

# 安装（需 Python 3.11+）
python3.11 -m pip install -e ".[torch,metrics]" -i https://pypi.org/simple/

# 安装兼容 CUDA 12.x 的 PyTorch
pip3.11 install torch==2.5.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu124
```

### 3. 配置 CUDA 库路径

```bash
# 写入持久化配置（解决 libcupti 等库找不到的问题）
cat > /etc/profile.d/nvidia_libs.sh << 'EOF'
export LD_LIBRARY_PATH=/usr/local/lib/python3.11/site-packages/nvidia/cusparse/lib:/usr/local/lib/python3.11/site-packages/nvidia/nccl/lib:/usr/local/lib/python3.11/site-packages/nvidia/cublas/lib:/usr/local/lib/python3.11/site-packages/nvidia/cudnn/lib:/usr/local/lib/python3.11/site-packages/nvidia/cuda_cupti/lib:/usr/local/lib/python3.11/site-packages/nvidia/cuda_runtime/lib:$LD_LIBRARY_PATH
EOF
source /etc/profile.d/nvidia_libs.sh
```

## 数据准备

### 下载原始数据

```bash
# 从 ModelScope 下载 DISC-Law-SFT 数据集
mkdir -p /root/sft/data
wget -O /root/sft/data/DISC-Law-SFT-Pair.csv \
  "https://modelscope.cn/datasets/AI-ModelScope/DISC-Law-SFT/resolve/master/DISC-Law-SFT-Pair.csv"
wget -O /root/sft/data/DISC-Law-SFT-Triplet.csv \
  "https://modelscope.cn/datasets/AI-ModelScope/DISC-Law-SFT/resolve/master/DISC-Law-SFT-Triplet.csv"
```

### 生成训练数据

```bash
python3.11 /root/sft/prepare_data.py
# 输出：/root/sft/data/law_sft.json（8000 条 ShareGPT 格式）
```

### 注册数据集到 LLaMA-Factory

在 `/root/LLaMA-Factory/data/dataset_info.json` 末尾添加：

```json
"law_sft": {
  "file_name": "/root/sft/data/law_sft.json",
  "formatting": "sharegpt",
  "columns": {
    "messages": "messages"
  },
  "tags": {
    "role_tag": "role",
    "content_tag": "content",
    "user_tag": "user",
    "assistant_tag": "assistant",
    "system_tag": "system"
  }
}
```

## 训练配置

训练配置文件：`/root/sft/lora_train.yaml`

```yaml
### model
model_name_or_path: /root/models/Qwen3.5-0.8B

### method
stage: sft
do_train: true
finetuning_type: lora
lora_rank: 16
lora_alpha: 32
lora_dropout: 0.05
lora_target: all

### dataset
dataset: law_sft
dataset_dir: /root/LLaMA-Factory/data
template: qwen3_nothink        # 非推理模式（不加 _nothink 会触发 thinking 模式）
cutoff_len: 2048
max_samples: 10000
overwrite_cache: true
preprocessing_num_workers: 4

### output
output_dir: /root/sft/output/qwen3-law-lora
logging_dir: /root/sft/logs
logging_steps: 10
save_steps: 200
plot_loss: true
overwrite_output_dir: true

### train
per_device_train_batch_size: 4
gradient_accumulation_steps: 4
learning_rate: 1.0e-4
num_train_epochs: 3
lr_scheduler_type: cosine
warmup_ratio: 0.1
bf16: true
flash_attn: fa2

### eval
val_size: 0.02
per_device_eval_batch_size: 2
eval_strategy: steps
eval_steps: 200
```

> **注意**：Qwen3.5 使用 `template: qwen3_nothink`，不要用 `qwen3`（否则会启用推理链模式）

## 启动训练

```bash
source /etc/profile.d/nvidia_libs.sh

# 前台运行（可观察进度）
llamafactory-cli train /root/sft/lora_train.yaml

# 后台运行（推荐）
nohup llamafactory-cli train /root/sft/lora_train.yaml \
  > /root/sft/logs/train.log 2>&1 &
```

### 监控训练进度

```bash
# 实时查看结构化日志（推荐）
tail -f /root/sft/output/qwen3-law-lora/trainer_log.jsonl

# 查看原始日志（含进度条）
cat /root/sft/logs/train.log | tr '\r' '\n' | grep "/1470" | tail -5
```

## 合并 LoRA 权重

训练完成后，将 LoRA adapter 合并到基础模型：

配置文件 `/root/sft/lora_export.yaml`：

```yaml
model_name_or_path: /root/models/Qwen3.5-0.8B
adapter_name_or_path: /root/sft/output/qwen3-law-lora
template: qwen3_nothink
finetuning_type: lora
export_dir: /root/sft/output/qwen3-law-merged
export_size: 2
export_legacy_format: false
```

```bash
source /etc/profile.d/nvidia_libs.sh
llamafactory-cli export /root/sft/lora_export.yaml
```

合并后输出路径：`/root/sft/output/qwen3-law-merged/`（完整模型，1.6GB）

## 训练结果

| 指标 | 值 |
|------|-----|
| 初始 Loss | 1.513 |
| 最终 Train Loss | **0.508** |
| Eval Loss | 0.593 |
| 总训练时长 | 2h 23min（L40 单卡） |
