# name and description will be used for Settings Window
import logging

friendly_name = "IFC-Tools"
description = "UI for manipulating IFC-Files"
author = "christoph@mellueh.de"


def activate():
    from som_gui import tool

    submodules = tool.Plugins.get_submodules("ifc_tools")
    logging.info("Activate IFCTools")

    for name, module in submodules:
        module.register()
    for name, module in submodules:
        module.activate()


def deactivate():
    from som_gui import tool

    submodules = tool.Plugins.get_submodules("ifc_tools")
    logging.info("Deactivate IFCTools")

    for name, module in submodules:
        module.register()
    for name, module in submodules:
        module.deactivate()


def retranslate_ui():
    logging.info("Retranslate IFCTools")
    from som_gui import tool

    submodules = tool.Plugins.get_submodules("ifc_tools")
    for name, module in submodules:
        module.retranslate_ui()


if __name__ == "__main__":
    pass
