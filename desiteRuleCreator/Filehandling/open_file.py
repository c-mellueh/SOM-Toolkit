from __future__ import annotations

from typing import TYPE_CHECKING, Type
from uuid import uuid4

from PySide6.QtWidgets import QInputDialog, QLineEdit
from lxml import etree

from desiteRuleCreator.Windows import graphs_window
from desiteRuleCreator.Windows.popups import msg_delete_or_merge
from desiteRuleCreator.Windows.popups import msg_unsaved
from desiteRuleCreator.data import classes, constants

if TYPE_CHECKING:
    from desiteRuleCreator.main_window import MainWindow


def string_to_bool(text: str) -> bool | None:
    if text == str(True):
        return True
    elif text == str(False):
        return False
    else:
        return None

def import_node_pos(graph_window:graphs_window.GraphWindow,path:str):
    def text(obj:classes.Object) -> str:
        if obj.is_concept:
            text = f"{obj.name}"
        else:
            text = f"{obj.name} ({obj.ident_attrib.value[0]})"
        return text

    def iter_child(parent_node:graphs_window.Node):

        for child in parent_node.aggregation.children:
            child_node = graphs_window.aggregation_to_node(child)
            con_type = parent_node.aggregation.connection_dict[child_node.aggregation]
            parent_node.add_child(child_node,con_type)
            iter_child(child_node)
        pass

    tree = etree.parse(path)
    projekt_xml = tree.getroot()
    xml_group_nodes = projekt_xml.find(constants.NODES)
    aggregation_dict = {aggregation.uuid:aggregation for aggregation in classes.Aggregation}
    node_dict = {}
    for xml_node in xml_group_nodes:
        uuid = xml_node.attrib.get(constants.IDENTIFIER)
        x_pos = float(xml_node.attrib.get(constants.X_POS))
        y_pos = float(xml_node.attrib.get(constants.Y_POS))
        aggregation:classes.Aggregation = aggregation_dict.get(uuid)
        node = graphs_window.Node(aggregation,graph_window)
        root = xml_node.attrib.get("root")
        if root == "True":
            root = True
        else:
            root = False
        node_dict[uuid] = (node,x_pos,y_pos,root)

    for node,x_pos,y_pos,root in node_dict.values():
        if root:
            graph_window.create_scene_by_node(node)
            graph_window.draw_tree(node)
            graph_window.combo_box.addItem(text(node.object))
            iter_child(node)
            graph_window.drawn_scenes.append(node.scene())

    for node,x_pos,y_pos,root in node_dict.values():
        node.setY(float(y_pos))
        node.setX(float(x_pos))

    graph_window.combo_box.setCurrentIndex(0)
    graph_window.combo_change()


def open_file(project: classes.Project, path: str = False) -> None:
    if not path:
        return
    tree = etree.parse(path)
    projekt_xml = tree.getroot()
    project.author = projekt_xml.attrib.get(constants.AUTHOR)
    project.name = projekt_xml.attrib.get("name")
    project.version = projekt_xml.attrib.get("version")

    if projekt_xml.attrib.get("version") is None:  # OLD FILES (Deprecated)
        import_old(projekt_xml)
        return

    def import_property_sets(xml_property_sets: list[etree._Element]) -> (list[classes.PropertySet], classes.Attribute):

        def import_attributes(xml_attributes: etree._Element,
                              property_set: classes.PropertySet) -> classes.Attribute | None:

            def transform_new_values(xml_attribute: etree._Element) -> list[str]:
                def empty_text(xml_value):
                    if xml_value.text is None:
                        return ""
                    else:
                        return xml_value.text

                value_type = xml_attribute.attrib.get("value_type")
                value = list()

                if value_type != constants.RANGE:
                    for xml_value in xml_attribute:
                        value.append(empty_text(xml_value))

                else:
                    for xml_range in xml_attribute:
                        from_to_list = list()
                        for xml_value in xml_range:
                            if xml_value.tag == "From":
                                from_to_list.append(empty_text(xml_value))
                            if xml_value.tag == "To":
                                from_to_list.append(empty_text(xml_value))
                        value.append(from_to_list)
                return value

            ident_attrib = None

            for xml_attribute in xml_attributes:
                attribs = xml_attribute.attrib
                name = attribs.get(constants.NAME)
                identifier = attribs.get(constants.IDENTIFIER)
                data_type = attribs.get(constants.DATA_TYPE)
                value_type = attribs.get(constants.VALUE_TYPE)
                is_identifier = attribs.get(constants.IS_IDENTIFIER)
                child_inh = string_to_bool(attribs.get(constants.CHILD_INHERITS_VALUE))
                value = transform_new_values(xml_attribute)
                attrib = classes.Attribute(property_set, name, value, value_type, data_type, child_inh, identifier)
                revit_mapping = attribs.get(constants.REVIT_MAPPING)
                attrib.revit_name = revit_mapping
                if is_identifier == str(True):
                    ident_attrib = attrib
            return ident_attrib

        property_sets: list[classes.PropertySet] = list()
        ident_attrib = None

        for xml_property_set in xml_property_sets:
            attribs = xml_property_set.attrib
            name = attribs.get(constants.NAME)
            identifier = attribs.get(constants.IDENTIFIER)
            property_set = classes.PropertySet(name, obj=None, identifier=identifier)

            xml_attrib_group = xml_property_set.find(constants.ATTRIBUTES)
            ident_value = import_attributes(xml_attrib_group, property_set)
            if ident_value is not None:
                ident_attrib = ident_value
            property_sets.append(property_set)

        return property_sets, ident_attrib

    def import_objects(xml_objects:list[etree._Element]):

        def get_obj_data(xml_object: etree._Element) -> (str, str, str, bool):

            name: str = xml_object.attrib.get(constants.NAME)
            parent: str = xml_object.attrib.get(constants.PARENT)
            identifier: str = xml_object.attrib.get(constants.IDENTIFIER)
            is_concept: str = xml_object.attrib.get(constants.IS_CONCEPT)

            return name, parent, identifier, string_to_bool(is_concept)

        def import_scripts(xml_scripts: etree._Element | None, obj: classes.Object) -> None:
            if xml_scripts is None:
                return
            for xml_script in xml_scripts:
                name = xml_script.attrib.get("name")
                code = xml_script.text
                script = classes.Script(name, obj)
                script.code = code

        for xml_object in xml_objects:
            xml_property_group = xml_object.find(constants.PROPERTY_SETS)
            xml_script_group = xml_object.find(constants.SCRIPTS)
            xml_mapping_group = xml_object.find(constants.IFC_MAPPINGS)

            property_sets, ident_attrib = import_property_sets(xml_property_group)
            name, parent, identifer, is_concept = get_obj_data(xml_object)
            obj = classes.Object(name, ident_attrib, identifier=identifer)
            ident_dict[identifer] = obj

            obj.ifc_mapping = [mapping.text for mapping in xml_mapping_group]

            for property_set in property_sets:
                obj.add_property_set(property_set)

            import_scripts(xml_script_group, obj)


    def create_ident_dict(item_list: list[Type[classes.Hirarchy]]) -> dict[str, Type[classes.Hirarchy]]:
        return {item.identifier: item for item in item_list}

    def link_parents(xml_predefined_psets: list[etree._Element], xml_objects: list[etree._Element]) -> None:
        def fill_dict(xml_dict: dict[str, str], xml_obj: etree._Element) -> None:
            xml_dict[xml_obj.attrib.get(constants.IDENTIFIER)] = xml_obj.attrib.get(constants.PARENT)

        def iterate() -> None:
            for xml_predefined_pset in xml_predefined_psets:
                fill_dict(xml_property_set_dict, xml_predefined_pset)
                xml_attributes = xml_predefined_pset.find(constants.ATTRIBUTES)
                for xml_attribute in xml_attributes:
                    fill_dict(xml_attribute_dict, xml_attribute)

            for xml_object in xml_objects:
                fill_dict(xml_object_dict, xml_object)
                xml_property_sets = xml_object.find(constants.PROPERTY_SETS)
                for xml_property_set in xml_property_sets:
                    fill_dict(xml_property_set_dict, xml_property_set)
                    xml_attributes = xml_property_set.find(constants.ATTRIBUTES)
                    for xml_attribute in xml_attributes:
                        uuid = xml_attribute.attrib["identifer"]
                        if xml_attribute_dict.get(uuid) is not None:
                            print(f"ERROR DUPLICATED UUID {uuid}")
                        fill_dict(xml_attribute_dict, xml_attribute)

        def create_link(item_dict: dict[str, Type[classes.Hirarchy]], xml_dict: dict[str, str]):
            for ident, item in item_dict.items():
                parent_ident = xml_dict[str(ident)]
                parent_item = item_dict.get(parent_ident)
                if parent_item is not None:
                    parent_item.add_child(child=item)

        xml_property_set_dict = dict()
        xml_object_dict = dict()
        xml_attribute_dict = dict()
        iterate()

        obj_dict = create_ident_dict(classes.Object)
        property_set_dict = create_ident_dict(classes.PropertySet)
        attribute_dict = create_ident_dict(classes.Attribute)

        create_link(obj_dict, xml_object_dict)
        create_link(property_set_dict, xml_property_set_dict)
        create_link(attribute_dict, xml_attribute_dict)

    def link_aggregation() -> None:
        def create_node_dict() -> dict[str, [object, graphs_window.Node]]:

            id_node_dict = dict()
            for xml_node in xml_group_nodes:
                identifier = xml_node.attrib.get(constants.IDENTIFIER)
                obj = ident_dict[xml_node.attrib.get(constants.OBJECT.lower())]
                aggregation = classes.Aggregation(obj,identifier)
                id_node_dict[identifier] = (aggregation, xml_node)
            return id_node_dict

        id_node_dict = create_node_dict()

        for identifier, (aggregation, xml_node) in id_node_dict.items():
            parent_id = xml_node.attrib.get(constants.PARENT)
            is_root = xml_node.attrib.get(constants.IS_ROOT)
            connection_type = xml_node.attrib.get(constants.CONNECTION)
            if parent_id != constants.NONE:
                parent_node: classes.Aggregation = id_node_dict[parent_id][0]
                parent_node.add_child(aggregation, int(connection_type))

    xml_group_predef_psets = projekt_xml.find(constants.PREDEFINED_PSETS)
    xml_group_objects = projekt_xml.find(constants.OBJECTS)
    xml_group_nodes = projekt_xml.find(constants.NODES)

    import_property_sets(xml_group_predef_psets)
    ident_dict: dict[str, classes.Object] = dict()
    import_objects(xml_group_objects)

    link_parents(xml_group_predef_psets, xml_group_objects)
    link_aggregation()


def new_file(main_window: MainWindow) -> None:
    new_file = msg_unsaved()
    if new_file:
        main_window.save_path = None
        project_name = QInputDialog.getText(main_window, "New Project", "new Project Name:", QLineEdit.Normal, "")

        if project_name[1]:
            main_window.project = classes.Project(main_window, project_name[0])
            main_window.setWindowTitle(main_window.project.name)
            main_window.project.name = project_name[0]
            main_window.clear_all()


def open_file_clicked(main_window: MainWindow):
    if classes.Object:
        result = msg_delete_or_merge()
        if result is None:
            return
        if result:
            main_window.clear_all()

def merge_new_file(main_window):
    print("MERGE NEEDS TO BE PROGRAMMED")  # TODO: Write Merge


## deprecated
def import_old(projekt_xml):
    def handle_identifier(obj: classes.Object):
        ident_text: str = obj.ident_attrib
        ident_list = ident_text.split(":")
        pset_name = ident_list[0]
        attribute_name = ident_list[1]

        attribute_found = False

        for property_set in obj.property_sets:
            if property_set.name == pset_name:
                for attribute in property_set.attributes:
                    if attribute.name == attribute_name:
                        obj.ident_attrib = attribute
                        attribute_found = True
                if not attribute_found:
                    atrb = classes.Attribute(property_set, attribute_name, [obj.name], constants.LIST)
                    obj.ident_attrib = atrb

    def transform_values(xml_object, value_type):
        value_list = list()
        if value_type == constants.LIST or value_type == constants.FORMAT:
            for xml_value in xml_object:
                value_list.append(xml_value.attrib.get("Wert"))

        if value_type == constants.RANGE:
            for xml_value in xml_object:
                domain = xml_value.attrib.get("Wert").split(":")
                if len(domain) > 1:
                    value_list.append([float(domain[0]), float(domain[1])])
                else:
                    value_list.append(domain)

        return value_list

    def transform_value_types(value_type):
        if value_type == "Wert":
            value_type = constants.LIST
        elif value_type == "Bereich":
            value_type = constants.RANGE
        elif value_type == "Format":
            value_type = constants.FORMAT
        else:
            raise ImportWarning(f"Imported ValueType {value_type} not known")
        return value_type

    fachdisziplinen = [obj.attrib.get("Fachdisziplin") for obj in projekt_xml if obj.tag == "Objekt"]
    fachdisziplinen = list(set(fachdisziplinen))

    fachdisziplinen_dict = dict()
    for fd in fachdisziplinen:
        obj = classes.Object(fd, str(uuid4()))
        fachdisziplinen_dict[fd] = obj

    for xml_object in projekt_xml:

        if xml_object.tag == "Objekt":
            obj = classes.Object(xml_object.attrib.get("Name"), xml_object.attrib["Identifier"])

            xml_property_sets = [x for x in xml_object if x.tag == "PropertySet"]

            for xml_property_set in xml_property_sets:
                pset_name = xml_property_set.attrib.get("Name")
                property_set = classes.PropertySet(pset_name)

                for xml_attribute in xml_property_set:
                    attrib = xml_attribute.attrib
                    name = attrib.get("Name")
                    value_type = transform_value_types(attrib.get("Art"))
                    data_type = attrib.get("Datentyp")

                    value = transform_values(xml_attribute, value_type)
                    atrb = classes.Attribute(property_set, name, value, value_type, data_type)

                obj.add_property_set(property_set)

                handle_identifier(obj)

                group_name = xml_object.attrib.get("Fachdisziplin")
                obj.parent = fachdisziplinen_dict[group_name]
