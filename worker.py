#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Worker — unified entry point, routes to the cheapest capable backend.

Usage:
  python worker.py "task"                            # DeepSeek Pro (default)
  python worker.py --flash "task"                    # DeepSeek Flash
  python worker.py --groq "task"                     # Groq (free, 300+ tok/s)
  python worker.py --ollama "task"                   # Ollama local (free)
  python worker.py --ollama qwen3.5:9b "task"        # specify Ollama model

Boss Mode options (combine with any backend):
  --context-file <path>   Inject file content as context (saves Boss output tokens)
  --code-only             Worker outputs code only — no explanations or markdown
  --output-file <path>    Write result to file instead of stdout (Boss just runs tests)

Environment variables:
  DEEPSEEK_API_KEY   — required for --flash / default Pro backend
  GROQ_API_KEY       — required for --groq
  OLLAMA_HOST        — optional, defaults to http://localhost:11434
"""
import sys
import json
import os
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

OLLAMA_DEFAULT = "gemma4:26b"
GROQ_DEFAULT = "llama-3.1-8b-instant"
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

CODE_ONLY_SYSTEM = (
    "You are a code generation assistant. "
    "Output ONLY the requested code. "
    "No markdown fences, no explanations, no comments unless part of the code itself."
)


def call_openai_compat(base_url: str, api_key: str, model: str,
                        prompt: str, system: str = "") -> str:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload = json.dumps({"model": model, "messages": messages}).encode("utf-8")
    req = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
        },
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"]


def call_ollama(model: str, prompt: str, system: str = "") -> str:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload = json.dumps({"model": model, "messages": messages, "stream": False}).encode("utf-8")
    req = urllib.request.Request(
        f"{OLLAMA_HOST}/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return data["message"]["content"]


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)

    backend = "deepseek-pro"
    ollama_model = OLLAMA_DEFAULT
    context_file = None
    output_file = None
    code_only = False
    remaining = []

    i = 0
    while i < len(args):
        a = args[i]
        if a == "--ollama":
            backend = "ollama"
            if i + 1 < len(args) and ":" in args[i + 1] and not args[i + 1].startswith("-"):
                i += 1
                ollama_model = args[i]
        elif a == "--groq":
            backend = "groq"
        elif a == "--flash":
            backend = "deepseek-flash"
        elif a == "--code-only":
            code_only = True
        elif a == "--context-file":
            i += 1
            context_file = args[i]
        elif a == "--output-file":
            i += 1
            output_file = args[i]
        else:
            remaining.append(a)
        i += 1

    prompt = " ".join(remaining)
    if not prompt:
        print("Error: missing task prompt.", file=sys.stderr)
        sys.exit(1)

    # Prepend file context — Worker sees the code, Boss doesn't burn output tokens on it
    if context_file:
        with open(context_file, encoding="utf-8") as f:
            content = f.read()
        prompt = f"[CONTEXT FILE: {context_file}]\n```\n{content}\n```\n\n[TASK]\n{prompt}"

    system = CODE_ONLY_SYSTEM if code_only else ""

    if backend == "ollama":
        result = call_ollama(ollama_model, prompt, system)
    elif backend == "groq":
        api_key = os.environ.get("GROQ_API_KEY", "")
        if not api_key:
            print("Error: GROQ_API_KEY not set.", file=sys.stderr)
            sys.exit(1)
        result = call_openai_compat(
            "https://api.groq.com/openai/v1", api_key, GROQ_DEFAULT, prompt, system
        )
    elif backend == "deepseek-flash":
        api_key = os.environ.get("DEEPSEEK_API_KEY", "")
        if not api_key:
            print("Error: DEEPSEEK_API_KEY not set.", file=sys.stderr)
            sys.exit(1)
        result = call_openai_compat(
            "https://api.deepseek.com", api_key, "deepseek-v4-flash", prompt, system
        )
    else:  # deepseek-pro
        api_key = os.environ.get("DEEPSEEK_API_KEY", "")
        if not api_key:
            print("Error: DEEPSEEK_API_KEY not set.", file=sys.stderr)
            sys.exit(1)
        result = call_openai_compat(
            "https://api.deepseek.com", api_key, "deepseek-v4-pro", prompt, system
        )

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"[worker] result written to {output_file}")
    else:
        print(result)


if __name__ == "__main__":
    main()
