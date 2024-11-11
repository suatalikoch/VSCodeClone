from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QPixmap

class ActivityBar(QVBoxLayout):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent = parent
        self.index = 0

        folders_item = ActivityButton("graphics/icons/folders_icon.png")
        folders_item.setToolTip("Folders")

        search_item = ActivityButton("graphics/icons/search_icon.png")
        search_item.setToolTip("Search (Ctrl+Shift+F)")

        source_control_item = ActivityButton("graphics/icons/source_control_icon.png")
        source_control_item.setToolTip("Source Control (Ctrl+Shift+G)")

        run_and_debug_item = ActivityButton("graphics/icons/run_and_debug_icon.png")
        run_and_debug_item.setToolTip("Run and Debug (Ctrl+Shift+D)")

        extensions_item = ActivityButton("graphics/icons/extensions_icon.png")
        extensions_item.setToolTip("Extensions (Ctrl+Shift+X)")

        testing_item = ActivityButton("graphics/icons/testing_icon.png")
        testing_item.setToolTip("Testing")

        accounts_item = ActivityButton("graphics/icons/accounts_icon.png")
        accounts_item.setToolTip("Accounts")

        manage_item = ActivityButton("graphics/icons/manage_icon.png")
        manage_item.setToolTip("Manage - New Code update available.")

        #self.show_search()
        #self.show_source_control()

        self.setContentsMargins(9, 8, 8, 8)
        self.setSpacing(20)
        self.addWidget(folders_item)
        self.addWidget(search_item)
        self.addWidget(source_control_item)
        self.addWidget(run_and_debug_item)
        self.addWidget(extensions_item)
        self.addWidget(testing_item)
        self.addSpacerItem(QSpacerItem(32, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        self.addWidget(accounts_item)
        self.addWidget(manage_item)

    def show_folders(self):
        widget = QWidget()
        widget.setStyleSheet("background-color: red;")

        self.parent.splitter.replaceWidget(0, widget)

    def show_search(self):
        widget = QWidget()
        widget.setStyleSheet("background-color: green;")

        self.parent.splitter.replaceWidget(0, widget)

    def show_source_control(self):
        widget = QWidget()
        widget.setStyleSheet("background-color: yellow;")

        self.parent.splitter.replaceWidget(0, widget)

    def show_run_and_debug(self):
        widget = QWidget()
        widget.setStyleSheet("background-color: orange;")

        self.parent.splitter.replaceWidget(0, widget)

    def show_extensions(self):
        widget = QWidget()
        widget.setStyleSheet("background-color: pink;")

        self.parent.splitter.replaceWidget(0, widget)

    def show_testing(self):
        widget = QWidget()
        widget.setStyleSheet("background-color: purple;")

        self.parent.splitter.replaceWidget(0, widget)        

class ActivityButton(QLabel):
    def __init__(self, icon_path, parent=None,):
        super().__init__(parent)

        self.icon = QPixmap(icon_path)
        self.setPixmap(self.icon)
        self.setScaledContents(True)
        self.setFixedSize(28, 28)
        self.setObjectName("ActivityBarButton")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
