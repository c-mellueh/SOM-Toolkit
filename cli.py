import logging

from pypi_latest import PypiLatest

from som_gui.__main__ import main, start_log

if __name__ == "__main__":
    start_log(logging.DEBUG)
    ppl = PypiLatest("SOMcreator", "1.2.7")
    latest = ppl.check_latest()
    if latest:
        ppl.upgrade()

    main()
