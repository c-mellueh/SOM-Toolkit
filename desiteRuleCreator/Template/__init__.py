import os

HOME_DIR = os.path.dirname(__file__)
TEMPLATE = "template.txt"

IFC_PATH = os.path.join(os.path.dirname(__file__),"ifc_classes")
IFC_4_1 = list(open(os.path.join(IFC_PATH,"ifc4_1.txt")))
