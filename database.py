import sqlite3
import os

def create_database() -> None:
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    with open("database.sql", "r") as f:
        cursor.executescript(f.read())
    conn.commit()
    conn.close()
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

def get_database() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    return conn, cursor
