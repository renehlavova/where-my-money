"""CSV loader class"""

import csv
from typing import Iterable, Type, TypeVar

from where_my_money.transactions import BaseTransaction

TransactionModel = TypeVar("TransactionModel", bound=BaseTransaction)


class CSVLoader:
    """CSV loader"""

    @staticmethod
    def load(source: str, model: Type[TransactionModel]) -> Iterable[TransactionModel]:
        """Load csv with transaction data"""

        with open(source, "r", encoding=model.__file_encoding__) as file:
            reader = csv.DictReader(file, delimiter=model.__delimiter__)

            for line in reader:
                if "sporici" in source:
                    line["account_type"] = "savings"
                else:
                    line["account_type"] = "basic"

                yield model.from_dict(line)  # type: ignore
