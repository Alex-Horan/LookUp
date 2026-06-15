import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton,
    QStackedWidget, QLineEdit, QScrollArea
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, Qt, pyqtSignal
from PyQt6.QtGui import QIcon

class NavBar(QWidget):
    open_in_new_tab = pyqtSignal(str)
    open_settings = pyqtSignal()
    navigate = pyqtSignal

    def __init__(self):
        super().__init__()
        self.setObjectName("navBar")
        self.setFixedHeight(28)
        
        self.nav_layout = QHBoxLayout(self)
        self.nav_layout.setContentsMargins(0,0,0, 0)
        self.nav_layout.setSpacing(2)
        
        self.btn_back = QPushButton("←"); 
        self.btn_back.setObjectName("navBtn")
        
        self.btn_forward = QPushButton("→"); 
        self.btn_forward.setObjectName("navBtn")
        
        self.btn_reload  = QPushButton("↻"); 
        self.btn_reload.setObjectName("navBtn")
        
        self.url_bar = QLineEdit()
        self.url_bar.setObjectName("urlBar")
        self.url_bar.setPlaceholderText("Search or enter an address...")
        self.url_bar.returnPressed.connect(self._navigate)
        
        self.btn_settings = QPushButton()
        self.btn_settings.setIcon(QIcon('./assets/settingsIcon.svg'))
        self.btn_settings.setObjectName("setBtn")
        self.btn_settings.clicked.connect(lambda: self.open_settings.emit())
        
        self.nav_layout.addWidget(self.btn_back)
        self.nav_layout.addWidget(self.btn_forward)
        self.nav_layout.addWidget(self.btn_reload)
        self.nav_layout.addSpacing(50)
        self.nav_layout.addWidget(self.url_bar)
        # nav_layout.addStretch()
        self.nav_layout.addSpacing(50)
        self.nav_layout.addWidget(self.btn_settings)
        self.nav_layout.addSpacing(5)
    
    
    
    
    
    def _navigate(self):
        pass