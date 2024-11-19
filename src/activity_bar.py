from PyQt6.QtCore import Qt, QSize, QPoint
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QSpacerItem, QSizePolicy, QMenu
from PyQt6.QtGui import QIcon, QAction

ICON_PATH = "resources/icons/"

class ActivityBar(QVBoxLayout):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent = parent
        self.index = 0

        # List of icon paths and tooltips
        self.icons = [
            (ICON_PATH + "folders_icon.png", "Folders", self.show_folders),
            (ICON_PATH + "search_icon.png", "Search (Ctrl+Shift+F)", self.show_search),
            (ICON_PATH + "source_control_icon.png", "Source Control (Ctrl+Shift+G)", self.show_source_control),
            (ICON_PATH + "run_and_debug_icon.png", "Run and Debug (Ctrl+Shift+D)", self.show_run_and_debug),
            (ICON_PATH + "extensions_icon.png", "Extensions (Ctrl+Shift+X)", self.show_extensions),
            (ICON_PATH + "testing_icon.png", "Testing", self.show_testing),
            (ICON_PATH + "accounts_icon.png", "Accounts", self.show_accounts),
            (ICON_PATH + "manage_icon.png", "Manage - New Code update available.", self.show_manage),
        ]

        for icon_path, tooltip, action in self.icons:
            self.button = ActivityButton(icon_path)
            self.button.setToolTip(tooltip),
            self.button.clicked.connect(action)
            self.addWidget(self.button)

        self.insertSpacerItem(6, QSpacerItem(32, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

        self.setup()
        
    def show_folders(self):
        if self.parent.side_bar.isHidden():
            if self.parent.splitter.widget(0) != self.parent.side_bar:
                self.parent.splitter.replaceWidget(0, self.parent.side_bar)
            self.parent.side_bar.show()

            return
        
        self.parent.side_bar.hide()

    def show_search(self):
        if self.search_widget.isHidden():
            if self.parent.splitter.widget(0) != self.search_widget:
                self.parent.splitter.replaceWidget(0, self.search_widget)
            self.search_widget.show()

            return
        
        self.search_widget.hide()

    def show_source_control(self):
        if self.source_control_widget.isHidden():
            if self.parent.splitter.widget(0) != self.source_control_widget:
                self.parent.splitter.replaceWidget(0, self.source_control_widget)
            self.source_control_widget.show()

            return
        
        self.source_control_widget.hide()

    def show_run_and_debug(self):
        if self.run_and_debug_widget.isHidden():
            if self.parent.splitter.widget(0) != self.run_and_debug_widget:
                self.parent.splitter.replaceWidget(0, self.run_and_debug_widget)
            self.run_and_debug_widget.show()

            return
        
        self.run_and_debug_widget.hide()

    def show_extensions(self):
        if self.extensions_widget.isHidden():
            if self.parent.splitter.widget(0) != self.extensions_widget:
                self.parent.splitter.replaceWidget(0, self.extensions_widget)
            self.extensions_widget.show()

            return
        
        self.extensions_widget.hide()

    def show_testing(self):
        if self.testing_widget.isHidden():
            if self.parent.splitter.widget(0) != self.testing_widget:
                self.parent.splitter.replaceWidget(0, self.testing_widget)  
            self.testing_widget.show()
            
            return
        
        self.testing_widget.hide()

    def show_accounts(self):
        self.account_menu.exec(self.button.mapToGlobal(self.button.rect().bottomRight() - QPoint(-1, int(self.account_menu.height() / 2))))

    def show_manage(self):
        self.manage_menu.exec(self.button.mapToGlobal(self.button.rect().bottomRight() - QPoint(-1, int(self.manage_menu.height() / 2))))
            
    def setup(self):
        self.search_widget = QWidget()
        self.search_widget.setStyleSheet("background-color: green")

        self.source_control_widget = QWidget()
        self.source_control_widget.setStyleSheet("background-color: yellow")

        self.run_and_debug_widget = QWidget()
        self.run_and_debug_widget.setStyleSheet("background-color: orange")

        self.extensions_widget = QWidget()
        self.extensions_widget.setStyleSheet("background-color: pink")

        self.testing_widget = QWidget()
        self.testing_widget.setStyleSheet("background-color: purple")

        self.setup_account_menu()
        self.setup_manage_menu()

    def setup_account_menu(self):
        self.account_menu = QMenu()

        action1 = QAction("suatalikoch (GitHub)", self)
        action2 = QAction("Settings Sync is On", self)
        action3 = QAction("Turn on Cloud Changes...", self)
        action4 = QAction("Turn on Remote Tunnel Access...", self)

        self.account_menu.addAction(action1)
        self.account_menu.addSeparator()
        self.account_menu.addAction(action2)
        self.account_menu.addSeparator()
        self.account_menu.addAction(action3)
        self.account_menu.addSeparator()
        self.account_menu.addAction(action4)

    def setup_manage_menu(self):
        self.manage_menu = QMenu()

        action1 = QAction("Command Palette...", self)
        action2 = QAction("Profiles", self)
        action3 = QAction("Settings", self)
        action4 = QAction("Extensions", self)
        action5 = QAction("Keyboard Shortcuts", self)
        action6 = QAction("Snippets", self)
        action7 = QAction("Tasks", self)
        action8 = QAction("Themes", self)
        action9 = QAction("Settings Sync is On", self)
        action0 = QAction("Check for Updates...", self)

        action1.setShortcut("Ctrl+Shift+P")
        action3.setShortcut("Ctrl+,")
        action4.setShortcut("Ctrl+Shift+X")
        action5.setShortcut("Ctrl+K, Ctrl+S")

        self.manage_menu.addAction(action1)
        self.manage_menu.addSeparator()
        self.manage_menu.addAction(action2)
        self.manage_menu.addAction(action3)
        self.manage_menu.addAction(action4)
        self.manage_menu.addAction(action5)
        self.manage_menu.addAction(action6)
        self.manage_menu.addAction(action7)
        self.manage_menu.addAction(action8)
        self.manage_menu.addSeparator()
        self.manage_menu.addAction(action9)
        self.manage_menu.addSeparator()
        self.manage_menu.addAction(action0)
        
class ActivityButton(QPushButton):
    def __init__(self, icon_path, parent=None,):
        super().__init__(parent)

        self.icon = QIcon(icon_path)
        self.setIcon(self.icon)
        self.setFlat(True)
        self.setFixedHeight(48)
        self.setIconSize(QSize(28, 28))
        self.setObjectName("ActivityBarButton")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
