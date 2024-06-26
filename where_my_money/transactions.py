"""Classes for transaction mapping"""

# pylint: disable=too-few-public-methods

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field
from unidecode import unidecode


def clean_dict(dct: dict) -> dict:
    """Clean dict from empty strings"""

    for key, value in dct.items():
        if value == "":
            dct[key] = None

    return dct


class BaseTransaction:
    """Parent transaction"""

    source: str
    __file_encoding__: str = "utf-8"
    __delimiter__: str = ","

    @staticmethod
    def from_dict(dct: dict) -> "BaseTransaction":
        """Base from dict method"""
        raise NotImplementedError


class GenericTransaction(BaseModel):
    """Mapping for all transactions"""

    id: str
    ### dimensions
    source: str
    account_type: str
    payment_type: str | None
    payment_instruction: str | None
    payment_category: str | None
    ### amount
    currency: str
    amount: float
    fee: float | None
    balance: float | None
    ### descriptions
    description: str | None
    ### counterparty
    counterparty: str | None
    counterparty_account_name: str | None
    ### dates
    payment_date: datetime | None
    started_date: datetime | None
    due_date: datetime | None
    completed_date: datetime | None
    ### bool
    is_completed: bool | None  # state + is_completed


class RevolutTransaction(BaseModel, BaseTransaction):
    """Mapping for Revolut transactions"""

    class Config:
        """Config for Revolut transactions"""

        allow_population_by_alias = True
        anystr_strip_whitespace = True

    __file_encoding__: str = "utf-8"
    __delimiter__: str = ","
    id: str
    source: str = "revolut"
    account_type: str = "basic"
    payment_type: str = Field(alias="Type")
    started_date: datetime = Field(alias="Started Date")
    completed_date: datetime = Field(alias="Completed Date")
    description: str | None = Field(alias="Description")
    amount: float = Field(alias="Amount")
    fee: float = Field(alias="Fee")
    currency: str = Field(alias="Currency")
    state: str = Field(alias="State")
    balance: float | None = Field(alias="Balance")

    def to_generic_transaction(self) -> "GenericTransaction":
        """Mapping to generic transaction"""

        return GenericTransaction(
            id=self.payment_type.lower() + str(self.started_date) + str(self.amount),
            source=self.source,
            account_type=self.account_type,
            payment_type=self.payment_type.lower(),
            payment_instruction=None,
            payment_category=None,
            currency=self.currency,
            amount=self.amount,
            fee=self.fee,
            balance=self.balance,
            description=unidecode(self.description.lower()) if self.description else None,
            counterparty=None,
            counterparty_account_name=None,
            payment_date=None,
            started_date=self.started_date,
            due_date=None,
            completed_date=self.completed_date,
            is_completed=self.state == "COMPLETED",
        )

    @staticmethod
    def from_dict(dct: dict) -> "RevolutTransaction":
        """Mapping from dict"""

        return RevolutTransaction(**clean_dict(dct))


class AirbankTransaction(BaseModel, BaseTransaction):
    """Mapping for Airbank transactions"""

    class Config:
        """Config for Airbank transactions"""

        allow_population_by_alias = True
        anystr_strip_whitespace = True

    __file_encoding__: str = "cp1250"
    __delimiter__: str = ";"
    id: str = Field(alias="Referenční číslo")
    source: str = "airbank"
    account_type: Literal["basic"] | Literal["savings"]
    payment_date: str = Field(alias="Datum provedení")
    payment_instruction: str = Field(alias="Směr úhrady")
    payment_type: str = Field(alias="Typ úhrady")
    payment_category: str = Field(alias="Kategorie plateb")
    currency: str = Field(alias="Měna účtu")
    amount: str = Field(alias="Částka v měně účtu")
    fee: str | None = Field(alias="Poplatek v měně účtu")
    counterparty: str | None = Field(alias="Název protistrany")
    counterparty_account_name: str | None = Field(alias="Název účtu protistrany")
    message_for_recipient: str | None = Field(alias="Zpráva pro příjemce")
    description: str | None = Field(alias="Poznámka k úhradě")
    business: str | None = Field(alias="Obchodní místo")
    started_date: str | None = Field(alias="Datum a čas zadání")
    due_date: str | None = Field(alias="Datum splatnosti")
    completed_date: str | None = Field(alias="Datum zaúčtování")
    is_completed: str = Field(alias="Zaúčtováno")

    def to_generic_transaction(self) -> "GenericTransaction":
        """Mapping to generic transaction"""

        return GenericTransaction(
            id=self.id,
            source=self.source,
            account_type=self.account_type,
            payment_type=unidecode(self.payment_type.lower()),
            payment_instruction=unidecode(self.payment_instruction.lower()),
            payment_category=unidecode(self.payment_category.lower()),
            currency=self.currency,
            amount=float(self.amount.replace(",", ".")),
            fee=float(self.fee.replace(",", "")) if self.fee is not None else None,
            balance=None,
            description=unidecode(self.description.lower())
            if self.description
            else (unidecode(self.message_for_recipient.lower()) if self.message_for_recipient else None),
            counterparty=unidecode(self.counterparty.lower())
            if self.counterparty
            else (unidecode(self.business.lower()) if self.business else None),
            counterparty_account_name=unidecode(self.counterparty_account_name.lower())
            if self.counterparty_account_name
            else None,
            payment_date=datetime.strptime(self.payment_date, "%d/%m/%Y") if self.payment_date else None,
            started_date=datetime.strptime(self.started_date, "%d/%m/%Y %H:%M:%S") if self.started_date else None,
            due_date=datetime.strptime(self.due_date, "%d/%m/%Y") if self.due_date else None,
            completed_date=datetime.strptime(self.completed_date, "%d/%m/%Y") if self.completed_date else None,
            is_completed=self.is_completed == "Ano",
        )

    @staticmethod
    def from_dict(dct: dict) -> "AirbankTransaction":
        """Mapping from dict"""

        kwargs = {str(key): value for key, value in clean_dict(dct).items()}

        return AirbankTransaction(**kwargs)


class RaiffeisenTransaction(BaseModel, BaseTransaction):
    """Mapping for Raiffeisen transactions"""

    __file_encoding__: str = "cp1250"
    __delimiter__: str = ";"
    id: str = Field(alias="Id transakce")
    source: str = "raiffeisen"
    account_type: Literal["basic"] | Literal["savings"]
    payment_date: str = Field(alias="Datum provedení")
    completed_date: str | None = Field(alias="Datum zaúčtování")
    payment_category: str = Field(alias="Kategorie transakce")
    counterparty_account_name: str | None = Field(alias="Název protiúčtu")
    payment_type: str | None = Field(alias="Typ transakce")
    message_for_recipient: str | None = Field(alias="Zpráva")
    description: str | None = Field(alias="Poznámka")
    amount: str = Field(alias="Zaúčtovaná částka")
    currency: str = Field(alias="Měna účtu")
    fee: str | None = Field(alias="Poplatek")
    counterparty: str | None = Field(alias="Název obchodníka")

    def to_generic_transaction(self) -> "GenericTransaction":
        """Mapping to generic transaction"""

        return GenericTransaction(
            id=self.id,
            source=self.source,
            account_type=self.account_type,
            payment_type=unidecode(self.payment_type.lower()) if self.payment_type else None,
            payment_instruction=None,
            payment_category=None,
            currency=self.currency,
            amount=float(self.amount.replace(",", ".").replace(" ", "")),
            fee=float(self.fee.replace(",", ".")) if self.fee is not None else None,
            balance=None,
            description=unidecode(self.description.lower())
            if self.description
            else (unidecode(self.message_for_recipient.lower()) if self.message_for_recipient else None),
            counterparty=unidecode(self.counterparty.lower()) if self.counterparty else None,
            counterparty_account_name=unidecode(self.counterparty_account_name.lower())
            if self.counterparty_account_name
            else None,
            payment_date=datetime.strptime(self.payment_date, "%d.%m.%Y"),
            started_date=None,
            due_date=None,
            completed_date=datetime.strptime(self.completed_date, "%d.%m.%Y %H:%M") if self.completed_date else None,
            is_completed=bool(self.completed_date),
        )

    @staticmethod
    def from_dict(dct: dict) -> "RaiffeisenTransaction":
        """Convert dict to RaiffeisenTransaction"""

        return RaiffeisenTransaction(**clean_dict(dct))
