from __future__ import annotations

import logging
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from desiteRuleCreator.main_window import MainWindow
import openpyxl
from openpyxl.cell.cell import Cell
from openpyxl.worksheet.worksheet import Worksheet
from desiteRuleCreator.data import classes, constants
from desiteRuleCreator.Filehandling import open_file
from desiteRuleCreator.Windows import graphs_window



def transform_value_types(value: str) -> (str, bool):
    special = False
    if value is not None:
        if value.lower() in ["string", "str"]:
            data_type = constants.XS_STRING
        elif value.lower() in ["double"]:
            data_type = constants.XS_DOUBLE
        elif value.lower() in ["boolean", "bool"]:
            data_type = constants.XS_BOOL
        elif value.lower() in ["int", "integer"]:
            data_type = constants.XS_INT
        else:
            special = True
            data_type = constants.XS_STRING
    else:
        data_type = constants.XS_STRING

    return data_type, special


def split_string(text: str) -> list[str] | None:
    if text is None:
        return None
    text = text.split(";")
    for i, item in enumerate(text):
        if "(" in item:
            item = item.split("(")
            text[i] = item[0]
        text[i] = text[i].strip()

    return text


def link_psets(cell: Cell, pset_dict: dict[str, [classes.PropertySet, Cell, classes.Object]],
               sheet: Worksheet, obj: classes.Object = None) -> None:
    parent_text = sheet.cell(cell.row + 2, cell.column + 1).value
    parent_list = split_string(parent_text)

    for text in parent_list:
        if text != "AE" and text != "-":
            value = pset_dict.get(text.upper())
            if value is not None:
                [eltern_pset, eltern_cell, dummy] = value
                if obj is not None:
                    new_pset = classes.PropertySet(eltern_pset.name)
                    eltern_pset.add_child(new_pset)
                    obj.add_property_set(new_pset)
                link_psets(eltern_cell, pset_dict, sheet, obj)
            else:
                logging.warning(
                    f"[{sheet.cell(cell.row, cell.column + 1).value}] Elternklasse: Kürzel {text.upper()} existiert nicht!")


def iterate_attributes(pset: classes.PropertySet, sheet: Worksheet, entry: Cell, cell_list: list[Cell]) -> None:
    """ 
    Iterate over Attributes
    Create Them and find special Datatypes
    """
    while entry.value is not None and entry not in cell_list:
        data_type_text = sheet.cell(row=entry.row, column=entry.column + 2).value
        attribute_name = entry.value
        data_type, special = transform_value_types(data_type_text)
        classes.Attribute(pset, attribute_name, [""], constants.VALUE_TYPE_LOOKUP[constants.LIST], data_type=data_type)
        if special:
            logging.warning(f"[{entry.value}] Property: {pset.name}:{attribute_name} datatype '{data_type_text}' unbekannt")
            pass

        entry = sheet.cell(row=entry.row + 1, column=entry.column)


def create_predefined_pset(sheet: Worksheet, cell: Cell, cell_list: list[Cell]) -> (classes.PropertySet, str):
    name = sheet.cell(row=cell.row, column=cell.column + 1).value
    abbreviation = sheet.cell(row=cell.row + 1, column=cell.column + 1).value.upper()

    pset = classes.PropertySet(name)
    entry = sheet.cell(row=cell.row + 4, column=cell.column)
    iterate_attributes(pset, sheet, entry, cell_list)
    return pset, abbreviation


def create_object(sheet: Worksheet, cell: Cell, pset_dict: dict[str, (classes.PropertySet, Cell, classes.Object)],
                  cell_list: list[Cell]) -> (classes.Object, classes.PropertySet, str, list[str]):
    name = sheet.cell(row=cell.row, column=cell.column + 1).value
    abbreviation = sheet.cell(row=cell.row + 1, column=cell.column + 1).value.upper()
    aggregate_children = sheet.cell(row=cell.row + 3, column=cell.column + 1).value
    ident = sheet.cell(row=cell.row, column=cell.column + 2).value

    pset = classes.PropertySet(name)

    entry = sheet.cell(row=cell.row + 5, column=cell.column)
    iterate_attributes(pset, sheet, entry, cell_list)

    ident_pset = classes.PropertySet("Allgemeine Eigenschaften")
    parent: classes.PropertySet = pset_dict["AE"][0]
    parent.add_child(ident_pset)
    ident_attrib: classes.Attribute = ident_pset.get_attribute_by_name("bauteilKlassifikation")

    ident_attrib.value = [ident]
    obj = classes.Object(name, ident_attrib)
    obj.add_property_set(ident_pset)
    obj.add_property_set(pset)

    aggregate_list = split_string(aggregate_children)
    if aggregate_list is None:
        logging.error(f"Achtung! {name} besitzt keinen Wert bei 'Besteht aus'")
        aggregate_list = []
    elif aggregate_list == ["-"]:
        aggregate_list = []

    return obj, pset, abbreviation, aggregate_list


def find_base_cells(sheet: Worksheet) -> list[Cell]:
    name_cells = list()

    row: tuple[Cell]
    for row in sheet:
        for cell in row:
            if cell.value is not None:
                text = cell.value.strip()
                if text in ["name", "name:"]:
                    if sheet.cell(cell.row + 1, cell.column).value == "Kürzel":
                        name_cells.append(cell)
                    else:
                        logging.error(f"{sheet.cell(cell.row + 1, cell.column)} hat den Wert 'name'")
    return name_cells


def create_items(sheet: Worksheet, base_cells: list[Cell]) ->(dict[str, (classes.PropertySet, Cell, classes.Object)],dict[classes.Object, list[str]]):
    pset_dict: dict[str, (classes.PropertySet, Cell, classes.Object)] =dict()
    aggregate_dict: dict[classes.Object, list[str]] =dict()

    for cell in base_cells:
        ident_value = sheet.cell(row=cell.row, column=cell.column + 2).value

        if ident_value is None:
            pset, kuerzel = create_predefined_pset(sheet, cell, base_cells)
            pset_dict[kuerzel] = (pset, cell, None)


        else:
            obj, pset, kuerzel, aggregate_list = create_object(sheet, cell, pset_dict, base_cells)
            aggregate_dict[obj] = aggregate_list
            if pset_dict.get(kuerzel) is not None:
                logging.error(f"[{obj.name} | {pset_dict[kuerzel][0].name}] Kuerzel: {kuerzel} identisch!")
            pset_dict[kuerzel] = (pset, cell, obj)

    return pset_dict,aggregate_dict

def build_tree(main_window) -> None:
    tree_dict: dict[str, classes.Object] = {obj.ident_attrib.value[0]:obj for obj in classes.Object}

    for ident, item in tree_dict.items():
        ident_list = ident.split(".")[:-1]
        parent_obj = tree_dict.get(".".join(ident_list))

        if parent_obj is not None:
            parent_obj.add_child(item)

    open_file.fill_tree(main_window)


def create_aggregation( pset_dict: dict[str, (classes.PropertySet, Cell, classes.Object)],
                 aggregate_dict: dict[classes.Object, list[str]],main_window:MainWindow) -> None:

    main_window.graph_window =graphs_window.GraphWindow(main_window,False)
    main_window.graph_window.import_excel(pset_dict,aggregate_dict)

    # node_dict = {obj:graphs_window.Node(obj) for obj in classes.Object}
    # print(node_dict)
    # for obj in classes.Object:
    #     node = node_dict[obj]
    #     aggregate_list = aggregate_dict[obj]
    #     if aggregate_list:
    #         scene = graphs_window.AggregationScene(node)
    #     for kuerzel in aggregate_list:
    #         dic = pset_dict.get(kuerzel)
    #         if dic is not None:
    #             obj_child = dic[2]
    #             if obj_child is not None:
    #                 node.add_child(node_dict[obj_child])
    #             else:
    #                 logging.error(f"[{obj.name}] Aggregation: Kürzel {kuerzel} existiert nicht")
    #         else:
    #             logging.error(f"[{obj.name}] Aggregation: Kürzel {kuerzel} existiert nicht")

def start(main_window, path: str) -> None:
    # TODO: add request for Identification Attribute

    book = openpyxl.load_workbook(path)
    sheet = book.active

    base_cells = find_base_cells(sheet)
    pset_dict,aggregate_dict = create_items(sheet,base_cells)

    for kuerzel, (pset, cell, obj) in pset_dict.items():
        link_psets(cell, pset_dict, sheet, pset.object)

    build_tree(main_window)
    create_aggregation(pset_dict,aggregate_dict,main_window)
