---
name: boss-mode
description: Use when planning features, writing code, or running superpowers workflows where heavy token usage is expected. Triggers AI worker delegation — Claude orchestrates, cheaper models execute, Claude verifies.
license: MIT
---

# Boss Mode — AI Worker Orchestration

Claude acts as **orchestrator (boss)**: plans, delegates, reviews, verifies.  
Cheaper models act as **workers**: execute code drafts, content, analysis.  
Claude never writes large code blocks itself when a worker can do it first.

## Three-Tier Model

| Tier | Role | When to use |
|------|------|-------------|
| **Claude** | Boss — orchestrate, decide, verify, file ops | Final decisions, architecture, running tests, talking to user |
| **DeepSeek** | Senior worker — code drafts, reasoning, analysis | Anything needing judgment but not file access |
| **Groq / Ollama** | Bulk worker — repetitive execution | Translation, formatting, high-volume tasks |

## When This Skill Applies

- Starting a superpowers planning/execution workflow
- About to write >30 lines of code yourself
- Running brainstorm → plan → implement cycles
- Writing test suites, documentation, PR descriptions (>200 words)
- Debug reasoning: analysing logs or tracing root cause
- Any task where Claude would spend tokens drafting content a worker could draft instead

## The Boss Loop

```
1. PLAN (Claude)
   Apply karpathy-guidelines: state assumptions, define success criteria
   Apply superpowers:writing-plans: break into phases

2. DELEGATE (Claude → Worker)
   Write a precise task prompt (see Delegation Protocol below)
   Call worker tool → get draft back

3. REVIEW (Claude)
   Read worker output critically
   Accept / request targeted fix (never rewrite yourself)

4. VERIFY (Claude)
   Run tests / execute code
   If fail → write fix instruction → delegate again → repeat
   Claude only writes code directly as last resort
```

## Delegation Protocol

Write worker prompts with these four elements:

```
CONTEXT: [what system/codebase/goal — include all relevant snippets, workers have no file access]
TASK: [exactly what to produce — be specific, one deliverable per call]
CONSTRAINTS: [style rules, existing patterns, what NOT to change]
SUCCESS: [how to know the output is correct — a test command, a checklist]
```

**Example:**
```
CONTEXT: Python project, SQLite + akshare, existing income.py fetches income statements
TASK: Write balance.py that fetches balance sheet via akshare.stock_balance_sheet_by_report_em(),
      saves to SQLite table 'balance_sheet', same structure as income.py
CONSTRAINTS: Follow income.py exactly — same error handling, same column naming convention
SUCCESS: pytest tests/test_balance.py passes, table created with correct schema
```

## Calling Workers

Configure these to match your own worker scripts or MCP tools:

**DeepSeek (preferred for reasoning + code):**
```bash
python /path/to/your/deepseek_worker.py "[delegation prompt]"
```

**Groq (bulk / translation):**
```bash
python /path/to/your/groq_worker.py "[delegation prompt]"
```

**Ollama (local, free tier):**
```bash
ollama run llama3.2 "[delegation prompt]"
```

> Workers don't have file access. Always include all necessary context inline in the prompt.

## Fix Loop (when tests fail)

```
Test fails
→ Write ONE targeted fix instruction (don't diagnose everything at once)
→ Delegate fix to same worker
→ Re-run test
→ Repeat max 3 rounds
→ After 3 rounds: Claude writes the fix directly, documents why worker failed
```

## Integration with Superpowers

| Superpowers skill | Boss Mode role |
|-------------------|----------------|
| `writing-plans` | Claude writes the plan (no delegation needed) |
| `executing-plans` | Each coding task → delegate to worker, Claude reviews |
| `brainstorming` | Claude brainstorms, DeepSeek handles deep-analysis sub-tasks |
| `verification-before-completion` | Always Claude — never delegate final verification |
| `systematic-debugging` | Claude diagnoses root cause, delegates fix writing |

## Karpathy Rules Applied to Delegation

- **State assumptions** in the delegation prompt — workers can't ask clarifying questions
- **Minimum viable task** — one clear deliverable per call, not "do everything"
- **Surgical** — tell worker exactly what file/function to write, not "refactor the project"
- **Verifiable** — always end the delegation prompt with a success criterion Claude can test

## What Claude Never Delegates

- Reading/writing files
- Running tests or shell commands
- Final architecture decisions
- Direct responses to the user
- Security-sensitive operations

## Quick Self-Check Before Writing Code

> "Could I write a 3-sentence delegation prompt for this and let a worker draft it?"  
> If yes → delegate first, review second.  
> If no (too intertwined with files/context) → write it yourself.
