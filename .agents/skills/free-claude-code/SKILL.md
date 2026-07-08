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

### 2. Starting the Proxy Server
Keep this running in a separate background terminal:
```powershell
C:\Users\sheke\AppData\Roaming\uv\tools\free-claude-code\Scripts\fcc-server.exe
```
* Once running, the Admin UI is accessible at: `http://127.0.0.1:8082/admin`

### 3. Model Mappings & Routing
To switch active model routing for Claude Code or Codex, edit `C:\Users\sheke\.fcc\.env`:
* **Sonnet Tier:** `MODEL_SONNET="nvidia_nim/z-ai/glm-5.2"` (Stable)
* **Haiku Tier:** `MODEL_HAIKU="gemini/models/gemini-3.5-flash"` (Fastest)
* **Opus Tier (Images):** `MODEL_OPUS="open_router/black-forest-labs/flux-1-schnell"` (Image Gen)
* **Default Fallback:** `MODEL="nvidia_nim/z-ai/glm-5.2"` (Default)

### 4. Running the Clients
* **Start Claude Code:**
  ```powershell
  C:\Users\sheke\AppData\Roaming\uv\tools\free-claude-code\Scripts\fcc-claude.exe
  ```
* **Start Codex:**
  ```powershell
  C:\Users\sheke\AppData\Roaming\uv\tools\free-claude-code\Scripts\fcc-codex.exe
  ```
  *(Note: You can pass specific model overrides using the `-m` flag, e.g., `-m gateway/gemini/models/gemini-3.5-flash`)*

### 5. Troubleshooting Port Bindings
If the server fails to start because port `8082` is already in use, locate the process ID and terminate it:
```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8082 -ErrorAction SilentlyContinue).OwningProcess | Stop-Process -Force
```

---

## Common Mistakes
* **Using Global Commands:** Invoking raw `fcc-server` or `fcc-claude` from the terminal (which fails under Python 3.14). Always specify the full `Scripts` path.
* **Editing Wrong Env:** Modifying `.env` in the codebase folder instead of the user home profile config: `C:\Users\sheke\.fcc\.env`.
