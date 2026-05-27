import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton,
    QStackedWidget, QLineEdit, QScrollArea
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, Qt


STYLE = """
    #url_bar {
        border-radius:9px;
        padding-left: 10px;
    }

    #navBtn {
        max-width: 28px;
        background-color: #232634;
        border: none;
        padding: 8px;
        width:10px;
        border-radius:9px;

    }
    #navBtn:hover {
        background-color: #414559;
    }

"""






HOME_URL = "https://duckduckgo.com"
class BrowserTab(QWidget):
    def __init__(self, url: str = HOME_URL):
        super().__init__()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.setStyleSheet(STYLE)
        
        
        # NavBar
        nav = QWidget()
        
        nav.setObjectName("navBar")
        nav.setFixedHeight(28)
        
        nav_layout = QHBoxLayout(nav)
        nav_layout.setContentsMargins(0,0,0,0)
        nav_layout.setSpacing(2)
        
        
        # Nav Buttons
        self.btn_back = QPushButton("←"); 
        self.btn_back.setObjectName("navBtn")
        
        self.btn_forward = QPushButton("→"); 
        self.btn_forward.setObjectName("navBtn")
        
        self.btn_reload  = QPushButton("↻"); 
        self.btn_reload.setObjectName("navBtn")
        
        self.url_bar = QLineEdit()
        self.url_bar.setObjectName("url_bar")
        self.url_bar.setPlaceholderText("Search or enter an address...")
        self.url_bar.returnPressed.connect(self.navigate)
        
    
        nav_layout.addWidget(self.btn_back)
        nav_layout.addWidget(self.btn_forward)
        nav_layout.addWidget(self.btn_reload)
        nav_layout.addSpacing(50)
        nav_layout.addWidget(self.url_bar)
        # nav_layout.addStretch()
        nav_layout.addSpacing(50)
        layout.addWidget(nav)
        
        
        # Web View
        self.view = QWebEngineView()
        layout.addWidget(self.view)
        
        #connections
        self.btn_back.clicked.connect(self.view.back)
        self.btn_forward.clicked.connect(self.view.forward)
        self.btn_reload.clicked.connect(self.view.reload)
        
        self.view.urlChanged.connect(self._on_url_changed)
        self.view.loadStarted.connect(lambda: self.btn_reload.setText("X"))
        self.view.loadFinished.connect(lambda: self.btn_reload.setText("↻"))
        self.view.titleChanged.connect(self._on_title_changed)
        
        self.on_title_update = None
        self.view.load(QUrl(url))
        
        
        # Search function
    def navigate(self):
        text=self.url_bar.text().strip()
        if not text.startswith(("https://", "http://")):
            if "." in text and " " not in text:
                text = "https://" + text
            else:
                text= "https://duckduckgo.com/html/?q=" + text.replace(" ","+")
        self.view.load(QUrl(text))
    def _on_url_changed(self, url: QUrl):
        self.url_bar.setText(url.toString())
        self.url_bar.setCursorPosition(0)
        self.btn_back.setEnabled(self.view.history().canGoBack())
        self.btn_forward.setEnabled(self.view.history().canGoForward())
    
    def _on_title_changed(self, title: str):
        if self.on_title_update:
            self.on_title_update(title)