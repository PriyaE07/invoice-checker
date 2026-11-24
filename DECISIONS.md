# Design Decisions

A record of the key technical decisions in this project, the alternatives
considered, and the reasoning behind each.

**Guiding principle:** use an LLM only where judgment is needed. Everything
involving money is deterministic code, and a person approves anything that
moves money or leaves the system.

---

## 1. Problem choice: accounts payable invoice checking

Small businesses such as clinics reorder supplies weekly, and checking each
invoice against its purchase order is slow, manual work. This system reduces
it to a short review. Chosen over a CRM data onboarding tool and a personal
finance app because it has a clear user, a well-defined workflow, and a
direct cost of errors (overpayment and fraud).

## 2. The LLM extracts and drafts; code decides

The LLM has three narrow jobs: extracting fields from invoice PDFs, matching
differently worded line items, and drafting emails. Every approve, hold, or
block decision is rule-based code.

LLM outputs are probabilistic, while payment decisions must be exact and
auditable. This split also neutralizes prompt injection: the LLM can only
return structured fields, so text hidden in a PDF cannot approve an invoice.

## 3. Fixed workflow over an autonomous agent

Every invoice follows the same pipeline: extract, match to a PO, run checks,
decide, draft, approve. No step requires the model to choose what happens
next, so a fixed workflow is deterministic, easier to test, and uses
significantly fewer tokens. An agent is better suited to open-ended analysis
such as "which vendors raised prices this quarter?", where the steps depend
on the question; that is a planned extension.

## 4. Synthetic data with an answer key, validated on real invoices

Real invoices, purchase orders, and vendor records are confidential, so no
public dataset contains all three together. A seeded generator produces
vendors, POs, and invoices with deliberately injected errors and a known
correct answer for each, which makes accuracy measurable. A small set of
hand-labeled real invoices tests performance on layouts the system was
never built around.

## 5. Exact decimal arithmetic for money

All amounts use `Decimal`, constructed from strings. Binary floats store most
decimal values approximately, which would cause correct invoices to fail
total checks by fractions of a cent. Constructing from strings avoids
inheriting float error at creation.

## 6. Validation layers: data shape vs. business rules

Pydantic models validate shape only: types, required fields, value ranges.
Business rules (line totals, PO matching, overbilling) live in a separate
checks module. An invoice with incorrect math must still load so it can be
flagged, explained, and acted on; rejecting it at the model layer would
silently drop the exact cases the system exists to catch.

## 7. Field descriptions as LLM instructions

`Field(description=...)` is used only on fields the LLM extracts, where it
acts as an extraction instruction (for example, distinguishing the invoice
number from the PO or account number). Internal records such as purchase
orders and vendors are created by code, so no description is needed there.

## 8. Minimal storage of bank details

Vendor records store only the last four digits of a bank account, enough to
detect a change while limiting exposure if data leaks. Bank details on an
invoice never update the vendor record: changed details are flagged as a
potential fraud signal and verified by phone using the contact on file,
mirroring standard accounts payable controls.

## 9. Reproducible test data

All randomness in the generator runs through a single seeded Faker instance,
so every run produces identical data. Changes in evaluation results can then
be attributed to code changes rather than data changes.

## 10. Sample data in version control, generated data excluded

A small sample dataset is committed so the data format is visible without
running anything. Full generated output, including PDFs, is excluded from
Git because it is large and fully reproducible from the seed.
