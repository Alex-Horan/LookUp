import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton,
    QStackedWidget, QLineEdit, QSizePolicy, QLabel, QScrollArea
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, Qt, QSize
from PyQt6.QtGui import QFont, QIcon


STYLE= """

/*The actual tab itself, the part you click to switch to it*/
#tabBtn {
    margin: 0px;
    padding: 0px;
    text-align: center;
    border: none;
    padding-left: 8px;
    }

/*The x button on the tab*/
#tabClose {
    margin: 0px;
    padding: 0px;
    border: none;
    padding-top:4px;
    
    min-width: 0px;
    max-width: 22px;
    width: 20px;
    
    border-top-right-radius: 9px;
    padding-left: 8px;
    
}


/*the whole tab, the container that holds both tabBtn and tabClose*/
#tabChip {

    background-color: #303446 ;
    border-top-right-radius: 9px;
    border: 2px solid #292c3c;
    border-bottom: none;
    
}


"""

ACTIVE_TAB_STYLE = """
/*The actual tab itself, the part you click to switch to it*/
#tabBtn {
    margin: 0px;
    padding: 0px;
    text-align: center;
    border: none;
    padding-left: 8px;
    
}

/*The x button on the tab*/
#tabClose {
    margin: 0px;
    padding: 0px;
    padding-top:4px;
    border: none;
    min-width: 0px;
    max-width: 22px;
    width: 20px;
    border-radius: 9px;
    padding-left: 8px;


    
}



/*the whole tab, the container that holds both tabBtn and tabClose*/
#tabChip {
    background-color: #626880;
    border: 2px solid #292c3c;
    border-top-right-radius: 9px;
    border-bottom: none;
    
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
        self.setStyleSheet(STYLE)
        
        
        self.tab_btn = QPushButton("New Tab")
        self.tab_btn.setFixedHeight(22)
        self.tab_btn.setObjectName("tabBtn")
        self.tab_btn.setCheckable(True)
        self.tab_btn.clicked.connect(on_click)

        self.close_btn = QPushButton()
        self.close_btn.setIcon(QIcon("./assets/closeTabIcon.svg"))
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
        if active:
            self.setStyleSheet(ACTIVE_TAB_STYLE)
        else:
            self.setStyleSheet(STYLE)
        