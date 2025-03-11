import copy

import SOMcreator
from SOMcreator import SOMProject, UseCase, Phase


def merge_projects(
    existing_project: SOMProject,
    import_project: SOMProject,
    phase_mapping: dict[Phase, Phase],
    use_case_mapping: dict[UseCase, UseCase],
):
    """

    :param existing_project: Existing Project
    :param import_project: Project that will be imported into existing Project
    :param phase_mapping: mapping Dict import Phase as Key existing Phase as Value
    :param use_case_mapping: mapping Dict import UseCase as Key existing UseCase as Value
    :return:
    """
    existing_identifiers = {
        o.ident_value for o in existing_project.get_classes(filter=False)
    }
    import_predef_pset_dict = {
        p: p for p in import_project.get_predefined_psets(filter=False)
    }
    existing_predefined_pset_name_dict = {
        p.name: p for p in existing_project.get_predefined_psets(filter=False)
    }

    for import_predef_pset in import_predef_pset_dict.keys():
        new_pset = existing_predefined_pset_name_dict.get(import_predef_pset.name)
        if not new_pset:
            _add_item(
                existing_project,
                import_project,
                import_predef_pset,
                phase_mapping,
                use_case_mapping,
            )
        else:
            import_predef_pset_dict[import_predef_pset] = new_pset

    for som_class in import_project.get_classes(filter=False):
        if som_class.ident_value not in existing_identifiers:
            _import_class(
                existing_project,
                import_project,
                som_class,
                import_predef_pset_dict,
                phase_mapping,
                use_case_mapping,
            )

    existing_project.plugin_dict = _merge_dicts(
        existing_project.plugin_dict, import_project.plugin_dict
    )
    existing_project.import_dict = _merge_dicts(
        existing_project.import_dict, import_project.import_dict
    )


def _calculate_new_filter_matrix(
    filter_matrix,
    existing_project: SOMProject,
    import_project: SOMProject,
    item,
    phase_mapping,
    use_case_mapping,
):
    for import_phase in import_project.get_phases():
        existing_phase = phase_mapping.get(import_phase)
        if existing_phase is None:
            continue

        for import_use_case in import_project.get_usecases():
            existing_use_case = use_case_mapping.get(import_use_case)
            if existing_use_case is None:
                continue
            phase_index = existing_project.get_phase_index(existing_phase)
            use_case_index = existing_project.get_usecase_index(existing_use_case)
            import_state = item.get_filter_state(import_phase, import_use_case)
            filter_matrix[phase_index][use_case_index] = import_state


def _merge_dicts(d1: dict, d2: dict):
    for key, value2 in d2.items():
        value1 = d1.get(key)
        if isinstance(value1, dict) and isinstance(value2, dict):
            _merge_dicts(value1, value2)
        elif value1 is None:
            d1[key] = value2
    return d1


def _add_item(
    existing_project: SOMcreator.SOMProject,
    import_project: SOMcreator.SOMProject,
    item,
    phase_mapping,
    use_case_mapping,
):
    new_filter_matrix = existing_project.create_filter_matrix(True)
    _calculate_new_filter_matrix(
        new_filter_matrix,
        existing_project,
        import_project,
        item,
        phase_mapping,
        use_case_mapping,
    )
    existing_project.add_item(item)
    item._project = existing_project
    item._filter_matrix = copy.deepcopy(new_filter_matrix)


def _import_class(
    existing_project: SOMcreator.SOMProject,
    import_project: SOMcreator.SOMProject,
    som_class: SOMcreator.SOMClass,
    old_predefined_psets_mapping,
    phase_mapping,
    use_case_mapping,
):
    _add_item(existing_project, import_project, som_class, phase_mapping, use_case_mapping)
    for property_set in som_class.get_property_sets(filter=False):
        _import_pset(
            existing_project,
            import_project,
            property_set,
            old_predefined_psets_mapping,
            phase_mapping,
            use_case_mapping,
        )

    for aggregation in som_class.aggregations:
        _add_item(
            existing_project,
            import_project,
            aggregation,
            phase_mapping,
            use_case_mapping,
        )


def _import_pset(
    existing_project,
    import_project,
    property_set: SOMcreator.SOMPropertySet,
    old_predefined_psets_mapping,
    phase_mapping,
    use_case_mapping,
):
    parent = old_predefined_psets_mapping.get(property_set.parent)
    _add_item(
        existing_project, import_project, property_set, phase_mapping, use_case_mapping
    )

    if parent is not None:
        property_set.parent = parent
        for som_property in property_set.get_properties(filter=False):
            _import_property(
                existing_project,
                import_project,
                som_property,
                phase_mapping,
                use_case_mapping,
                parent,
            )
    else:
        for som_property in property_set.get_properties(filter=False):
            _import_property(
                existing_project,
                import_project,
                som_property,
                phase_mapping,
                use_case_mapping,
            )


def _import_property(
    existing_project,
    import_project,
    som_property:SOMcreator.SOMProperty,
    phase_mapping,
    use_case_mapping,
    parent_pset: SOMcreator.SOMPropertySet = None,
):
    if parent_pset:
        parent_property = {
            a.name: a for a in parent_pset.get_properties(filter=False)
        }.get(som_property.name)
        if parent_property:
            som_property.parent = parent_property
    _add_item(
        existing_project, import_project, som_property, phase_mapping, use_case_mapping
    )
