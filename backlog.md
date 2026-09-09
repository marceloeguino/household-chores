# Household Chores — Backlog

Derived from `_docs/plan.md`. Tasks are ordered so each one is small, buildable, and testable on its own.

## 1. Members: data model + admin

Create a `Member` model (name, and any minimal identifying fields) in the `chores` app. Register it in Django admin so household members can be added/edited without a custom UI yet. Write and run the migration.

## 2. Chores: data model (recurrence + rotation order)

Create a `Chore` model: title, description, recurrence rule (e.g. `NONE` / `DAILY` / `WEEKLY` / `CUSTOM` with an interval), and whatever's needed to track rotation order among members (e.g. a `ManyToMany`/`M2M through` to `Member`, plus a pointer to "next up"). Register in admin. Migration.

## 3. ChoreInstance: due dates + completion

Create a `ChoreInstance` model: FK to `Chore`, `due_date`, FK to assigned `Member`, `completed` (bool), `completed_at`. This is the concrete, dated occurrence of a chore. Register in admin. Migration.

## 4. Rotation assignment logic

Implement the logic that, given a `Chore`'s recurrence, generates the next `ChoreInstance` and assigns it to the next `Member` in rotation (cycling back to the start after the last member). Cover with unit tests: rotation wraps correctly, skips nobody, handles a single-member household.

## 5. Chore list view (home page)

Build a view + template listing all upcoming `ChoreInstance`s: chore title, assignee, due date, and status (upcoming / due today / overdue). Basic URL routing in `config/urls.py` and `chores/urls.py`.

## 6. Mark chore complete

Add an action (button/form/endpoint) to mark a `ChoreInstance` as completed, setting `completed_at`. Reflect the change in the list view immediately.

## 7. Overdue highlighting

In the list view, visually distinguish overdue chores (due date in the past and not completed) from upcoming ones.

## 8. Add/edit chores and members via the app (not just admin)

Basic forms to create a `Member` and create a `Chore` (with its recurrence) from the app's own UI, not just Django admin.

## 9. Test coverage

Add tests for: model creation/validation, rotation logic (already covered in #4 but expand edge cases), view responses (list page renders, mark-complete updates state), and overdue detection logic.

## 10. Polish: basic styling + README/usage docs

Light CSS for readability, and update `README.md` with a short "how to use" section once the app is functional end-to-end.
