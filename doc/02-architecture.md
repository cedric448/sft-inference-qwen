# 架构文档

## 目录结构

```
/root/sft/
├── README.md                    # 项目总览
├── CODEBUDDY.md                 # 项目配置备忘
├── doc/                         # 文档目录
│   ├── 01-project-design.md    # 项目设计
│   ├── 02-architecture.md      # 架构（本文件）
│   ├── 03-finetune.md          # 微调指南
│   ├── 04-deployment.md        # 部署指南
│   └── 05-usage.md             # 使用指南
├── data/                        # 训练数据
│   ├── law_sft.json            # 8000 条 ShareGPT 格式训练数据
│   ├── DISC-Law-SFT-Pair.csv   # 原始数据（143,374 条）
│   └── DISC-Law-SFT-Triplet.csv # 原始数据（16,000 条）
├── output/
│   ├── qwen3-law-lora/         # LoRA adapter 权重
│   │   ├── adapter_model.safetensors  # 42MB LoRA 参数
│   │   ├── adapter_config.json
│   │   ├── checkpoint-*/       # 训练检查点
│   │   ├── training_loss.png   # Loss 曲线图
│   │   └── trainer_log.jsonl   # 训练日志
│   └── qwen3-law-merged/       # 合并后完整模型（用于推理）
│       ├── model.safetensors   # 1.6GB 完整权重
│       ├── config.json
│       └── tokenizer.json
├── logs/
│   ├── train.log               # 训练进程日志
│   └── serve.log               # 推理服务日志
├── lora_train.yaml             # LLaMA-Factory 训练配置
├── lora_export.yaml            # LoRA 合并导出配置
├── prepare_data.py             # 数据预处理脚本
└── serve.py                    # OpenAI 兼容推理服务

/root/models/
└── Qwen3.5-0.8B/               # 基础模型权重（来自腾讯云 COS）

/root/LLaMA-Factory/            # LLaMA-Factory 框架源码（editable 安装）
```

## 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                        数据流                                │
│                                                             │
│  DISC-Law-SFT (ModelScope)                                  │
│         │                                                   │
│         ▼                                                   │
│  prepare_data.py (采样 8000 条, 转 ShareGPT 格式)           │
│         │                                                   │
│         ▼                                                   │
│  law_sft.json ──────────────────────────────────────────┐  │
│                                                         │  │
│                        训练流                           │  │
│                                                         │  │
│  Qwen3.5-0.8B（基础权重）                               │  │
│         │                                               │  │
│         ▼                                               ▼  │
│  LLaMA-Factory (LoRA SFT) ◄──────────────────── 训练数据  │
│         │                                               │  │
│         ▼                                               │  │
│  qwen3-law-lora（LoRA adapter）                         │  │
│         │                                               │  │
│         ▼                                               │  │
│  llamafactory export（权重合并）                         │  │
│         │                                               │  │
│         ▼                                               │  │
│  qwen3-law-merged（完整模型）                            │  │
│                                                             │
│                        推理流                               │
│                                                             │
│  serve.py（FastAPI + transformers）                         │
│         │                                                   │
│         ▼                                                   │
│  0.0.0.0:8000（OpenAI 兼容接口）                           │
│         │                                                   │
│         ▼                                                   │
│  外网访问：http://43.135.74.4:8000                          │
└─────────────────────────────────────────────────────────────┘
```

## 关键依赖版本

| 包 | 版本 |
|----|------|
| Python | 3.11.11 |
| torch | 2.6.0+cu124 |
| transformers | 5.5.0 |
| llamafactory | 0.9.5.dev0 |
| peft | 0.18.1 |
| accelerate | 1.11.0 |
| trl | 0.24.0 |
| fastapi | 最新 |
| uvicorn | 最新 |

## GPU 环境

- **型号**：NVIDIA L40
- **显存**：46GB
- **CUDA Driver**：570.158.01（CUDA 12.8）
- **PyTorch CUDA 版本**：cu124（向下兼容）
- **LD_LIBRARY_PATH**：见 `/etc/profile.d/nvidia_libs.sh`
