# Invoice Checker

Checks vendor invoices against purchase orders before a company pays them.
It extracts invoice data from PDFs, runs rule-based checks (math, PO match,
duplicates, bank details), decides whether to approve, hold, or block, and
drafts emails for a person to approve. Portfolio project, built in Python.

## Tools and commands

- Package manager: uv. Never use pip directly.
- Run code: `uv run <file or command>`
- Add a package: `uv add <package>`
- Run tests: `uv run pytest` (once pytest is added)
- Source code lives in `src/invoice_checker/`

## Code rules

- Money is always `Decimal`, never `float`.
- Dates are `datetime.date`.
- Data shapes live in `models.py` as Pydantic models.
- Follow PEP 8. Type hints on all functions.
- Keep functions small and readable. This code must be easy to explain.

## Design decisions

- The LLM only reads invoices, matches differently-worded items, and writes
  emails. Code makes every decision that involves money.
- It is a fixed workflow, not an agent.
- Models only validate single fields. Cross-field checks (line totals, PO
  matching, overbilling) go in a separate checks module, because the system
  must flag bad invoices, not crash on them.
- Negative amounts are allowed on purpose, for credit notes.
- `Field(description=...)` is only used on fields the LLM fills in. Those
  descriptions are instructions to the LLM.
- Bank details: only the last 4 digits are stored. Never update vendor
  records from an invoice.
- Emails go only to addresses saved in vendor records, and only after a
  person approves them.
- Invoice versions are kept, never overwritten or deleted.

## How to work with me

- I am learning. I write the core logic myself: models, checks, decision
  rules, and LLM steps. Do not write those unless I ask.
- You can help with: setup, scaffolding, tests, Docker, deployment, and
  explaining code or errors.
- Before changing files, explain what you will change and why.
- Explain new concepts in plain English.
- Do not commit or push. I do that myself.
