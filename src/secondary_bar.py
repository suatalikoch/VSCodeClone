from PyQt6.QtWidgets import QWidget

class SecondaryBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setAutoFillBackground(True)
        self.setObjectName("SecondaryBar")
        