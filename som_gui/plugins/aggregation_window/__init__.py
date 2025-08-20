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
        module.activate()


def deactivate():
    logging.info("Deactivate Aggregation Window")
    from som_gui import tool

    submodules = tool.Plugins.get_submodules("aggregation_window")
    for name, module in submodules:
        module.deactivate()


def on_new_project():
    logging.info("New Project handling Aggregation")
    from som_gui import tool

    submodules = tool.Plugins.get_submodules("aggregation_window")
    for _, module in submodules:
        module.on_new_project()


def retranslate_ui():
    logging.info("Retranslate Aggregation Window")
    from som_gui import tool

    submodules = tool.Plugins.get_submodules("aggregation_window")
    for name, module in submodules:
        module.retranslate_ui()


if __name__ == "__main__":
    pass
