import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree, Element
import json

import os


def extract_complex_type_names():
    children = [c for c in root]
    elements = [e for e in root.iterfind(".//xs:element", namespace) if e in children]
    return [e.get("name") for e in elements if not e.get("abstract") and e.get("type")]


def find_parent_classes(type_name):
    element = root.find(f'.//xs:element[@name="{type_name}"]', namespace)
    return element.get("substitutionGroup")


def get_parent_list(type_name):
    parent = type_name
    parent_list = [parent]

    while True:
        parent = find_parent_classes(parent)
        if parent is None:
            return parent_list
        if parent.startswith("ifc:"):
            parent = parent[4:]
        parent_list.append(parent)


def get_class_names(t: ElementTree):
    root: Element = t.getroot()
    ns_uri = root.tag.split('}')[0].strip('{')
    ns = {'ns': ns_uri}
    # Extract the class names
    class_names = [
        cn.text
        for cn in root.findall(".//ns:ApplicableClasses/ns:ClassName", ns)
    ]
    print(f"Result: {class_names}")
    return class_names


def create_pset_class_dict():
    folder_path = "./psd"
    pset_class_dict = {}
    for fn in os.listdir(folder_path):
        path = os.path.join(folder_path, fn)
        tree = ET.parse(path)
        print(f"Parse {fn}")
        pset_class_dict[fn[:-4]] = get_class_names(tree)

    folder_path = "./qto"
    for fn in os.listdir(folder_path):
        path = os.path.join(folder_path, fn)
        tree = ET.parse(path)
        print(f"Parse {fn}")
        pset_class_dict[fn[:-4]] = get_class_names(tree)

    return pset_class_dict


def import_parents():
    parent_dict = dict()
    for name in extract_complex_type_names():
        parentlist = get_parent_list(name)
        parent_dict[name] = parentlist
    with open("./parent.json", "w") as f:
        json.dump(parent_dict, f)


def import_class_pset():
    pset_class_dict = create_pset_class_dict()
    class_pset_dict = dict()
    for pset_name, classes in pset_class_dict.items():
        for cl in classes:
            if cl not in class_pset_dict:
                class_pset_dict[cl] = list()
            if pset_name not in class_pset_dict[cl]:
                class_pset_dict[cl].append(pset_name)
    with open("./pset_class.json", "w") as f:
        json.dump(class_pset_dict, f)


if __name__ == "__main__":
    path = "./IFC.xml"
    tree = ET.parse(path)
    root = tree.getroot()
    namespace = {
        "xs": "http://www.w3.org/2001/XMLSchema",
        "ns": "http://buildingSMART-tech.org/xml/psd/PSD_IFC4.xsd",
    }
    import_parents()
    import_class_pset()
