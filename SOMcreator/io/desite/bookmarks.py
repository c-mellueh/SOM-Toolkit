from __future__ import annotations
import os
import jinja2
from lxml import etree
from SOMcreator.Template import HOME_DIR, BOOKMARK_TEMPLATE
import SOMcreator
from SOMcreator.util import xml

def _handle_bookmark_list(proj: SOMcreator.Project) -> etree.ElementTree:
    xml_bookmarks = etree.Element("bookmarks")
    xml_bookmarks.set("xmlnsxsi", "http://www.w3.org/2001/XMLSchema-instance")
    xml_bookmark_list = etree.SubElement(xml_bookmarks, "cBookmarkList")

    obj: SOMcreator.Object
    for obj in sorted(proj.get_objects(filter=True), key=lambda o: o.ident_value):
        xml_bookmark = etree.SubElement(xml_bookmark_list, "cBookmark")
        xml_bookmark.set("ID", str(obj.uuid))

        if isinstance(obj.ident_attrib, SOMcreator.Attribute):
            xml_bookmark.set("name", str(obj.ident_attrib.value[0]))

        xml_bookmark.set("bkmType", "2")
        xml_col = etree.SubElement(xml_bookmark, "col")
        xml_col.set("v", "Type##xs:string")

        attribute = obj.ident_attrib
        if attribute is None:
            continue
        xml_col = etree.SubElement(xml_bookmark, "col")
        data_type = xml.transform_data_format(attribute.data_type)
        text = f"{attribute.property_set.name}:{attribute.name}##{data_type}"
        xml_col.set("v", text)

        for property_set in obj.get_property_sets(filter=True):
            for attribute in property_set.get_attributes(filter=True):
                if attribute != obj.ident_attrib:
                    xml_col = etree.SubElement(xml_bookmark, "col")
                    data_type = xml.transform_data_format(attribute.data_type)
                    text = f"{property_set.name}:{attribute.name}##{data_type}"
                    xml_col.set("v", text)
    return etree.ElementTree(xml_bookmarks)


def _get_attribute_dict(proj: SOMcreator.Project) -> dict[str, str]:
    attribute_dict = {}
    for obj in proj.get_objects(filter=True):
        for property_set in obj.get_property_sets(filter=True):
            for attribute in property_set.get_attributes(filter=True):
                attribute_dict[f"{property_set.name}:{attribute.name}"] = xml.transform_data_format(attribute.data_type)

    return attribute_dict


def export_bookmarks(proj: SOMcreator.Project, path: str) -> None:
    if not os.path.isdir(path):
        return

    with open(os.path.join(path, "bookmarks.bkxml"), "wb") as f:
        tree = _handle_bookmark_list(proj)
        tree.write(f, xml_declaration=True, pretty_print=True, encoding="utf-8", method="xml")

    attrib_dict = _get_attribute_dict(proj)
    file_loader = jinja2.FileSystemLoader(HOME_DIR)
    env = jinja2.Environment(loader=file_loader)
    env.trim_blocks = True
    env.lstrip_blocks = True
    template = env.get_template(BOOKMARK_TEMPLATE)
    code = template.render(attribute_dict=attrib_dict)
    with open(os.path.join(path, "bookmark_script.js"), "w") as f:
        f.write(code)
