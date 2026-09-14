from datetime import datetime

from pydantic import BaseModel, Field


class MemberCreate(BaseModel):
    name: str


class Member(BaseModel):
    id: int
    name: str


class ExpenseCreate(BaseModel):
    description: str
    amount: float = Field(gt=0)
    paid_by: int
    participants: list[int] = Field(min_length=1)


class Expense(BaseModel):
    id: int
    description: str
    amount: float
    paid_by: int
    participants: list[int]
    created_at: datetime


class Balance(BaseModel):
    member_id: int
    name: str
    balance: float
