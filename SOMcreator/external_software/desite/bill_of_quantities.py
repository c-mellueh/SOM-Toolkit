from __future__ import annotations
import csv
from ... import classes


def get_distinct_attributes(property_sets: list[classes.PropertySet]):
    attribute_names = list()

    for property_set in property_sets:
        attribute: classes.Attribute
        attribute_names += [attribute.name for attribute in property_set.attributes]

    distinct_attribute_names = list(dict.fromkeys(attribute_names))

    return distinct_attribute_names


def export_boq(project: classes.Project, path: str, pset_name: str) -> None:
    if not path:
        return

    with open(path, "w", ) as file:
        writer = csv.writer(file, delimiter=";")
        property_sets = [property_set for property_set in classes.PropertySet if
                         property_set.name == pset_name]
        distinct_attribute_names = get_distinct_attributes(property_sets)
        header = ["Ident", "Object"] + [f"{pset_name}:{name}" for name in distinct_attribute_names]
        writer.writerow(header)

        for obj in project.objects:
            if pset_name not in [pset.name for pset in obj.property_sets]:
                continue

            property_set = obj.get_property_set_by_name(pset_name)
            ident = obj.ident_attrib
            line = [f"{ident.property_set.name}:{ident.name}", ident.value[0]]

            for attribute_name in distinct_attribute_names:
                attribute: classes.Attribute = property_set.get_attribute_by_name(attribute_name)

                if attribute is not None:
                    line.append("|".join(attribute.value))
                else:
                    line.append("")
            writer.writerow(line)
