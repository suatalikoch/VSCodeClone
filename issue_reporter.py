from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QTextEdit, QLabel,
                             QScrollArea, QPushButton, QCheckBox, QComboBox, QSizePolicy, QSpacerItem)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class IssueReporterWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window title and size
        self.setWindowTitle("Issue Reporter")
        self.setAutoFillBackground(True)
        self.setStyleSheet("background-color: #f8f8f8")
        self.setGeometry(100, 100, 684, 760)
        self.setMinimumSize(382, 230)

        self.issue_info_label = QLabel("Before you report an issue here please <a href='https://github.com/microsoft/vscode/wiki/Submitting-Bugs-and-Suggestions' style='color: #005fb8; text-decoration: none;'>review the guidance we provide</a>.")
        self.issue_info_label.setFont(QFont(self.issue_info_label.font().family(), 12))
        self.issue_info_label.setOpenExternalLinks(True)

        # Add a combo box for selecting issue type
        self.issue_type_combo = QComboBox(self)
        self.issue_type_combo.addItems(["Bug Report", "Feature Request", "Performance Issues (freeze, slow, crash)"])
        self.issue_type_combo.setCursor(Qt.CursorShape.PointingHandCursor)
        self.issue_type_combo.setStyleSheet(
            """
                QComboBox {
                    border: none;
                    height: 36px;
                    font-size: 15px;
                    background-color: #ffffff;
                }

                QComboBox:focus {
                    border: 1px solid #005fb8;
                }
            """
        )

        self.issue_type_label = QLabel("This is a")
        self.issue_type_label.setFont(QFont(self.issue_info_label.font().family(), 12))

        self.layout_issue_type = QHBoxLayout()
        self.layout_issue_type.addWidget(self.issue_type_label)
        self.layout_issue_type.addWidget(self.issue_type_combo)

        # Add a combo box for selecting issue source
        self.issue_for_combo = QComboBox(self)
        self.issue_for_combo.addItems(["Select source", "Visual Studio Code", "A VS Code extension", "Extensions Marketplace", "Don't know"])
        self.issue_for_combo.setCursor(Qt.CursorShape.PointingHandCursor)
        self.issue_for_combo.setStyleSheet(
            """
                QComboBox {
                    border: none;
                    height: 36px;
                    font-size: 15px;
                    background-color: #ffffff;
                }

                QComboBox:focus {
                    border: 1px solid #005fb8;
                }
            """
        )

        self.issue_for_label = QLabel("For <font color='#cb1100'>*</font>")
        self.issue_for_label.setFont(QFont(self.issue_info_label.font().family(), 12))

        self.layout_issue_for = QHBoxLayout()
        self.layout_issue_for.addWidget(self.issue_for_label)
        self.layout_issue_for.addWidget(self.issue_for_combo)

        # Add system/environment details (form layout)
        self.issue_title = QLineEdit(self)
        self.issue_title.setPlaceholderText("Please enter a title.")
        self.issue_title.setFont(QFont(self.issue_info_label.font().family(), 12))
        self.issue_title.setCursor(Qt.CursorShape.PointingHandCursor)
        self.issue_title.setStyleSheet(
            """
                QLineEdit {
                    height: 34px;
                    background-color: #ffffff;
                    border: 1px solid #ced4da;
                }

                QLineEdit:focus {
                    border: 1px solid #005fb8;
                }
            """
        )

        self.issue_title_label = QLabel("Title <font color='#cb1100'>*</font>")
        self.issue_title_label.setFont(QFont(self.issue_info_label.font().family(), 12))
        self.issue_title_label.setCursor(Qt.CursorShape.PointingHandCursor)

        self.layout_issue_title = QHBoxLayout()
        self.layout_issue_title.addWidget(self.issue_title_label)
        self.layout_issue_title.addWidget(self.issue_title)

        # Add steps to reproduce
        self.steps_to_reproduce = QTextEdit(self)
        self.steps_to_reproduce.setPlaceholderText("Please enter details.")
        self.steps_to_reproduce.setMinimumHeight(150)
        self.steps_to_reproduce.setStyleSheet(
            """
                QTextEdit {
                    padding: 1px;
                    border: none;
                    font-size: 16px;
                    background-color: #ffffff;
                }

                QTextEdit:focus {
                    border: 1px solid #005fb8;
                }
            """
        )

        self.steps_to_reproduce_label = QLabel("Steps to Reproduce <font color='#cb1100'>*</font>")
        self.steps_to_reproduce_label.setFont(QFont(self.steps_to_reproduce_label.font().family(), 12))

        self.reproduce_details = QLabel("Share the steps needed to reliably reproduce the problem. Please include actual and expected results. We support GitHub-flavored Markdown. You will be able to edit your issue and add screenshots when we preview it on GitHub.")
        self.reproduce_details.setWordWrap(True)
        
        self.system_information_label = QLabel("Include my system information (<a href='#'>show</a>)")
        self.system_information = QCheckBox(self.system_information_label.text())
        self.system_information.setCursor(Qt.CursorShape.PointingHandCursor)
        self.system_information.setChecked(True)
        
        self.enabled_extensions_label = QLabel("Include my enabled extensions (<a href='#'>show</a>)")
        self.enabled_extensions = QCheckBox(self.enabled_extensions_label.text())
        self.enabled_extensions.setCursor(Qt.CursorShape.PointingHandCursor)
        self.enabled_extensions.setChecked(True)
        
        self.experiment_info_label = QLabel("Include A/B experiment info (<a href='#'>show</a>)")
        self.experiment_info = QCheckBox(self.experiment_info_label.text())
        self.experiment_info.setCursor(Qt.CursorShape.PointingHandCursor)
        self.experiment_info.setChecked(True)
        
        # Add a button to submit the report
        self.submit_button = QPushButton("Preview on GitHub", self)
        self.submit_button.clicked.connect(self.submit_report)
        self.submit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.submit_button.setStyleSheet(
            """
                QPushButton {
                    padding: 6px 10px;
                    background-color: #005fb8;
                    border-radius: 2px;
                    color: #ffffff;
                }

                QPushButton:hover {
                    background-color: #0258a8;
                }
            """
        )

        self.layout_end = QHBoxLayout()
        self.layout_end.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.layout_end.addWidget(self.submit_button)

        large_widget = QWidget(self)
        large_layout = QVBoxLayout(large_widget)

        large_layout.addWidget(self.issue_info_label)
        large_layout.addSpacing(20)
        large_layout.addLayout(self.layout_issue_type)
        large_layout.addSpacing(20)
        large_layout.addLayout(self.layout_issue_for)
        large_layout.addSpacing(20)
        large_layout.addLayout(self.layout_issue_title)
        large_layout.addSpacing(16)
        large_layout.addWidget(self.steps_to_reproduce_label)
        large_layout.addWidget(self.reproduce_details)
        large_layout.addSpacing(6)
        large_layout.addWidget(self.steps_to_reproduce)
        large_layout.addSpacing(6)
        large_layout.addWidget(self.system_information)
        large_layout.addWidget(self.enabled_extensions)
        large_layout.addWidget(self.experiment_info)
        large_layout.addLayout(self.layout_end)

        large_layout.setContentsMargins(50, 25, 50, 40)

        large_widget.setLayout(large_layout)

        scroll_area = QScrollArea(self)
        scroll_area.setWidget(large_widget)
        scroll_area.setStyleSheet("border: none;")
        scroll_area.setWidgetResizable(True)

        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(scroll_area)

        # Set the main layout for the window
        self.setLayout(layout)

    def submit_report(self):
        """Handle the submission of the issue report."""
        # Collect the information entered by the user
        issue_type = self.issue_type_combo.currentText()
        issue_for = self.issue_for_combo.currentText()
        issue_title = self.issue_title.text()
        steps_to_reproduce = self.steps_to_reproduce.toPlainText()
        system_information = self.system_information.isChecked()
        enabled_extensions = self.enabled_extensions.isChecked()
        experiment_info = self.experiment_info.isChecked()

        # For now, we just print the collected information to the console
        print("Issue Report Submitted:")
        print(f"This is a: {issue_type}")
        print(f"For: {issue_for}")
        print(f"Title: {issue_title}")
        print(f"Steps to Reproduce: {steps_to_reproduce}")
        print(f"Include my system information: {system_information}")
        print(f"Include my enabled extensions: {enabled_extensions}")
        print(f"Include A/B experiment info: {experiment_info}")

        # In a real application, you could send the report to a server or save it as a file.
        # Example of how to send it to a server:
        # send_to_server(issue_description, steps_to_reproduce, os_version, python_version, app_version, issue_type)

        # You can add further logic to handle form submission here (e.g., saving to a file, sending via email, etc.)
        self.close()
