import sys, subprocess, os, shutil, chardet, logging

from PyQt6.QtCore import QSize, Qt, QEvent, QRect, QFileInfo, QMimeData, QUrl, QSettings, QPoint, pyqtSignal
from PyQt6.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QTabWidget, QWidget, QFrame,
                             QSplitter, QTextEdit, QFileDialog, QListWidget, QListWidgetItem, QMessageBox)
from PyQt6.QtGui import QCursor, QIcon, QDrag, QColor, QDesktopServices, QGuiApplication

from src.custom_title_bar import CustomTitleBar
from src.side_bar import SideBar
from src.monaco_editor import MonacoEditor
from src.secondary_bar import SecondaryBar
from src.activity_bar import ActivityBar
from src.status_bar import StatusBar
from src.pylint_worker import PylintWorker
from src.terminal import TerminalWidget
from src.process_worker import ProcessMonitor
from src.developer_tools import DeveloperToolsPanel, HoverEventFilter
from src.issue_reporter import IssueReporterWindow

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] - %(message)s", datefmt="%d/%m/%Y %H:%M:%S")

class MainWindow(QMainWindow):
    COMPANY_NAME = "AsteiliaCorporation"
    APPLICATION_NAME = "VSCodeClone"
    ICON_PATH = "resources/icons/"
    MINIMUM_WINDOW_WIDTH = 400
    MINIMUM_WINDOW_HEIGHT = 270
    DEFAULT_TAB_HEIGHT = 35
    DEFAULT_TAB_PADDING = 15

    handleReleaseSignal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.clear_recent_files()

        # Initialize a dictionary to keep track of file paths for each tab
        self.file_paths = {}  # Maps QTextEdit widgets to file paths
        self.is_welcome_open = False
        self.is_release_notes_open = False

        self.setup_ui()
        self.connect_signals()
        self.initialize_tabs()
        self.apply_styles()

        ############################# - Should be removed from here -  #############################
        self.handleReleaseSignal.connect(self.side_bar.trigger_mouse_release)
        self.splitter.splitterMoved.connect(self.on_splitter_moved)
        ############################################################################################

    def setup_ui(self):
        """Main method to set up the user interface. Handles window properties, component initialization, and layout creation."""
        self._setup_window_properties()
        self.initialize_variables()

        self.layout = self.create_main_layout()
        self.setCentralWidget(self.layout)

        self.hover_filter = HoverEventFilter(self)
        self.installEventFilter(self.hover_filter)

        for child in self.findChildren(QWidget):
            child.installEventFilter(self.hover_filter)

    def _setup_window_properties(self):
        """Configures the window properties such as size, minimum size, flags, and attributes."""
        screen_size = QApplication.primaryScreen().size()

        self.resize(QSize(screen_size.width() // 2, screen_size.height() // 2))
        self.setMinimumSize(QSize(self.MINIMUM_WINDOW_WIDTH, self.MINIMUM_WINDOW_HEIGHT))
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setObjectName("MainWindow")
        self.setWindowTitle(self.APPLICATION_NAME)
        self.setFocus()
        self.setMouseTracking(True)

    def initialize_variables(self):
        """Initialize variables that control window state, dragging, resizing, and tab tracking."""
        # Variables to handle resizing
        self.resizing = False
        self.last_mouse_pos = QPoint(0, 0)
        self.resize_edge_size = 10  # Pixel size for resize edge (e.g., 10px from the edge)
        self.is_resizing_left = False
        self.is_resizing_right = False
        self.is_resizing_top = False
        self.is_resizing_bottom = False

        self.dragging = False
        self.start_size = self.size()
        self.original_geometry = None
        self.has_snapped = False  # Track if it has snapped during drag

        self.untitled_tab_count = 0

        self.open_windows = []

    def connect_signals(self):
        """Connect all signals to their corresponding slots."""
        self._connect_signal_group(self._get_drag_signals())
        self._connect_signal_group(self._get_tab_signals())

    def _get_drag_signals(self):
        return {
            self.title_bar.mousePressed: self.start_dragging,
            self.title_bar.mouseMoved: self.handle_movement,
            self.title_bar.mouseReleased: self.stop_dragging,
        }

    def _get_tab_signals(self):
        return {
            self.tabs.tabCloseRequested: self.close_tab,
            self.tabs.currentChanged: self.status_bar.update_status_bar,
        }

    def apply_styles(self):
        style_path = "styles/theme.qss"

        with open(style_path, "r") as file:
            self.setStyleSheet(file.read())
            logging.info(f"Loaded styles from '{style_path}'.")

        style_path = "styles/main.qss"

        with open(style_path, "r") as file:
            self.setStyleSheet(file.read())
            logging.info(f"Loaded styles from '{style_path}'.")

        style_path = "styles/title_bar.qss"

        with open(style_path, "r") as file:
            self.title_bar.setStyleSheet(file.read())
            logging.info(f"Loaded styles from '{style_path}'.")

        style_path = "styles/activity_bar.qss"

        with open(style_path, "r") as file:
            self.activity_bar_widget.setStyleSheet(file.read())
            logging.info(f"Loaded styles from '{style_path}'.")

        style_path = "styles/side_bar.qss"

        with open(style_path, "r") as file:
            self.side_bar.setStyleSheet(file.read())
            logging.info(f"Loaded styles from '{style_path}'.")

        style_path = "styles/secondary_bar.qss"

        with open(style_path, "r") as file:
            self.secondary_bar.setStyleSheet(file.read())
            logging.info(f"Loaded styles from '{style_path}'.")

        style_path = "styles/terminal.qss"

        with open(style_path, "r") as file:
            self.terminal_widget.setStyleSheet(file.read())
            logging.info(f"Loaded styles from '{style_path}'.")

        style_path = "styles/status_bar.qss"

        with open(style_path, "r") as file:
            self.status_bar_widget.setStyleSheet(file.read())
            logging.info(f"Loaded styles from '{style_path}'.")

    def _connect_signal_group(self, signal_slot_dict):
        """Connect each signal to its corresponding slot."""
        for signal, slot in signal_slot_dict.items():
            signal.connect(slot)

    def initialize_tabs(self):
        file_paths = self.load_recent_files() # Method to fetch recently opened files dynamically

        for file_path in file_paths:
            file_name = file_path.split('/')[-1]

            widget = self.create_text_edit(file_path)

            self.file_paths[widget] = file_path

            icon_index = self.side_bar.file_system_model.index(file_path)
            icon = self.side_bar.file_system_model.data(icon_index, role=Qt.ItemDataRole.DecorationRole)

            self.tabs.addTab(widget, QIcon(icon), file_name)
            self.tabs.tabBar().setTabToolTip(self.tabs.indexOf(widget), file_path)
            self.tabs.setStyleSheet(
                """
                    QTabWidget#TabBar::pane {
                        border-top: 1px solid #e5e5e5;
                    }
                """
            )

    def load_recent_files(self):
        """Load the list of recently opened files."""
        settings = QSettings(self.COMPANY_NAME, self.APPLICATION_NAME)
        recent_files = settings.value("recentFiles", [])

        return recent_files

    def save_recent_file(self, file_path):
        """Saves the recently opened file."""
        settings = QSettings(self.COMPANY_NAME, self.APPLICATION_NAME)
        recent_files = settings.value("recentFiles", [])

        if file_path not in recent_files:
            recent_files.append(file_path)

        settings.setValue("recentFiles", recent_files)

    def clear_recent_files(self):
        """Clear the list of recent files in the settings."""
        settings = QSettings(self.COMPANY_NAME, self.APPLICATION_NAME)

        # Clear the recent files list in the settings
        settings.remove("recentFiles")  # This removes the "recentFiles" key entirely

        # Optionally, you could set it to an empty list instead of removing the key
        # settings.setValue("recentFiles", [])

        # Optionally, log or print the action for debugging purposes
        logging.info("Recent files cleared from settings.")

    def get_tab_index_by_file(self, file_name):
        """Helper function to check if a file is already open and return the tab index."""
        for tab_index in range(self.tabs.count()):
            current_widget = self.tabs.widget(tab_index)

            if self.file_paths.get(current_widget) == file_name:
                return tab_index
            
        return None

    def create_text_edit(self, file_path=None):
        widget = MonacoEditor(self)

        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                widget.setText(content)

        # Connect the textChanged signal to a method that checks for problems and updates status_bar
        widget.textChanged.connect(self.check_for_problems)
        widget.cursorPositionChanged.connect(self.status_bar.update_status_bar)

        return widget

    def create_tabs(self):
        """Create and return the tabs for the window (this method should be defined elsewhere)."""
        tabs = QTabWidget()
        tabs.setTabsClosable(True)
        tabs.setAutoFillBackground(True)
        tabs.setMovable(True)
        tabs.setObjectName("TabBar")
        tabs.tabBar().setCursor(Qt.CursorShape.PointingHandCursor)

        return tabs

    def detect_encoding(self, text=None, file_path=None):
        """Detect the file encoding."""
        if text is None and file_path is None:
            return None # Should handle the case when neither is provided

        if file_path:
            with open(file_path, 'rb') as file:
                raw_data = file.read()
                result = chardet.detect(raw_data)
                encoding = result["encoding"]

        # If `text` is provided, you could try to detect the encoding of the text itself
        # (though this might be less accurate)
        if text:
            # Some kind of detection logic for the string text (using chardet or similar)
            return "UTF-8"  # Default fallback, assuming UTF-8 for now

        return encoding

    def detect_line_endings(self, text):
        if "\r\n" in text:
            return "CRLF"
        elif "\n" in text:
            return "LF"
        elif "\r" in text:
            return "CR"
        return "None"

    def detect_language(self, file_path):
        extension_to_language = {
            ".py": "{ } Python",
            ".js": "{ } JavaScript",
            ".html": "{ } HTML",
            ".css": "{ } CSS",
            ".qss": "{ } QSS",
            ".java": "{ } Java",
            ".cpp": "{ } C++",
            # Add more as needed
        }
    
        file_extension = file_path.split('.')[-1] if '.' in file_path else ''

        return extension_to_language.get('.' + file_extension, "{ } Plain Text")

    def create_main_layout(self):
        """Creates and returns the main layout for the window."""
        # Create a panel for additional tabs
        self.panel = self.create_additional_tabs_panel()
        self.panel.tabBar().setCursor(Qt.CursorShape.PointingHandCursor)

        self.tabs = self.create_tabs()
        self.status_bar = StatusBar(self)
        self.side_bar = SideBar(self)
        self.secondary_bar = SecondaryBar(self)
        self.table = ProcessMonitor()
        self.developer_tools = DeveloperToolsPanel()
        self.issue_reporter = IssueReporterWindow()

        splitter1 = QSplitter()
        splitter1.setMouseTracking(True)
        splitter1.setOrientation(Qt.Orientation.Vertical)
        splitter1.addWidget(self.tabs)
        splitter1.addWidget(self.panel)
        splitter1.setSizes([int(splitter1.height() * 0.80), int(splitter1.height() * 0.20)])
        splitter1.setObjectName("VerticalSplitter")

        self.splitter = QSplitter()
        self.splitter.setMouseTracking(True)
        self.splitter.addWidget(self.side_bar)
        self.splitter.addWidget(splitter1)
        self.splitter.addWidget(self.secondary_bar)
        self.splitter.setSizes([int(self.splitter.width() * 0.175), int(self.splitter.width() * 0.65), int(self.splitter.width() * 0.175)])
        self.splitter.setObjectName("HorizontalSplitter")

        self.activity_bar = ActivityBar(self)
        self.title_bar = CustomTitleBar(self)

        self.activity_bar_widget = QWidget()
        self.activity_bar_widget.setFixedWidth(46)
        self.activity_bar_widget.setObjectName("ActivityBar")
        self.activity_bar_widget.setLayout(self.activity_bar)
        self.activity_bar_widget.setMouseTracking(True)

        # Add a 1px separator
        self.vseparator = QFrame()
        self.vseparator.setFrameShape(QFrame.Shape.VLine)  # Horizontal line
        self.vseparator.setFrameShadow(QFrame.Shadow.Plain)
        self.vseparator.setLineWidth(1)
        self.vseparator.setStyleSheet("color: #e5e5e5;")
        self.vseparator.setFixedWidth(1)

        layout1 = QHBoxLayout()
        layout1.setContentsMargins(0, 0, 0, 0)
        layout1.setSpacing(0)
        layout1.addWidget(self.activity_bar_widget)
        layout1.addWidget(self.vseparator)
        layout1.addWidget(self.splitter)

        self.status_bar_widget = QWidget()
        self.status_bar_widget.setMouseTracking(True)
        self.status_bar_widget.setFixedHeight(21)
        self.status_bar_widget.setLayout(self.status_bar)
        self.status_bar_widget.setObjectName("StatusBar")

        # Add a 1px separator
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.Shape.HLine)  # Horizontal line
        self.separator.setFrameShadow(QFrame.Shadow.Plain)
        self.separator.setLineWidth(1)
        self.separator.setStyleSheet("color: #e5e5e5;")
        self.separator.setFixedHeight(1)

        # Add a 1px separator
        self.separator1 = QFrame()
        self.separator1.setFrameShape(QFrame.Shape.HLine)  # Horizontal line
        self.separator1.setFrameShadow(QFrame.Shadow.Plain)
        self.separator1.setLineWidth(1)
        self.separator1.setStyleSheet("color: #e5e5e5;")
        self.separator1.setFixedHeight(1)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.title_bar)
        layout.addWidget(self.separator)
        layout.addLayout(layout1, 1)
        layout.addWidget(self.separator1)
        layout.addWidget(self.status_bar_widget)

        container = QWidget()
        container.setContentsMargins(1, 1, 1, 1)
        container.setLayout(layout)
        container.setMouseTracking(True)
        container.setObjectName("Container")

        return container

    def create_additional_tabs_panel(self):
        panel = QTabWidget()
        panel.setMovable(True)
        panel.setObjectName("PanelBar")

        tab_names = ["PROBLEMS", "OUTPUT", "DEBUG CONSOLE", "TERMINAL", "PORTS"]
        tooltips = ["Problems (Ctrl+Shift+M)", "Output (Ctrl+Shift+U)", "Debug Console (Ctrl+Shift+Y)", "Terminal (Ctrl+`)", "Ports"]

        for i, tab_name in enumerate(tab_names):
            widget = self.create_additional_tab_widget(tab_name)
            panel.addTab(widget, tab_name)
            panel.tabBar().setTabToolTip(i, tooltips[i])

        return panel

    def create_additional_tab_widget(self, tab_name):
        if tab_name == "PROBLEMS": # PROBLEMS tab
            widget = QListWidget()
            widget.setObjectName("PanelTab")
            self.problems_widget = widget
        elif tab_name == "TERMINAL":
            widget = TerminalWidget()
            self.terminal_widget = widget
        else:
            widget = QTextEdit()
            widget.setReadOnly(True) # Make it read-only
            widget.setObjectName("PanelTab")

        return widget

    def create_new_tab(self, initial_content=None):
        """Creates a new tab with a text editor and optional initial content."""
        new_tab = MonacoEditor(self)

        if initial_content:
            new_tab.set_content(initial_content)
        else:
            new_tab.append_content("Select a language, or fill with template, or open a different editor to get started.\nStart typing to dismiss or don't show this again.")

        # Connect the textChanged signal to a method that checks for problems
        # - # new_tab.textChanged.connect(self.check_for_problems)
        # - # new_tab.cursorPositionChanged.connect(self.status_bar.update_status_bar)

        self.untitled_tab_count += 1

        tab_name = f"Untitled - {self.untitled_tab_count}"

        self.tabs.addTab(new_tab, tab_name)
        self.tabs.setCurrentWidget(new_tab)  # Switch to the new tab
        self.tabs.tabBar().setTabToolTip(self.tabs.indexOf(new_tab), tab_name)

        self.tabs.setStyleSheet(
            """
                QTabWidget#TabBar::pane {
                    border-top: 1px solid #e5e5e5;
                }
            """
        )

    def create_new_window(self):
        # Create a new instance of MainWindow
        self.new_window = MainWindow()
        self.new_window.show()  # Show the new window

        self.open_windows.append(self.new_window)  # Add to list to keep reference

    def open_file(self):
        options = QFileDialog.Option.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "",
                                                   "All Files (*.*);;Text Files (*.txt);;Image Files (*.png;*.jpg;*.bmp);;Python Files (*.py);; Markdown Files (*.md)",
                                                   options=options)

        if file_name:
            # Check if the file is already opened in a tab
            
            existing_tab_index = self.get_tab_index_by_file(file_name)

            if existing_tab_index is not None:
                self.tabs.setCurrentIndex(existing_tab_index) # Switch to the existing tab
                logging.info("File is already open in another tab.")

                return

            # Add logic to handle the opened file, e.g., opening it in a new tab
            new_tab = MonacoEditor(self)

            # Load the file content
            try:
                with open(file_name, 'r') as file:
                    content = file.read()
                    new_tab.set_content(content)
                    
                    # Connect the textChanged signal to a method that checks for problems
                    #new_tab.textChanged.connect(self.check_for_problems)
                    #new_tab.cursorPositionChanged.connect(self.status_bar.update_status_bar)

                    logging.info(f"Opening file: {file_name}.")
            except Exception as e:
                new_tab.set_content(f"Error loading file: {e}.")
                logging.error(f"Error opening file {file_name}: {e}.")

            # Set file path and update the recent files list
            self.file_paths[new_tab] = file_name
            self.save_recent_file(file_name)
            
            # Set the tab icon based on the file system model
            icon_index = self.side_bar.file_system_model.index(file_name)
            icon = self.side_bar.file_system_model.data(icon_index, role=Qt.ItemDataRole.DecorationRole)

            tab_name = QFileInfo(file_name).fileName()

            self.tabs.addTab(new_tab, QIcon(icon), tab_name)
            self.tabs.setCurrentWidget(new_tab)  # Switch to the new tab
            self.tabs.tabBar().setTabToolTip(self.tabs.indexOf(new_tab), file_name)

            self.tabs.setStyleSheet(
                """
                    QTabWidget#TabBar::pane {
                        border-top: 1px solid #e5e5e5;
                    }
                """
            )

    def open_folder(self):
        """Open a folder using a file dialog and display it in the sidebar."""
        options = QFileDialog.Option.ReadOnly
        folder_name = QFileDialog.getExistingDirectory(self, "Open Folder", "", options=options)

        if folder_name:
            logging.info(f"Opening folder: {folder_name}.")
            
            # Add logic to handle the opened folder
            self.side_bar.file_system_model.setRootPath(folder_name)  # Set the root path to the opened folder
            self.side_bar.setRootIndex(self.side_bar.file_system_model.index(folder_name))  # Show the folder in the tree view
        else:
            logging.warning(f"No folder selected.")

    def save_tab(self):
        """Handles saving the currently selected tab."""
        if self.tabs.count() <= 0:
            logging.warning("No tab selected to save.")

            return

        current_index = self.tabs.currentIndex()
        current_widget = self.tabs.currentWidget()
        current_file_path = self.file_paths.get(current_index)

        if current_file_path:
            # Save to the existing file
            current_widget.get_content(self._save_to_file, current_file_path)
        else:
            # Trigger Save As if no file path is stored
            self.save_as()

    def save_as(self):
        """Handles 'Save As' functionality."""
        if self.tabs.count() <= 0:
            logging.warning("No tab selected to save.")

            return

        options = QFileDialog.Option.ReadOnly
        file_name, _ = QFileDialog.getSaveFileName(self, "Save As", "", "All Files (*.*);;Text Files (*.txt);;Python Files (*.py)", options=options)

        if file_name:
            current_widget = self.tabs.currentWidget()

            if current_widget:
                current_widget.get_content(self._save_to_file, file_name)
                self.file_paths[self.tabs.currentIndex()] = file_name # Store the file path for future saves
                self.tabs.setTabText(self.tabs.currentIndex(), QFileInfo(file_name).fileName()) # Update tab name

    def save_all(self):
        """Handles saving all tabs."""
        if self.tabs.count() <= 0:
            logging.warning("No tabs to save.")

            return

        for index in range(self.tabs.count()):
            current_widget = self.tabs.widget(index)
            current_file_path = self.file_paths.get(index)

            if current_widget and current_file_path:
                current_widget.get_content(self._save_to_file, current_file_path)

    def close_editor(self):
        current_index = self.tabs.currentIndex()
        
        if current_index >= 0:
            self.close_tab(current_index)

    def close_folder(self):
        self.side_bar.file_system_model.setRootPath("") # Reset the file system model's root path
        self.side_bar.setRootIndex(self.side_bar.file_system_model.index("")) # Reset the sidebar view

    def close_window(self):
        self.close() # Close the current window

    def exit(self):
        QApplication.quit() # Exit the application

    def _save_to_file(self, content, file_path):
        """Save the content to the specified file path. Handles errors gracefully and provides feedback to the user."""
        if content is None:
            logging.warning(f"Content is None. Failed to save {file_path}.")

            return
        
        try:
            with open(file_path, 'w', encoding="utf-8") as file:
                file.write(content)
                logging.info(f"File saved successfully at {file_path}.")
        except Exception as e:
            logging.error(f"Failed to save file {file_path}. Error: {e}.")

    def close_tab(self, index):
        """Close a tab and remove its associated data and resources."""
        if index >= 0: # Ensure the index is valid
            current_widget = self.tabs.widget(index)

            # Check if the current widget has unsaved changes
            if isinstance(current_widget, MonacoEditor):
                current_widget.is_modified()
                
                if current_widget.is_modified:
                    # Ask the user if they want to save before closing
                    response = QMessageBox.question(
                        self, "Unsaved Changes", 
                        "You have unsaved changes. Do you want to save before closing?", 
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel,
                        QMessageBox.StandardButton.Yes
                    )

                    if response == QMessageBox.StandardButton.Yes:
                        current_index = self.tabs.currentIndex()
                        file_path = self.file_paths.get(current_index)
                        print(self.file_paths)
                        print(file_path, file_path)
                        current_widget.get_content(self._save_to_file, file_path)
                    elif response == QMessageBox.StandardButton.Cancel:
                        return  # User chose to cancel the close operation
                    
                # Disconnect any signals related to the tab (if necessary)
                #current_widget.textChanged.disconnect(self.check_for_problems)
                #current_widget.cursorPositionChanged.disconnect(self.status_bar.update_status_bar)

            # Remove the file path associated with the tab before closing
            if current_widget in self.file_paths:
                del self.file_paths[current_widget]

            if self.is_welcome_open:
                self.is_welcome_open = False

            if self.is_release_notes_open:
                self.is_release_notes_open = False

            self.tabs.removeTab(index) # Remove the tab at the given index

            if self.tabs.count() == 0:
                self.tabs.setStyleSheet(
                    """
                        QTabWidget#TabBar::pane {
                            border: none;
                        }
                    """
                )

    def show_problems(self):
        if self.panel.isHidden():
            self.panel.show()

        self.panel.setCurrentIndex(0)

    def show_output(self):
        if self.panel.isHidden():
            self.panel.show()

        self.panel.setCurrentIndex(1)

    def show_debug_console(self):
        if self.panel.isHidden():
            self.panel.show()

        self.panel.setCurrentIndex(2)

    def show_terminal(self):
        if self.panel.isHidden():
            self.panel.show()

        self.panel.setCurrentIndex(3)

    def run_without_debugging(self):
        current_index = self.tabs.currentIndex()

        if current_index < 0:
            logging.warning(f"No tab selected to run.")

            return
        
        current_widget = self.tabs.currentWidget()
        current_file_path = self.file_paths.get(current_widget)

        if not current_file_path:
            self.terminal_widget.append(f"Warning: No file path associated with the current tab.")
            logging.warning(f"No file path associated with the current tab.")

            return

        try:
            # Clear previous output
            self.clear_terminal()
            
            # Run the file using subprocess and capture the output
            result = subprocess.run(
                ['python', current_file_path],
                capture_output=True,
                text=True,
                check=False,
                timeout=30 # Timeout in seconds
            )

            # Display output in the terminal widget
            if result.stdout:
                self.terminal_widget.append(result.stdout)

            if result.stderr:
                self.terminal_widget.append(result.stderr)

        except FileNotFoundError as e:
            # Handle case where Python is not found (this can happen on some systems if Python is not installed or misconfigured)
            self.terminal_widget.append(f"Error: Python executable not found: {e}.")
            logging.error(f"Python executable not found: {e}.")
        except PermissionError as e:
            # Handle permission errors (e.g., file access issues)
            self.terminal_widget.append(f"Error: Permission denied when trying to run the file: {e}.")
            logging.error(f"Permission denied: {e}.")
        except Exception as e:
            self.terminal_widget.append(f"Error: Failed to run the file: {e}.")
            logging.error(f"Failed to run the file: {e}.")

    def welcome(self):
        if self.is_welcome_open:
            return

        # Create a new tab with a text editor
        welcome_tab = QWidget()

        self.tabs.addTab(welcome_tab, QIcon(self.ICON_PATH + "app_icon.png"), "Welcome")
        self.tabs.setCurrentWidget(welcome_tab)  # Switch to the new tab
        self.tabs.tabBar().setTabToolTip(self.tabs.indexOf(welcome_tab), "Welcome")

        self.tabs.setStyleSheet(
            """
                QTabWidget#TabBar::pane {
                    border-top: 1px solid #e5e5e5;
                }
            """
        )

        self.is_welcome_open = True

    def documentation(self):
        url = QUrl("https://go.microsoft.com/fwlink/?LinkID=533484#vscode")
        QDesktopServices.openUrl(url)

    def show_release_notes(self):
        if self.is_release_notes_open:
            return

        # Create a new tab with a text editor
        release_notes_tab = QWidget()

        self.tabs.addTab(release_notes_tab, "Release Notes - 19.5.0")
        self.tabs.setCurrentWidget(release_notes_tab)  # Switch to the new tab

        self.tabs.setStyleSheet(
            """
                QTabWidget#TabBar::pane {
                    border-top: 1px solid #e5e5e5;
                }
            """
        )

        self.is_release_notes_open = True

    def video_tutorials(self):
        url = QUrl("https://code.visualstudio.com/docs/getstarted/introvideos#VSCode")
        QDesktopServices.openUrl(url)

    def tips_and_tricks(self):
        url = QUrl("https://go.microsoft.com/fwlink/?linkid=852118")
        QDesktopServices.openUrl(url)

    def join_us_on_youtube(self):
        url = QUrl("https://aka.ms/vscode-youtube")
        QDesktopServices.openUrl(url)

    def search_feature_requests(self):
        url = QUrl("https://github.com/Microsoft/vscode/issues?q=is%3Aopen+is%3Aissue+label%3Afeature-request+sort%3Areactions-%2B1-desc")
        QDesktopServices.openUrl(url)

    def open_issue_reporter(self):
        self.issue_reporter.show()

    def view_license(self):
        url = QUrl("https://code.visualstudio.com/license?lang=en")
        QDesktopServices.openUrl(url)

    def privacy_statement(self):
        url = QUrl("https://go.microsoft.com/fwlink/?LinkId=521839")
        QDesktopServices.openUrl(url)

    def open_developer_options(self):
        self.developer_tools.show()

    def open_process_explorer(self):
        self.table.show()

    def about(self):
        QMessageBox.information(self, "Visual Studio Code", "Version: 1.95.0 (user setup)\nCommit: 912bb683695358a54ae0c670461738984cbb5b95\nDate: 2024-10-28T20:16:24.561Z\nElectron: 32.2.1\nElectronBuildId: 10427718\nChromium: 128.0.6613.186\nNode.js: 20.18.0\nV8: 12.8.374.38-electron.0\nOS: Windows_NT x64 10.0.22631", QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Ok)

    def mimeData(self, indexes):
        # Create a QMimeData object that contains the file paths to drag.
        mime_data = QMimeData()
        file_paths = []

        for index in indexes:
            if index.isValid():
                # Get the file path from the model (you might need to adjust this depending on your model)
                file_path = self.side_bar.file_system_model.filePath(index)
                file_paths.append(file_path)

        mime_data.setUrls([QUrl.fromLocalFile(path) for path in file_paths])

        return mime_data

    def startDrag(self, supportedActions):
        index = self.side_bar.currentIndex()

        if index.isValid():
            mimeData = self.mimeData([index])  # Use your existing mimeData method
            drag = QDrag(self.side_bar)
            drag.setMimeData(mimeData)
            drag.exec_(supportedActions)

    def dragMoveEvent(self, event):
        # Handle the drag move event.

        if event.source() == self.side_bar:
            event.accept()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self, event):
        # Handle the drop event.

        if event.source() == self.side_bar:
            event.accept()

            for url in event.mimeData().urls():
                target_path = self.side_bar.file_system_model.filePath(self.side_bar.indexAt(event.pos()))
                source_path = url.toLocalFile()

                if target_path and os.path.isdir(source_path):
                    # Move the file from source_path to target_path
                    
                    try:
                        shutil.move(source_path, os.path.join(target_path, os.path.basename(source_path)))
                        logging.info(f"Moved file from {source_path} to {target_path}.")

                        # Refresh the file system model to update the view
                        self.side_bar.file_system_model.refresh()
                    except Exception as e:
                        logging.error(f"Error moving file: {e}.")
        else:
            super().dropEvent(event)

    def add_problem(self, message, file_name = None, line_number = None, problem_type = "Error"):
        formatted_message = f"{problem_type}: {message}"

        if file_name and line_number:
            formatted_message += f" (File: {file_name}, Line: {line_number})"

        item = QListWidgetItem(formatted_message)

        if problem_type == "Error":
            item.setForeground(Qt.GlobalColor.red)
        elif problem_type == "Warning":
            item.setForeground(QColor(255, 165, 0))
        else:
            item.setForeground(Qt.GlobalColor.black)
        
        self.problems_widget.addItem(item)

    def check_for_problems(self):
        self.problems_widget.clear() # Clear previous problems

        current_widget = self.tabs.currentWidget() # Get the current QTextEdit widget

        if current_widget is not None:  # Check if there's a current widget
            code = current_widget.get_content() # Get the current text in the editor

            # Start Pylint in a separate thread
            self.pylint_worker = PylintWorker(code)
            self.pylint_worker.finished.connect(self.process_pylint_output)
            self.pylint_worker.start()

    def process_pylint_output(self, output):
        for line in output.splitlines():
            if any(code in line for code in ["E", "W"]): # Error or Warning
                parts = line.split(":", 4)

                if len(parts) >= 4:
                    file_name = parts[0].strip() # File name
                    line_number = parts[1].strip() # Line number
                    column_number = parts[2].strip() # Column number
                    error_code = parts[3].strip() # Error code
                    message = ':'.join(parts[4:]).strip() # Join the rest for the message

                    # Determine problem type based on error code

                    if error_code.startswith("E"): # Error
                        problem_type = "Error"
                    elif error_code.startswith("W"): # Warning
                        problem_type = "Warning"
                    else:
                        problem_type = "Info"

                    # Add the problem to the widget
                    self.add_problem(message, file_name, f"{line_number} {column_number}", problem_type)

    def clear_terminal(self):
        self.terminal_widget.clear_terminal()

    def get_cursor(self, x, y, width, height):
        # Define cursor and resize direction based on position
        cursor = None

        # Determine cursor and resizing direction
        if x <= self.resize_edge_size and y <= self.resize_edge_size:
            cursor = Qt.CursorShape.SizeFDiagCursor # Top Left Corner
        elif width - 10 <= x and y <= self.resize_edge_size:
            cursor = Qt.CursorShape.SizeBDiagCursor # Top Right Corner
        elif x <= self.resize_edge_size and height - 10 <= y:
            cursor = Qt.CursorShape.SizeBDiagCursor # Bottom Left Corner
        elif width - 10 <= x and height - 10 <= y:
            cursor = Qt.CursorShape.SizeFDiagCursor # Bottom Right Corner
        elif self.resize_edge_size < x < width - 10 and y <= self.resize_edge_size:
            cursor = Qt.CursorShape.SizeVerCursor # Top Center
        elif self.resize_edge_size < x < width - 10 and y >= height - 10:
            cursor = Qt.CursorShape.SizeVerCursor # Bottom Center
        elif x <= self.resize_edge_size and self.resize_edge_size < y < height - 10:
            cursor = Qt.CursorShape.SizeHorCursor # Left Center
        elif x > width - 10 and self.resize_edge_size < y < height - 10:
            cursor = Qt.CursorShape.SizeHorCursor # Right Center
        else:
            cursor = Qt.CursorShape.ArrowCursor

        return cursor

    def handle_snapping(self, global_x, global_y, screen_rect):
        """Handle snapping logic to the edges and corners of the screen."""
        # Check for snapping
        snap_margin = 54 # Margin for snapping

        width = screen_rect.width()
        height = screen_rect.height()

        # Initialize target geometry as the original
        target_geometry = QRect(self.original_geometry)

        top = screen_rect.top()
        bottom = screen_rect.bottom()
        left = screen_rect.left()
        right = screen_rect.right()

        # Snap to half the screen width

        if abs(global_x - left) < snap_margin:
            target_geometry.setRect(left, top, width // 2, height)  # Snap to left half
        elif abs(global_x - right) < snap_margin:
            target_geometry.setRect(right - width // 2, top, width // 2, height)  # Snap to right half
        elif abs(global_y - top) < snap_margin:
            target_geometry.setRect(left, top, width, height)  # Snap to top half

        # Check for corners
        if (abs(global_x - left) < snap_margin and abs(global_y - top) < snap_margin):
            target_geometry.setRect(left, top, width // 2, height // 2)  # Snap to top-left
        elif (abs(global_x - right) < snap_margin and abs(global_y - top) < snap_margin):
            target_geometry.setRect(right - width // 2, top, width // 2, height // 2)  # Snap to top-right
        elif (abs(global_x - left) < snap_margin and abs(global_y - bottom) < snap_margin):
            target_geometry.setRect(left, bottom - height // 2, width // 2, height // 2)  # Snap to bottom-left
        elif (abs(global_x - right) < snap_margin and abs(global_y - bottom) < snap_margin):
            target_geometry.setRect(right - width // 2, bottom - height // 2, width // 2, height // 2)  # Snap to bottom-right

        return target_geometry

    def handle_corner_resizing(self, delta, new_size):
        if self.resize_direction == "top-left":
            new_size.setWidth(new_size.width() - delta.x())
            new_size.setHeight(new_size.height() - delta.y())
            self.move(self.x() + delta.x(), self.y() + delta.y()) # Move down and right
        elif self.resize_direction == "top-right":
            new_size.setWidth(new_size.width() + delta.x())
            new_size.setHeight(new_size.height() - delta.y())
        elif self.resize_direction == "bottom-left":
            new_size.setWidth(new_size.width() - delta.x())
            new_size.setHeight(new_size.height() + delta.y())
            self.move(self.x() + delta.x(), self.y()) # Move right
        elif self.resize_direction == "bottom-right":
            new_size.setWidth(new_size.width() + delta.x())
            new_size.setHeight(new_size.height() + delta.y())

    def is_inside_window(self, x, y, width, height):
        return  0 <= x <= width and 0 <= y <= height

    def changeEvent(self, event):
        if event.type() == QEvent.Type.WindowStateChange:
            self.title_bar.window_state_changed(self.windowState())

        super().changeEvent(event)
        event.accept()

    def start_dragging(self):
        self.drag_start_pos = QCursor.pos()  # Store the starting position of the cursor
        self.original_geometry = self.geometry() # Store the original geometry

    def handle_movement(self):
        self.dragging = True

        # Calculate the new position of the window
        delta = QCursor.pos() - self.drag_start_pos
        new_position = self.pos() + delta
        self.move(new_position.x(), new_position.y())
        self.drag_start_pos = QCursor.pos() # Update the start position for the next move

    def stop_dragging(self):
        if self.dragging:
            screen_rect = self.screen().availableGeometry()
            global_x, global_y = QCursor.pos().x(), QCursor.pos().y()

            target_geometry = self.handle_snapping(global_x, global_y, screen_rect)

            if target_geometry != self.original_geometry:
                if target_geometry != QGuiApplication.primaryScreen().availableGeometry():
                    self.setGeometry(target_geometry) # Snap to the calculated geometry
                else:
                    self.showMaximized()

                self.has_snapped = True # Set the snap flag if snapped
            else:
                if target_geometry == QGuiApplication.primaryScreen().availableGeometry():
                    self.showMinimized()
                else:
                    self.resize(self.start_size) # Reset to original size
                    
                self.has_snapped = False # Reset snapping state   

        self.dragging = False

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.isMaximized():
                # Prevent resizing if the window is maximized
                return
            
            mouse_pos = event.pos()

            # Check if the mouse is near the edges (resize zones)
            if mouse_pos.x() <= self.resize_edge_size:
                self.is_resizing_left = True
            if mouse_pos.x() >= self.width() - self.resize_edge_size:
                self.is_resizing_right = True
            if mouse_pos.y() <= self.resize_edge_size:
                self.is_resizing_top = True
            if mouse_pos.y() >= self.height() - self.resize_edge_size:
                self.is_resizing_bottom = True

            # Save the initial mouse position
            self.last_mouse_pos = event.globalPosition()
            self.resizing = True

    def mouseMoveEvent(self, event):
        if self.isMaximized():
            # Don't allow resizing if the window is maximized and do NOT update cursor
            return
        
        width = self.width()
        height = self.height()

        x = event.pos().x()
        y = event.pos().y()

        cursor = self.get_cursor(x, y, width, height)

        self.setCursor(cursor)

        if self.resizing:
            self.setUpdatesEnabled(False)  # Disable updates during resizing

            # Calculate new size based on direction and mouse movement
            delta = event.globalPosition() - self.last_mouse_pos

            # Resize based on which edge/corner the user is dragging
            new_rect = self.geometry()

            if self.is_resizing_left:
                if width == self.MINIMUM_WINDOW_WIDTH:
                    if delta.x() < 0:
                        new_rect.setLeft(int(new_rect.left() + delta.x()))
                else:
                    new_rect.setLeft(int(new_rect.left() + delta.x()))
            if self.is_resizing_right:
                new_rect.setRight(int(new_rect.right() + delta.x()))
            if self.is_resizing_top:
                if height == self.MINIMUM_WINDOW_HEIGHT:
                    if delta.y() < 0:
                        new_rect.setTop(int(new_rect.top() + delta.y()))
                else:
                    new_rect.setTop(int(new_rect.top() + delta.y()))
            if self.is_resizing_bottom:
                new_rect.setBottom(int(new_rect.bottom() + delta.y()))

            self.setGeometry(new_rect) # Resize the window

            # Update the last mouse position
            self.last_mouse_pos = event.globalPosition()

            event.accept()

            self.setUpdatesEnabled(True)  # Re-enable updates after resizing

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.resizing = False
            self.is_resizing_left = False
            self.is_resizing_right = False
            self.is_resizing_top = False
            self.is_resizing_bottom = False

            self.start_size = self.size() # Store the starting size

    def on_splitter_moved(self, pos, index):
        self.handleReleaseSignal.emit()

        print(pos, index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('windowsvista')  # Sets the app style to Fusion (Qt's cross-platform style)

    window = MainWindow()
    window.show()

    app.exec()
