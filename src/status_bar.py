from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QTextEdit
from PyQt6.QtGui import QIcon

ICON_PATH = "resources/icons/"

class StatusBar(QHBoxLayout):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.parent = parent
        self.tabs = parent.tabs
        self.file_paths = parent.file_paths
        self.detect_encoding = parent.detect_encoding
        self.detect_line_endings = parent.detect_line_endings
        self.detect_language = parent.detect_language

        self.remote_window_button = QPushButton(parent)
        self.remote_window_button.setIcon(QIcon(ICON_PATH + "remote_window_icon.png"))
        self.remote_window_button.setIconSize(QSize(14, 14))
        self.remote_window_button.setObjectName("RemoteWindowButton")
        self.remote_window_button.setMouseTracking(True)
        self.remote_window_button.clicked.connect(self.show_remote_window)
        self.remote_window_button.setToolTip("Open a Remote Window")
        self.remote_window_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.error_button = StatusBarButton(ICON_PATH + "error_icon.png", QSize(14, 14))
        self.error_button.clicked.connect(self.show_problems)
        self.error_button.setToolTip("No Problems")

        self.warning_button = StatusBarButton(ICON_PATH + "warning_icon.png", QSize(12, 12))
        self.warning_button.clicked.connect(self.show_problems)
        self.warning_button.setToolTip("No Problems")

        self.port_forward_button = StatusBarButton(ICON_PATH + "port_forward_icon.png", QSize(14, 14))
        self.port_forward_button.clicked.connect(self.show_ports)
        self.port_forward_button.setToolTip("No Ports Forwarded")

        self.line_col_label = QLabel("Ln 1, Col 1")
        self.line_col_label.setToolTip("Go to Line/Column")
        self.line_col_label.setCursor(Qt.CursorShape.PointingHandCursor)

        self.spaces_label = QLabel("Spaces: 4")
        self.spaces_label.setToolTip("Select Indentation")
        self.spaces_label.setCursor(Qt.CursorShape.PointingHandCursor)

        self.encoding_label = QLabel("UTF-8")
        self.encoding_label.setToolTip("Select Encoding")
        self.encoding_label.setCursor(Qt.CursorShape.PointingHandCursor)

        self.crlf_label = QLabel("CRLF")
        self.crlf_label.setToolTip("Select End of Line Sequence")
        self.crlf_label.setCursor(Qt.CursorShape.PointingHandCursor)

        self.language_label = QLabel("{ } Python")
        self.language_label.setToolTip("Select Language Mode")
        self.language_label.setCursor(Qt.CursorShape.PointingHandCursor)

        self.version_label = QLabel("3.10.0 ('.venv': venv)")
        self.version_label.setToolTip(".\\.venv\\Scripts\python.exe")
        self.version_label.setCursor(Qt.CursorShape.PointingHandCursor)

        self.notification_button = QPushButton(parent)
        self.notification_button.setIcon(QIcon(ICON_PATH + "notification_icon.png"))
        self.notification_button.setIconSize(QSize(12, 12))
        self.notification_button.setObjectName("NotificationButton")
        self.notification_button.setMouseTracking(True)
        self.notification_button.clicked.connect(self.show_notifications)
        self.notification_button.setToolTip("No Notifications")
        self.notification_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.setContentsMargins(0, 0, 0, 0)
        self.addWidget(self.remote_window_button)
        self.addWidget(self.error_button)
        self.addWidget(self.warning_button)
        self.addWidget(self.port_forward_button)
        self.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.addWidget(self.line_col_label)
        self.addWidget(self.spaces_label)
        self.addWidget(self.encoding_label)
        self.addWidget(self.crlf_label)
        self.addWidget(self.language_label)
        self.addWidget(self.version_label)
        self.addWidget(self.notification_button)

    def update_status_bar(self):
        if not self.tabs.currentWidget():
            return

        current_widget = self.tabs.currentWidget()

        if not isinstance(current_widget, QTextEdit):
            return

        cursor = current_widget.textCursor()

        line = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1

        file_path = self.file_paths.get(current_widget, "Unknown File")
        text = current_widget.toPlainText()

        # Check if status bar actually needs to be updated
        if self.line_col_label.text() != f"Ln {line}, Col {col}":
            self.line_col_label.setText(f"Ln {line}, Col {col}")

        if self.spaces_label.text() != f"Spaces: 4":
            self.spaces_label.setText(f"Spaces: 4")

        encoding = self.detect_encoding(file_path)

        if self.encoding_label.text() != encoding:
            self.encoding_label.setText(encoding)

        line_endings = self.detect_line_endings(text)

        if self.crlf_label.text() != f"{line_endings}":
            self.crlf_label.setText(f"{line_endings}")

        language = self.detect_language(file_path)

        if self.language_label.text() != f"{language}":
            self.language_label.setText(f"{language}")

        if self.version_label.text() != "3.10.0 ('.venv': venv)":
            self.version_label.setText("3.10.0 ('.venv': venv)")

    def show_remote_window(self):
        print("Remote Window")

    def show_problems(self):
        if self.parent.panel.isHidden():
            self.parent.panel.show()

        self.parent.panel.setCurrentIndex(0)
    
    def show_ports(self):
        if self.parent.panel.isHidden():
            self.parent.panel.show()

        self.parent.panel.setCurrentIndex(4)

    def show_notifications(self):
        print("Notifications")

class StatusBarButton(QPushButton):
    def __init__(self, icon_path, icon_size, parent=None):
        super().__init__(parent)

        self.setText("0")
        self.setIcon(QIcon(icon_path))
        self.setIconSize(icon_size)
        self.setObjectName("StatusBarButton")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
