import sys
import os
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QLineEdit, QPushButton, QInputDialog)
from PyQt5.QtWebEngineWidgets import QWebEngineView

# This file stores their search choice so they only see the setup prompt once
CONFIG_FILE = "search_config.txt"

SEARCH_ENGINES = {
    "Google": "https://www.google.com/search?q=",
    "DuckDuckGo": "https://duckduckgo.com/?q=",
    "Bing": "https://www.bing.com/search?q="
}

class BrowseWeb(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BrowseWeb")
        self.resize(1024, 768) # Default desktop window size
        
        # Load setting or show first-launch dialog
        self.search_engine = self.load_or_select_search_engine()

        # Create Chromium browser core
        self.browser = QWebEngineView()
        
        # Open home page
        homepage = self.search_engine.split("?")[0]
        self.browser.setUrl(QUrl(homepage))
        
        # UI controls
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        
        self.back_btn = QPushButton("←")
        self.back_btn.clicked.connect(self.browser.back)
        
        self.forward_btn = QPushButton("→")
        self.forward_btn.clicked.connect(self.browser.forward)
        
        # Set up layouts
        layout = QVBoxLayout()
        nav_bar = QHBoxLayout()
        nav_bar.addWidget(self.back_btn)
        nav_bar.addWidget(self.forward_btn)
        nav_bar.addWidget(self.url_bar)
        
        layout.addLayout(nav_bar)
        layout.addWidget(self.browser)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        # Sync address bar with navigation
        self.browser.urlChanged.connect(self.update_url_bar)

    def load_or_select_search_engine(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                saved_url = f.read().strip()
                if saved_url in SEARCH_ENGINES.values():
                    return saved_url
        
        # First-run prompt
        engines = list(SEARCH_ENGINES.keys())
        choice, ok = QInputDialog.getItem(
            self, 
            "BrowseWeb Setup", 
            "Choose your default search engine:", 
            engines, 
            0, 
            False
        )
        selected_url = SEARCH_ENGINES["Google"] # Default backup
        if ok and choice:
            selected_url = SEARCH_ENGINES[choice]
            
        with open(CONFIG_FILE, "w") as f:
            f.write(selected_url)
        return selected_url

    def navigate_to_url(self):
        text = self.url_bar.text()
        if "." in text and " " not in text: # Direct link
            if not text.startswith("http"):
                text = "https://" + text
            self.browser.setUrl(QUrl(text))
        else: # Search query
            search_url = self.search_engine + text.replace(" ", "+")
            self.browser.setUrl(QUrl(search_url))

    def update_url_bar(self, q):
        self.url_bar.setText(q.toString())

app = QApplication(sys.argv)
window = BrowseWeb()
window.show()
sys.exit(app.exec_())
