import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton,
    QStackedWidget, QLineEdit, QSizePolicy, QLabel, QScrollArea
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, Qt, QSize
from PyQt6.QtGui import QFont


STYLE= """

/*The actual tab itself, the part you click to switch to it*/
#tabBtn {
    margin: 0px;
    padding: 0px;
    text-align: left;
    border: none;
    background-color: white;
}


/*The x button on the tab*/
#tabClose {
    margin: 0px;
    padding: 0px;
    border: none;
    min-width: 0px;
    max-width: 22px;
    background-color: white;
    border-top-right-radius: 9px;
}


/*the whole tab, the container that holds both tabBtn and tabClose*/
#tabChip {
    background-color: white;
    margin-right: 10px;
}

/* the top tab bar holding each instance of tabChip */
#tabStrip, #tabContainer, #tabScroll {
    background-color: #1a1a1a;  /* dark background so rounded corners show */
}
"""


class TabChip(QWidget):
    def __init__(self, on_click, on_close):
        super().__init__()
        
        
        self.setObjectName("tabChip")
        self.setFixedHeight(22)
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background-color: white;")
        self.setStyleSheet(STYLE)
        
        
        self.tab_btn = QPushButton("New Tab")
        self.tab_btn.setFixedHeight(22)
        self.tab_btn.setObjectName("tabBtn")
        self.tab_btn.clicked.connect(on_click)

        self.close_btn = QPushButton("×")
        self.close_btn.setObjectName("tabClose")
        self.close_btn.setFixedHeight(22)
        self.close_btn.setFixedWidth(18)

        self.close_btn.clicked.connect(on_close)
        layout.addWidget(self.tab_btn)
        layout.addWidget(self.close_btn)
        
    def set_title(self, title: str):
        short = (title[:22] + "...") if len(title) > 22 else title
        self.tab_btn.setText(short or "New Tab")
    
    def set_active(self, active: bool):
        self.tab_btn.setChecked(active)