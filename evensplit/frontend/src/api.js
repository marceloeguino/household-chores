// Centralized backend access layer.
// Every UI component talks to the backend ONLY through the functions below.
// For now these are mocked with in-memory data + fake latency; swapping to
// real HTTP calls to the FastAPI backend later only requires editing this file.

const USE_MOCK = false;
const BASE_URL = "http://localhost:8123";

let members = [
  { id: 1, name: "Alex" },
  { id: 2, name: "Sam" },
  { id: 3, name: "Jordan" },
];

let expenses = [
  {
    id: 1,
    description: "Groceries",
    amount: 60,
    paid_by: 1,
    participants: [1, 2, 3],
    created_at: new Date().toISOString(),
  },
];

let nextMemberId = 4;
let nextExpenseId = 2;

function delay(ms = 150) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function computeBalances(members, expenses) {
  const balance = Object.fromEntries(members.map((m) => [m.id, 0]));
  for (const e of expenses) {
    const share = e.amount / e.participants.length;
    balance[e.paid_by] += e.amount;
    for (const pid of e.participants) {
      balance[pid] -= share;
    }
  }
  return members.map((m) => ({
    member_id: m.id,
    name: m.name,
    balance: Math.round(balance[m.id] * 100) / 100,
  }));
}

async function mockRequest(fn) {
  await delay();
  return fn();
}

export async function getMembers() {
  if (USE_MOCK) {
    return mockRequest(() => structuredClone(members));
  }
  const res = await fetch(`${BASE_URL}/members`);
  return res.json();
}

export async function addMember(name) {
  if (USE_MOCK) {
    return mockRequest(() => {
      const m = { id: nextMemberId++, name };
      members.push(m);
      return structuredClone(m);
    });
  }
  const res = await fetch(`${BASE_URL}/members`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });
  return res.json();
}

export async function getExpenses() {
  if (USE_MOCK) {
    return mockRequest(() => structuredClone(expenses));
  }
  const res = await fetch(`${BASE_URL}/expenses`);
  return res.json();
}

export async function addExpense({ description, amount, paid_by, participants }) {
  if (USE_MOCK) {
    return mockRequest(() => {
      const e = {
        id: nextExpenseId++,
        description,
        amount,
        paid_by,
        participants,
        created_at: new Date().toISOString(),
      };
      expenses.push(e);
      return structuredClone(e);
    });
  }
  const res = await fetch(`${BASE_URL}/expenses`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ description, amount, paid_by, participants }),
  });
  return res.json();
}

export async function deleteExpense(id) {
  if (USE_MOCK) {
    return mockRequest(() => {
      expenses = expenses.filter((e) => e.id !== id);
      return { ok: true };
    });
  }
  const res = await fetch(`${BASE_URL}/expenses/${id}`, { method: "DELETE" });
  return { ok: res.ok };
}

export async function getBalances() {
  if (USE_MOCK) {
    return mockRequest(() => computeBalances(members, expenses));
  }
  const res = await fetch(`${BASE_URL}/balances`);
  return res.json();
}
