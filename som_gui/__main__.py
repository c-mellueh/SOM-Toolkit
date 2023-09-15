# __main__.py
import logging
import os
import sys
from logging import config

from PySide6.QtWidgets import QApplication

from som_gui import main_window, logs


def start_log(state: int | None = None) -> None:
    if os.path.exists(logs.LOG_PATH):
        os.remove(logs.LOG_PATH)
    config.fileConfig(logs.CONF_PATH, defaults={'logfilename': logs.LOG_PATH.replace("\\", "/")})
    if state is None:
        return
    if logging.getLogger("root") is None:
        return
    sh_list = [handler for handler in logging.getLogger("root").handlers if isinstance(handler, logging.StreamHandler)]
    for handler in sh_list:
        handler.setLevel(state)


def main(initial_file: str | None = None):
    app = QApplication(sys.argv)
    window = main_window.MainWindow(app, initial_file)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    start_log()
    main()
