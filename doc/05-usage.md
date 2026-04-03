# 使用指南

## API 接口

服务地址：`http://43.135.74.4:8000`（或本地 `http://localhost:8000`）

接口兼容 OpenAI Chat Completions 格式，可直接替换 OpenAI SDK 的 `base_url`。

---

## 查询可用模型

```bash
curl http://43.135.74.4:8000/v1/models
```

返回：
```json
{
  "object": "list",
  "data": [
    {
      "id": "qwen3-law",
      "object": "model",
      "owned_by": "local"
    }
  ]
}
```

---

## 法律问答示例

### curl 调用

```bash
curl http://43.135.74.4:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3-law",
    "messages": [
      {
        "role": "system",
        "content": "你是一位专业的中国法律顾问，请根据用户的问题提供准确、简洁的法律解答。"
      },
      {
        "role": "user",
        "content": "劳动合同到期后公司不续签，需要支付经济补偿金吗？"
      }
    ],
    "max_tokens": 512,
    "temperature": 0.7
  }'
```

### 示例回答

> 根据《中华人民共和国劳动合同法》第四十六条和第四十七条的规定，劳动合同到期后公司不续签，需要支付经济补偿金。具体计算方式为：工作年限乘以经济补偿金标准，即每月经济补偿金标准为劳动者在本月工资数额的两倍，而劳动者在劳动合同解除前工作的年限，为工作年限。

---

## Python 调用

### 使用 openai SDK

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://43.135.74.4:8000/v1",
    api_key="any",  # 本地服务不验证 key
)

response = client.chat.completions.create(
    model="qwen3-law",
    messages=[
        {
            "role": "system",
            "content": "你是一位专业的中国法律顾问，请根据用户的问题提供准确、简洁的法律解答。"
        },
        {
            "role": "user",
            "content": "合同纠纷的诉讼时效是多久？"
        }
    ],
    max_tokens=512,
    temperature=0.7,
)

print(response.choices[0].message.content)
```

### 使用 requests

```python
import requests

resp = requests.post(
    "http://43.135.74.4:8000/v1/chat/completions",
    json={
        "model": "qwen3-law",
        "messages": [
            {"role": "system", "content": "你是一位专业的中国法律顾问，请根据用户的问题提供准确、简洁的法律解答。"},
            {"role": "user", "content": "离婚财产分割的原则是什么？"}
        ],
        "max_tokens": 512,
        "temperature": 0.7,
    }
)
print(resp.json()["choices"][0]["message"]["content"])
```

---

## 请求参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `model` | string | qwen3-law | 模型名称 |
| `messages` | array | 必填 | 对话历史，支持 system/user/assistant |
| `max_tokens` | int | 512 | 最大生成 token 数 |
| `temperature` | float | 0.7 | 采样温度，0~1，越低越确定性 |
| `top_p` | float | 0.9 | nucleus 采样概率 |

---

## 法律问答场景示例

| 场景 | 示例问题 |
|------|---------|
| 劳动法 | 被违法解除劳动合同可以要求赔偿金吗？ |
| 合同法 | 口头合同有法律效力吗？ |
| 民事诉讼 | 起诉需要哪些材料？ |
| 婚姻法 | 婚前财产婚后会变成共同财产吗？ |
| 刑法 | 盗窃多少金额构成犯罪？ |
| 房产 | 购房合同违约如何处理？ |

---

## 注意事项

- 本模型仅供参考，不构成正式法律建议
- 涉及具体案件请咨询持证律师
- 法律条文以最新颁布版本为准
