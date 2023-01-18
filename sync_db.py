import sys

from fast.models import Base
from fast.db import engine


def main(args: list[str]) -> None:
    if args == ["create"] or not args:
        Base.metadata.create_all(engine)
    elif args == ["drop"]:
        Base.metadata.drop_all(engine)


if __name__ == "__main__":
    main(sys.argv[1:])
