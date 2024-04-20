"""Category general class for Where My Money app."""

import logging
import re

from sqlmodel import Session, select
import yaml
from where_my_money.models import CategorizedTransaction, Category
from where_my_money.seed import DEFAULT_CATEGORY_ID

from where_my_money.transactions import GenericTransaction

logger = logging.getLogger(__name__)


class CategoryMapper:
    """Pydantic class to categorize every transaction and return a category."""

    def __init__(self, mapping_file: str, database_engine):
        self.mapping_file = mapping_file
        self.database_engine = database_engine
        self.mapping = self.load_mapping_from_yaml(mapping_file)
        category_dict = self.get_category_dict()
        try:
            self.mapping = [{**rule, "category_id": category_dict[rule["category"]]} for rule in self.mapping]
        except KeyError:
            logger.error("Category not found in database.")
            raise

    def get_category_dict(self) -> dict:
        """Convert category to category id."""
        with Session(self.database_engine) as session:
            categories = session.query(Category).all()
            category_dict = {category.name: category.id for category in categories}

        return category_dict

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

        for rule in self.mapping:
            conditions_met = []

            for column, patterns in rule.items():
                if column in ["category", "category_id"]:
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
                assigned_category_id = rule["category_id"]
                break
        else:
            assigned_category_id = DEFAULT_CATEGORY_ID

        return CategorizedTransaction(**transaction.dict(), category_id=assigned_category_id)

    @staticmethod
    def get_category_from_api(transaction: GenericTransaction) -> CategorizedTransaction:
        """Return category based on public data."""
        raise NotImplementedError
