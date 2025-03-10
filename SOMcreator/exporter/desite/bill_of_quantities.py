from __future__ import annotations
import csv
import SOMcreator


def get_distinct_property_names(property_sets: list[SOMcreator.SOMPropertySet]) ->list[str]:
    property_names = list()

    for property_set in property_sets:
        property_names += [
            som_property.name for som_property in property_set.get_properties(filter=True)
        ]

    distinct_names = list(dict.fromkeys(property_names))

    return distinct_names


def export_boq(project: SOMcreator.SOMProject, path: str, pset_name: str) -> None:
    if not path:
        return

    with open(
        path,
        "w",
    ) as file:
        writer = csv.writer(file, delimiter=";")
        property_sets = [
            property_set
            for property_set in SOMcreator.SOMPropertySet
            if property_set.name == pset_name
        ]
        distinct_property_names = get_distinct_property_names(property_sets)
        header = ["Ident", "Object"] + [
            f"{pset_name}:{name}" for name in distinct_property_names
        ]
        writer.writerow(header)

        for som_class in project.get_classes(filter=True):
            if pset_name not in [
                pset.name for pset in som_class.get_property_sets(filter=True)
            ]:
                continue

            property_set = som_class.get_property_set_by_name(pset_name)
            ident = som_class.identifier_property
            if not isinstance(ident,SOMcreator.SOMProperty):
                continue
            line = [f"{ident.property_set.name}:{ident.name}", ident.allowed_values[0]]

            for property_name in distinct_property_names:
                som_property: SOMcreator.SOMProperty = property_set.get_property_by_name(
                    property_name
                )

                if som_property is not None:
                    line.append("|".join(som_property.allowed_values))
                else:
                    line.append("")
            writer.writerow(line)
