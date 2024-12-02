import os, json, logging

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile

logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] [%(levelname)s] - %(message)s", datefmt="%d/%m/%Y %H:%M:%S")

class MonacoEditor(QWebEngineView):
    def __init__(self, parent, object_name="MonacoEditor", font="Consolas", font_size=11, content=None, theme="vs-light", file_path=None):
        super().__init__(parent)

        profile = QWebEngineProfile.defaultProfile()
        profile.settings().setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        profile.settings().setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True)
        profile.settings().setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
        profile.settings().setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, False)

        self.setObjectName(object_name)
        self.setFont(QFont(font, font_size))
        self.loadFinished.connect(self.setup_monaco_editor)

        self.monaco_ready = False
        self.retry_count = 0
        self.max_retries = 5
        self.theme = theme

        if content:
            self.content = content
            QTimer.singleShot(1000, lambda: self.set_content(content))

        self.file_path = file_path or ""
        self.folder_path = os.path.dirname(self.file_path).split('/')[-1]
        self.file_name = os.path.basename(self.file_path)

        self.setHtml(self.create_editor_html())

    def create_editor_html(self):
        """Generates the HTML needed to initialize Monaco editor."""
        with open("D:/Projects/GitHub/VSCodeClone/html/monaco_editor.html", 'r') as file:
            html_content = file.read()

        return html_content

    def setup_monaco_editor(self):
        """This method will be called when the page finishes loading"""
        logging.debug("Monaco Editor has finished loading.")

        self.check_monaco_ready()

    def check_monaco_ready(self):
        """Checks if Monaco editor is ready by running JavaScript."""
        self.page().runJavaScript(
            """
                function checkMonacoReady() {
                    if (window.monacoReady) {
                        return 'ready';
                    }
                    return 'not_ready';
                }
                checkMonacoReady();
            """, self.on_monaco_ready
        )

    def on_monaco_ready(self, result):
        """Callback for when Monaco is ready."""
        if result == "ready":
            logging.info("Monaco Editor is fully initialized.")
            
            self.monaco_ready = True

            if hasattr(self, 'content'):
                self.set_content(self.content) # Set initial content once Monaco is ready
        else:
            logging.warning("Monaco Editor is not ready yet. Retrying...")

            self.retry_count += 1

            if self.retry_count < self.max_retries:
                QTimer.singleShot(1000 * self.retry_count, self.check_monaco_ready)
            else:
                logging.error("Failed to initialize Monaco Editor after multiple retries.")

    def on_content_received(self, content):
        """Handles the content returned from Monaco editor."""
        logging.debug(f"Received content: {content}.")

        return content

    def is_modified(self):
        """Check if Monaco editor content is modified by querying the JS flag."""
        self.page().runJavaScript(
            """
                function isModified() {
                    if (window.isModified) {
                        return true;
                    }
                    return false;
                }
                isModified();
            """, self._on_is_modified
        )

    def _on_is_modified(self, result):
        self.is_modified = result
        logging.debug(f"Monaco content modified: {self.is_modified}")

    def get_content(self, callback, file_path, retry_count=0):
        """Retrieves content from the Monaco editor and calls the provided callback."""
        if not self.monaco_ready:
            if retry_count < self.max_retries:
                logging.warning("Monaco Editor is not ready. Retrying to get content...")
                QTimer.singleShot(1000, lambda: self.get_content(callback, retry_count + 1))
            else:
                logging.error("Failed to get content after multiple retries.")

            return

        js_code = """
            var model = monaco.editor.getModels()[0]; // Get the first editor model
            model.getValue(); // Get content from the model
        """

        return self.page().runJavaScript(js_code, lambda result: callback(result, file_path))

    def append_content(self, additional_content, retry_count=0):
        """Appends content to the Monaco editor's current content."""
        if not self.monaco_ready:
            if retry_count < self.max_retries:
                logging.warning("Monaco Editor is not ready. Retrying to append content...")
                QTimer.singleShot(1000, lambda: self.append_content(additional_content, retry_count + 1))
            else:
                logging.error("Failed to append content after multiple retries.")

            return
        
        # Escape the content properly using json.dumps() to handle special characters
        additional_content = json.dumps(additional_content)
        
        js_code = f"""
            var model = monaco.editor.getModels()[0];  // Get the first editor model
            var currentContent = model.getValue();  // Get the current content
            model.setValue(currentContent + {additional_content});  // Append the new content
        """
    
        self.page().runJavaScript(js_code)

    def set_content(self, content, retry_count=0):
        if not self.monaco_ready:
            if retry_count < self.max_retries:
                logging.warning("Monaco Editor is not ready. Retrying to set content...")
                QTimer.singleShot(1000, lambda: self.set_content(content, retry_count + 1))
            else:
                logging.error("Failed to set content after multiple retries.")

            return

        # Ensure that the content is safely escaped, handling quotes and newlines
        escaped_content = json.dumps(content)

        js_code = f"""
            var model = monaco.editor.getModels()[0];  // Get the first editor model
            model.setValue({escaped_content});  // Set content in the model
        """
        
        self.page().runJavaScript(js_code)

    def set_font(self, font, size):
        """Sets the font for the Monaco editor."""
        if not self.monaco_ready:
            logging.error("Monaco Editor is not ready. Cannot set font.")

            return
        
        self.page().runJavaScript(
            f"""
                document.getElementById('container').style.fontFamily = '{font}';
                document.getElementById('container').style.fontSize = '{size}px';
            """
        )

        logging.info(f"Font set to: {font}.")

    def set_theme(self, theme):
        """Dynamically changes the Monaco Editor theme."""
        if not self.monaco_ready:
            logging.error("Monaco Editor is not ready. Cannot set theme.")

            return
        
        self.theme = theme
        self.page().runJavaScript(f"monaco.editor.setTheme('{theme}');")

        logging.info(f"Theme set to: {theme}.")

    def resize_monaco_editor(self):
        """Resizes Monaco editor when the parent widget is resized."""
        self.page().runJavaScript(
            """
                if (window.monacoEditor) {
                    window.monacoEditor.layout();  // Adjust Monaco editor size to match the container's new size
                }
            """
        )

    def resizeEvent(self, event):
        """Override resizeEvent to trigger Monaco's resize when the window is resized."""
        super().resizeEvent(event)
        # Call Monaco resize on window resize
        self.resize_monaco_editor()
