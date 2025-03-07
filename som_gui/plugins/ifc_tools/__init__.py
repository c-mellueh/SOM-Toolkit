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
        module.load_ui_triggers()

def deactivate():
    pass

if __name__ == "__main__":
    pass
