import sqlite3
from datetime import datetime
import os

class Database():
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "data.db")

        self.con = sqlite3.connect(db_path)
        self.cur = self.con.cursor()
    
    
    # implements schema to db file
    def firstStart(self):
        try:
            with open("schema.sql", "r") as f:
                schema_sql = f.read()
            self.cur.executescript(schema_sql)
            self.con.commit()
        except FileNotFoundError:
            raise FileNotFoundError("oopsie daisy uhhhhhhh no schema found....")
    
    
    def addBookmark(self, name, url):
        self.cur.execute("INSERT INTO Bookmarks (url, name) VALUES (?, ?);", url, name)
        self.con.commit()
        
        
    def addHistoryEntry(self, url):
        time = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")

        self.cur.execute("INSERT INTO History (url, timestamp) VALUES (?, ?);", (url, time))
        self.con.commit()
        
    def listBookmarks(self):
        self.cur.execute("SELECT * FROM Bookmarks;")
        bookmarks = self.cur.fetchall()
        return bookmarks
    
    def listHistory(self):
        self.cur.execute("SELECT * FROM History;")
        history = self.cur.fetchall()
        return history