# Qwen3.5-0.8B 法律领域 SFT 微调

基于 Qwen3.5-0.8B 的中文通用法律领域监督微调（SFT）项目，使用 LoRA 方法在 DISC-Law-SFT 数据集上训练，并提供 OpenAI 兼容的推理服务。

## 模型能力

- 中文法律问题解答（劳动法、合同法、婚姻法、刑法、民事诉讼等）
- 输出简洁、准确，适合快速法律咨询
- 基于真实法律条文，引用相关法规

## 快速体验

```bash
curl http://43.135.74.4:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3-law",
    "messages": [
      {"role": "system", "content": "你是一位专业的中国法律顾问，请根据用户的问题提供准确、简洁的法律解答。"},
      {"role": "user", "content": "劳动合同到期后公司不续签，需要支付经济补偿金吗？"}
    ],
    "max_tokens": 512
  }'
```

## 项目概览

| 项目 | 详情 |
|------|------|
| 基础模型 | Qwen3.5-0.8B |
| 微调方式 | LoRA（rank=16, alpha=32） |
| 训练框架 | LLaMA-Factory 0.9.5 |
| 训练数据 | DISC-Law-SFT，采样 8,000 条 |
| 训练 Loss | 1.513 → **0.508** |
| 推理服务 | FastAPI + transformers，OpenAI 兼容 |
| 硬件 | NVIDIA L40 48GB |
| 训练时长 | 2 小时 23 分钟 |

## 文档

| 文档 | 内容 |
|------|------|
| [项目设计](doc/01-project-design.md) | 技术选型、数据策略、训练结果 |
| [架构说明](doc/02-architecture.md) | 目录结构、系统架构图、依赖版本 |
| [微调指南](doc/03-finetune.md) | 环境搭建、数据准备、训练配置、权重合并 |
| [部署指南](doc/04-deployment.md) | 推理服务启动、公网访问配置 |
| [使用指南](doc/05-usage.md) | API 接口、curl/Python 调用示例 |

## 目录结构

```
.
├── README.md
├── doc/                    # 项目文档
├── data/                   # 训练数据
│   └── law_sft.json       # 8000 条 ShareGPT 格式数据
├── output/
│   ├── qwen3-law-lora/    # LoRA adapter
│   └── qwen3-law-merged/  # 合并后完整模型（1.6GB）
├── logs/                   # 训练和推理日志
├── lora_train.yaml         # 训练配置
├── lora_export.yaml        # 权重合并配置
├── prepare_data.py         # 数据预处理脚本
└── serve.py                # OpenAI 兼容推理服务
```

## API 接口

服务地址：`http://43.135.74.4:8000`

```python
from openai import OpenAI

client = OpenAI(base_url="http://43.135.74.4:8000/v1", api_key="any")
response = client.chat.completions.create(
    model="qwen3-law",
    messages=[
        {"role": "system", "content": "你是一位专业的中国法律顾问，请根据用户的问题提供准确、简洁的法律解答。"},
        {"role": "user", "content": "合同纠纷的诉讼时效是多久？"}
    ]
)
print(response.choices[0].message.content)
```

## 免责声明

本模型仅供参考，不构成正式法律建议。涉及具体案件请咨询持证律师。
