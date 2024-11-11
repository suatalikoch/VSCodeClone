from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QToolButton, QPushButton, QWidget, QSpacerItem, QSizePolicy

class CustomTitleBar(QWidget):
    # Define signals
    mousePressed = pyqtSignal()
    mouseMoved = pyqtSignal(int, int)
    mouseReleased = pyqtSignal() 

    new_text_file_requested = pyqtSignal()  # Signal to request a new file
    new_window_requested = pyqtSignal()
    open_file_requested = pyqtSignal()
    open_folder_requested = pyqtSignal()
    save_requested = pyqtSignal()
    save_as_requested = pyqtSignal()
    save_all_requested = pyqtSignal()
    close_editor_requested = pyqtSignal()
    close_folder_requested = pyqtSignal()
    close_window_requested = pyqtSignal()
    exit_requested = pyqtSignal()

    problems_requested = pyqtSignal()
    output_requested = pyqtSignal()
    debug_console_requested = pyqtSignal()
    terminal_requested = pyqtSignal()

    run_without_debugging_requested = pyqtSignal()

    welcome_requested = pyqtSignal()
    show_all_commands_requested = pyqtSignal()
    documentation_requested = pyqtSignal()
    editor_playground_requested = pyqtSignal()
    show_release_notes_requested = pyqtSignal()
    get_started_with_accessibility_features_requested = pyqtSignal()
    keyboard_shortcut_reference_requested = pyqtSignal()
    video_tutorials_requested = pyqtSignal()
    tips_and_tricks_requested = pyqtSignal()
    join_us_on_youtube_requested = pyqtSignal()
    search_feature_requests_requested = pyqtSignal()
    report_issue_requested = pyqtSignal()
    view_license_requested = pyqtSignal()
    privacy_statement_requested = pyqtSignal()
    toggle_developer_options_requested = pyqtSignal()
    open_process_explorer_requested = pyqtSignal()
    restart_to_update_requested = pyqtSignal()
    about_requested = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)

        self.setFixedHeight(34)

        self.setMouseTracking(True)
        self.setAutoFillBackground(True)
        self.setObjectName("TitleBar")

        self.is_dragging = False
        self.start_pos = None
        self.main_window = parent

        title_bar_layout = QHBoxLayout(self)
        title_bar_layout.setContentsMargins(0, 0, 0, 0)
        title_bar_layout.setSpacing(0)

        self.title_icon = QLabel()
        self.title_icon.setPixmap(QIcon("graphics/icons/app-icon.svg").pixmap(20, 20)) # Set size as needed
        self.title_icon.setContentsMargins(8, 0, 8, 0)
        self.title_icon.setObjectName("AppIcon")

        title_bar_layout.addWidget(self.title_icon)

        menu_bar = parent.menuBar()
        menu_bar.setObjectName("MenuBar")

        file_menu = menu_bar.addMenu("File")
        edit_menu = menu_bar.addMenu("Edit")
        selection_menu = menu_bar.addMenu("Selection")
        view_menu = menu_bar.addMenu("View")
        go_menu = menu_bar.addMenu("Go")
        run_menu = menu_bar.addMenu("Run")
        terminal_menu = menu_bar.addMenu("Terminal")
        help_menu = menu_bar.addMenu("Help")

        # Actions
        file_actions = [
            self.create_action("New Text File", "Ctrl+N", self),
            self.create_action("New File...", "Ctrl+Alt+Meta+N", self),
            self.create_action("New Window", "Ctrl+Shift+N", self),
            self.create_action("New Window with Profile", ">", self, submenu_items=[
                self.create_action("Profile 1", None, self),
                self.create_action("Profile 2", None, self),
                self.create_action("Profile 3", None, self),
            ]),
            None,  # Separator
            self.create_action("Open File...", "Ctrl+O", self),
            self.create_action("Open Folder...", "Ctrl+K, Ctrl+O", self),
            self.create_action("Open Workspace from File...", None, self),
            self.create_action("Open Recent", ">", self, submenu_items=[
                self.create_action("Recent File 1", None, self),
                self.create_action("Recent File 2", None, self),
                self.create_action("Recent File 3", None, self),
            ]),
            None,  # Separator
            self.create_action("Add Folder to Workspace...", None, self),
            self.create_action("Save Workspace As...", None, self),
            self.create_action("Duplicate Workspace", None, self),
            None,  # Separator
            self.create_action("Save", "Ctrl+S", self),
            self.create_action("Save As...", "Ctrl+Shift+S", self),
            self.create_action("Save All", "Ctrl+K, S", self),
            None,  # Separator
            self.create_action("Share", ">", self),
            None,  # Separator
            self.create_action("Auto Save", None, self),
            self.create_action("Preferences", ">", self),
            None,  # Separator
            self.create_action("Revert File", None, self),
            self.create_action("Close Editor", "Ctrl+F4", self),
            self.create_action("Close Folder", "Ctrl+K, F", self),
            self.create_action("Close Window", "Alt+F4", self),
            None,  # Separator
            self.create_action("Exit", None, self),
        ]

        edit_actions = [
            self.create_action("Undo", "Ctrl+Z", self),
            self.create_action("Redo", "Ctrl+Y", self),
            None,  # Separator
            self.create_action("Cut", "Ctrl+X", self),
            self.create_action("Copy", "Ctrl+C", self),
            self.create_action("Paste", "Ctrl+V", self),
            None,  # Separator
            self.create_action("Find", "Ctrl+F", self),
            self.create_action("Replace", "Ctrl+H", self),
            None,  # Separator
            self.create_action("Find in Files", "Ctrl+Shift+F", self),
            self.create_action("Replace in Files", "Ctrl+Shift+H", self),
            None,  # Separator
            self.create_action("Toggle Line Comment", "Ctrl+/", self),
            self.create_action("Toggle Block Comment", "Shift+Alt+A", self),
            self.create_action("Emmel: Expand Abbreviation", "Tab", self),
        ]

        selection_actions = [
            self.create_action("Select All", "Ctrl+A", self),
            self.create_action("Expand Selection", "Shift+Alt+Right", self),
            self.create_action("Shrink Selection", "Shift+Alt+Left", self),
            None,  # Separator
            self.create_action("Copy Line Up", "Shift+Alt+Up", self),
            self.create_action("Copy Line Down", "Shift+Alt+Down", self),
            self.create_action("Move Lien Up", "Alt+Up", self),
            self.create_action("Move Line Down", "Alt+Down", self),
            self.create_action("Duplicate Selection", None, self),
            None,  # Separator
            self.create_action("Add Cursor Above", "Ctrl+Alt+Up", self),
            self.create_action("Add Cursor Below", "Ctrl+Alt+Down", self),
            self.create_action("Add Cursor to Line Ends", "Shift+Alt+I", self),
            self.create_action("Add Next Occurence", "Ctrl+D", self),
            self.create_action("Add Previous Occurence", None, self),
            self.create_action("Select All Occurences", "Ctrl+Shift+L", self),
            None,  # Separator
            self.create_action("Switch to Ctrl+Click for Multi-Cursor", None, self),
            self.create_action("Column Selection Mode", None, self),
        ]

        view_actions = [
            self.create_action("Command Palette...", "Ctrl+Shift+P", self),
            self.create_action("Open View...", None, self),
            None,  # Separator
            self.create_action("Appearance", ">", self),
            self.create_action("Editor Layout", ">", self),
            None,  # Separator
            self.create_action("Search", "Ctrl+Shift+F", self),
            self.create_action("Source Control", "Ctrl+Shift+G", self),
            self.create_action("Run", "Ctrl+Shift+D", self),
            self.create_action("Extensions", "Ctrl+Shift+X", self),
            self.create_action("Testing", None, self),
            None,  # Separator
            self.create_action("Problems", "Ctrl+Shift+M", self),
            self.create_action("Output", "Ctrl+Shift+U", self),
            self.create_action("Debug Console", "Ctrl+Shift+V", self),
            self.create_action("Terminal", "Ctrl+`", self),
            None,  # Separator
            self.create_action("Word Wrap", "Alt+Z", self),
        ]

        go_actions = [
            self.create_action("Back", "Alt+Left", self),
            self.create_action("Forward", "Alt+Right", self),
            self.create_action("Last Edit Location", "Ctrl+K, Ctrl+Q", self),
            None,  # Separator
            self.create_action("Switch Editor", ">", self),
            self.create_action("Switch Group", ">", self),
            None,  # Separator
            self.create_action("Go to File...", "Ctrl+P", self),
            self.create_action("Go to Symbol in Workspace...", "Ctrl+T", self),
            None,  # Separator
            self.create_action("Go to Symbol in Editor...", "Ctrl+Shift+O", self),
            self.create_action("Go to Definition", "F12", self),
            self.create_action("Go to Declaration", None, self),
            self.create_action("Go to Type Definition", None, self),
            self.create_action("Go to Implementations", "Ctrl+F12", self),
            self.create_action("Go to References", "Shift+F12", self),
            None,  # Separator
            self.create_action("Go to Line/Column...", "Ctrl+G", self),
            self.create_action("Go to Bracket", "Ctrl+Shift+\\", self),
            None,  # Separator
            self.create_action("Next Problem", "F8", self),
            self.create_action("Previous Problem", "Shift+F8", self),
            None,  # Separator
            self.create_action("Next Change", "Alt+F3", self),
            self.create_action("Previous Change", "Shift+Alt+F3", self),
        ]

        run_actions = [
            self.create_action("Start Debugging", "F5", self),
            self.create_action("Run Without Debugging", "Ctrl+F5", self),
            self.create_action("Stop Debugging", "Shift+F5", self),
            self.create_action("Restart Debugging", "Ctrl+Shift+F5", self),
            None,  # Separator
            self.create_action("Open Configurations", None, self),
            self.create_action("Add Configuration...",  None, self),
            None,  # Separator
            self.create_action("Step Over", "F10", self),
            self.create_action("Step Into", "F11", self),
            self.create_action("Step Out", "Shift+F11", self),
            self.create_action("Continue", "F5", self),
            None,  # Separator
            self.create_action("Toggle Breakpoint", "F9", self),
            self.create_action("New Breakpoint", ">", self),
            None,  # Separator
            self.create_action("Enable All Breakpoints", None, self),
            self.create_action("Disable All Breakpoints", None, self),
            self.create_action("Remove All Breakpoints", None, self),
            None,  # Separator
            self.create_action("Install Additional Debuggers...", None, self),
        ]

        terminal_actions = [
            self.create_action("New Terminal", "Ctrl+Shift+`", self),
            self.create_action("Split Terminal", "Ctrl+Alt+5", self),
            None,  # Separator
            self.create_action("Run Task...", None, self),
            self.create_action("Run Build Task...", "Ctrl+Shift+B", self),
            self.create_action("Run Active File", None, self),
            self.create_action("Run Selected Text", None, self),
            None,  # Separator
            self.create_action("Show Running Tasks...", None, self),
            self.create_action("Restart Running Task...", None, self),
            self.create_action("Terminate Task...", None, self),
            None,  # Separator
            self.create_action("Configure Tasks...", None, self),
            self.create_action("Configure Default Build Task...", None, self),
        ]

        help_actions = [
            self.create_action("Welcome", "Ctrl+Shift+P", self),
            self.create_action("Show All Commands", None, self),
            self.create_action("Documentation", None, self),
            self.create_action("Editor Playground", None, self),
            self.create_action("Show Release Notes", None, self),
            self.create_action("Get Started with Accessibility Features", None, self),
            None,  # Separator
            self.create_action("Keyboard Shortcuts Reference", "Ctrl+K, Ctrl+R", self),
            self.create_action("Video Tutorials", None, self),
            self.create_action("Tips and Tricks", None, self),
            None,  # Separator
            self.create_action("Join Us on YouTube", None, self),
            self.create_action("Search Feature Request", None, self),
            self.create_action("Report Issue", None, self),
            None,  # Separator
            self.create_action("View License", None, self),
            self.create_action("Privacy Statement", None, self),
            None,  # Separator
            self.create_action("Toggle Developer Tools", None, self),
            self.create_action("Open Process Explorer", None, self),
            None,  # Separator
            self.create_action("Check for Updates...", None, self),
            None,  # Separator
            self.create_action("About", None, self),
        ]

        file_actions[0].triggered.connect(self.new_text_file_requested.emit) # Emit signal on trigger
        file_actions[2].triggered.connect(self.new_window_requested.emit)
        file_actions[5].triggered.connect(self.open_file_requested.emit)
        file_actions[6].triggered.connect(self.open_folder_requested.emit)
        file_actions[14].triggered.connect(self.save_requested.emit)
        file_actions[15].triggered.connect(self.save_as_requested.emit)
        file_actions[16].triggered.connect(self.save_all_requested.emit)
        file_actions[24].triggered.connect(self.close_editor_requested.emit)
        file_actions[25].triggered.connect(self.close_folder_requested.emit)
        file_actions[26].triggered.connect(self.close_window_requested.emit)
        file_actions[28].triggered.connect(self.exit_requested.emit)

        view_actions[12].triggered.connect(self.problems_requested.emit)
        view_actions[13].triggered.connect(self.output_requested.emit)
        view_actions[14].triggered.connect(self.debug_console_requested.emit)
        view_actions[15].triggered.connect(self.terminal_requested.emit)

        run_actions[1].triggered.connect(self.run_without_debugging_requested.emit)

        help_actions[0].triggered.connect(self.welcome_requested.emit)
        help_actions[2].triggered.connect(self.documentation_requested.emit)
        help_actions[4].triggered.connect(self.show_release_notes_requested.emit)
        help_actions[8].triggered.connect(self.video_tutorials_requested.emit)
        help_actions[9].triggered.connect(self.tips_and_tricks_requested.emit)
        help_actions[11].triggered.connect(self.join_us_on_youtube_requested.emit)
        help_actions[12].triggered.connect(self.search_feature_requests_requested.emit)
        help_actions[13].triggered.connect(self.report_issue_requested.emit)
        help_actions[15].triggered.connect(self.view_license_requested.emit)
        help_actions[16].triggered.connect(self.privacy_statement_requested.emit)
        help_actions[18].triggered.connect(self.toggle_developer_options_requested.emit)
        help_actions[19].triggered.connect(self.open_process_explorer_requested.emit)
        help_actions[23].triggered.connect(self.about_requested.emit)

        self.add_actions_to_menu(file_menu, file_actions)
        self.add_actions_to_menu(edit_menu, edit_actions)
        self.add_actions_to_menu(selection_menu, selection_actions)
        self.add_actions_to_menu(view_menu, view_actions)
        self.add_actions_to_menu(go_menu, go_actions)
        self.add_actions_to_menu(run_menu, run_actions)
        self.add_actions_to_menu(terminal_menu, terminal_actions)
        self.add_actions_to_menu(help_menu, help_actions)

        title_bar_layout.addWidget(menu_bar, 0, Qt.AlignmentFlag.AlignVCenter)

        self.connect_signals(parent)

        self.go_back_button = QPushButton(self)
        self.go_back_button.setIcon(QIcon("graphics/icons/back_icon.png"))
        self.go_back_button.setIconSize(QSize(18, 18))
        self.go_back_button.setObjectName("MenuBarButton")
        self.go_back_button.clicked.connect(self.go_back)
        self.go_back_button.setToolTip("Go Back (Alt+LeftArrow)")
        self.go_back_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.go_forward_button = QPushButton(self)
        self.go_forward_button.setIcon(QIcon("graphics/icons/forward_icon.png"))
        self.go_forward_button.setIconSize(QSize(18, 18))
        self.go_forward_button.setObjectName("MenuBarButton")
        self.go_forward_button.clicked.connect(self.go_forward)
        self.go_forward_button.setToolTip("Go Forward (Alt+RightArrow)")
        self.go_forward_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.go_forward_button.setDisabled(True)

        self.search_button = QPushButton("Python", self)
        self.search_button.setMaximumWidth(400)
        self.search_button.setIcon(QIcon("graphics/icons/search_icon.png"))
        self.search_button.setObjectName("SearchButton")
        self.search_button.clicked.connect(self.search)
        self.search_button.setToolTip("Search Python - app.py - Python - Visual Studio Code")
        self.search_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.side_bar_toggle_button = QPushButton(self)
        self.side_bar_toggle_button.setIcon(QIcon("graphics/icons/side_bar_icon.png"))
        self.side_bar_toggle_button.setIconSize(QSize(18, 18))
        self.side_bar_toggle_button.setObjectName("MenuBarButton")
        self.side_bar_toggle_button.clicked.connect(self.toggle_primary_side_bar)
        self.side_bar_toggle_button.setToolTip("Toggle Primary Side Bar (Ctrl+B)")
        self.side_bar_toggle_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.panel_toggle_button = QPushButton(self)
        self.panel_toggle_button.setIcon(QIcon("graphics/icons/panel_icon.png"))
        self.panel_toggle_button.setIconSize(QSize(18, 18))
        self.panel_toggle_button.setObjectName("MenuBarButton")
        self.panel_toggle_button.clicked.connect(self.toggle_panel)
        self.panel_toggle_button.setToolTip("Toggle Panel (Ctrl+J)")
        self.panel_toggle_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.secondary_bar_toggle_button = QPushButton(self)
        self.secondary_bar_toggle_button.setIcon(QIcon("graphics/icons/secondary_bar_icon.png"))
        self.secondary_bar_toggle_button.setIconSize(QSize(18, 18))
        self.secondary_bar_toggle_button.setObjectName("MenuBarButton")
        self.secondary_bar_toggle_button.clicked.connect(self.toggle_secondary_side_bar)
        self.secondary_bar_toggle_button.setToolTip("Toggle Secondary Side Bar (Ctrl+Alt+B)")
        self.secondary_bar_toggle_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.customize_layout_button = QPushButton(self)
        self.customize_layout_button.setIcon(QIcon("graphics/icons/customize_layout_icon.png"))
        self.customize_layout_button.setIconSize(QSize(18, 18))
        self.customize_layout_button.setObjectName("MenuBarButton")
        self.customize_layout_button.clicked.connect(self.customize_layout)
        self.customize_layout_button.setToolTip("Customize layout...")
        self.customize_layout_button.setCursor(Qt.CursorShape.PointingHandCursor)

        title_bar_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        title_bar_layout.addWidget(self.go_back_button)
        title_bar_layout.addWidget(self.go_forward_button)
        title_bar_layout.addWidget(self.search_button, 1)
        title_bar_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        title_bar_layout.addWidget(self.side_bar_toggle_button)
        title_bar_layout.addWidget(self.panel_toggle_button)
        title_bar_layout.addWidget(self.secondary_bar_toggle_button)
        title_bar_layout.addWidget(self.customize_layout_button)

        # Min button
        self.min_button = QToolButton(self)
        self.min_button.setIcon(QIcon("graphics/icons/minimize_icon.png"))
        self.min_button.clicked.connect(self.window().showMinimized)
        self.min_button.setToolTip("Minimize")
        self.min_button.setToolTipDuration(5000)

        # Max button
        self.max_button = QToolButton(self)
        self.max_button.setIcon(QIcon("graphics/icons/maximize_icon.png"))
        self.max_button.clicked.connect(self.window().showMaximized)
        self.max_button.setToolTip("Maximize")
        self.max_button.setToolTipDuration(5000)

        # Close button
        self.close_button = QToolButton(self)
        self.close_button.setIcon(QIcon("graphics/icons/close_icon.png"))
        self.close_button.clicked.connect(self.window().close)
        self.close_button.setToolTip("Close")
        self.close_button.setToolTipDuration(5000)

        # Normal button
        self.normal_button = QToolButton(self)
        self.normal_button.setIcon(QIcon("graphics/icons/restore_icon.png"))
        self.normal_button.clicked.connect(self.window().showNormal)
        self.normal_button.setVisible(False)
        self.normal_button.setToolTip("Normal")
        self.normal_button.setToolTipDuration(5000)

        buttons = [
            self.min_button,
            self.normal_button,
            self.max_button,
            self.close_button,
        ]

        for button in buttons:
            button.setFixedSize(QSize(45, 34))

            if button == self.close_button:
                button.setObjectName("CloseToolButton")
            else:
                button.setObjectName("ToolButton")

            title_bar_layout.addWidget(button)

    def connect_signals(self, parent):
        """Connect all signals to their corresponding slots."""
        self._connect_signal_group(self._get_file_signals(parent))
        self._connect_signal_group(self._get_run_signals(parent))
        self._connect_signal_group(self._get_view_signals(parent))
        self._connect_signal_group(self._get_help_signals(parent))

    def _connect_signal_group(self, signal_slot_dict):
        """Connect each signal to its corresponding slot."""
        for signal, slot in signal_slot_dict.items():
            signal.connect(slot)

    def _get_file_signals(self, parent):
        return {
            self.new_text_file_requested: parent.create_new_tab,
            self.new_window_requested: parent.create_new_window,
            self.open_file_requested: parent.open_file,
            self.open_folder_requested: parent.open_folder,
            self.save_requested: parent.save_tab,
            self.save_as_requested: parent.save_as,
            self.save_all_requested: parent.save_all,
            self.close_editor_requested: parent.close_editor,
            self.close_folder_requested: parent.close_folder,
            self.close_window_requested: parent.close_window,
            self.exit_requested: parent.exit,
        }    

    def _get_view_signals(self, parent):
        return {
            self.problems_requested: parent.show_problems,
            self.output_requested: parent.show_output,
            self.debug_console_requested: parent.show_debug_console,
            self.terminal_requested: parent.show_terminal,
        }

    def _get_run_signals(self, parent):
        return {
            self.run_without_debugging_requested: parent.run_without_debugging,
        }

    def _get_help_signals(self, parent):
        return {
            self.welcome_requested: parent.welcome,
            self.documentation_requested: parent.documentation,
            self.show_release_notes_requested: parent.show_release_notes,
            self.video_tutorials_requested: parent.video_tutorials,
            self.tips_and_tricks_requested: parent.tips_and_tricks,
            self.join_us_on_youtube_requested: parent.join_us_on_youtube,
            self.search_feature_requests_requested: parent.search_feature_requests,
            self.report_issue_requested: parent.open_issue_reporter,
            self.view_license_requested: parent.view_license,
            self.privacy_statement_requested: parent.privacy_statement,
            self.open_process_explorer_requested: parent.open_process_explorer,
            self.toggle_developer_options_requested: parent.open_developer_options,
            self.about_requested: parent.about,
        }

    def create_action(self, name, shortcut=None, parent=None, submenu_items=None):
        """Create actions that might have submenus."""
        action = QAction(name, parent)
        
        if shortcut:
            action.setShortcut(shortcut)

        if submenu_items:
            self.create_submenu(action, submenu_items)

        return action

    def create_submenu(self, parent_action, submenu_actions):
        """Create a submenu for the given parent action."""
        submenu = parent_action.menu()

        # Add actions to the submenu
        for submenu_action in submenu_actions:
            if submenu:
                submenu.addAction(submenu_action)

        # Assign the submenu to the parent action
        parent_action.setMenu(submenu)

    def add_actions_to_menu(self, menu, actions):
        for action in actions:
            if action is None:
                menu.addSeparator()
            else:
                menu.addAction(action)

    def go_back(self):
        print("Go Back")

    def go_forward(self):
        print("Go Forward")

    def search(self):
        print("Search")

    def toggle_primary_side_bar(self):
        if self.main_window.side_bar.isHidden():
            self.main_window.side_bar.show()

            return
        
        self.main_window.side_bar.hide()

    def toggle_panel(self):
        if self.main_window.panel.isHidden():
            self.main_window.panel.show()

            return
        
        self.main_window.panel.hide()

    def toggle_secondary_side_bar(self):
        if self.main_window.secondary_bar.isHidden():
            self.main_window.secondary_bar.show()

            return
        
        self.main_window.secondary_bar.hide()

    def customize_layout(self):
        print("Customize Layout")

    def window_state_changed(self, state):
        if state == Qt.WindowState.WindowMaximized:
            self.normal_button.setVisible(True)
            self.max_button.setVisible(False)
        else:
            self.normal_button.setVisible(False)
            self.max_button.setVisible(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = True
            self.start_pos = event.globalPosition().toPoint() - self.parent().pos() # Store the offset
            self.mousePressed.emit() # Emit signal

        super().mousePressEvent(event)
        event.accept()

    def mouseMoveEvent(self, event):
        if self.is_dragging:
            self.mouseMoved.emit(event.globalPosition().x(), event.globalPosition().y()) # Emit signal with current position

        super().mouseMoveEvent(event)
        event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = False
            self.mouseReleased.emit() # Emit signal

        super().mouseReleaseEvent(event)
        event.accept()

    def mouseDoubleClickEvent(self, event):
        # Restore or maximize the window on double-click
        if event.button() == Qt.MouseButton.LeftButton:
            if self.main_window.isMaximized():
                self.main_window.showNormal()
            else:
                self.main_window.showMaximized()
