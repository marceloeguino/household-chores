# Household Chores — Spec

## Idea

> A tool for managing shared household chores

## Scope decisions

Brainstormed one question at a time to narrow the vague idea down to a buildable spec:

1. **Household scope** — Single household. One shared list of members and chores; no multi-tenant / multi-family support. Keeps the data model simple (no household/account boundary needed).
2. **Assignment model** — Automatic rotation. Recurring chores cycle through household members automatically so nobody has to remember to reassign them.
3. **Scheduling** — Recurring schedule + due dates. Each chore has a recurrence (e.g. daily/weekly/custom interval) and a concrete due date; overdue chores should be visible.
4. **Gamification** — None. Keep it purely functional: track, assign, and complete chores. No points, streaks, or leaderboards.

## Features (this homework's scope)

1. **Household members** — Maintain a roster of people in the household (name at minimum).
2. **Chores with recurrence + due dates** — Define chores with a title/description, a recurrence rule (one-off or repeating on an interval), and a due date.
3. **Automatic rotation assignment** — When a recurring chore's cycle comes up, the app assigns it to the next person in rotation among household members, without manual reassignment.
4. **Completion tracking** — Mark a chore instance as done; see which chores are upcoming, due, or overdue.

## Out of scope (for this homework)

- Multiple households / multi-tenancy / user accounts per household
- Points, streaks, leaderboards, or any gamification
- Notifications/reminders (email, push, etc.)
- Mobile app / native UI — web only (Django)

## Data model sketch

- `Member` — name
- `Chore` — title, description, recurrence rule, interval
- `ChoreInstance` (or similar) — chore, due date, assigned member, completed (bool), completed_at

This is a starting sketch; the backlog (`backlog.md`) will refine it into concrete Django models and tasks.
