# Agent instructions for EvenSplit

This is the `evensplit/` subproject inside the `household-chores` repo (Homework 2 of the AI Dev Tools Zoomcamp — unrelated to the household-chores app in the repo root).

- Spec lives in `_docs/specs.md` — read it before making product decisions.
- `frontend/` is a React + Vite SPA. All backend calls are centralized in `frontend/src/api.js` — never call `fetch`/`axios` directly from components.
- `backend/` is a FastAPI app managed with `uv`. Keep it database-agnostic: use SQLAlchemy, not raw SQLite-specific code.
- Write tests before/alongside implementing backend endpoints (`backend/tests/`). Run them with `uv run pytest` from `backend/`.
- Keep scope to what's in `_docs/specs.md`. Equal-split expenses only — no custom split ratios, no multi-group support, no auth.
