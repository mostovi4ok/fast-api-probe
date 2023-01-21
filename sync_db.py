from typing import Literal

import click

from fast.models import Base
from fast.db import engine


@click.command()
@click.option(
    "--db_action",
    default="create",
    type=click.Choice(["create", "drop"]),
)
def main(db_action: Literal["create", "drop"]) -> None:
    """Program for creating or deleting a database."""

    if db_action == "create":
        Base.metadata.create_all(engine)
    elif db_action == "drop":
        Base.metadata.drop_all(engine)


if __name__ == "__main__":
    main()
