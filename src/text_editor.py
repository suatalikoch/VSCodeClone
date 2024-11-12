from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtGui import QFont

class TextEditor(QTextEdit):
    def __init__(self, object_name, font="Consolas", font_size=11, content=None, parent=None):
        super().__init__(parent)

        self.setFont(QFont(font, font_size))
        self.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.setObjectName(object_name)
        self.append(content)
        self.setStyleSheet(self.get_text_editor_style())

    def get_text_editor_style(self):
        return """
            QTextEdit#TextEditor {
                background-color: #ffffff;
                border: none;
            }

            QTextEdit#TextEditor QScrollBar {
                background: #ffffff;
            }

            QTextEdit#TextEditor QScrollBar::handle {
                background-color: #c1c1c1;
            }

            QTextEdit#TextEditor QScrollBar::handle:hover {
                background-color: #929292;
            }

            QTextEdit#TextEditor QScrollBar::handle:pressed {
                background-color: #666666;
            }

            QTextEdit#TextEditor QScrollBar::handle:vertical {
                min-height: 20px;
            }
                
            QTextEdit#TextEditor QScrollBar::add-line, QScrollBar::sub-line {
                background: none;
            }

            QTextEdit#TextEditor QScrollBar::up-arrow, QScrollBar::down-arrow {
                background: none;
            }

            QTextEdit#TextEditor QScrollBar:vertical {
                border-left: 1px solid #f2f2f2;
                width: 13px;
            }

            QTextEdit#TextEditor QScrollBar:horizontal {
                border-top: 1px solid #f2f2f2;
                border-left: 1px solid #f2f2f2;
                border-right: 1px solid #f2f2f2;
                height: 13px;
            }

            QTextEdit#TextEditor QScrollBar::handle:horizontal {
                min-width: 20px;
            }

            QTextEdit#NewTab {
                border: none;
            }
        """
