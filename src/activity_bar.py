from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QPixmap

ICON_PATH = "resources/icons/"

class ActivityBar(QVBoxLayout):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent = parent
        self.index = 0

        # List of icon paths and tooltips
        self.icons = [
            (ICON_PATH + "folders_icon.png", "Folders"),
            (ICON_PATH + "search_icon.png", "Search (Ctrl+Shift+F)"),
            (ICON_PATH + "source_control_icon.png", "Source Control (Ctrl+Shift+G)"),
            (ICON_PATH + "run_and_debug_icon.png", "Run and Debug (Ctrl+Shift+D)"),
            (ICON_PATH + "extensions_icon.png", "Extensions (Ctrl+Shift+X)"),
            (ICON_PATH + "testing_icon.png", "Testing"),
            (ICON_PATH + "accounts_icon.png", "Accounts"),
            (ICON_PATH + "manage_icon.png", "Manage - New Code update available."),
        ]

        for icon_path, tooltip in self.icons:
            button = ActivityButton(icon_path)
            button.setToolTip(tooltip),
            self.addWidget(button)

        self.insertSpacerItem(6, QSpacerItem(32, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.setContentsMargins(9, 8, 8, 8)
        self.setSpacing(20)

    def show_section(self, color: str):
        """Generalized method to show sections with a specified background color."""
        widget = QWidget()
        widget.setStyleSheet(f"background-color: {color};")
        self.parent.splitter.replaceWidget(0, widget)
        
    def show_folders(self):
        self.show_section("red")

    def show_search(self):
        self.show_section("green")

    def show_source_control(self):
        self.show_section("yellow")

    def show_run_and_debug(self):
        self.show_section("orange")

    def show_extensions(self):
        self.show_section("pink")

    def show_testing(self):
        self.show_section("purple")        

class ActivityButton(QLabel):
    def __init__(self, icon_path, parent=None,):
        super().__init__(parent)

        self.icon = QPixmap(icon_path)
        self.setPixmap(self.icon)
        self.setScaledContents(True)
        self.setFixedSize(28, 28)
        self.setObjectName("ActivityBarButton")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
