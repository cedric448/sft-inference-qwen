# Qwen3.5-0.8B SFT 微调项目

## 项目目标

对 Qwen3.5-0.8B 模型进行法律领域的 SFT（监督微调），使模型具备专业的法律知识问答能力。

## 模型信息

- **基础模型**: Qwen3.5-0.8B
- **权重来源**: 腾讯云 COS 对象存储 `cedricbwang-public-1258272081/Qwen3.5-0.8B`
- **本地路径**: `/root/models/Qwen3.5-0.8B`

## 硬件环境

- **GPU**: NVIDIA L40（48GB VRAM）
- **训练显存估算**: LoRA rank=16, batch=4 约 8~12GB，L40 绰绰有余

## 训练方案

| 项目 | 选择 |
|------|------|
| 微调目标 | 法律领域知识注入（通用法律，中文） |
| 训练框架 | LLaMA-Factory |
| 训练方式 | LoRA（rank=16, alpha=32） |
| 数据格式 | ShareGPT JSON |
| 推荐数据量 | 5,000~10,000 条（推荐来源：DISC-Law-SFT） |

## 推荐数据集

- **DISC-Law-SFT**：中文法律SFT数据集，~300K条，从中采样 5K~10K 条
- **LawBench**：中文法律评测+训练数据，~20K条

## 目录结构

```
/root/sft/
├── CODEBUDDY.md
├── data/                  # 训练数据
│   └── law_sft.json
├── output/
│   ├── qwen3-law-lora/    # LoRA adapter 输出
│   └── qwen3-law-merged/  # 合并后完整模型
├── logs/
└── lora_train.yaml        # LLaMA-Factory 训练配置
/root/models/
└── Qwen3.5-0.8B/          # 基础模型权重
```

## 训练配置（lora_train.yaml 关键参数）

```yaml
model_name_or_path: /root/models/Qwen3.5-0.8B
stage: sft
finetuning_type: lora
template: qwen
cutoff_len: 2048
lora_rank: 16
lora_alpha: 32
lora_target: all
per_device_train_batch_size: 4
gradient_accumulation_steps: 4
num_train_epochs: 3
learning_rate: 1.0e-4
lr_scheduler_type: cosine
bf16: true
flash_attn: fa2
```

## 已确认配置

- [x] 法律细分方向：**通用法律**
- [x] 语言：**中文**
- [x] COS Region：**ap-beijing**
- [x] 输出风格：**简洁答复**

## 代理配置

- **代理工具**: startvpn
- **启动命令**: `startvpn`
- 需要访问 PyPI、GitHub、HuggingFace 等外网资源时，先运行 `startvpn` 开启代理

## COS 下载命令参考

```bash
export TENCENTCLOUD_SECRET_ID="<your-secret-id>"
export TENCENTCLOUD_SECRET_KEY="<your-secret-key>"

# 使用 coscmd 下载模型权重
pip install coscmd
coscmd config -a $TENCENTCLOUD_SECRET_ID -s $TENCENTCLOUD_SECRET_KEY \
  -b cedricbwang-public-1258272081 -r ap-beijing
coscmd download -r Qwen3.5-0.8B /root/models/Qwen3.5-0.8B
```
