from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import ExpenseDB, ExpenseParticipant, MemberDB


def list_members(db: Session):
    return [{"id": m.id, "name": m.name} for m in db.scalars(select(MemberDB)).all()]


def add_member(db: Session, name: str):
    member = MemberDB(name=name)
    db.add(member)
    db.commit()
    db.refresh(member)
    return {"id": member.id, "name": member.name}


def member_exists(db: Session, member_id: int) -> bool:
    return db.get(MemberDB, member_id) is not None


def _expense_to_dict(e: ExpenseDB):
    return {
        "id": e.id,
        "description": e.description,
        "amount": e.amount,
        "paid_by": e.paid_by,
        "participants": [p.member_id for p in e.participants],
        "created_at": e.created_at,
    }


def list_expenses(db: Session):
    return [_expense_to_dict(e) for e in db.scalars(select(ExpenseDB)).all()]


def add_expense(db: Session, description: str, amount: float, paid_by: int, participants: list[int]):
    expense = ExpenseDB(description=description, amount=amount, paid_by=paid_by)
    db.add(expense)
    db.flush()
    for pid in participants:
        db.add(ExpenseParticipant(expense_id=expense.id, member_id=pid))
    db.commit()
    db.refresh(expense)
    return _expense_to_dict(expense)


def delete_expense(db: Session, expense_id: int) -> bool:
    expense = db.get(ExpenseDB, expense_id)
    if expense is None:
        return False
    db.delete(expense)
    db.commit()
    return True


def balances(db: Session):
    members = list_members(db)
    balance = {m["id"]: 0.0 for m in members}
    for e in list_expenses(db):
        share = e["amount"] / len(e["participants"])
        balance[e["paid_by"]] += e["amount"]
        for pid in e["participants"]:
            balance[pid] -= share
    return [
        {"member_id": m["id"], "name": m["name"], "balance": round(balance[m["id"]], 2)}
        for m in members
    ]
