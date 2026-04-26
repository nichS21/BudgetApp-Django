from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, NUMERIC, String, BOOLEAN
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import ModelBase

from dataclasses import dataclass


# Used to avoid circular imports for FK relationship
if TYPE_CHECKING:
    from .user import User


class Expense(ModelBase):
    __tablename__ = "expense"

    id: Mapped[int] = mapped_column(primary_key=True)
    frequency: Mapped[float] = mapped_column(NUMERIC())
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(511))
    cost: Mapped[float] = mapped_column(NUMERIC())
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    is_debt: Mapped[bool] = mapped_column(BOOLEAN)


    def __repr__(self) -> str:
        return f"Expense(id={self.id} user={self.user_id}, name={self.name}, cost={self.cost}, frequency={self.frequency})"
    

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