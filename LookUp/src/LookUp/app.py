"""
A no-nonsense browser for humans in the modern day
"""

import toga
from toga.style.pack import COLUMN, ROW
from toga.style import Pack


HOME_URL = "https://google.com"


class BrowserTab:
    def __init__(self, title: str = "New Tab", url: str = HOME_URL) -> None:
        self.title    = title
        self.tab_pill = None
        self.tab_btn  = None
        self._build(url)

    def _build(self, url: str) -> None:
        self.back_btn    = toga.Button("◀", on_press=self.go_back)
        self.forward_btn = toga.Button("▶", on_press=self.go_forward)
        self.refresh_btn = toga.Button("⟳", on_press=self.refresh)

        self.url_input = toga.TextInput(
            value=url,
            placeholder="Enter a URL and press Enter to search...",
            on_confirm=self.navigate,
            style=Pack(flex=1),
        )

        self.go_btn = toga.Button("Go", on_press=self.navigate)

        nav_bar = toga.Box(
            children=[
                self.back_btn, self.forward_btn, self.refresh_btn,
                self.url_input, self.go_btn,
            ],
            style=Pack(direction=ROW, margin=6),
        )

        self.webview = toga.WebView(url=url, style=Pack(flex=1))

        self.content = toga.Box(
            children=[nav_bar, self.webview],
            style=Pack(direction=COLUMN, flex=1),
        )

    def navigate(self, widget=None, **kwargs) -> None:
        url = self.url_input.value.strip()
        if not url:
            return
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        self.url_input.value = url
        self.webview.url = url

    def go_back(self, widget=None, **kwargs) -> None:
        self.webview.evaluate_javascript("window.history.back()")

    def go_forward(self, widget=None, **kwargs) -> None:
        self.webview.evaluate_javascript("window.history.forward()")

    def refresh(self, widget=None, **kwargs) -> None:
        self.webview.evaluate_javascript("window.location.reload()")

    def go_home(self) -> None:
        self.url_input.value = HOME_URL
        self.webview.url = HOME_URL




class LookUp(toga.App):

    def startup(self) -> None:
        self._tabs:      list[BrowserTab] = []
        self._active_id: int = -1

        self._content_area = toga.Box(
            style=Pack(direction=COLUMN, flex=1),
        )

        self._tabs_box = toga.Box(
            style=Pack(direction=ROW, flex=1, margin_top=1, margin_bottom=1),
        )

        self._new_tab_btn = toga.Button(
            " + ",
            on_press=lambda w: self._new_tab(),
            style=Pack(width=34, margin_left=2, margin_right=2),
        )

        top_bar = toga.Box(
            children=[self._tabs_box, self._new_tab_btn],
            style=Pack(direction=ROW, margin=2),
        )

        root = toga.Box(
            children=[top_bar, self._content_area],
            style=Pack(direction=COLUMN, flex=1),
        )

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = root
        self._new_tab()
        self.main_window.show()

    # Tab management
    def _new_tab(self, url: str = HOME_URL, title: str = "New Tab") -> BrowserTab:
        tab = BrowserTab(title=title, url=url)
        self._tabs.append(tab)

        close_x = toga.Button(
            "x",
            on_press=lambda w: self._close_tab(tab),
            style=Pack(margin=4),
        )
        tab_btn = toga.Button(
            title,
            on_press=lambda w: self._switch_to(tab),
            style=Pack(margin=4),
        )
        tab_pill = toga.Box(
            children=[tab_btn, close_x],
            style=Pack(direction=ROW),
        )

        tab.tab_pill = tab_pill
        tab.tab_btn  = tab_btn

        self._tabs_box.add(tab_pill)
        self._switch_to(tab)
        return tab

    def _switch_to(self, tab: BrowserTab) -> None:
        self._active_id = self._tabs.index(tab)
        if self._content_area.children:
            self._content_area.remove(self._content_area.children[0])
        self._content_area.add(tab.content)
        self.main_window.title = tab.url_input.value

    def _close_tab(self, tab: BrowserTab) -> None:
        if len(self._tabs) <= 1:
            self.app.exit()
            return
        idx = self._tabs.index(tab)
        self._tabs_box.remove(tab.tab_pill)
        self._tabs.pop(idx)
        self._switch_to(self._tabs[min(idx, len(self._tabs) - 1)])

    def _current_tab(self):
        if 0 <= self._active_id < len(self._tabs):
            return self._tabs[self._active_id]
        return None

def main():
    return LookUp("LookUp", "org.example.lookup")