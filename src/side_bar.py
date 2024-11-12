import os, logging

from PyQt6.QtCore import Qt, QFileInfo
from PyQt6.QtWidgets import QTreeView, QAbstractItemView
from PyQt6.QtGui import QIcon, QFileSystemModel

from src.text_editor import TextEditor
from src.python_highlighter import PythonHighlighter

class SideBar(QTreeView):
    def __init__(self, parent):
        super().__init__(parent)

        self.file_system_model = FileSystemModel(self)
        self.tabs = parent.tabs
        self.save_recent_file = parent.save_recent_file
        self.file_paths = parent.file_paths
        self.check_for_problems = parent.check_for_problems
        self.update_status_bar = parent.status_bar.update_status_bar

        # Create a tree view for the file system model
        self.setModel(self.file_system_model)
        self.setRootIndex(self.file_system_model.index(os.path.dirname(os.path.abspath(__file__))))  # Show the root
        self.setAutoFillBackground(True)
        self.setMouseTracking(True)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        self.clicked.connect(self.open_file_from_tree)
        self.setObjectName("SideBar")
        self.setHeaderHidden(True)
        self.setAnimated(True)
        self.setStyleSheet(
            """
                QHeaderView:section {
                    background-color: #f8f8f8;
                    border: none;
                    padding-top: 8px;
                    font-weight: 600;
                }
            """
        )

        self.hide_unwanted_columns()

    def hide_unwanted_columns(self):
        # Hide unwanted columns (e.g., Size, Type, Date Modified)
        self.hideColumn(1)  # Hide Size
        self.hideColumn(2)  # Hide Type
        self.hideColumn(3)  # Hide Date Modified

    def open_file_from_tree(self, index):
        # Get the file path from the model
        file_path = self.file_system_model.filePath(index)

        # Check if the clicked item is a file
        if QFileInfo(file_path).isFile():
            
            # Check if the file is already opened in a tab
            for tab_index in range(self.tabs.count()):
                current_widget = self.tabs.widget(tab_index)

                if self.file_paths.get(current_widget) == file_path:
                    self.tabs.setCurrentIndex(tab_index) # Swith to the existing tab
                    logging.info("File is already open in another tab.")

                    return

            # If the file is not already opened, create a new QTextEdit widget
            new_tab = TextEditor("TextEditor")

            logging.info(f"Opening file: {file_path}.")

            # Load the file content
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    new_tab.setText(content)

                    # Connect the textChanged signal to a method that checks for problems
                    new_tab.textChanged.connect(self.check_for_problems)
                    new_tab.cursorPositionChanged.connect(self.update_status_bar)
            except Exception as e:
                new_tab.setText(f"Error loading file: {e}.")
                logging.error(f"Failed to open file {file_path}: {e}.")

            self.save_recent_file(file_path)

            self.highlighter = PythonHighlighter(new_tab.document())

            icon_index = self.file_system_model.index(file_path)
            icon = self.file_system_model.data(icon_index, role=Qt.ItemDataRole.DecorationRole)

            # Add the new tab
            self.tabs.addTab(new_tab, QIcon(icon), QFileInfo(file_path).fileName())
            self.tabs.setCurrentWidget(new_tab) # Switch to the new tab
            self.tabs.tabBar().setTabToolTip(self.tabs.indexOf(new_tab), file_path)

            # Store the file path for this tab
            self.file_paths[new_tab] = file_path

class FileSystemModel(QFileSystemModel):
    def __init__(self, parent):
        super().__init__(parent)

        # Create the file system model for the container
        self.setRootPath("")  # Set root path to the desired location
        self.setNameFilters(["*.py", "*.txt", "*.md", "*.html", "*.js"])
        self.setNameFilterDisables(True)
