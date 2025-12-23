from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.ext.declarative import declarative_base

from alembic.config import Config
from alembic import command

from src import db_config
from src.settings import PROJECT_ROOT

from pathlib import Path


Base = declarative_base()


def create_db() -> None:
    if not database_exists(url=db_config.get_db_uri()):
        create_database(url=db_config.get_db_uri())


def run_migrations() -> None:
    alembic_config = Config()
    alembic_config.set_main_option(name="script_location", value=f"{Path(PROJECT_ROOT, "migrations")}")
    alembic_config.set_main_option(name="sqlalchemy.url", value=db_config.get_db_uri())

    command.upgrade(config=alembic_config, revision="head")
