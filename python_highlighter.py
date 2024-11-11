from PyQt6.QtGui import QColor, QTextCharFormat, QSyntaxHighlighter
from PyQt6.QtCore import QRegularExpression

class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)

        self.highlighting_rules = []
        self.setup_highlighting()

    def setup_highlighting(self):
        # Define formats for different syntax elements
        self.add_highlighting_rule(r'\b(def|class|lambda|global|nonlocal|match|case)\b', QColor("#0000ff"))  # Definitions
        self.add_highlighting_rule(r'\b(if|elif|else|while|for|try|in|is|not|and|or|except|with|break|continue|pass)\b', QColor("#af00db"))  # Control flow
        self.add_highlighting_rule(r'\b(import|from|as|return|raise|async|await|del|assert|yield)\b', QColor("#af00db"))  # Other keywords
        self.add_highlighting_rule(r'\b(len|print|range|type|str|int|float|list|dict|set|tuple|bool|input|open|sum|max|min|map|filter|zip|enumerate|sorted|reversed|all|any)\b', QColor("#795e26"))  # Built-ins
        self.add_highlighting_rule(r'\b(True|False|None)\b', QColor("#0000ff"))  # Constants
        self.add_highlighting_rule(r'(?<!\w)(@\w+)', QColor("#795e88"))  # Decorators
        self.add_highlighting_rule(r'\"([^"\\]*(\\.)?)*\"|\'([^\'\\]*(\\.)?)*\'', QColor("#a31515"))  # Strings
        self.add_highlighting_rule(r'(#.*$)', QColor("#008000"))  # Comments
        self.add_highlighting_rule(r'\'\'\'(.*?)\'\'\'|\"\"\"(.*?)\"\"\"', QColor("#a31515"))  # Multiline comments
        self.add_highlighting_rule(r'\b\d+(\.\d+)?\b', QColor("#098658"))  # Numbers
        self.add_highlighting_rule(r'\b[a-zA-Z_][a-zA-Z0-9_]*\s*:\s*[a-zA-Z_][a-zA-Z0-9_]*\b', QColor("darkcyan"))  # Type annotations
        self.add_highlighting_rule(r'\b(KeyError|ValueError|TypeError)\b', QColor("#267f99"))  # Exceptions

    def add_highlighting_rule(self, pattern, color):
        fmt = QTextCharFormat()
        fmt.setForeground(color)
        self.highlighting_rules.append((pattern, fmt))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            expression = QRegularExpression(pattern)
            match_iterator = expression.globalMatch(text)

            while match_iterator.hasNext():
                match = match_iterator.next()
                start = match.capturedStart()
                length = match.capturedLength()
                self.setFormat(start, length, fmt)
