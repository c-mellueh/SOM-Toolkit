from __future__ import annotations

import logging
import os

import ifcopenshell
import ifcopenshell.guid
from ifcopenshell.util import element
import SOMcreator

FILE_SPLIT = "; "
ELEMENT = "Element"
GROUP = "SubGroup"
IFC_REP = "IfcRep"
DESCRIPTION = "automatisch erzeugt"
NAME = "bauteilName"


def get_ifc_el_info(
    entity: ifcopenshell.entity_instance,
    property_bundle: tuple[str, str, str, str, str, str],
) -> tuple[str | None, str | None, str | None]:
    def check_for_existence(pset_name: str, property_name: str):
        pset_dict = psets.get(pset_name)
        if pset_dict is None:
            logging.warning(
                f"Für Entität '{entity.GlobalId}' konnte keine Gruppe erstellt werden da das Propertyset "
                f"'{pset_name}' nicht gefunden werden konnte"
            )
            return False, None
        value = pset_dict.get(property_name)

        if value is None:
            logging.warning(
                f"Für Entität '{entity.GlobalId}' konnte keine Gruppe erstellt werden da das Attribut "
                f"'{pset_name}:{property_name}' nicht gefunden werden konnte"
            )
            return False, None
        return True, value

    (
        main_pset,
        main_property,
        group_pset,
        group_property,
        identity_pset,
        identity_property,
    ) = property_bundle
    identity_property: str
    """-> Bauteilklassifikation, idGruppe"""
    psets = element.get_psets(entity)

    check_1, attrib = check_for_existence(main_pset, main_property)
    check_2, gruppe = check_for_existence(group_pset, group_property)
    check_3, identity = check_for_existence(identity_pset, identity_property)

    if all((check_1, check_2, check_3)):
        return attrib, gruppe, identity
    else:
        return None, None, None


def create_structure_dict(
    ifc_file: ifcopenshell.file,
    project: SOMcreator.SOMProject,
    property_bundle: tuple[str, str, str, str, str, str],
) -> dict:
    """Iterate over all Entities, build the targeted Datastructure"""
    targeted_group_structure = {GROUP: {}, ELEMENT: {}, IFC_REP: None}
    bk_dict = {som_class.ident_value: som_class for som_class in project.get_classes(filter=True)}

    for index, el in enumerate(list(ifc_file.by_type("IfcElement"))):
        attrib, gruppe, identity = get_ifc_el_info(el, property_bundle)
        if attrib is None or gruppe is None:
            continue

        parts = gruppe.upper().split("_")
        focus_dict = targeted_group_structure
        for part in parts:
            if part not in focus_dict[GROUP]:
                focus_dict[GROUP][part] = {GROUP: {}, ELEMENT: list(), IFC_REP: None}
            focus_dict = focus_dict[GROUP][part]

        som_class: SOMcreator.SOMClass = bk_dict.get(attrib)
        abbrev = som_class.abbreviation
        if abbrev.upper() not in focus_dict[GROUP]:
            focus_dict[GROUP][abbrev] = {GROUP: {}, ELEMENT: list(), IFC_REP: None}
        focus_dict[GROUP][abbrev][ELEMENT].append(el)
    return targeted_group_structure


def fill_existing_groups(
    ifc_file: ifcopenshell.file,
    structure_dict: dict,
    property_bundle: tuple[str, str, str, str, str, str],
) -> None:
    """Take existing Groups by identity property and sort them into the Datastructure"""

    for group in ifc_file.by_type("IfcGroup"):
        attrib, gruppe, identity = get_ifc_el_info(group, property_bundle)
        if identity is None:
            continue
        parts = identity.upper().split("_")
        focus_dict = structure_dict
        skip = False
        for part in parts:
            if part in focus_dict[GROUP] and not skip:
                focus_dict = focus_dict[GROUP][part]
            else:
                skip = True
        if skip:
            continue

        focus_dict[IFC_REP] = group


def create_aggregation_structure(
    ifc_file: ifcopenshell.file,
    structure: dict,
    id_gruppe: list[str],
    parent_group,
    is_sammler: bool,
    property_bundle,
    owner_history,
    abbreviation_dict:dict[str, SOMcreator.SOMClass],
    fill_with_empty_values: bool,
    som_class=None,
):
    """Take targeted group structure and build it in IFC-File"""

    (
        main_pset,
        main_property,
        group_pset,
        group_property,
        identity_pset,
        identity_property,
    ) = property_bundle

    def create_ifc_property(property_name: str, value: str):
        if value is None:
            prop = ifc_file.create_entity(
                "IfcPropertySingleValue", property_name, DESCRIPTION, None, None
            )
        else:
            prop = ifc_file.create_entity(
                "IfcPropertySingleValue",
                property_name,
                DESCRIPTION,
                ifc_file.create_entity("IfcLabel", value),
                None,
            )
        return prop

    def create_ifc_pset(
        pset_name,
        property_dict: dict[str, str],
        relating_entity: ifcopenshell.entity_instance | None = None,
    ):
        properties = list()
        for property_name, value in property_dict.items():
            properties.append(create_ifc_property(property_name, value))
        pset = ifc_file.create_entity(
            "IfcPropertySet",
            ifcopenshell.guid.new(),
            owner_history,
            pset_name,
            DESCRIPTION,
            properties,
        )
        if relating_entity is not None:
            ifc_file.create_entity(
                "IfcRelDefinesByProperties",
                ifcopenshell.guid.new(),
                owner_history,
                f"Relationship {pset_name}",
                DESCRIPTION,
                [relating_entity],
                pset,
            )
        return pset

    def fill_group_with_empty_values(
        ifc_group: ifcopenshell.entity_instance,
        group_class: SOMcreator.SOMClass,
        identity,
    ):
        for pset in group_class.get_property_sets(filter=True):
            proeprties = {
                som_property.name: None for som_property in pset.get_properties(filter=True)
            }
            if pset.name == main_pset:
                proeprties[main_property] = group_class.ident_value
                proeprties[NAME] = group_class.name
                proeprties[identity_property] = "_".join(identity)

            if pset.name == group_pset:
                proeprties[group_property] = "_".join(identity[:-2])
            create_ifc_pset(pset.name, proeprties, ifc_group)

    def create_ifc_group(
        group_class: SOMcreator.SOMClass,
        group_name: str,
        identity: list[str],
        parent: ifcopenshell.entity_instance = None,
    ) -> ifcopenshell.entity_instance:
        logging.info(f"create_new_group: {group_name}")
        ifc_group = ifc_file.create_entity(
            "IfcGroup", ifcopenshell.guid.new(), owner_history, group_name, DESCRIPTION
        )
        ifc_file.create_entity(
            "IfcRelAssignsToGroup",
            ifcopenshell.guid.new(),
            owner_history,
            group_class.name,
            DESCRIPTION,
            [],
            None,
            ifc_group,
        )

        if not is_sammler and fill_with_empty_values:
            fill_group_with_empty_values(ifc_group, group_class, identity)
        else:
            properties = dict()
            properties[main_property] = group_class.ident_value
            properties[NAME] = group_class.name
            properties[identity_property] = "_".join(identity)
            create_ifc_pset(main_pset, properties, ifc_group)
            properties = dict()
            if is_sammler:
                properties[group_property] = "_".join(identity[:-1])
            else:
                properties[group_property] = "_".join(identity[:-2])
            if group_pset in [
                pset.name for pset in group_class.get_property_sets(filter=True)
            ]:
                create_ifc_pset(group_pset, properties, ifc_group)

        if parent is not None:
            for is_grouped_relation_ship in parent.IsGroupedBy:
                is_grouped_relation_ship[4] = list(is_grouped_relation_ship[4]) + [
                    ifc_group
                ]
                return ifc_group
        return ifc_group

    for abbreviation in structure[GROUP]:
        ifc_rep = structure[GROUP][abbreviation][IFC_REP]
        new_id_gruppe = id_gruppe + [abbreviation]
        if is_sammler:
            som_class = abbreviation_dict.get(abbreviation.upper())
            if som_class is None:
                continue
            name = som_class.name
        else:
            name = f"{som_class.name}_{abbreviation}"
        if ifc_rep is None:
            group = create_ifc_group(som_class, name, new_id_gruppe, parent_group)
            structure[GROUP][abbreviation][IFC_REP] = group
        else:
            group = ifc_rep
        create_aggregation_structure(
            ifc_file,
            structure[GROUP][abbreviation],
            new_id_gruppe,
            group,
            not is_sammler,
            property_bundle,
            owner_history,
            abbreviation_dict,
            fill_with_empty_values,
            som_class,
        )

    if not is_sammler:
        for relation_ship in parent_group.IsGroupedBy:
            relation_ship[4] = list(
                set(relation_ship[4]).union(set(structure[ELEMENT]))
            )
        return


def main(
    ifc_path: os.PathLike | str,
    export_path: os.PathLike | str,
    project: SOMcreator.SOMProject,
    main_pset: str,
    main_property: str,
    group_pset: str,
    group_property: str,
    identity_pset: str,
    identity_property: str,
    fill_with_empty_values=False,
):
    ifc_file = ifcopenshell.open(ifc_path)
    owner_history = list(ifc_file.by_type("IfcOwnerHistory"))[0]
    property_bundle = (
        main_pset,
        main_property,
        group_pset,
        group_property,
        identity_pset,
        identity_property,
    )

    targeted_group_structure = create_structure_dict(
        ifc_file, project, property_bundle
    )
    fill_existing_groups(ifc_file, targeted_group_structure, property_bundle)
    kuerzel_dict = {
        som_class.abbreviation.upper(): som_class for som_class in project.get_classes(filter=True)
    }
    create_aggregation_structure(
        ifc_file,
        targeted_group_structure,
        [],
        None,
        True,
        property_bundle,
        owner_history,
        kuerzel_dict,
        fill_with_empty_values,
        None,
    )
    ifc_file.write(export_path)
