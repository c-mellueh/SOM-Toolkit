import logging
# name and description will be used for Settings Window
friendly_name = "Aggreation Window"
description = "UI for displaying Aggregations in UML-Style window"
author = "christoph.mellueh.de"

def activate():
    from som_gui import tool
    submodules = tool.Plugins.get_submodules("aggregation_window")
    logging.info("Activate Aggregation Window")
    
    for name, module in submodules:
        module.register()
    for name, module in submodules:
        module.load_ui_triggers()

def deactivate():
    logging.info("Deactivate Aggregation Window")

if __name__ == "__main__":
    pass
