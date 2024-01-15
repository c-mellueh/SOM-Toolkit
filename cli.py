import importlib.util
import logging
import os
import subprocess
import sys
from importlib import import_module

import main as main_func

# implement pip as a subprocess:

MAPPING = {"pypi-latest": "pypi_latest"}
REVERSE_MAPPING = {val: key for key, val in MAPPING.items()}


def check_for_pp_latest():
    if importlib.util.find_spec("pypi_latest") is None:
        subprocess.run([sys.executable, "-m", "pip", "install", "pypi-latest"])
        os.kill(os.getpid(), 9)


def install_missing_packages():
    check_for_pp_latest()
    from pypi_latest import PypiLatest

    made_an_update = False
    with open("./requirements.txt", "r") as file:
        lines = set(line.strip() for line in file.readlines())

    for line in lines:
        package_name = line
        logging.info(f"Check {package_name} for updates")
        if package_name in MAPPING:
            package_name = MAPPING[package_name]

        if (module_spec := importlib.util.find_spec(package_name)) is not None:
            package = import_module(module_spec.name)
            if not "__version__" in dir(package):
                continue
            local_version = package.__version__
            ppl = PypiLatest(package_name, local_version)
            latest = ppl.check_latest()
            if not latest:
                ppl.upgrade()
                made_an_update = True
        else:
            logging.info(f"Install {package_name}")
            ppl = PypiLatest(package_name, "0.0.0")
            ppl.upgrade()
            made_an_update = True

    if made_an_update:
        print()
        print("*" * 60)
        print(f"Update installiert, Runtime neu starten!")
        print("*" * 60)
        return False
    return False


def cli():
    if install_missing_packages():
        return
    main_func.start_log(logging.DEBUG)
    from main import main

    main()


if __name__ == "__main__":
    cli()
