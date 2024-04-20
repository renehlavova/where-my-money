from sqlmodel import Session
from where_my_money.models import CategorizedTransaction


class LocalWriter:
    """Class to write categorized transaction to local database."""

    def __init__(self, database_engine):
        self.database_engine = database_engine
        self._session: Session | None = None

    def __enter__(self):
        self._session = Session(self.database_engine)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._session is None:
            return
        self._session.commit()
        self._session.close()
        self._session = None

    def write_transaction(self, categorized_transaction: CategorizedTransaction):
        """Write a categorized transaction to database."""
        if self._session is None:
            raise RuntimeError("Sesssion is not open, use with statement.")
        self._session.add(categorized_transaction)
