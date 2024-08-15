class IfcToSQLProperties:
    ifc_file_name = ""
    project_name = ""
    guids: dict[str, str] = dict()
    main_attribute = ("", "")
    ifc = None
