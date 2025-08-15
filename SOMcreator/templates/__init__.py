import os
import importlib.resources
import json

HOME_DIR = os.path.dirname(__file__)
TEMPLATE = "template.txt"
FAST_TEMPLATE = "fast_template.txt"
MAPPING_TEMPLATE = "mapping_template.txt"
BOOKMARK_TEMPLATE = "bookmark_template.txt"
UNTESTED = "untested_template.txt"

with importlib.resources.open_text("SOMcreator.templates", "ifc.json") as file:
    dict = json.load(file)
    IFC_4_1 = [entity.strip() for entity in dict["ifc4.1"]]

with importlib.resources.open_text("SOMcreator.templates", "units_bsdd.json") as file:
    dict = json.load(file)
    UNITS_DICT = {e["QudtUri"]:e for e in dict if e.get("QudtUri")}