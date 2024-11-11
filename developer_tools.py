from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QAbstractItemView, QLayout
from PyQt6.QtCore import QEvent, QObject, Qt
from PyQt6.QtGui import QFont

class DeveloperToolsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)

        # Label to display widget info
        self.info_label = QLabel("Hover over a widget to inspect it", self)
        layout.addWidget(self.info_label)

        self.setLayout(layout)

    def update_widget_info(self, widget):
        """Update the panel with detailed widget information when hovered."""
        widget_info = f"Widget Type: {widget.__class__.__name__}\n"
        widget_info += f"Object Name: {widget.objectName()}\n"
        widget_info += f"Geometry: {widget.geometry()}\n"
        widget_info += f"Position: {widget.pos()}\n"
        widget_info += f"Size: {widget.size()}\n"
        widget_info += f"Rect: {widget.rect()}\n"
        widget_info += f"Is Visible: {widget.isVisible()}\n"
        widget_info += f"Is Enabled: {widget.isEnabled()}\n"
        widget_info += f"Is Window: {widget.isWindow()}\n"
        widget_info += f"Has Focus: {widget.hasFocus()}\n"
        widget_info += f"Is Active Window: {widget.isActiveWindow()}\n"
        widget_info += f"Parent Widget: {widget.parentWidget() if widget.parentWidget() else 'None'}\n"
        widget_info += f"Children Count: {len(widget.findChildren(QWidget))}\n"
        
        # Geometry/Size constraints
        widget_info += f"Minimum Size: {widget.minimumSize()}\n"
        widget_info += f"Maximum Size: {widget.maximumSize()}\n"
        
        # Layout and sizing info
        layout = widget.layout
        
        widget_info += f"Has Layout: {'Yes' if layout else 'No'}\n"
        
        if layout:
            if isinstance(layout, QLayout):
                widget_info += f"Layout Spacing: {layout.spacing()}\n"
            else:
                widget_info += "Layout Spacing: N/A\n"
        
        widget_info += f"Cursor Shape: {widget.cursor().shape()}\n"
        widget_info += f"Focus Policy: {widget.focusPolicy()}\n"
        widget_info += f"Context Menu Policy: {widget.contextMenuPolicy()}\n"
        
        # Focusable status
        widget_info += f"Is Focusable: {'Yes' if widget.focusPolicy() != Qt.FocusPolicy.NoFocus else 'No'}\n"
        
        # Is Right to Left (useful for RTL languages)
        widget_info += f"Is Right to Left: {'Yes' if widget.isRightToLeft() else 'No'}\n"
        
        # Tooltips & StatusTip
        widget_info += f"ToolTip: {widget.toolTip() if widget.toolTip() else 'None'}\n"
        widget_info += f"StatusTip: {widget.statusTip() if widget.statusTip() else 'None'}\n"
        widget_info += f"WhatsThis: {widget.whatsThis() if widget.whatsThis() else 'None'}\n"
        
        # Actionable status
        widget_info += f"Actions: {len(widget.actions())} actions\n"
        
        # Window Flags and Style
        widget_info += f"Window Flags: {widget.windowFlags()}\n"
        widget_info += f"Style: {widget.style().objectName()}\n"
        
        # Interaction/Selection Model
        if isinstance(widget, QAbstractItemView):
            widget_info += f"Selection Model: {widget.selectionModel()}\n"

        # Dynamic Properties
        dynamic_properties = widget.dynamicPropertyNames()
        if dynamic_properties:
            widget_info += f"Dynamic Properties: {', '.join([str(prop) for prop in dynamic_properties])}\n"
        
        # Font details
        font: QFont = widget.font()
        widget_info += f"Font: {font.family()}, Size: {font.pointSize()}, Weight: {font.weight()}\n"
        
        # Background color
        background_color = widget.palette().color(widget.backgroundRole())
        widget_info += f"Background Color: {background_color.name()}\n"
        
        # Drag-and-Drop Support
        widget_info += f"Accepts DnD: {'Yes' if widget.acceptDrops() else 'No'}\n"
        
        # Mouse Tracking
        widget_info += f"Mouse Tracking Enabled: {'Yes' if widget.hasMouseTracking() else 'No'}\n"
        
        # Styles
        widget_info += f"Palette: {widget.palette().color(widget.foregroundRole()).name()}\n"  # Foreground color
        widget_info += f"Stylesheet: {widget.styleSheet() if widget.styleSheet() else 'None'}\n"

        # Update the label to show the detailed information
        self.info_label.setText(widget_info)

class HoverEventFilter(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

    def eventFilter(self, obj, event):
        """This is the event filter function for hovering."""
        if event.type() == QEvent.Type.HoverEnter:
            if isinstance(obj, QWidget):
                # Send info of the widget that the mouse is hovering over
                self.parent().developer_tools.update_widget_info(obj)

        return super().eventFilter(obj, event)
