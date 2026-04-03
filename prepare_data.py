#!/usr/bin/env python3
"""
从 DISC-Law-SFT CSV 文件采样 8000 条，转换为 LLaMA-Factory ShareGPT 格式
"""
import json
import random
import csv

SAMPLE_SIZE = 8000
OUTPUT_PATH = "/root/sft/data/law_sft.json"
SYSTEM_PROMPT = "你是一位专业的中国法律顾问，请根据用户的问题提供准确、简洁的法律解答。"
random.seed(42)

def load_csv(path, input_col="input", output_col="output"):
    rows = []
    with open(path, encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for row in reader:
            inp = row.get(input_col, "").strip()
            out = row.get(output_col, "").strip()
            if inp and out and len(inp) > 5 and len(out) > 10:
                rows.append({"input": inp, "output": out})
    return rows

print("加载 Pair 数据...")
pair_data = load_csv("/root/sft/data/DISC-Law-SFT-Pair.csv")
print(f"Pair 有效条数: {len(pair_data)}")

print("加载 Triplet 数据...")
triplet_data = load_csv("/root/sft/data/DISC-Law-SFT-Triplet.csv")
print(f"Triplet 有效条数: {len(triplet_data)}")

all_data = pair_data + triplet_data
print(f"总计: {len(all_data)} 条")

# 采样
sample_n = min(SAMPLE_SIZE, len(all_data))
samples = random.sample(all_data, sample_n)

# 转换为 ShareGPT 格式
output = []
for item in samples:
    entry = {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": item["input"]},
            {"role": "assistant", "content": item["output"]}
        ]
    }
    output.append(entry)

print(f"最终样本: {len(output)} 条")

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"已保存至: {OUTPUT_PATH}")
print("\n示例（第1条）:")
print(json.dumps(output[0], ensure_ascii=False, indent=2)[:600])
