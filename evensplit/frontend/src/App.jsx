import { useEffect, useState } from "react";
import {
  getMembers,
  addMember,
  getExpenses,
  addExpense,
  deleteExpense,
  getBalances,
} from "./api";
import "./App.css";

function fmt(n) {
  return n.toLocaleString(undefined, { style: "currency", currency: "USD" });
}

export default function App() {
  const [members, setMembers] = useState([]);
  const [expenses, setExpenses] = useState([]);
  const [balances, setBalances] = useState([]);
  const [loading, setLoading] = useState(true);

  const [newMemberName, setNewMemberName] = useState("");
  const [desc, setDesc] = useState("");
  const [amount, setAmount] = useState("");
  const [paidBy, setPaidBy] = useState("");
  const [participants, setParticipants] = useState([]);

  async function refreshAll() {
    const [m, e, b] = await Promise.all([getMembers(), getExpenses(), getBalances()]);
    setMembers(m);
    setExpenses(e);
    setBalances(b);
  }

  useEffect(() => {
    refreshAll().then(() => setLoading(false));
  }, []);

  async function handleAddMember(ev) {
    ev.preventDefault();
    if (!newMemberName.trim()) return;
    await addMember(newMemberName.trim());
    setNewMemberName("");
    await refreshAll();
  }

  function toggleParticipant(id) {
    setParticipants((prev) =>
      prev.includes(id) ? prev.filter((p) => p !== id) : [...prev, id]
    );
  }

  async function handleAddExpense(ev) {
    ev.preventDefault();
    const amt = parseFloat(amount);
    if (!desc.trim() || !amt || !paidBy || participants.length === 0) return;
    await addExpense({
      description: desc.trim(),
      amount: amt,
      paid_by: Number(paidBy),
      participants: participants.map(Number),
    });
    setDesc("");
    setAmount("");
    setPaidBy("");
    setParticipants([]);
    await refreshAll();
  }

  async function handleDelete(id) {
    await deleteExpense(id);
    await refreshAll();
  }

  const memberName = (id) => members.find((m) => m.id === id)?.name ?? "?";

  if (loading) return <div className="app">Loading…</div>;

  return (
    <div className="app">
      <h1>EvenSplit</h1>
      <p className="subtitle">Track shared expenses and see who owes whom.</p>

      <div className="grid">
        <section className="card">
          <h2>Members</h2>
          <ul className="member-list">
            {members.map((m) => (
              <li key={m.id}>{m.name}</li>
            ))}
          </ul>
          <form onSubmit={handleAddMember} className="row">
            <input
              placeholder="Add member name"
              value={newMemberName}
              onChange={(e) => setNewMemberName(e.target.value)}
            />
            <button type="submit">Add</button>
          </form>
        </section>

        <section className="card">
          <h2>Balances</h2>
          <ul className="balance-list">
            {balances.map((b) => (
              <li key={b.member_id} className={b.balance >= 0 ? "positive" : "negative"}>
                <span>{b.name}</span>
                <span>
                  {b.balance >= 0
                    ? `is owed ${fmt(b.balance)}`
                    : `owes ${fmt(-b.balance)}`}
                </span>
              </li>
            ))}
          </ul>
        </section>
      </div>

      <section className="card">
        <h2>Add expense</h2>
        <form onSubmit={handleAddExpense} className="expense-form">
          <input
            placeholder="Description"
            value={desc}
            onChange={(e) => setDesc(e.target.value)}
          />
          <input
            type="number"
            step="0.01"
            placeholder="Amount"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
          />
          <select value={paidBy} onChange={(e) => setPaidBy(e.target.value)}>
            <option value="">Paid by…</option>
            {members.map((m) => (
              <option key={m.id} value={m.id}>
                {m.name}
              </option>
            ))}
          </select>
          <div className="participants">
            <span>Split among:</span>
            {members.map((m) => (
              <label key={m.id}>
                <input
                  type="checkbox"
                  checked={participants.includes(m.id)}
                  onChange={() => toggleParticipant(m.id)}
                />
                {m.name}
              </label>
            ))}
          </div>
          <button type="submit">Add expense</button>
        </form>
      </section>

      <section className="card">
        <h2>Expenses</h2>
        <table>
          <thead>
            <tr>
              <th>Description</th>
              <th>Amount</th>
              <th>Paid by</th>
              <th>Split among</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {expenses.map((e) => (
              <tr key={e.id}>
                <td>{e.description}</td>
                <td>{fmt(e.amount)}</td>
                <td>{memberName(e.paid_by)}</td>
                <td>{e.participants.map(memberName).join(", ")}</td>
                <td>
                  <button onClick={() => handleDelete(e.id)} className="link-button">
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}
