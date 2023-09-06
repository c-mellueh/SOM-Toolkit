# __main__.py
from som_gui import main_window,logs
import os
import logging
from logging import config
from PySide6.QtWidgets import QApplication
import sys


def main(initial_file: str | None = None):
    def start_log() -> None:
        if os.path.exists(logs.LOG_PATH):
            os.remove(logs.LOG_PATH)
        config.fileConfig(logs.CONF_PATH, defaults={'logfilename': logs.LOG_PATH.replace("\\", "/")})
    start_log()
    app = QApplication(sys.argv)
    window = main_window.MainWindow(app, initial_file)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()