# Delegation Prompt Examples

Each example below is a complete, ready-to-use delegation prompt. Copy any of them, swap in your actual code or content, and send it directly to a worker model. The four-part structure (CONTEXT / TASK / CONSTRAINTS / SUCCESS) is already filled in.

---

### 1. Write a new Python module following an existing pattern

**When to use:** Adding a new endpoint, model, or plugin that mirrors existing modules in your codebase.

```
CONTEXT: We have a FastAPI app with service-layer modules under `app/services/`. Each service
follows the same pattern: a Pydantic model for input, a `run()` method that returns a dict,
and a `handle_errors` decorator. Existing example: `app/services/user_lookup.py`.
Database is PostgreSQL via SQLAlchemy 2.0 async sessions.

TASK: Write `app/services/order_summary.py` that accepts order_id: str and customer_id: str,
fetches the order with its line items from the DB, and returns:
{"order_id", "total_items", "total_amount", "status", "created_at"}.
Follow the exact structure and error-handling pattern as user_lookup.py.

CONSTRAINTS:
- Use @handle_errors from app/decorators.py
- Signature: async def run(order_id: str, customer_id: str) -> dict
- Raise OrderNotFoundError (app/exceptions.py) if no rows found
- Type-hint everything; keep under 80 lines

SUCCESS: I can import it and call `await order_summary.run("ord-123", "cust-456")` immediately.
```

---

### 2. Generate a pytest test suite for an existing function

**When to use:** You've written a function and need comprehensive tests fast.

```
CONTEXT: Pure Python function in app/pricing.py. Calculates discounted price given a base price,
discount code string, and optional user tier. Codes: SAVE10=10% off, SAVE20=20% off.
Tiers: "gold"=extra 5%, "platinum"=extra 10%. Returns float rounded to 2dp.
Raises ValueError for unknown codes, TypeError if price is not a number.

TASK: Write a complete pytest test suite at tests/test_pricing.py covering: valid codes,
unknown code, each tier, tier + code stacking, zero price, negative price (raises),
non-numeric price (raises), no code/tier. Use @pytest.mark.parametrize where it reduces repetition.

CONSTRAINTS:
- pytest 7+ conventions; no unittest.TestCase
- Each test name describes the scenario (e.g., test_save20_with_platinum_returns_correct_price)
- Mock nothing — function is pure

SUCCESS: `pytest tests/test_pricing.py -v` passes all tests, 100% coverage on app/pricing.py.
```

---

### 3. Refactor a function to reduce complexity

**When to use:** A function has grown unwieldy and needs splitting into testable helpers.

```
CONTEXT: Function generate_report() in app/reports.py has cyclomatic complexity of 14.
Mixed concerns: filtering, formatting, writing. We want the same output, just cleaner.

BEFORE (excerpt):
def generate_report(transactions, start_date, end_date, fmt="csv"):
    rows = []
    for t in transactions:
        if t["date"] >= start_date and t["date"] <= end_date:
            if t["status"] in ("complete", "refunded"):
                row = []
                row.append(t["id"])
                if t["status"] == "complete":
                    row.append("+" + str(t["amount"]))
                else:
                    row.append("-" + str(t["amount"]))
                row.append(t["date"].strftime("%Y-%m-%d"))
                if fmt == "csv":
                    rows.append(",".join(row))
                elif fmt == "tsv":
                    rows.append("\t".join(row))
    return "\n".join(rows)

TASK: Refactor into app/reports.py by extracting at least three helpers
(_filter_transactions, _format_row, _build_output). Keep generate_report as public entry point.
Identical output for all inputs.

CONSTRAINTS:
- Each helper must be a pure function
- Max 15 lines per function
- Use a dict for format delimiters instead of if/elif
- Keep original argument order and defaults

SUCCESS: flake8 McCabe complexity ≤ 6 per function; existing tests/test_reports.py still pass.
```

---

### 4. Write a PR description from a git diff summary

**When to use:** Finished a feature branch and need a structured PR description quickly.

```
CONTEXT: Branch feat/add-bulk-export vs main. Changes:
- app/exporters/bulk_csv.py (new, 120 lines): exports up to 50k rows in chunks via csv.DictWriter
- app/exporters/__init__.py (+3): registers bulk_csv
- app/api/export_routes.py (+45): new POST /api/v1/export/bulk accepting {"query": {...}, "format": "csv"}
- tests/test_bulk_csv.py (new, 95 lines): chunking, empty results, column ordering
- config/defaults.py (+2): BULK_EXPORT_CHUNK_SIZE = 5000
- migrations/014_add_export_jobs_table.sql (new): creates export_jobs table

TASK: Write a PR description with: 1-sentence summary, ## What changed bullet list,
## How to test (3 specific curl steps), ## Notes for reviewers (2-3 design callouts).

CONSTRAINTS:
- Summary under 80 characters
- Test steps use real endpoint path and realistic JSON payloads
- Notes mention chunking behaviour and migration's IF NOT EXISTS

SUCCESS: A colleague can understand scope, test locally, and know what to scrutinise.
```

---

### 5. Translate a batch of UI strings to another language

**When to use:** Small batch of user-facing strings needing accurate translation.

```
CONTEXT: UI strings from a SaaS dashboard — button labels, modals, empty states.
Audience: Spanish-speaking users in Mexico. Use "tú" (not "usted"). Keep placeholders
like {count} exactly as-is — do not translate them.

TASK: Translate these 5 strings to Mexican Spanish:
1. "Save changes"
2. "Are you sure you want to delete this project? This action cannot be undone."
3. "You have {count} unread notification(s)"
4. "No results found. Try adjusting your filters."
5. "Last updated 2 minutes ago"

CONSTRAINTS:
- Return a JSON object: English string as key, Spanish translation as value
- Do not modify {count}
- No explanatory text — just the JSON

SUCCESS: I can paste the JSON directly into locales/es-MX.json and the UI renders correctly.
```

---

### 6. Analyse an error log and suggest root causes

**When to use:** Debugging a production incident and want structured analysis of log evidence.

```
CONTEXT: Node.js Express API + NGINX + PostgreSQL 14. At 03:47 UTC, elevated 502s for 6 minutes.
No deploys in preceding 2 hours. Traffic normal (~200 req/s). PostgreSQL server confirmed healthy.

LOG SNIPPET:
[03:47:02] ERROR - POST /api/orders - ECONNREFUSED 127.0.0.1:5432
[03:47:02] WARN  - db pool exhausted (active=20, idle=0, waiting=14)
[03:47:05] ERROR - GET /api/products/:id - query timeout after 30000ms
[03:47:08] WARN  - db pool exhausted (active=20, idle=0, waiting=31)
[03:47:30] INFO  - db pool recovered (active=3, idle=17, waiting=0)

TASK: Provide: (a) most likely root cause (1 sentence), (b) 2-3 alternatives ranked by likelihood
with supporting evidence, (c) 3 concrete remediation steps.

CONSTRAINTS:
- Base conclusions only on what's visible in the log
- Format as markdown for an incident postmortem document
- No speculation about application code bugs — focus on infrastructure/connection management

SUCCESS: On-call engineer has clear next steps to investigate and prevent recurrence.
```
