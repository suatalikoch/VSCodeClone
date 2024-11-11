import os, sys, subprocess

from PyQt6.QtCore import QThread, pyqtSignal

class PylintWorker(QThread):
    finished = pyqtSignal(str)

    def __init__(self, code):
        super().__init__()

        self.code = code

    def run(self):
        # Save the current content to a temporary file for Pylint to analyze
        with open("temp_code.py", 'w') as temp_file:
            temp_file.write(self.code)

        # Run Pylint on the temporary file
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pylint", "temp_code.py"],
                capture_output=True,
                text=True,
                check=False
            )
            os.remove("temp_code.py") # Clean up temporary file
            self.finished.emit(result.stdout)  # Emit the results back to the main thread
        except FileNotFoundError as fnf_error:
            self.finished.emit(f"Pylint not found: {fnf_error}.")
        except SyntaxError as e:
            self.finished.emit(f"Failed to run Pylint: {e}.")
