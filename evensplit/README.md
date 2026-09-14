# EvenSplit

A small full-stack expense splitter: add shared expenses among a group of people, see who owes whom.

Built as Homework 2 for the [AI Dev Tools Zoomcamp](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp) — spec, frontend prototype (mocked backend), FastAPI backend, then a real database, all with an AI coding agent.

See [`_docs/specs.md`](_docs/specs.md) for the spec.

## Frontend

```bash
cd frontend
npm install
npm run dev
```

## Backend

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

## Tests

```bash
cd backend
uv run pytest
```
