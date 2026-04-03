# 部署指南

## 推理服务架构

使用 FastAPI + transformers 实现 OpenAI 兼容的 HTTP 推理服务，监听 `0.0.0.0:8000`。

> **说明**：Qwen3.5 架构（`Qwen3_5ForConditionalGeneration`）在 vLLM 0.8.x 及以下版本中尚未支持，因此使用 transformers 原生推理 + FastAPI 包装的方式提供服务。等 vLLM 支持后可迁移以获得更高吞吐。

## 环境准备

```bash
source /etc/profile.d/nvidia_libs.sh

pip3.11 install fastapi uvicorn "transformers>=5.0.0"
```

## 启动服务

```bash
source /etc/profile.d/nvidia_libs.sh

# 后台启动
nohup python3.11 /root/sft/serve.py > /root/sft/logs/serve.log 2>&1 &

# 查看启动日志
tail -f /root/sft/logs/serve.log
```

服务启动完成后日志会显示：
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## 服务端点

| 端点 | 方法 | 描述 |
|------|------|------|
| `/v1/models` | GET | 列出可用模型 |
| `/v1/chat/completions` | POST | Chat 推理接口（OpenAI 兼容） |

## 公网访问

本机公网 IP：**43.135.74.4**

服务默认监听所有网卡（`0.0.0.0`），直接通过公网 IP 访问：

```
http://43.135.74.4:8000
```

### 防火墙配置（如需要）

```bash
# 开放 8000 端口
firewall-cmd --permanent --add-port=8000/tcp
firewall-cmd --reload
```

## serve.py 服务配置说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `host` | 0.0.0.0 | 监听地址 |
| `port` | 8000 | 监听端口 |
| `model` | qwen3-law | 服务模型名称 |
| `dtype` | bfloat16 | 推理精度 |
| `device_map` | auto | 自动分配 GPU |

## 停止服务

```bash
# 查找进程
ps aux | grep serve.py | grep -v grep

# 停止
kill <PID>
```

## 生产建议

- 在 `serve.py` 前加 Nginx 反向代理，支持 HTTPS
- 添加 API Key 认证（在 FastAPI 中间件中实现）
- 使用 `systemd` 服务管理，确保开机自启
- 迁移到 vLLM（待其支持 Qwen3.5 架构后），可大幅提升并发吞吐
