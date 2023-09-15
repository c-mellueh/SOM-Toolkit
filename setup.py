import os

from setuptools import setup


def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path)) as fp:
        return fp.read()


def get_version(rel_path: str) -> str:
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            # __version__ = "0.9"
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


setup(
    name='som-Toolkit',
    version=get_version("som_gui/__init__.py"),
    description='A usefule GUI for your BIM-Data Specification',
    author='Christoph Mellüh',
    author_email='christoph.mellueh@deutschebahn.com',
    packages=['som-Toolkit'],  # would be the same as name
    install_requires=['PySide6', 'openpyxl', 'lxml', 'jinja2','SOMcreator','ifcopenshell','tqdm',"pypi-latest"],  # external packages acting as dependencies
)
