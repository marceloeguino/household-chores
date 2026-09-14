from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud
from .db import Base, engine, get_db
from .schemas import Balance, Expense, ExpenseCreate, Member, MemberCreate

Base.metadata.create_all(bind=engine)

app = FastAPI(title="EvenSplit API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def seed_if_empty():
    db = next(get_db())
    try:
        if not crud.list_members(db):
            for name in ("Alex", "Sam", "Jordan"):
                crud.add_member(db, name)
    finally:
        db.close()


@app.get("/members", response_model=list[Member])
def list_members(db: Session = Depends(get_db)):
    return crud.list_members(db)


@app.post("/members", response_model=Member, status_code=201)
def create_member(payload: MemberCreate, db: Session = Depends(get_db)):
    return crud.add_member(db, payload.name)


@app.get("/expenses", response_model=list[Expense])
def list_expenses(db: Session = Depends(get_db)):
    return crud.list_expenses(db)


@app.post("/expenses", response_model=Expense, status_code=201)
def create_expense(payload: ExpenseCreate, db: Session = Depends(get_db)):
    if not crud.member_exists(db, payload.paid_by):
        raise HTTPException(status_code=422, detail="paid_by is not a known member")
    for pid in payload.participants:
        if not crud.member_exists(db, pid):
            raise HTTPException(status_code=422, detail=f"participant {pid} is not a known member")
    return crud.add_expense(
        db, payload.description, payload.amount, payload.paid_by, payload.participants
    )


@app.delete("/expenses/{expense_id}", status_code=204)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    if not crud.delete_expense(db, expense_id):
        raise HTTPException(status_code=404, detail="expense not found")


@app.get("/balances", response_model=list[Balance])
def get_balances(db: Session = Depends(get_db)):
    return crud.balances(db)
