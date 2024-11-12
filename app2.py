import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget

class CustomTitleBar(QWidget):
    def __init__(self):
        super().__init__()

        layout = QGridLayout()

        widget = QWidget()
        #widget.setFixedSize(16, 16)
        widget.setStyleSheet("background-color: black;")

        widget1 = QWidget()
        #widget1.setFixedSize(16, 16)
        widget1.setStyleSheet("background-color: black;")

        widget2 = QWidget()
        #widget2.setFixedSize(16, 16)
        widget2.setStyleSheet("background-color: black;")

        layout.addWidget(widget, 0, 0, 1, 1)
        layout.addWidget(widget1, 0, 1, 1, 1)
        layout.addWidget(widget2, 0, 2, 1, 1)

        layout.setColumnStretch(0, 1)  # Left widget will take minimal space
        layout.setColumnStretch(1, 2)  # Center widget will take most of the space
        layout.setColumnStretch(2, 1)  # Right widget will take minimal space

        self.setFixedHeight(34)
        self.setAutoFillBackground(True)
        self.setStyleSheet("background-color: red;")

        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(1280, 720)

        title_bar = CustomTitleBar()

        activity_bar = QWidget()
        activity_bar.setFixedWidth(46)
        activity_bar.setStyleSheet("background-color: orange;")

        side_bar = QWidget()
        side_bar.setFixedWidth(256)
        side_bar.setStyleSheet("background-color: pink;")

        content = QWidget()
        content.setStyleSheet("background-color: lightblue;")

        secondary_bar = QWidget()
        secondary_bar.setFixedWidth(256)
        secondary_bar.setStyleSheet("background-color: purple;")

        status_bar = QWidget()
        status_bar.setFixedHeight(22)
        status_bar.setStyleSheet("background-color: green;")

        layout = QGridLayout()
        layout.setContentsMargins(6, 6, 6, 6)

        layout.addWidget(title_bar, 0, 0, 1, 4)
        layout.addWidget(activity_bar, 1, 0, 2, 1)
        layout.addWidget(side_bar, 1, 1, 2, 1)
        layout.addWidget(content, 1, 2, 2, 1)
        layout.addWidget(secondary_bar, 1, 3, 2, 1)
        layout.addWidget(status_bar, 4, 0, 1, 4)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

app = QApplication(sys.argv)
app.setStyle("windowsvista")

window = MainWindow()
window.show()

app.exec()
