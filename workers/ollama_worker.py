#!/usr/bin/env python3
"""Call local Ollama API with a prompt and print the response."""
import json, os, sys, urllib.request

try:
    prompt = sys.argv[1]
    model = os.environ.get("OLLAMA_MODEL", "llama3.2")

    data = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False
    }).encode()

    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=data,
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(req) as resp:
        body = json.loads(resp.read())
    print(body["response"])
except urllib.error.URLError:
    print("Error: Ollama not running. Start it with: ollama serve", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
