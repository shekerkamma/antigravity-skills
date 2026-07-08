---
name: free-claude-code
description: >-
  Configure, launch, troubleshoot, and use the Free Claude Code proxy (fcc-server)
  to run Claude Code and Codex with alternative free/paid API providers.
---

# Free Claude Code Helper

## Overview
This skill provides developer agents with the exact steps, environment configurations, and command-line paths needed to run the `free-claude-code` proxy.

## Dependencies
None.

## Quick Start
To interact with the proxy or check setup, locate the configuration file:
* **Active config file:** `C:\Users\sheke\.fcc\.env`

Check model routing by running:
```powershell
Get-Content C:\Users\sheke\.fcc\.env | Select-String -Pattern "MODEL"
```

---

## Workflow

### 1. Direct Executable Path Workaround (Python 3.14)
Because the global alias wrappers (`fcc-server`, `fcc-claude`, `fcc-codex`) have a packaging parser conflict with Python 3.14.0 on Windows, **always run the executables using their direct virtual environment paths**:

* **Server:** `C:\Users\sheke\AppData\Roaming\uv\tools\free-claude-code\Scripts\fcc-server.exe`
* **Claude CLI:** `C:\Users\sheke\AppData\Roaming\uv\tools\free-claude-code\Scripts\fcc-claude.exe`
* **Codex CLI:** `C:\Users\sheke\AppData\Roaming\uv\tools\free-claude-code\Scripts\fcc-codex.exe`

### 2. Starting the Proxy Server (With Voice Support)
Keep this running in a separate background terminal:
```powershell
C:\Users\sheke\AppData\Roaming\uv\tools\free-claude-code\Scripts\fcc-server.exe
```
* **Voice Transcription Mode:** If the user wants local speech-to-text (Whisper) support, launch using:
  ```powershell
  C:\Users\sheke\AppData\Roaming\uv\tools\free-claude-code\Scripts\fcc-server.exe --voice-local
  ```

### 3. Model Mappings & Routing
To switch active model routing for Claude Code or Codex, edit `C:\Users\sheke\.fcc\.env`:
* **Sonnet Tier:** `MODEL_SONNET="nvidia_nim/z-ai/glm-5.2"` (Stable)
* **Haiku Tier:** `MODEL_HAIKU="gemini/models/gemini-3.5-flash"` (Fastest)
* **Opus Tier (Images):** `MODEL_OPUS="open_router/black-forest-labs/flux-1-schnell"` (Image Gen)
* **Default Fallback:** `MODEL="nvidia_nim/z-ai/glm-5.2"` (Default)

### 4. Running the Clients with Dynamic Settings
* **Start Claude Code (High-Context Gemini Mode):**
  When running high-context models like Gemini, manually override the auto-compacting window in the terminal before starting `fcc-claude`:
  ```powershell
  $env:CLAUDE_CODE_AUTO_COMPACT_WINDOW=900000
  C:\Users\sheke\AppData\Roaming\uv\tools\free-claude-code\Scripts\fcc-claude.exe
  ```
  *(For standard 200k models like GLM or DeepSeek, default to `$env:CLAUDE_CODE_AUTO_COMPACT_WINDOW=190000`)*

* **Start Codex (Low-Latency Coder Override):**
  To use the fast Gemini 3.5 Flash model inside Codex:
  ```powershell
  C:\Users\sheke\AppData\Roaming\uv\tools\free-claude-code\Scripts\fcc-codex.exe -m gateway/gemini/models/gemini-3.5-flash
  ```

### 5. IDE Integration (VS Code / Cursor)
To connect your IDE extensions (OpenAI or Anthropic-compatible chat assistants) to the proxy:
* **API Base URL:** Set to `http://localhost:8082/v1`
* **API Key:** Use the value of the `AUTH_TOKEN` defined in `C:\Users\sheke\.fcc\.env`.

### 6. Troubleshooting Port Bindings
If the server fails to start because port `8082` is already in use, locate the process ID and terminate it:
```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8082 -ErrorAction SilentlyContinue).OwningProcess | Stop-Process -Force
```

---

## Common Mistakes
* **Using Global Commands:** Invoking raw `fcc-server` or `fcc-claude` from the terminal (which fails under Python 3.14). Always specify the full `Scripts` path.
* **Editing Wrong Env:** Modifying `.env` in the codebase folder instead of the user home profile config: `C:\Users\sheke\.fcc\.env`.
