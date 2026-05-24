from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, NUMERIC, String, BOOLEAN
from sqlalchemy.orm import Mapped, column_property, mapped_column

from marshmallow import Schema, fields

from . import ModelBase

from dataclasses import dataclass


# Used to avoid circular imports for FK relationship
if TYPE_CHECKING:
    from .user import User


class Expense(ModelBase):
    __tablename__ = "expense"

    id: Mapped[int] = mapped_column(primary_key=True)
    frequency: Mapped[float] = mapped_column(NUMERIC())     # Frequency of occurrence relative to a month. For example, quarterly is 1/3 the total quarterly cost, applied every month
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(511))
    cost: Mapped[float] = mapped_column(NUMERIC())
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    is_debt: Mapped[bool] = mapped_column(BOOLEAN)
    monthly_cost: Mapped[float] = column_property(cost * frequency)

    def __repr__(self) -> str:
        return f"Expense(id={self.id}, user={self.user_id}, name={self.name}, cost={self.cost}, frequency={self.frequency})"
    

# Dataclasses for use as parameters for endpoints
@dataclass
class ExpenseCreate():
    frequency: float
    name: str
    description: str
    cost: float
    user_id: int
    is_debt: bool


@dataclass
class ExpenseUpdate():
    frequency: float
    name: str
    description: str
    cost: float
    is_debt: bool


# Marshmallow Schema for serialization/deserialization
class ExpenseSchema(Schema):
    frequency = fields.Float()
    name = fields.Str()
    description = fields.Str()
    cost = fields.Float()
    user_id = fields.Int()
    is_debt = fields.Bool()
    monthly_cost = fields.Float()
