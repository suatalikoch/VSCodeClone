#from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QFont
from PyQt6.QtWebEngineWidgets import QWebEngineView

# Importing PyQt5 for QScintilla
#from PyQt5.QtWidgets import QPlainTextEdit  # For using QScintilla
#from QScintilla.Qsci import QsciScintilla, QsciLexerPython

class MonacoEditor(QWebEngineView):
    def __init__(self, object_name, font="Consolas", font_size=11, content=None, parent=None):
        super().__init__(parent)

        self.setFont(QFont(font, font_size))
        #self.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.setObjectName(object_name)
        #self.append(content)
        self.setStyleSheet(self.get_text_editor_style())

        self.setUrl(QUrl("https://cdn.jsdelivr.net/npm/monaco-editor@0.38.0/min/vs/loader.js"))
        self.loadFinished.connect(self.setup_monaco_editor)

        html_content = """
        <html>
            <head>
                <!-- Load require.js -->
                <script src="https://cdn.jsdelivr.net/npm/requirejs@2.3.6/require.js"></script>
                <script>
                    // Configure require.js to load Monaco from the CDN
                    require.config({ 
                        paths: { 'vs': 'https://cdn.jsdelivr.net/npm/monaco-editor@0.38.0/min/vs' } 
                    });

                    // When require.js is loaded, initialize Monaco Editor
                    require(['vs/editor/editor.main'], function() {
                        monaco.editor.create(document.body, {
                            value: 'def hello_world():\\n    print("Hello from Monaco!")',
                            language: 'python',
                            theme: 'vs-light',
                            automaticLayout: true
                        });
                    });
                </script>
            </head>
            <body style="margin:0; height:100%;">
            </body>
        </html>
        """
        
        # Load the Monaco HTML content directly into QWebEngineView
        self.setHtml(html_content)

    def setup_monaco_editor(self):
        """This method will be called when the page finishes loading"""
        print("Monaco Editor has finished loading.")

        # Optionally, you could run more JavaScript code here to interact with Monaco

    def set_content(self, content):
        # Ensure that the content is safely escaped, handling quotes and newlines
        content = content.replace("'", "\\'").replace("\n", "\\n").replace("\r", "")
        
        # Run JavaScript to set the value in Monaco
        self.page().runJavaScript(
            f"""
                monaco.editor.getModels()[0].setValue('{content}');
            """
        )

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
