#!/usr/bin/env python3
"""Call Groq API with a prompt and print the response."""
import json, os, sys, urllib.request

try:
    prompt = sys.argv[1]
    api_key = os.environ["GROQ_API_KEY"]

    data = json.dumps({
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}]
    }).encode()

    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    )

    with urllib.request.urlopen(req) as resp:
        body = json.loads(resp.read())
    print(body["choices"][0]["message"]["content"])
except KeyError:
    print("Error: GROQ_API_KEY environment variable not set.", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
