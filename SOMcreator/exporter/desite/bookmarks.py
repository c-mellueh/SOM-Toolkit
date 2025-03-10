from __future__ import annotations
import os
import jinja2
from lxml import etree
from SOMcreator.templates import HOME_DIR, BOOKMARK_TEMPLATE
import SOMcreator
from SOMcreator.util import xml


def _handle_bookmark_list(proj: SOMcreator.SOMProject) -> etree.ElementTree:
    xml_bookmarks = etree.Element("bookmarks")
    xml_bookmarks.set("xmlnsxsi", "http://www.w3.org/2001/XMLSchema-instance")
    xml_bookmark_list = etree.SubElement(xml_bookmarks, "cBookmarkList")

    obj: SOMcreator.SOMClass
    for obj in sorted(proj.get_classes(filter=True), key=lambda o: o.ident_value):
        xml_bookmark = etree.SubElement(xml_bookmark_list, "cBookmark")
        xml_bookmark.set("ID", str(obj.uuid))

        if isinstance(obj.identifier_property, SOMcreator.SOMProperty):
            xml_bookmark.set("name", str(obj.identifier_property.allowed_values[0]))

        xml_bookmark.set("bkmType", "2")
        xml_col = etree.SubElement(xml_bookmark, "col")
        xml_col.set("v", "Type##xs:string")

        som_property = obj.identifier_property
        if som_property is None:
            continue
        xml_col = etree.SubElement(xml_bookmark, "col")
        data_type = xml.transform_data_format(som_property.data_type)
        text = f"{som_property.property_set.name}:{som_property.name}##{data_type}"
        xml_col.set("v", text)

        for property_set in obj.get_property_sets(filter=True):
            for som_property in property_set.get_properties(filter=True):
                if som_property != obj.identifier_property:
                    xml_col = etree.SubElement(xml_bookmark, "col")
                    data_type = xml.transform_data_format(som_property.data_type)
                    text = f"{property_set.name}:{som_property.name}##{data_type}"
                    xml_col.set("v", text)
    return etree.ElementTree(xml_bookmarks)


def _get_property_dict(proj: SOMcreator.SOMProject) -> dict[str, str]:
    property_dict = {}
    for obj in proj.get_classes(filter=True):
        for property_set in obj.get_property_sets(filter=True):
            for som_property in property_set.get_properties(filter=True):
                property_dict[f"{property_set.name}:{som_property.name}"] = (
                    xml.transform_data_format(som_property.data_type)
                )

    return property_dict


def export_bookmarks(proj: SOMcreator.SOMProject, path: str) -> None:
    if not os.path.isdir(path):
        return

    with open(os.path.join(path, "bookmarks.bkxml"), "wb") as f:
        tree = _handle_bookmark_list(proj)
        tree.write(
            f, xml_declaration=True, pretty_print=True, encoding="utf-8", method="xml"
        )

    property_dict = _get_property_dict(proj)
    file_loader = jinja2.FileSystemLoader(HOME_DIR)
    env = jinja2.Environment(loader=file_loader)
    env.trim_blocks = True
    env.lstrip_blocks = True
    template = env.get_template(BOOKMARK_TEMPLATE)
    code = template.render(attribute_dict=property_dict)
    with open(os.path.join(path, "bookmark_script.js"), "w") as f:
        f.write(code)
