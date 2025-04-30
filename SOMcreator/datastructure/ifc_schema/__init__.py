from typing import Literal, get_args
import os
import json
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
import logging

IFC2X3_TYPE = Literal["IFC2x3"]
IFC4_TYPE = Literal["IFC4"]
IFC4_3_TYPE = Literal["IFC4_3"]
IFC2X3 = get_args(IFC2X3_TYPE)[0]
IFC4 = get_args(IFC4_TYPE)[0]
IFC4_3 = get_args(IFC4_3_TYPE)[0]
VERSION_TYPE = Literal[IFC2X3_TYPE, IFC4_TYPE, IFC4_3_TYPE]
PREDEFINED_SPLITTER = "/"
PSD = "psd"
QTO = "qto"

APPDATA_SECTION = "ifc_schema"
VERSION_OPTION = "versions"


class IfcProperties:
    parent_dict: dict[str, dict[str, list[str]]] = dict()
    pset_class_dict: dict[str, dict[str, list[str]]] = dict()


def get_properties():
    return IfcProperties


def read_jsons(version: str):
    prop = get_properties()
    p = get_resource_folder_path()
    with open(os.path.join(p, version, "parent.json"), "r") as f:
        d: dict[str, list[str]] = json.load(f)  # type: ignore
    prop.parent_dict[version] = d

    with open(os.path.join(p, version, "pset_class.json"), "r") as f:
        d: dict[str, list[str]] = json.load(f)  # type: ignore
    prop.pset_class_dict[version] = d


def get_resource_folder_path():
    from SOMcreator.datastructure.ifc_schema.resources import PATH

    return PATH


def get_all_psets(version: VERSION_TYPE) -> set[str]:
    allowed_psets: set[str] = set()
    folder_path = os.path.join(get_resource_folder_path(), version, PSD)
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Version {version} not found")
    allowed_psets.update({os.path.splitext(fn)[0] for fn in os.listdir(folder_path)})
    return allowed_psets


def get_property_sets_of_class(
    class_name: str, version: str, predefined_type: str | None = None
) -> set[str]:
    parent_dict = get_parent_dict(version)
    property_dict = get_pset_class_dict(version)
    sets: set[str] = set()
    for c in parent_dict.get(class_name, []):
        sets.update(set(property_dict.get(c, set())))
    if predefined_type is not None:
        sets.update(set(property_dict.get(f"{class_name}/{predefined_type}", set())))
    return sets


def get_property_set_path(property_set_name: str, version: VERSION_TYPE) -> str:
    path = get_resource_folder_path()
    if property_set_name.startswith("Pset"):
        path = os.path.join(path, version, PSD)
    elif property_set_name.startswith("Qto"):
        path = os.path.join(path, version, QTO)
    else:
        raise ValueError(
            f"PropertySet '{property_set_name}' doesn't exist in IFC Specification"
        )

    file_path = os.path.join(path, f"{property_set_name}.xml")
    if not os.path.exists(file_path):
        raise ValueError(
            f"PropertySet '{property_set_name}' doesn't exist in {version}"
        )
    return file_path


def get_properties_by_pset_name(
    property_set_name: str, version: VERSION_TYPE
) -> set[str]:
    file_path = get_property_set_path(property_set_name, version)
    etree = ET.parse(file_path)
    definitions = etree.find("PropertyDefs")
    if definitions is None:
        return set()
    definitions = [property_def.find("Name") for property_def in definitions]
    names = {n.text for n in definitions if n is not None and n.text is not None}
    return names


def get_property_data(
    property_set_name: str, property_name: str, version: VERSION_TYPE
) -> tuple[str, str, str]:
    def _get_property_def(name: str) -> Element[str]:
        for property_def in etree.getroot().find("PropertyDefs") or []:
            n = property_def.find("Name")
            n = n.text if n is not None else ""
            if n == name:
                return property_def
        raise ValueError(
            f"Property '{property_name}' doesn't exist in PropertySet '{property_set_name}'"
        )

    def _get_type() -> str:
        missing_datype_error = ValueError(
            f"Property '{property_set_name}:{property_name}' has no Datatype"
        )
        property_type = definition.find("PropertyType")
        if property_type is None:
            raise missing_datype_error
        if len(property_type) > 1:
            raise ValueError(
                f"Property '{property_set_name}:{property_name}' has multiple ValueTypes"
            )
        t = property_type[0]
        if t.tag != "TypePropertySingleValue":
            logging.info(f"ValueType {t.tag} unknown")
            return "IfcLabel"
        dt = t.find("DataType")
        if dt is None:
            raise missing_datype_error
        dt_value = dt.get("type")
        if dt_value is None:
            raise missing_datype_error
        return dt_value

    file_path = get_property_set_path(property_set_name, version)
    etree = ET.parse(file_path)
    definition = _get_property_def(property_name)

    name = definition.find("Name")
    name = name.text if name is not None and name.text is not None else ""

    description = definition.find("Definition")
    description = (
        description.text
        if description is not None and description.text is not None
        else ""
    )
    datatype = _get_type()
    return (name, description, datatype)


def get_predefined_types(class_name: str, version: str) -> list[str]:
    def _get_complext_type(name: str) -> Element:
        children = [c for c in root]
        element = {
            e.get("name"): e
            for e in root.iterfind(".//xs:complexType", namespace)
            if e in children
        }.get(name)
        if element is None:
            raise ValueError
        return element

    def _find_enumeration(elem: Element):
        cc = elem.find("xs:complexContent", namespace)
        if cc is None:
            raise ValueError
        ext = cc.find("xs:extension", namespace)
        if ext is None:
            return None
        attr = ext.find('xs:attribute[@name="PredefinedType"]', namespace)
        if attr is None:
            return None
        t = attr.get("type")
        if t is None:
            raise ValueError
        if t.startswith("ifc:"):
            return t[4:]
        return t

    def _get_values_by_enum(type_enum: str) -> list[str]:
        element = root.find(f'xs:simpleType[@name="{type_enum}"]', namespace)
        if element is None:
            raise ValueError
        restriction = element.find("xs:restriction", namespace)
        if restriction is None:
            return []
        values = [e.get("value") for e in restriction]
        return [v.upper() for v in values if v is not None]

    path = os.path.join(get_resource_folder_path(), version, "IFC.xml")
    tree = ET.parse(path)
    root = tree.getroot()
    namespace = {"xs": "http://www.w3.org/2001/XMLSchema"}
    if not class_name:
        return []
    ct = _get_complext_type(class_name)
    enum = _find_enumeration(ct)
    if enum is None:
        return []
    return _get_values_by_enum(enum)


def is_subclass(class_name: str, parent_name: str, version: str) -> bool:
    parent_list = get_parent_dict(version).get(class_name)
    if not parent_list:
        return False
    return parent_name in parent_list


def get_all_classes(version: str, class_filter: str | None = None) -> list[str]:
    classes = list(get_parent_dict(version).keys())
    if class_filter is None:
        return classes
    return [c for c in classes if is_subclass(c, class_filter, version)]


def get_parent_dict(version: str) -> dict[str, list[str]]:
    if version not in get_properties().parent_dict:
        read_jsons(version)
    return get_properties().parent_dict[version]


def get_pset_class_dict(version: str) -> dict[str, list[str]]:
    if version not in get_properties().pset_class_dict:
        read_jsons(version)
    return get_properties().pset_class_dict[version]


def class_exists_in_version(class_name: str, version: VERSION_TYPE):
    if PREDEFINED_SPLITTER in class_name:
        class_name = class_name.split(PREDEFINED_SPLITTER)[0]
    return class_name in get_all_classes(version)


def predefined_type_exists_in_version(
    class_name: str, predefined_type: str, version: VERSION_TYPE
):
    if not class_exists_in_version(class_name, version):
        return False
    return predefined_type in get_predefined_types(class_name, version)
