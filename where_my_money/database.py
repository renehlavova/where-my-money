"""Create database."""

import os
import sys
from sqlmodel import SQLModel, Session, create_engine
from where_my_money.models import *
from where_my_money.seed import categories


DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///database.db")

engine = create_engine(DATABASE_URI)


def delete_table():
    """Delete existing tables in database."""
    SQLModel.metadata.drop_all(engine)


def create_all():
    """Create engine."""
    SQLModel.metadata.create_all(engine)


def insert_seed_data():
    """Load categories to table."""
    with Session(engine) as session:
        for category in categories:
            session.add(category)
        session.commit()


if __name__ == "__main__":
    if input("Do you want to recreate database? [Y/n] ").lower() != "y":
        sys.exit()

    delete_table()
    create_all()
    insert_seed_data()
