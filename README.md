# Household Chores

A small Django app for managing shared household chores: track chores, rotate them automatically among household members, and keep tabs on what's due and overdue.

Built as Homework 1 for the [AI Dev Tools Zoomcamp](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp) — going from a vague one-line idea to a spec, a backlog, and a working Django app with an AI coding agent.

See [`_docs/plan.md`](_docs/plan.md) for the spec and [`backlog.md`](backlog.md) for the implementation backlog.

## Setup

\`\`\`bash
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
\`\`\`

## Running tests

\`\`\`bash
uv run python manage.py test
\`\`\`
