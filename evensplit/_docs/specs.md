# EvenSplit — Spec

## Idea

An expense splitter: track shared expenses among a group of people and see who owes whom.

## Scope (v1, single session/group)

- One shared group of members (no multi-group, no auth/accounts — matches the homework's time-boxed scope).
- Add a member (name only).
- Add an expense: description, amount, who paid, split equally among selected members.
- View a running list of expenses (description, amount, payer, date).
- View net balances per member (positive = owed money, negative = owes money) computed from all expenses.
- Delete an expense (recalculates balances).

## Out of scope (v1)

- Unequal/custom splits (percentage or exact amount per person) — equal split only.
- Multiple groups / multi-tenancy / user accounts.
- Settling up / payment tracking (marking a debt as paid).
- Notifications.

## Data model

- `Member` — id, name
- `Expense` — id, description, amount, paid_by (Member), participants (Members, equal split), created_at

## Architecture

- `frontend/` — React + Vite SPA. All backend calls centralized in one API module (`src/api.js`), mocked initially with in-memory data, later pointed at the real backend.
- `backend/` — FastAPI (via `uv`). Starts with a mock in-memory store, then swaps to SQLite via SQLAlchemy (kept database-agnostic).
- `openapi.yaml` — contract between frontend and backend, written after the frontend prototype settles on what it needs.

## Name

**EvenSplit** — chosen for clarity: the app's whole job is making sure shared costs come out even.
