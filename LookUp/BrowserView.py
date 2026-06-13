from PyQt6.QtWidgets import QMenu
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QContextMenuEvent
from PyQt6.QtCore import pyqtSignal

class BrowserView(QWebEngineView):
    open_in_new_tab = pyqtSignal(str)
    # back_sig = pyqtSignal()
    # forward_sig = pyqtSignal()
    # reload_sig = pyqtSignal()
        
    def contextMenuEvent(self, event: QContextMenuEvent):
        menu = QMenu(self)
        link_url = self.lastContextMenuRequest().linkUrl()
        
        
        
        back_action = menu.addAction("Back")
        forward_action = menu.addAction("Forward")
        reload_action = menu.addAction("Reload")
        
        back_action.triggered.connect(self.back)
        forward_action.triggered.connect(self.forward)
        reload_action.triggered.connect(self.reload)
                
        new_tab_action = None
        if not link_url.isEmpty():
            new_tab_action = menu.addAction("Open Link in New Tab")
            
        if new_tab_action:
            new_tab_action.triggered.connect(lambda: self.open_in_new_tab.emit(link_url.toString()))
        
        menu.exec(event.globalPos())