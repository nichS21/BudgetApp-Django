from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from marshmallow import Schema, fields

from . import ModelBase

from dataclasses import dataclass


# Used to avoid circular imports for FK relationship
if TYPE_CHECKING:
    from .user import User


class Income(ModelBase):
    __tablename__ = "income"

    id: Mapped[int] = mapped_column(primary_key=True)
    annual_salary: Mapped[int] = mapped_column()
    income_tax: Mapped[float] = mapped_column(Float(5))             # For example: 100.00% 
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    # Create reference to User object through income
    user: Mapped["User"] = relationship(back_populates="income")

    def __repr__(self) -> str:
        return f"Income(id={self.id}, annual salary={self.annual_salary}, income tax={self.income_tax}, user id={self.user_id})"
    

# Pydantic Dataclasses for use as endpoint parameters
@dataclass
class IncomeCreate():
    annual_salary: int
    income_tax: float
    user_id: int

@dataclass
class IncomeUpdate():
    annual_salary: int
    income_tax: float


# Marshmallow Schema for serialization/deserialization
class IncomeSchema(Schema):
    annual_salary = fields.Int()
    income_tax = fields.Float()
    user_id = fields.Int()
