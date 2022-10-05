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


def fill_tree(main_window: MainWindow) -> None:
    root_item = main_window.object_tree.invisibleRootItem()
    item_dict: dict[classes.Object, classes.CustomObjectTreeItem] = {obj: main_window.add_object_to_tree(obj,root_item)
                                                                     for obj in classes.Object}

    for obj in classes.Object:
        tree_item = item_dict[obj]
        if obj.parent is not None:
            parent_item = item_dict[obj.parent]
            root = tree_item.treeWidget().invisibleRootItem()
            item = root.takeChild(root.indexOfChild(tree_item))
            parent_item.addChild(item)


def import_data(main_window: MainWindow, path: str = False) -> None:
    if path:
        main_window.clear_object_input()

        tree = etree.parse(path)
        projekt_xml = tree.getroot()
        author = projekt_xml.attrib.get(constants.AUTHOR)
        name = projekt_xml.attrib.get("name")

        if projekt_xml.attrib.get("version") is None:  # OLD FILES
            import_old(projekt_xml)
            main_window.project = classes.Project(main_window, name, author)
        else:
            import_new(projekt_xml, main_window)
            main_window.project = classes.Project(main_window, name, author)
            main_window.project.version = projekt_xml.attrib.get("version")
        fill_tree(main_window)


def import_new(projekt_xml: etree._Element, main_window: MainWindow) -> None:

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

            property_sets, ident_attrib = import_property_sets(xml_property_group)
            name, parent, identifer, is_concept = get_obj_data(xml_object)
            obj = classes.Object(name, ident_attrib, identifier=identifer)
            ident_dict[identifer] = obj

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
                node = graphs_window.Node(obj, graph_win)
                id_node_dict[identifier] = (node, xml_node)
            return id_node_dict

        graph_win: graphs_window.GraphWindow = graphs_window.GraphWindow(main_window, False)
        main_window.graph_window = graph_win
        id_node_dict = create_node_dict()

        for identifier, (node, xml_node) in id_node_dict.items():
            parent_id = xml_node.attrib.get(constants.PARENT)
            is_root = xml_node.attrib.get(constants.IS_ROOT)
            connection_type = xml_node.attrib.get(constants.CONNECTION)
            if parent_id != constants.NONE:
                parent_node: graphs_window.Node = id_node_dict[parent_id][0]
                parent_node.add_child(node, int(connection_type))
            if is_root == "True":
                scene = graphs_window.AggregationScene(node)
                graph_win.scenes.append(scene)

        graph_win.update_combo_list()
        for node in graph_win.root_nodes:
            graph_win.change_scene(node)

        for identifier, (node, xml_node) in id_node_dict.items():
            x_pos = xml_node.attrib.get(constants.X_POS)
            y_pos = xml_node.attrib.get(constants.Y_POS)
            node.setX(float(x_pos))
            node.setY(float(y_pos))

        graph_win.combo_box.setCurrentIndex(0)
        graph_win.combo_change()

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


def open_file_dialog(main_window: MainWindow, path: str = ""):
    if classes.Object:
        result = msg_delete_or_merge()
        if result is None:
            return
        elif result:
            main_window.clear_all()
            main_window.open_file(path)
        else:
            main_window.merge_new_file()
            main_window.open_file(path)

    else:
        main_window.open_file(path)


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
