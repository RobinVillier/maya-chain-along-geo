# Widget principal du template

from PySide2 import QtWidgets
from CustomAppTemplate.core.logic import run_template_logic


class CustomWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CustomWidget, self).__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        self.button = QtWidgets.QPushButton("Exécuter la logique template")
        self.button.clicked.connect(self.executer_template)
        layout.addWidget(self.button)

    def executer_template(self):
        run_template_logic()
