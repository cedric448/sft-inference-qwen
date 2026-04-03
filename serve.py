"""
OpenAI-compatible inference server for qwen3-law model.
Endpoints: POST /v1/chat/completions, GET /v1/models
"""
import time
import uuid
import torch
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_PATH = "/root/sft/output/qwen3-law-merged"
MODEL_NAME = "qwen3-law"

print(f"Loading model from {MODEL_PATH} ...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    trust_remote_code=True,
)
model.eval()
print("Model loaded.")

app = FastAPI(title="qwen3-law API")


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: Optional[str] = MODEL_NAME
    messages: List[Message]
    max_tokens: Optional[int] = 512
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.9
    stream: Optional[bool] = False


@app.get("/v1/models")
def list_models():
    return {
        "object": "list",
        "data": [{
            "id": MODEL_NAME,
            "object": "model",
            "created": int(time.time()),
            "owned_by": "local",
        }]
    }


@app.post("/v1/chat/completions")
def chat_completions(req: ChatRequest):
    if req.stream:
        raise HTTPException(status_code=400, detail="Streaming not supported yet.")

    messages = [{"role": m.role, "content": m.content} for m in req.messages]
    text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    inputs = tokenizer(text, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=req.max_tokens or 512,
            temperature=req.temperature if req.temperature and req.temperature > 0 else 1.0,
            top_p=req.top_p or 0.9,
            do_sample=(req.temperature or 0.7) > 0,
            pad_token_id=tokenizer.eos_token_id,
        )

    generated = outputs[0][inputs.input_ids.shape[1]:]
    reply = tokenizer.decode(generated, skip_special_tokens=True)

    return {
        "id": f"chatcmpl-{uuid.uuid4().hex[:8]}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": MODEL_NAME,
        "choices": [{
            "index": 0,
            "message": {"role": "assistant", "content": reply},
            "finish_reason": "stop",
        }],
        "usage": {
            "prompt_tokens": inputs.input_ids.shape[1],
            "completion_tokens": len(generated),
            "total_tokens": inputs.input_ids.shape[1] + len(generated),
        }
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
