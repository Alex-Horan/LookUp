from PyQt6 import QtCore
from PyQt6 import QtWidgets
from PyQt6.QtCore import QUrl, Qt  
from PyQt6.QtWidgets import QWidget, QScrollArea
from PyQt6.QtGui import QWheelEvent

class DraggableTabStrip(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def wheelEvent(self, event: QWheelEvent):
        delta = event.angleDelta()
        scroll_amount = delta.x() if delta.x() != 0 else delta.y()

        # Walk up to find the parent QScrollArea (tab_scroll)
        p = self.parent()
        while p and not isinstance(p, QScrollArea):
            p = p.parent()

        if p:
            p.horizontalScrollBar().setValue(
                p.horizontalScrollBar().value() - scroll_amount
            )
        event.accept()
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.window().windowHandle().startSystemMove()
        super().mousePressEvent(event)