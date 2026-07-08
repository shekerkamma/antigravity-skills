# 🤖 Free Claude Code Setup Guide

You now have **Free Claude Code** successfully installed and configured on your machine. This proxy intercepts calls from Claude Code and routes them to free/alternative AI providers.

---

## ⚙️ Active Configuration

Your proxy settings are saved in:
* **Config File:** `C:\Users\sheke\.fcc\.env`

### 🔑 Configured API Providers & Keys

| Provider | Status | Default / Configured Model |
| :--- | :--- | :--- |
| **DeepSeek** | ✅ Configured | `deepseek/deepseek-v4-pro` (Default Fallback) |
| **NVIDIA NIM** | ✅ Configured | `nvidia_nim/z-ai/glm-5.2` |
| **OpenRouter** | ✅ Configured | `open_router/black-forest-labs/flux-1-schnell` |
| **Google AI Studio** | ✅ Configured | `gemini/models/gemini-3.5-flash` |
| **Groq Cloud** | ✅ Configured | `groq/llama-3.1-8b-instant` |

> [!NOTE]
> Since you have Groq, NVIDIA NIM, OpenRouter, Gemini, and DeepSeek configured, you can route different Claude model tiers (Opus, Sonnet, Haiku) to different providers in the `.env` file under `MODEL_OPUS`, `MODEL_SONNET`, and `MODEL_HAIKU`.

### 📋 Supported Model Slugs (All Active Providers)

Here is a list of popular and recommended models you can configure for your tiers (`MODEL_OPUS`, `MODEL_SONNET`, `MODEL_HAIKU`, or default `MODEL`):

| Provider | Model Name | Model Slug to Use | Tier Recommendation |
| :--- | :--- | :--- | :--- |
| **Groq** | Llama 3.3 70B Instruct | `groq/llama-3.3-70b-versatile` | ⭐ **Sonnet** (General coding & logic) |
| **Groq** | Llama 3.1 8B Instruct | `groq/llama-3.1-8b-instant` | ⭐ **Haiku** (Extremely fast completions) |
| **Groq** | Mixtral 8x7B Instruct | `groq/mixtral-8x7b-32768` | **Haiku** (Fast, good context) |
| **Groq** | Gemma 2 9B | `groq/gemma2-9b-it` | **Haiku** (Alternative helper) |
| **NVIDIA NIM** | Nemotron 3 Super 120B | `nvidia_nim/nvidia/nemotron-3-super-120b-a12b` | ⭐ **Opus** (Highest reasoning / complex coding) |
| **NVIDIA NIM** | GLM 5.1 | `nvidia_nim/z-ai/glm5.1` | **Opus** (Deep reasoning) |
| **NVIDIA NIM** | Kimi K2.5 | `nvidia_nim/moonshotai/kimi-k2.5` | **Opus** (High context reasoning) |
| **NVIDIA NIM** | MiniMax M2.5 | `nvidia_nim/minimaxai/minimax-m2.5` | **Opus** (Complex logic & math) |
| **OpenRouter** | Hermes 3 Llama 3.1 405B (Free) | `open_router/nousresearch/hermes-3-llama-3.1-405b:free` | ⭐ **Opus** (Highest capability / 405B parameter) |
| **OpenRouter** | Llama 3.3 70B (Free) | `open_router/meta-llama/llama-3.3-70b-instruct:free` | **Sonnet** (General coding & logic) |
| **OpenRouter** | Llama 3.2 3B (Free) | `open_router/meta-llama/llama-3.2-3b-instruct:free` | **Haiku** (Low-latency completions) |
| **OpenRouter** | Qwen 3 Coder (Free) | `open_router/qwen/qwen3-coder:free` | ⭐ **Sonnet** (Latest state-of-the-art coder) |
| **Google AI Studio** | Gemini 3.5 Flash | `gemini/models/gemini-3.5-flash` | ⭐ **Haiku** (Native fast low-latency coding) |
| **Google AI Studio** | Gemini 3.1 Pro Preview | `gemini/models/gemini-3.1-pro-preview` | ⭐ **Sonnet** (Excellent general coding & context) |
| **DeepSeek** | DeepSeek V4 Pro | `deepseek/deepseek-v4-pro` | ⭐ **Opus / Sonnet** (Flagship coding & reasoning) |
| **DeepSeek** | DeepSeek V4 Flash | `deepseek/deepseek-v4-flash` | **Haiku** (Low-latency completions) |

---

## 🚀 Execution Commands

> [!IMPORTANT]
> **Python 3.14 Compatibility Note:**
> Due to a package resolution issue with the pre-released Python 3.14.0 wrapper executables installed by `uv` on Windows, running the global `fcc-server` or `fcc-claude` wrappers directly may result in a `ModuleNotFoundError: No module named 'click.parser'` error.
> 
> To bypass this, **always use the direct paths** inside the virtual environment `Scripts` folder as listed below.

### 1. Start the Proxy Server
Keep this running in a separate terminal window while you work:
```powershell
C:\Users\sheke\AppData\Roaming\uv\tools\free-claude-code\Scripts\fcc-server.exe
```

### 2. Run Claude Code (Free Mode)
Open a new terminal window and start the agent:
```powershell
C:\Users\sheke\AppData\Roaming\uv\tools\free-claude-code\Scripts\fcc-claude.exe
```

### 3. Run Codex (Free Mode)
```powershell
C:\Users\sheke\AppData\Roaming\uv\tools\free-claude-code\Scripts\fcc-codex.exe
```

### 4. Admin UI (Local Dashboard)
When the server is running, you can access the local dashboard to change settings, validate new keys, or test models:
* **URL:** [http://127.0.0.1:8082/admin](http://127.0.0.1:8082/admin)

---

## 🎨 Image Generation Integration (Nano Banana Pro)

You can query Google's Gemini-based image generation models through your OpenRouter key by using the chat completions endpoint with special image parameters.

### 📋 Model References
* **Model ID:** `google/gemini-3-pro-image` (Nano Banana Pro) or `google/gemini-3.1-flash-image` (Nano Banana 2)
* **OpenRouter Endpoint:** `https://openrouter.ai/api/v1/chat/completions`

### 🔑 Query Payload Format
To generate an image, you must specify `"modalities": ["image"]` and limit `max_tokens` (e.g., `100`) to avoid token-reservation credit blocks:

```json
{
  "model": "google/gemini-3-pro-image",
  "messages": [
    {
      "role": "user",
      "content": "Your image description prompt here..."
    }
  ],
  "modalities": ["image"],
  "max_tokens": 100
}
```

### 📦 Output Structure
Upon success, the response JSON contains a base64-encoded PNG image string located at:
`response['choices'][0]['message']['images'][0]['image_url']['url']`

You can decode this base64 string directly and save it as a local `.png` file.
