from PySide6.QtWidgets import QTabWidget, QVBoxLayout, QDialog


class Dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.West)
        self.layout().addWidget(self.tab_widget)
