from fast.models import Base
from fast.db import engine


def main() -> None:
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    main()
