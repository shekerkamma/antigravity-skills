#!/usr/bin/env python3
"""
Sol Bridge — Multi-Model Communication Engine for Grill Codeex
==============================================================

Bridges Claude (planning/review) with secondary models (critique/build)
by making direct HTTP API calls using only Python standard libraries.

Modes:
  --mode critique   Read ALIGNED_PLAN.md, send to secondary model for
                    adversarial review, append critique to PLAN-REVIEW-LOG.md.
  --mode build      Send the finalized plan to secondary model, parse
                    structured file output, write files to disk.

Providers Supported (Auto-detected from keys):
  1. OpenRouter (OPENROUTER_API_KEY)
  2. Gemini (GEMINI_API_KEY)
  3. DeepSeek (DEEPSEEK_API_KEY)
  4. Groq (GROQ_API_KEY)
  5. OpenAI (OPENAI_API_KEY)
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
import re
import argparse
import datetime

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MAX_RETRIES = 3
RETRY_BACKOFF_BASE = 2  # seconds
REQUEST_TIMEOUT = 180  # seconds

PROVIDERS = {
    #"openrouter": {
    #    "env_key": "OPENROUTER_API_KEY",
    #    "url": "https://openrouter.ai/api/v1/chat/completions",
    #    "default_critique": "anthropic/claude-3.5-sonnet",
    #    "default_build": "deepseek/deepseek-chat",
    #},
    "gemini": {
        "env_key": "GEMINI_API_KEY",
        "url": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
        "default_critique": "gemini-2.5-flash",
        "default_build": "gemini-2.5-pro",
    },
    "deepseek": {
        "env_key": "DEEPSEEK_API_KEY",
        "url": "https://api.deepseek.com/chat/completions",
        "default_critique": "deepseek-chat",
        "default_build": "deepseek-chat",
    },
    "groq": {
        "env_key": "GROQ_API_KEY",
        "url": "https://api.groq.com/openai/v1/chat/completions",
        "default_critique": "llama-3.3-70b-versatile",
        "default_build": None, # Groq context limit too small for full build
    },
    "openai": {
        "env_key": "OPENAI_API_KEY",
        "url": "https://api.openai.com/v1/chat/completions",
        "default_critique": "gpt-4o",
        "default_build": "gpt-4o",
    }
}

# ---------------------------------------------------------------------------
# Provider Resolution
# ---------------------------------------------------------------------------

def get_provider_and_key():
    """Detect the best available API provider based on env vars/files."""
    # Read from .fcc/.env if available
    home = os.path.expanduser("~")
    env_vars = dict(os.environ)
    
    for env_path in [
        os.path.join(home, ".config", "watch", ".env"),
        os.path.join(home, ".fcc", ".env"),
        ".env",
    ]:
        if os.path.exists(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        stripped = line.strip()
                        if not stripped or stripped.startswith("#"): continue
                        if "=" in stripped:
                            k, v = stripped.split("=", 1)
                            env_vars[k.strip()] = v.strip('"').strip("'")
            except Exception:
                pass

    for provider_name, config in PROVIDERS.items():
        key = env_vars.get(config["env_key"])
        if key:
            return provider_name, key, config

    return None, None, None

# ---------------------------------------------------------------------------
# API Client
# ---------------------------------------------------------------------------

def call_chat_api(url, api_key, system_prompt, user_content, model, temperature=0.2):
    """Call the OpenAI-compatible Chat Completions API with retry and backoff."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    
    # OpenRouter specific headers
    if "openrouter" in url:
        headers["HTTP-Referer"] = "https://github.com/google/antigravity"
        headers["X-Title"] = "Grill Codeex"

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        "temperature": temperature,
    }

    data = json.dumps(payload).encode("utf-8")

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                body = json.loads(resp.read().decode("utf-8"))
                content = body["choices"][0]["message"]["content"]

                usage = body.get("usage", {})
                if usage:
                    log(f"  Tokens — prompt: {usage.get('prompt_tokens', '?')}, "
                        f"completion: {usage.get('completion_tokens', '?')}, "
                        f"total: {usage.get('total_tokens', '?')}")

                return content

        except urllib.error.HTTPError as e:
            err_body = ""
            try: err_body = e.read().decode("utf-8")
            except Exception: pass

            if e.code == 429 and attempt < MAX_RETRIES:
                wait = RETRY_BACKOFF_BASE ** attempt
                log(f"  Rate limited (429). Retrying in {wait}s...", level="WARN")
                time.sleep(wait)
                continue
            elif e.code >= 500 and attempt < MAX_RETRIES:
                wait = RETRY_BACKOFF_BASE ** attempt
                log(f"  Server error ({e.code}). Retrying in {wait}s...", level="WARN")
                time.sleep(wait)
                continue
            else:
                log(f"HTTP Error {e.code}: {e.reason}", level="ERROR")
                log(f"Details: {err_body}", level="ERROR")
                sys.exit(1)

        except Exception as e:
            if attempt < MAX_RETRIES:
                wait = RETRY_BACKOFF_BASE ** attempt
                log(f"  Connection error: {e}. Retrying in {wait}s...", level="WARN")
                time.sleep(wait)
                continue
            log(f"Error calling API: {e}", level="ERROR")
            sys.exit(1)

    sys.exit(1)

def log(msg, level="INFO"):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    prefix = {"INFO": "▸", "WARN": "⚠", "ERROR": "✗", "OK": "✓"}.get(level, "▸")
    print(f"[sol-bridge {ts}] {prefix} {msg}", file=sys.stderr)

# ---------------------------------------------------------------------------
# Modes
# ---------------------------------------------------------------------------

CRITIQUE_PROMPT = """\
You are an elite Systems Architect and Security Reviewer performing an adversarial review.
Find weaknesses — do not praise. Analyze for:
1. Architectural Soundness (coupling, scalability)
2. Security Flaws (auth gaps, injection, data exposure)
3. Implementation Risks (race conditions, errors)
4. Missing Edge Cases
5. Data Model Issues

For each finding provide:
- Severity tag: [CRITICAL], [HIGH], [MEDIUM], or [LOW]
- One-line summary
- Concrete recommendation

Output clean Markdown under header: ## Adversarial Critique — Round {round_num}
"""

def run_critique(config, api_key, args):
    model = args.model or config["default_critique"]
    log(f"Critique mode — plan: {args.plan}, model: {model}")

    with open(args.plan, "r", encoding="utf-8") as f:
        plan_content = f.read()

    log_path = os.path.join(os.path.dirname(args.plan) or ".", "PLAN-REVIEW-LOG.md")
    round_num = 1
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            round_num = len(re.findall(r"## Adversarial Critique — Round \d+", f.read())) + 1
            
    log(f"  Starting adversarial round {round_num}")
    sys_prompt = CRITIQUE_PROMPT.replace("{round_num}", str(round_num))

    if args.dry_run:
        log("  [DRY RUN] Would send plan for critique. Skipping.", level="WARN")
        return

    critique = call_chat_api(config["url"], api_key, sys_prompt, plan_content, model)

    ts = datetime.datetime.now().isoformat()
    with open(log_path, "a", encoding="utf-8") as f:
        if round_num == 1:
            f.write("# Plan Review Log\n\n")
        f.write(f"\n## Round {round_num} — {ts}\n")
        f.write(f"**Model:** {model}\n\n")
        f.write(critique + "\n")

    log(f"  Critique round {round_num} written to {log_path}", level="OK")


BUILD_PROMPT = """\
You are a high-velocity software engineer. Implement the exact codebase defined in the plan.
CRITICAL OUTPUT FORMAT:
For EVERY file you create, wrap it exactly like this:
=== START FILE: <relative/path/to/file.ext> ===
<complete file contents here>
=== END FILE: <relative/path/to/file.ext> ===
Rules:
- NO prose. NO explanations. NO global markdown blocks.
- Relative paths must use forward slashes.
- NO placeholders or TODOs. Write complete files.
"""

def run_build(config, api_key, args):
    model = args.model or config["default_build"]
    if not model:
        log("Provider does not support build mode (e.g., context limit too small).", level="ERROR")
        sys.exit(1)
        
    log(f"Build mode — plan: {args.plan}, model: {model}")
    out_dir = args.output_dir or "."
    log(f"  Output directory: {out_dir}")

    with open(args.plan, "r", encoding="utf-8") as f:
        plan_content = f.read()

    if args.dry_run:
        log("  [DRY RUN] Would send plan for code generation. Skipping.", level="WARN")
        return

    response = call_chat_api(config["url"], api_key, BUILD_PROMPT, plan_content, model, temperature=0.1)

    pattern = re.compile(r'=== START FILE:\s*(.*?)\s*===\n(.*?)=== END FILE:\s*\1\s*===', re.DOTALL)
    matches = list(pattern.finditer(response))

    if not matches:
        log("No valid file blocks found.", level="ERROR")
        raw_path = os.path.join(out_dir, "SOL_RAW_RESPONSE.md")
        os.makedirs(out_dir, exist_ok=True)
        with open(raw_path, "w", encoding="utf-8") as f:
            f.write(response)
        log(f"  Raw response saved to {raw_path}", level="WARN")
        sys.exit(1)

    written = []
    for match in matches:
        filepath = match.group(1).strip()
        content = match.group(2)

        clean_path = os.path.normpath(filepath)
        if clean_path.startswith("..") or os.path.isabs(clean_path):
            log(f"  SKIPPING unsafe path: {filepath}", level="WARN")
            continue

        full_path = os.path.join(out_dir, clean_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        log(f"  Wrote: {clean_path} ({len(content.encode('utf-8')):,} bytes)")
        written.append(clean_path)

    man_path = os.path.join(out_dir, "SOL_BUILD_MANIFEST.md")
    with open(man_path, "w", encoding="utf-8") as f:
        f.write("# Sol Build Manifest\n\n")
        f.write(f"**Date:** {datetime.datetime.now().isoformat()}\n")
        f.write(f"**Model:** {model}\n\n")
        f.write("## Files\n")
        for p in written: f.write(f"- `{p}`\n")
        
    log(f"  Build complete: {len(written)} files. Manifest at {man_path}", level="OK")

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Multi-model bridge engine for Grill Codeex")
    parser.add_argument("--mode", choices=["critique", "build"], required=True)
    parser.add_argument("--plan", default="ALIGNED_PLAN.md")
    parser.add_argument("--model", help="Override default model for the provider")
    parser.add_argument("--output-dir", help="Output directory for build mode")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    provider_name, api_key, config = get_provider_and_key()
    if not provider_name and not args.dry_run:
        log("No valid API keys found.", level="ERROR")
        sys.exit(1)

    log("=" * 50)
    log(f"Sol Bridge | Mode: {args.mode} | Provider: {provider_name or 'dry-run'}")
    log("=" * 50)

    if not os.path.exists(args.plan):
        log(f"Plan file not found: {args.plan}", level="ERROR")
        sys.exit(1)

    if args.mode == "critique": run_critique(config, api_key, args)
    elif args.mode == "build": run_build(config, api_key, args)
    
if __name__ == "__main__":
    main()
