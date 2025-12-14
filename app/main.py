from __future__ import annotations
import pathlib
import sys

# Allow running as `python -m app.main` or `python app/main.py`
if __name__ == "__main__" and (__package__ is None or __package__ == ""):
    sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))

from app.cli import constants
from app.services.login_services import print_menu


def main() -> None:
    print_menu(constants.login_menu)


if __name__ == "__main__":
    main()


