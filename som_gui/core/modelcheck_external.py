from __future__ import annotations
from typing import TYPE_CHECKING, Type
if TYPE_CHECKING:
    from som_gui import tool

def open_window(modelcheck_external: Type[tool.ModelcheckExternal], modelcheck_window: Type[tool.ModelcheckWindow],
                project: Type[tool.Project]):
    if modelcheck_external.is_window_allready_build():
        modelcheck_external.get_window().show()
        return

    window = modelcheck_external.create_window()
    check_box_widget = modelcheck_window.create_checkbox_widget()
    window.setCentralWidget(check_box_widget)
    main_pset_name, main_attribute_name = project.get().get_main_attribute()
    modelcheck_window.connect_check_widget(check_box_widget)
    modelcheck_external.create_menubar(window, main_pset_name, main_attribute_name)
    window.show()
