import os

HOME_DIR = os.path.dirname(__file__)
TEMPLATE = "template.txt"

IFC_PATH = os.path.join(os.path.dirname(__file__),"ifc_classes")
IFC_4_1_PATH = os.path.join(IFC_PATH,"ifc4_1.txt")
IFC_4_1= [entity.strip() for entity in open(IFC_4_1_PATH,"r")]

