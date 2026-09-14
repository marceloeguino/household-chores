"""In-memory mock store. Swapped for a real database in a later step."""
from datetime import datetime, timezone


class MockStore:
    def __init__(self):
        self._members = {}
        self._expenses = {}
        self._next_member_id = 1
        self._next_expense_id = 1
        self.seed()

    def seed(self):
        for name in ("Alex", "Sam", "Jordan"):
            self.add_member(name)

    def list_members(self):
        return list(self._members.values())

    def add_member(self, name: str):
        member = {"id": self._next_member_id, "name": name}
        self._members[member["id"]] = member
        self._next_member_id += 1
        return member

    def member_exists(self, member_id: int) -> bool:
        return member_id in self._members

    def list_expenses(self):
        return list(self._expenses.values())

    def add_expense(self, description, amount, paid_by, participants):
        expense = {
            "id": self._next_expense_id,
            "description": description,
            "amount": amount,
            "paid_by": paid_by,
            "participants": participants,
            "created_at": datetime.now(timezone.utc),
        }
        self._expenses[expense["id"]] = expense
        self._next_expense_id += 1
        return expense

    def delete_expense(self, expense_id: int) -> bool:
        return self._expenses.pop(expense_id, None) is not None

    def balances(self):
        balance = {m: 0.0 for m in self._members}
        for e in self._expenses.values():
            share = e["amount"] / len(e["participants"])
            balance[e["paid_by"]] += e["amount"]
            for pid in e["participants"]:
                balance[pid] -= share
        return [
            {"member_id": mid, "name": self._members[mid]["name"], "balance": round(bal, 2)}
            for mid, bal in balance.items()
        ]


store = MockStore()
