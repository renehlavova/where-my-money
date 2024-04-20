"""Models for tables related to transactions."""

from datetime import datetime
from sqlmodel import Field, SQLModel

from where_my_money.transactions import GenericTransaction

__all__ = ["Category"]


class Category(SQLModel, table=True):
    """Pydantic class for categories."""

    id: int = Field(
        default=None,
        primary_key=True,
    )
    name: str = Field(foreign_key="categorizedtransaction.category_id")
    group: str
    active: bool = True


class CategorizedTransaction(SQLModel, GenericTransaction, table=True):
    """Pydantic class for categorized transaction."""

    id: str = Field(primary_key=True)
    source: str = Field(index=True)
    account_type: str = Field(index=True)
    payment_type: str | None
    payment_instruction: str | None
    payment_category: str | None
    currency: str
    amount: float
    fee: float | None
    balance: float | None
    description: str | None
    counterparty: str | None
    counterparty_account_name: str | None
    payment_date: datetime | None
    started_date: datetime | None
    due_date: datetime | None
    completed_date: datetime | None
    is_completed: bool | None
    category_id: int
