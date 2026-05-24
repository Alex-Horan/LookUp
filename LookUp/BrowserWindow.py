import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton,
    QStackedWidget, QLineEdit, QScrollArea
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, Qt
from BrowserTab import BrowserTab
from TabChip import TabChip

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("LookUp")
        self.resize(1320, 900)
        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)
        self.setCentralWidget(root)
 
        # Tab strip
        tab_strip = QWidget()
        tab_strip.setObjectName("tabStrip")
        tab_strip.setFixedHeight(38)
        self.tab_strip_layout = QHBoxLayout(tab_strip)
        self.tab_strip_layout.setContentsMargins(0, 0, 0, 0)
        self.tab_strip_layout.setSpacing(0)
        self.tab_strip_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
 
        self.new_tab_btn = QPushButton("+")
        self.new_tab_btn.setObjectName("newTabBtn")
        self.new_tab_btn.clicked.connect(lambda: self.add_tab())
        self.tab_strip_layout.addWidget(self.new_tab_btn)
        self.tab_strip_layout.addStretch()
 
        root_layout.addWidget(tab_strip)
 
        # Page stack
        self.stack = QStackedWidget()
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
 
        insert_pos = self.tab_strip_layout.count() - 2  # before + and stretch
        self.tab_strip_layout.insertWidget(insert_pos, chip)
 
        self.stack.addWidget(page)
        self.chips.append(chip)
        self.pages.append(page)
 
        self.switch_tab(index)
 
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
 
        self.tab_strip_layout.removeWidget(chip)
        chip.deleteLater()
        self.stack.removeWidget(page)
        page.deleteLater()
 
        self.switch_tab(min(index, len(self.pages) - 1))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec())