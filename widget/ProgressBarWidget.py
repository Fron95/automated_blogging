# progressbar_widget.py
from PySide6.QtWidgets import QProgressBar

class ProgressBarWidget(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("progressBar")
        self.setGeometry(40, 950, 231, 41)
        self.setMaximum(104)
        self.setValue(0)
