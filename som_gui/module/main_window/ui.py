from PySide6.QtWidgets import QMainWindow, QApplication
from .qt import ui_MainWindow
from . import trigger
from som_gui.ressources.icons import get_icon


class MainWindow(QMainWindow):
    def __init__(self, application: QApplication):
        super(MainWindow, self).__init__()
        self.ui = ui_MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.app: QApplication = application
        self.setWindowIcon(get_icon())

    # Open / Close windows
    def closeEvent(self, event):
        result = trigger.close_event()
        if result:
            self.app.closeAllWindows()
            event.accept()
        else:
            event.ignore()

    def paintEvent(self, event):
        super().paintEvent(event)
        trigger.paint_event()
