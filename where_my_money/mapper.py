"""Category general class for Where My Money app."""

import logging
import re

from sqlmodel import Session, select
import yaml
from where_my_money.models import CategorizedTransaction, Category

from where_my_money.transactions import GenericTransaction

logger = logging.getLogger(__name__)

DEFAULT_CATEGORY = "Nezařazený výdaj"


class CategoryMapper:
    """Pydantic class to categorize every transaction and return a category."""

    def __init__(self, mapping_file: str, database_engine):
        self.mapping_file = mapping_file
        self.database_engine = database_engine
        self.mapping = self.load_mapping_from_yaml(mapping_file)

    @staticmethod
    def load_mapping_from_yaml(mapping_file: str) -> list[dict]:
        """Load mapping from YAML file."""
        try:
            with open(mapping_file, "r", encoding="utf-8") as file:
                mapping = yaml.safe_load(file)
        except FileNotFoundError:
            logger.error("Mapping file %s not found.", mapping_file)
            raise
        except yaml.YAMLError:
            logger.error("Loading mapping file %s failed.", mapping_file)
            raise

        return mapping

    def get_category_from_mapping(self, transaction: GenericTransaction) -> CategorizedTransaction:
        """Return category from mapping."""
        category_dict = self.get_category_id()

        for rule in self.mapping:
            conditions_met = []

            for column, patterns in rule.items():
                if column == "category":
                    continue

                if isinstance(patterns, str):
                    patterns = [patterns]
                conditions_met_column = any(
                    re.match(pattern, str(getattr(transaction, column)))
                    for pattern in patterns
                    if getattr(transaction, column) is not None
                )

                conditions_met.append(conditions_met_column)

            if all(conditions_met):
                assigned_category = rule["category"]
                break
        else:
            assigned_category = DEFAULT_CATEGORY

        category_id = category_dict.get(assigned_category, category_dict[DEFAULT_CATEGORY])

        return CategorizedTransaction(**transaction.dict(), category_id=category_id)

    @staticmethod
    def get_category_from_api(transaction: GenericTransaction) -> CategorizedTransaction:
        """Return category based on public data."""
        raise NotImplementedError

    def get_category_id(self) -> dict:
        """Convert category to category id."""
        with Session(self.database_engine) as session:
            categories = session.query(Category).all()
            category_dict = {category.name: category.id for category in categories}

        return category_dict
