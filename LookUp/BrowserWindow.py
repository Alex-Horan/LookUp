import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton,
    QStackedWidget, QLineEdit, QScrollArea, QSpacerItem
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, Qt
from BrowserTab import BrowserTab
from TabChip import TabChip
from DraggableTabStrip import DraggableTabStrip
from DraggableSpace import DraggableSpace

# import os
# os.environ["QT_QPA_PLATFORMTHEME"] = ""

STYLE = """
#navBar {
    margin-top: 0;
    padding-top: 0;
}

#newTabBtn {
  max-width: 20px;
}

/* Thing that holds the forward, back, and refresh buttons + url bar
(url bar is weird and may need to be styled inside of the BrowserTab file for some reason)
*/
#navBar {
    
}

/* the top tab bar holding each instance of tabChip */
#tabStrip, #tabContainer, #tabScroll {
    background-color: black;
    margin-bottom: 0;
    padding-bottom: 0;
}
"""



class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LookUp")
        # self.setObjectName("MainWindow")
        self.resize(1320, 900)
        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)
        self.setCentralWidget(root)
        root.setStyleSheet(STYLE)
 
        # Tab strip
        tab_bar = QWidget()
        tab_bar.setObjectName("tabStrip")
        tab_bar.setFixedHeight(100)
        tab_bar_layout = QHBoxLayout(tab_bar)
        tab_bar_layout.setContentsMargins(0, 0, 0, 0)
        tab_bar_layout.setSpacing(0)
        tab_bar.setFixedHeight(28)

        # button on the left
        
        tab_bar_layout.addWidget(DraggableSpace(25))
        self.new_tab_btn = QPushButton("+")
        self.new_tab_btn.setObjectName("newTabBtn")
        self.new_tab_btn.clicked.connect(lambda: self.add_tab())
        tab_bar_layout.addWidget(self.new_tab_btn)

        # Scrollable + draggable chip area !!!! holds the container that holds tabs !!!!! nesting hell
        self.tab_scroll = QScrollArea()
        self.tab_scroll.setWidgetResizable(True)
        self.tab_scroll.setFixedHeight(34)
        self.tab_scroll.setObjectName("tabScroll")
        self.tab_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.tab_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.tab_scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")


        # tab container, holds tab chips
        self.tab_container = DraggableTabStrip()
        # self.tab_container.setStyleSheet("background: transparent;")
        self.tab_container_layout = QHBoxLayout(self.tab_container)
        self.tab_container.setObjectName("tabContainer")
        self.tab_container_layout.setContentsMargins(0, 0, 0, 0)
        self.tab_container_layout.setSpacing(0)
        self.tab_container_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.tab_container_layout.addStretch()


        self.tab_scroll.setWidget(self.tab_container)
        tab_bar_layout.addWidget(self.tab_scroll)


        root_layout.addWidget(tab_bar)
 
        # Page stack
        self.stack = QStackedWidget()
        self.stack.setContentsMargins(0,0,0,0)
        root_layout.addWidget(self.stack)
 
        self.chips: list[TabChip] = []
        self.pages: list[BrowserTab] = []
 
        self.add_tab("https://duckduckgo.com/")
        
 
    def add_tab(self, url: str = "https://duckduckgo.com/"):
        index = len(self.pages)

        chip = TabChip(
            on_click=lambda: self.switch_tab(self.chips.index(chip)),
            on_close=lambda: self.close_tab(self.chips.index(chip)),
        )
        page = BrowserTab(url)
        page.on_title_update = lambda t, c=chip: c.set_title(t)

        insert_pos = self.tab_container_layout.count() - 1  # before stretch
        self.tab_container_layout.insertWidget(insert_pos, chip)

        self.stack.addWidget(page)
        self.chips.append(chip)
        self.pages.append(page)

        self.switch_tab(index)

        # scroll to the new tab
        self.tab_scroll.horizontalScrollBar().setValue(
            self.tab_scroll.horizontalScrollBar().maximum()
        )
 
    def switch_tab(self, index: int):
        if not (0 <= index < len(self.pages)):
            return
        self.stack.setCurrentIndex(index)
        for i, chip in enumerate(self.chips):
            chip.set_active(i == index)
            
 
    def close_tab(self, index: int):
        if len(self.pages) == 1:
            return
 
        chip = self.chips.pop(index)
        page = self.pages.pop(index)
 
        self.tab_container_layout.removeWidget(chip)
        chip.deleteLater()
        self.stack.removeWidget(page)
        page.deleteLater()
 
        self.switch_tab(min(index, len(self.pages) - 1))
        



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec())