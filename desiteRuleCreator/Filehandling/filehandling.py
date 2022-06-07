from uuid import uuid4

from PySide6.QtWidgets import QFileDialog, QInputDialog, QLineEdit, QMessageBox
from lxml import etree

from desiteRuleCreator import __version__ as project_version
from desiteRuleCreator.Windows.popups import msg_delete_or_merge
from desiteRuleCreator.Windows.popups import msg_unsaved, msg_close
from desiteRuleCreator.data import classes, constants
from desiteRuleCreator.data.classes import Object, PropertySet, Attribute


# from .run import MainWindow

def string_to_bool(text):
    if text == str(True):
        return True
    elif text == str(False):
        return False
    else:
        return None


def fill_tree(main_window):
    def fill_next_level(objects, item_dict):

        new_item_dict = dict()
        for el in objects:
            parent_widget = item_dict.get(el.parent)
            if parent_widget is not None:
                tree_widget_item = main_window.add_object_to_tree(el, parent_widget)
                new_item_dict[el] = tree_widget_item

        objects = [obj for obj in objects if obj not in new_item_dict.keys()]

        if objects:
            fill_next_level(objects, new_item_dict)

    item_dict = dict()
    objects = Object.iter

    for obj in objects:
        if obj.parent is None:
            tree_widget_item = main_window.add_object_to_tree(obj)
            item_dict[obj] = tree_widget_item

    objects = [obj for obj in objects if obj not in item_dict.keys()]

    fill_next_level(objects, item_dict)


def import_data(widget, path: str = False):
    if path:
        widget.clear_object_input()

        tree = etree.parse(path)
        projekt_xml = tree.getroot()

        if projekt_xml.attrib.get("version") is None:  # OLD FILES
            import_old(projekt_xml)
            widget.project = classes.Project(projekt_xml.attrib.get("Name"), author="CMellueh")
        else:
            import_new(projekt_xml)
            widget.project = classes.Project(projekt_xml.attrib.get("name"))
        fill_tree(widget)
        widget.ui.tree.resizeColumnToContents(0)
        widget.save_path = path

        widget.setWindowTitle(widget.project.name)


def import_new(projekt_xml):
    def import_property_sets(xml_property_sets) -> (list[PropertySet], Attribute):
        property_sets = list()
        ident_attrib = None

        for xml_property_set in xml_property_sets:
            attribs = xml_property_set.attrib
            name = attribs.get(constants.NAME)
            identifier = attribs.get(constants.IDENTIFIER)
            property_set = PropertySet(name, obj=None, identifier=identifier)
            value = import_attributes(xml_property_set, property_set)
            if value is not None:
                ident_attrib = value
            property_sets.append(property_set)
        return property_sets, ident_attrib

    def import_attributes(xml_object, property_set):
        def transform_new_values(xml_attribute):
            value_type = xml_attribute.attrib.get("value_type")
            value = list()

            if value_type != constants.RANGE:
                for xml_value in xml_attribute:
                    value.append(xml_value.text)

            else:
                for xml_range in xml_attribute:
                    from_to_list = list()
                    for xml_value in xml_range:
                        if xml_value.tag == "From":
                            from_to_list.append(xml_value.text)
                        if xml_value.tag == "To":
                            from_to_list.append(xml_value.text)
                    value.append(from_to_list)
            return value

        ident_attrib = None
        for xml_attribute in xml_object:
            if xml_attribute.tag == "Attribute":
                attribs = xml_attribute.attrib
                name = attribs.get(constants.NAME)
                identifier = attribs.get(constants.IDENTIFIER)
                data_type = attribs.get(constants.DATA_TYPE)
                value_type = attribs.get(constants.VALUE_TYPE)
                is_identifier = attribs.get(constants.IS_IDENTIFIER)
                child_inh = string_to_bool(attribs.get(constants.CHILD_INHERITS_VALUE))
                value = transform_new_values(xml_attribute)
                attrib = Attribute(property_set, name, value, value_type, data_type, child_inh, identifier)
                if is_identifier == str(True):
                    ident_attrib = attrib
        return ident_attrib

    def import_scripts(xml_script, obj):
        name = xml_script.attrib.get("name")
        code = xml_script.text
        script = classes.Script(name, obj)
        script.code = code

    def get_obj_data(xml_object):

        name = xml_object.attrib.get(constants.NAME)
        parent = xml_object.attrib.get(constants.PARENT)
        identifier = xml_object.attrib.get(constants.IDENTIFIER)
        is_concept = xml_object.attrib.get(constants.IS_CONCEPT)
        if is_concept == "True":
            value = True
        else:
            value = False
        is_concept = value
        return name, parent, identifier, is_concept

    def create_ident_dict(item_list):
        return {item.identifier: item for item in item_list}

    def link_parents(xml_predefined_psets, xml_objects):
        def iterate(xml_property_set_dict, xml_object_dict, xml_attribute_dict):
            for xml_predefined_pset in xml_predefined_psets:
                fill_dict(xml_property_set_dict, xml_predefined_pset)
                for xml_attribute in xml_predefined_pset:
                    fill_dict(xml_attribute_dict, xml_attribute)

            for xml_object in xml_objects:
                fill_dict(xml_object_dict, xml_object)
                for xml_property_set in xml_object:
                    fill_dict(xml_property_set_dict, xml_property_set)
                    for xml_attribute in xml_property_set:
                        fill_dict(xml_attribute_dict, xml_attribute)

        def fill_dict(xml_dict, xml_obj):
            xml_dict[xml_obj.attrib.get(constants.IDENTIFIER)] = xml_obj.attrib.get(constants.PARENT)

        def create_link(obj_dict, xml_dict):
            for ident, obj in obj_dict.items():

                parent_ident = xml_dict[str(ident)]
                parent = obj_dict.get(parent_ident)
                if parent is not None:
                    parent.add_child(obj, copy=False)

        xml_property_set_dict = dict()
        xml_object_dict = dict()
        xml_attribute_dict = dict()
        iterate(xml_property_set_dict, xml_object_dict, xml_attribute_dict)

        obj_dict = create_ident_dict(Object.iter)
        property_set_dict = create_ident_dict(PropertySet.iter)
        attribute_dict = create_ident_dict(Attribute.iter)

        create_link(obj_dict, xml_object_dict)
        create_link(attribute_dict, xml_attribute_dict)
        create_link(property_set_dict, xml_property_set_dict)

    xml_predefined_psets = [x for x in projekt_xml if x.tag == constants.PREDEFINED_PSET]
    xml_objects = [x for x in projekt_xml if x.tag == constants.OBJECT]

    import_property_sets(xml_predefined_psets)

    for xml_object in xml_objects:
        xml_property_sets = [x for x in xml_object if x.tag == constants.PROPERTY_SET]
        xml_scripts = [x for x in xml_object if x.tag == constants.SCRIPT]
        property_sets, ident_attrib = import_property_sets(xml_property_sets)
        name, parent, identifer, is_concept = get_obj_data(xml_object)
        obj = Object(name, ident_attrib, is_concept, identifier=identifer)

        for property_set in property_sets:
            obj.add_property_set(property_set)

        for xml_script in xml_scripts:
            import_scripts(xml_script, obj)

    link_parents(xml_predefined_psets, xml_objects)


def import_old(projekt_xml):
    def handle_identifier(xml_object):
        attributes = xml_object.attrib
        identifier_string: str = attributes.get("Identifier")
        property_set = PropertySet(identifier_string.split(":")[0])
        attribute = Attribute(property_set, identifier_string.split(":")[1], [attributes.get("Name")],
                              constants.LIST)
        return attribute

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
        obj = Object(fd, str(uuid4()), None, True)
        fachdisziplinen_dict[fd] = obj

    for xml_object in projekt_xml:

        if xml_object.tag == "Objekt":
            ident_attrib = handle_identifier(xml_object)

            group_name = xml_object.attrib.get("Fachdisziplin")
            obj = Object(xml_object.attrib.get("Name"), ident_attrib)
            obj.add_attribute(ident_attrib)
            obj.parent = fachdisziplinen_dict[group_name]

            for xml_property_set in xml_object:
                pset_name = xml_property_set.attrib.get("Name")
                if pset_name in obj.psetNameDict:
                    property_set = obj.psetNameDict[pset_name]
                else:
                    property_set = PropertySet(pset_name)

                for xml_attribute in xml_property_set:
                    attrib = xml_attribute.attrib
                    name = attrib.get("Name")
                    value_type = transform_value_types(attrib.get("Art"))
                    data_type = attrib.get("Datentyp")

                    value = transform_values(xml_attribute, value_type)
                    atrb = Attribute(property_set, name, value, value_type, data_type)
                    obj.add_attribute(atrb)


def save_as_clicked(main_window):
    if main_window.save_path is not None:
        path = \
            QFileDialog.getSaveFileName(main_window, "Save XML", main_window.save_path, "xml Files (*.xml *.DRCxml)")[0]
    else:
        path = QFileDialog.getSaveFileName(main_window, "Save XML", "", "xml Files (*.xml *.DRCxml)")[0]

    if path:
        main_window.save(path)
    return path


def save(main_window, path):
    def add_parent(xml_object, obj):
        if obj.parent is not None:
            xml_object.set(constants.PARENT, str(obj.parent.identifier))
        else:
            xml_object.set(constants.PARENT, constants.NONE)

    def add_predefined_property_sets(xml_project):
        for predefined_pset in classes.PropertySet.iter:
            if predefined_pset.object is None:
                predefined_pset: classes.PropertySet = predefined_pset
                xml_pset = etree.SubElement(xml_project, constants.PREDEFINED_PSET)
                xml_pset.set(constants.NAME, predefined_pset.name)
                xml_pset.set(constants.IDENTIFIER, str(predefined_pset.identifier))
                xml_pset.set(constants.PARENT, constants.NONE)

                for attribute in predefined_pset.attributes:
                    add_attribute(attribute, predefined_pset, xml_pset)

    def add_property_set(property_set: PropertySet, xml_object):
        xml_pset = etree.SubElement(xml_object, constants.PROPERTY_SET)
        xml_pset.set(constants.NAME, property_set.name)
        xml_pset.set(constants.IDENTIFIER, str(property_set.identifier))
        add_parent(xml_pset, property_set)

        for attribute in property_set.attributes:
            add_attribute(attribute, property_set, xml_pset)

    def add_object(obj: Object, xml_project):
        xml_object = etree.SubElement(xml_project, constants.OBJECT)
        xml_object.set(constants.NAME, obj.name)
        xml_object.set(constants.IDENTIFIER, obj.identifier)
        xml_object.set("is_concept", str(obj.is_concept))
        add_parent(xml_object, obj)

        for property_set in obj.property_sets:
            add_property_set(property_set, xml_object)

        for script in obj.scripts:
            script: classes.Script = script
            xml_script = etree.SubElement(xml_object, "Script")
            xml_script.set(constants.NAME, script.name)
            xml_script.text = script.code
        pass

    def add_attribute(attribute, property_set, xml_pset):
        xml_attribute = etree.SubElement(xml_pset, constants.ATTRIBUTE)
        xml_attribute.set(constants.NAME, attribute.name)
        xml_attribute.set(constants.DATA_TYPE, attribute.data_type)
        xml_attribute.set(constants.VALUE_TYPE, attribute.value_type)
        xml_attribute.set(constants.IDENTIFIER, str(attribute.identifier))
        xml_attribute.set(constants.CHILD_INHERITS_VALUE, str(attribute.child_inherits_values))
        add_parent(xml_attribute, attribute)

        obj = property_set.object
        if obj is not None and attribute == obj.ident_attrib:
            ident = True
        else:
            ident = False

        xml_attribute.set(constants.IS_IDENTIFIER, str(ident))
        add_value(attribute, xml_attribute)

    def add_value(attribute, xml_attribute):
        values = attribute.value
        for value in values:
            xml_value = etree.SubElement(xml_attribute, "Value")
            if attribute.value_type == constants.RANGE:
                xml_from = etree.SubElement(xml_value, "From")
                xml_to = etree.SubElement(xml_value, "To")
                xml_from.text = str(value[0])
                if len(value) > 1:
                    xml_to.text = str(value[1])
            else:
                xml_value.text = str(value)

    main_window.save_path = path

    xml_project = etree.Element(constants.PROJECT)
    xml_project.set(constants.NAME, main_window.project.name)
    xml_project.set(constants.VERSION, project_version)

    add_predefined_property_sets(xml_project)
    for obj in Object.iter:
        add_object(obj, xml_project)

    tree = etree.ElementTree(xml_project)

    with open(path, "wb") as f:
        tree.write(f, pretty_print=True, encoding="utf-8", xml_declaration=True)

    main_window.project.reset_changed()


def save_clicked(main_window):
    if main_window.save_path is None:
        path = main_window.save_as_clicked()
    else:
        save(main_window, main_window.save_path)
        path = main_window.save_path
    return path


def new_file(main_window):
    new_file = msg_unsaved()
    if new_file:
        main_window.save_path = None
        project_name = QInputDialog.getText(main_window, "New Project", "new Project Name:", QLineEdit.Normal, "")

        if project_name[1]:
            main_window.project = classes.Project(project_name[0])
            main_window.setWindowTitle(main_window.project.name)
            main_window.project.name = project_name[0]
            main_window.clear_all()


def open_file_dialog(main_window, path=False):
    if Object.iter:
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


def close_event(main_window, event):
    status = main_window.project.changed
    if status:
        reply = msg_close()
        if reply == QMessageBox.Save:
            path = main_window.save_clicked()
            if not path or path is None:
                return False
            else:
                return True
        elif reply == QMessageBox.No:
            return True
        else:
            return False
    else:
        return True
