import logging

import SOMcreator
from pypi_latest import PypiLatest

from som_gui.__main__ import start_log


def cli():
    start_log(logging.DEBUG)
    ppl = PypiLatest("SOMcreator", SOMcreator.__version__)
    latest = ppl.check_latest()
    if not latest:
        ppl.upgrade()
        print()
        print("*" * 60)
        print(f"Update von SOMcreator installiert, Runtime neu start!")
        print("*" * 60)
        return
    from som_gui.__main__ import main

    main()


if __name__ == "__main__":
    cli()
