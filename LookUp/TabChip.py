import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton,
    QStackedWidget, QLineEdit, QSizePolicy, QLabel
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, Qt, QSize
from PyQt6.QtGui import QFont


class TabChip(QWidget):
    def __init__(self, on_click, on_close):
        super().__init__()
        self.setObjectName("tabStrip")
        self.setFixedHeight(38)
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        
        self.tab_btn = QPushButton("New Tab")
        self.tab_btn.setObjectName("tabBtn")
        self.tab_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.tab_btn.clicked.connect(on_click)
        
        self.close_btn = QPushButton("x")
        self.close_btn.setObjectName("tabClose")
        self.close_btn.clicked.connect(on_close)
        layout.addWidget(self.tab_btn)
        layout.addWidget(self.close_btn)
        
    def set_title(self, title: str):
        short = (title[:22] + "...") if len(title) > 22 else title
        self.tab_btn.setText(short or "New Tab")
    
    def set_active(self, active: bool):
        self.tab_btn.setChecked(active)