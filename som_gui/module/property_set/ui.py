from PySide6.QtWidgets import QTableWidget, QWidget, QLineEdit
from PySide6.QtCore import Qt
from PySide6 import QtGui
from som_gui.module import property_set
from .window import Ui_layout_main
from som_gui.icons import get_icon

class PsetTableWidget(QTableWidget):

    def __init__(self, parent: QWidget):
        super().__init__(parent)

    def paintEvent(self, event):
        super().paintEvent(event)
        property_set.trigger.repaint_event()


class PropertySetWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.widget = Ui_layout_main()
        self.widget.setupUi(self)
        self.widget.verticalLayout_2.setSpacing(2)
        self.widget.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.widget.verticalLayout_2.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setWindowIcon(get_icon())

    def paintEvent(self, event):
        super().paintEvent(event)
        property_set.trigger.repaint_pset_window(self)


class LineInput(QLineEdit):
    def __init__(self) -> None:
        super(LineInput, self).__init__()

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        super().keyPressEvent(event)
        # seperator = settings.get_seperator()
        # sep_bool = settings.get_seperator_status()
        # if not event.matches(QtGui.QKeySequence.StandardKey.Paste) and sep_bool:
        #     super(LineInput, self).keyPressEvent(event)
        #     return
        # text = QtGui.QGuiApplication.clipboard().text()
        # text_list = text.split(seperator)
        # if len(text_list) < 2:
        #     super(LineInput, self).keyPressEvent(event)
        #     return
        #
        # dif = len(text_list) - len(self.pset_window.input_lines2)
        # if dif >= 0:
        #     for i in range(dif + 1):
        #         self.pset_window.new_line()
        # for i, (text, lines) in enumerate(zip(text_list, self.pset_window.input_lines2.values())):
        #     text = text.strip()
        #     line: LineInput = lines[0]
        #     line.setText(text)
