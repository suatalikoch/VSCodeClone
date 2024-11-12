import subprocess, datetime, os, json, logging

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTextEdit, QVBoxLayout, QListWidget
from PyQt6.QtGui import QFont, QTextCursor

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] - %(message)s", datefmt="%d/%m/%Y %H:%M:%S")

class TerminalWidget(QTextEdit):
    DEFAULT_COMMANDS = ["run", "exit", "help", "clear", "list", "status", "quit"]

    def __init__(self, parent=None):
        """Initialize the terminal with necessary configurations and load commands"""
        super().__init__(parent)

        self.setReadOnly(False)
        self.setFont(QFont("Consolas", 10))
        self.setObjectName("TerminalTab")
        self.clear_terminal()

        self.cursor = self.textCursor()
        self.cursor.movePosition(QTextCursor.MoveOperation.End)
        
        self.command_history = []
        self.history_index = -1 # Starting with -1 means no commands are loaded yet

        # Setup for suggestions
        self.suggestions_widget = QListWidget(self) # Create a list widget for suggestions
        self.suggestions_widget.setFixedWidth(200)
        self.suggestions_widget.setObjectName("Suggestions")
        self.suggestions_widget.hide() # Initially hide it

        layout = QVBoxLayout(self)
        layout.addWidget(self.suggestions_widget)

        self.setLayout(layout)

        self.commands = []
        self.load_commands()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return:
            command = self.get_current_command()
            
            if command:
                self.execute_command(command)
                self.command_history.append(command)  # Store the command in history
                self.history_index = len(self.command_history)  # Reset index for new command
                logging.info(f"Executed command: {command}.")
        elif event.key() in (Qt.Key.Key_Up, Qt.Key.Key_Down):
            direction = 1 if event.key() == Qt.Key.Key_Down else -1
            self.navigate_history(direction)
            self.suggestions_widget.setCurrentRow(self.suggestions_widget.currentRow() + (1 if event.key() == Qt.Key.Key_Down else -1))

            return # Early exit after handling Up key
        elif event.key() == Qt.Key.Key_Tab: # Use Tab for auto-completion
            current_line = self.get_current_command()
            completions = self.auto_complete(current_line)

            if completions:
                self.insert_completion(completions[0])
        else:
            super().keyPressEvent(event)
        
        # Hide suggestions after handling command input or execution
        self.suggestions_widget.hide()
        self.handle_suggestions()

    def navigate_history(self, direction):
        """Navigate through command history."""
        if self.command_history:
            new_index = self.history_index + direction
            
            if 0 <= new_index < len(self.command_history):
                self.history_index = new_index
                self.set_text_from_history()
                logging.info(f"Navigated history: index {self.history_index}, command: {self.command_history[self.history_index]}")

    def get_current_command(self):
        """Get the last line of the terminal input."""
        return self.toPlainText().splitlines()[-1].strip()

    def insert_text_at_cursor(self, text):
        """Inserts the given text at the cursor position."""
        cursor = self.textCursor()                    # Move the cursor to the start of the last line
        cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock) # Move to the start of the current line
        cursor.select(QTextCursor.SelectionType.LineUnderCursor)    # Select the current line
        cursor.removeSelectedText()                   # Remove the current line
        cursor.insertText(text)                       # Insert the completed command
        cursor.movePosition(QTextCursor.MoveOperation.End)          # Move cursor to the end of the line
        self.setTextCursor(cursor)                    # Set the cursor back to the QTextEdit

    def handle_suggestions(self):
        """"Show suggestions based on current input."""
        current_line = self.get_current_command()

        if current_line:
            completions = self.auto_complete(current_line)

            if completions:
                self.show_suggestions(completions)
            else:
                self.suggestions_widget.hide()

    def auto_complete(self, command):
        """Find and return matching commands for autocompletion."""
        if not command:
            return [] # Return empty if no command is provided
        
        command_lower = command.lower()
        matches = []

        for cmd in self.commands:
            cmd_lower = cmd.lower()

            if cmd_lower == command_lower:
                matches.insert(0, cmd) # Add exact match at the front
            elif command_lower in cmd_lower:
                matches.append(cmd) # Add substring match

        # Log the autocompletion attempt
        logging.info(f"Autocompletion for '{command}': Found matches: {matches}")

        return matches

    def show_suggestions(self, completions):
        """Display the list of completion suggestions."""
        if not completions:
            self.suggestions_widget.hide()

            return # Early exit if there are no completions
        
        # Clear the suggestions list and add new completions
        self.suggestions_widget.clear()
        self.suggestions_widget.addItems(completions)

        # Get the current cursor position
        cursor = self.textCursor()
        cursor_rect = self.cursorRect(cursor)

        # Get global position for the widget
        global_pos = self.mapToGlobal(cursor_rect.bottomLeft())

        # Calculate the width of the current text
        current_text = self.get_current_command()
        text_width =self.fontMetrics().horizontalAdvance(current_text)

        # Move the suggestions list just after the command text
        # Adjust the x position to the right of the current command
        self.suggestions_widget.move(global_pos.x() + text_width, global_pos.y())
        
        # Show the suggestions list
        self.suggestions_widget.show()

    def insert_completion(self, completion):
        """Insert the completion suggestion into the current line."""
        self.insert_text_at_cursor(completion)

        # Log the action
        logging.info(f"Inserted completion: {completion}.")

    def set_text_from_history(self):
        """Set the current line to the selected history command."""
        if self.command_history and 0 <= self.history_index < len(self.command_history):
            last_command = self.command_history[self.history_index]
            
            self.insert_text_at_cursor(last_command)

            #Log the action
            logging.info(f"Set command from history: {last_command}.")
        else:
            logging.warning("History index out of bounds.")

    def execute_command(self, command):
        """Execute a shell command and display the output."""
        if command.strip():
            timestamp = datetime.datetime.now().strftime("[%d/%m/%Y %H:%M:%S]")
            self.append(f"{timestamp} > {command}")

            try:
                # Run the command in a subprocess
                result = subprocess.run(command.split(), capture_output=True, text=True, check=False)
                self.append(result.stdout) # Append standard output

                if result.stderr:
                    self.append(f"Error: {result.stderr}.") # Append standard error if any

                logging.info(f"Executed command successfully: {command}.") # Log success
            except subprocess.CalledProcessError as e:
                logging.error(f"Command failed: {e}. Command {command}, Return Code: {e.returncode}, stderr: {e.stderr}.")
                self.append(f"Error: Command failed with return code {e.returncode}.")
                self.append(f"stderr: {e.stderr}.")
            except FileNotFoundError as e:
                logging.error(f"FileNotFoundError: {e}. Command {command}.")
                self.append(f"Error: Command not found.")
            except Exception as e:
                logging.error(f"An unexpected error occured: {e}. Command: {command}.")
                self.append(f"An unexpected error occured: {e}.")

            self.append("")  # Add a new line for the next command

    def clear_terminal(self, welcome_message="Welcome to the terminal.\n"):
        """Clear the terminal and display an optional welcome message."""
        self.clear()
        self.append(welcome_message)
        logging.info("Terminal cleared.")

    def load_commands(self, config_file="configuration/commands.json"):
        config_dir = os.path.dirname(config_file)

        # Ensure the directory exists
        if not os.path.exists(config_dir):
            logging.warning(f"Configuration directory NOT found.")
            self.create_default_dir(config_dir)

        # Load or create the config file
        if os.path.exists(config_file):
            self.load_from_file(config_file)
        else:
            logging.warning(f"Config file '{config_file}' not found.")
            self.create_default_config(config_file)

    def load_from_file(self, config_file):
        """Load commands from the specified JSON configuration file."""
        try:
            with open(config_file, 'r') as file:
                data = json.load(file)
                self.commands = data.get("commands", [])
            logging.info(f"Loaded commands from '{config_file}.'")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"Error loading commands: {e}.")

    def create_default_config(self, config_file):
        """Create a default configuration file with default commands."""
        self.commands = self.DEFAULT_COMMANDS

        try:
            with open(config_file, 'w') as file:
                json.dump({"commands": self.commands}, file)
            logging.info(f"Created default configuration file: '{config_file}.'")
        except IOError as e:
           logging.error(f"Error writing to config file: {e}.")
    
    def create_default_dir(self, config_dir):
        """Create the configuration directory if it does not exists."""
        try:
            os.makedirs(config_dir)
            logging.info(f"Created configuration directory: '{config_dir}.'")
        except OSError as e:
            logging.error(f"Error creating directory '{config_dir}: {e}.'")
