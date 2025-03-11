import uuid
from xml.etree.ElementTree import Element

from lxml import etree

import SOMcreator
from SOMcreator.constants import value_constants
from . import handle_header
from SOMcreator.util import xml


def _handle_section(
    id_dict, aggregation: SOMcreator.SOMAggregation, xml_item: Element
) -> None:
    xml_child = etree.SubElement(xml_item, "section")
    id_dict[aggregation] = aggregation.uuid
    xml_child.set("ID", aggregation.uuid)
    xml_child.set("name", aggregation.som_class.name)
    xml_child.set("pre", "")
    xml_child.set("type", "typeBsGroup")
    xml_child.set("takt", "")

    for child in sorted(aggregation.get_children(filter=True), key=lambda x: x.name):
        connection_type = child.parent_connection
        if connection_type == value_constants.AGGREGATION:
            _handle_section(id_dict, child, xml_child)
        else:
            _handle_section(id_dict, child, xml_item)


def _handle_elementsection(xml_parent: Element):
    xml_elementsection = etree.SubElement(xml_parent, "elementSection")
    xml_root = etree.SubElement(xml_elementsection, "section")
    xml_root.set("ID", str(uuid.uuid4()))
    xml_root.set("name", "BS Autogenerated")
    xml_root.set("pre", "")
    xml_root.set("type", "typeBsContainer")
    xml_root.set("takt", "")

    root_classes: list[SOMcreator.SOMAggregation] = [
        aggreg for aggreg in SOMcreator.SOMAggregation if aggreg.is_root
    ]

    root_classes.sort(key=lambda x: x.name)

    id_dict = dict()
    for aggreg in root_classes:
        _handle_section(id_dict, aggreg, xml_root)

    return xml_elementsection, id_dict


def _handle_property_type_section(xml_repo) -> dict[str, int]:
    xml_property_type_section = etree.SubElement(xml_repo, "propertyTypeSection")

    property_dict = dict()

    i = 1
    for som_property in SOMcreator.SOMProperty:
        # use property_text instead of property to remove duplicates
        property_text = f"{som_property.property_set.name}:{som_property.name}"
        if property_text not in property_dict:
            xml_ptype = etree.SubElement(xml_property_type_section, "ptype")
            xml_ptype.set("key", str(i))
            xml_ptype.set("name", property_text)
            xml_ptype.set("datatype", xml.transform_data_format(som_property.data_type))
            xml_ptype.set("unit", "")
            xml_ptype.set("inh", "false")
            property_dict[property_text] = i
            i += 1

    return property_dict


def _handle_property_section(
    xml_repo: etree.Element, id_dict: dict, property_dict: dict
) -> None:
    xml_property_section = etree.SubElement(xml_repo, "propertySection")

    for node, ref_id in id_dict.items():
        obj: SOMcreator.SOMClass = node.object
        for property_set in obj.get_property_sets(filter=True):
            for som_property in property_set.get_properties(filter=True):
                property_text = f"{som_property.property_set.name}:{som_property.name}"
                ref_type = property_dict[property_text]
                xml_property = etree.SubElement(xml_property_section, "property")
                xml_property.set("refID", str(ref_id))
                xml_property.set("refType", str(ref_type))
                if som_property == obj.identifier_property:
                    xml_property.text = som_property.allowed_values[0]
                else:
                    xml_property.text = "füllen!"


def _handle_repository(
    xml_parent: Element, id_dict: dict[SOMcreator.SOMAggregation, str]
) -> None:
    xml_repo = etree.SubElement(xml_parent, "repository")
    xml_id_mapping = etree.SubElement(xml_repo, "IDMapping")

    for i, (item, id_value) in enumerate(id_dict.items()):
        xml_id = etree.SubElement(xml_id_mapping, "ID")
        xml_id.set("k", str(i + 1))
        xml_id.set("v", str(id_value))

    property_dict = _handle_property_type_section(xml_repo)
    _handle_property_section(xml_repo, id_dict, property_dict)


def _handle_relation_section(xml_parent: Element) -> None:
    xml_relation_section = etree.SubElement(xml_parent, "relationSection")
    etree.SubElement(xml_relation_section, "IDMapping")
    xml_relation = etree.SubElement(xml_relation_section, "relation")
    xml_relation.set("name", "default")


def export_bs(project: SOMcreator.SOMProject, path: str) -> None:
    if not path:
        return
    xml_boq_export = handle_header(project.author, "bsExport")
    xml_elementsection, id_dict = _handle_elementsection(xml_boq_export)

    etree.SubElement(xml_boq_export, "linkSection")
    _handle_repository(xml_boq_export, id_dict)
    _handle_relation_section(xml_boq_export)

    tree = etree.ElementTree(xml_boq_export)

    with open(path, "wb") as f:
        tree.write(
            f, xml_declaration=True, pretty_print=True, encoding="utf-8", method="xml"
        )
