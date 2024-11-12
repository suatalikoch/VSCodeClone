import os, psutil

from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView

class ProcessWorker(QThread):
    # Signal to send data back to the main thread
    data_updated = pyqtSignal(list)
    
    def __init__(self, project_dir):
        super().__init__()

        self.project_dir = project_dir
        self.running = True  # Flag to control the thread loop

    def run(self):
        """Run the worker thread. Fetch processes continuously in the background."""
        while self.running:
            processes = self.get_project_processes(self.project_dir)

            # Fetch CPU and memory data asynchronously
            for proc in processes:
                self.fetch_process_data(proc)  # Fetch the data for each process

            self.data_updated.emit(processes)  # Emit the updated process list to the main thread
            self.msleep(10000)  # Sleep for 1 second before the next fetch

    def stop(self):
        """Stop the worker thread."""
        self.running = False
        self.quit()
        self.wait()

    def get_project_processes(self, project_dir):
        """Get processes running in the specified project directory."""
        project_processes = []

        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cwd']):
            try:
                # Check if the process is running in the project directory
                if proc.info['cwd'] and proc.info['cwd'].startswith(project_dir):
                    project_processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return project_processes

    def fetch_process_data(self, proc):
        """Fetch CPU and memory usage for a process."""
        # Fetch CPU usage asynchronously with minimal delay
        proc.cpu_percent(interval=None)  # Only trigger cpu_percent calculation without blocking
        # You don't need to call cpu_percent(interval=0.1) in the UI thread, fetch it here.

        # Update memory usage
        proc.mem_usage = proc.memory_info().rss / (1024 * 1024)  # Convert from bytes to MB

class ProcessMonitor(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Process Explorer")
        self.resize(960, 470)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        layout = QVBoxLayout(self)

        # Create QTableWidget and set column count and headers
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(6)  # Columns: Process Name, Command, Working Dir, CPU, Memory, PID
        self.tableWidget.setHorizontalHeaderLabels(
            ["Process Name", "Command", "Working Dir", "CPU (%)", "Memory (MB)", "PID"]
        )
        self.tableWidget.setAlternatingRowColors(True)

        # Make the first column stretchable
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

        # Add the table to the layout
        layout.addWidget(self.tableWidget)

        # Get the project directory and create the worker thread to fetch process data
        project_dir = os.path.dirname(os.path.abspath(__file__))  # Get the project directory
        self.worker = ProcessWorker(project_dir)
        self.worker.data_updated.connect(self.update_process_list)
        self.worker.start()

        self.setLayout(layout)

    def update_process_list(self, processes):
        """Update the QTableWidget with new process data."""
        self.tableWidget.setRowCount(len(processes))  # Update the table row count

        for row, proc in enumerate(processes):
            # Update CPU usage by calling cpu_percent (with a small interval)
            cpu_usage = proc.cpu_percent()  # Incremental update

            # Get memory usage in MB (convert bytes to MB)
            mem_usage_mb = proc.mem_usage

            # Add data to each row
            self.tableWidget.setItem(row, 0, QTableWidgetItem(proc.info['name']))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(" ".join(proc.info['cmdline'])))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(proc.info['cwd'] or "N/A"))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(f"{int(cpu_usage)}"))
            self.tableWidget.setItem(row, 4, QTableWidgetItem(f"{int(mem_usage_mb)}"))
            self.tableWidget.setItem(row, 5, QTableWidgetItem(str(proc.info['pid'])))

    def closeEvent(self, event):
        """Ensure worker thread is stopped properly when the window is closed."""
        self.worker.stop()
        event.accept()
