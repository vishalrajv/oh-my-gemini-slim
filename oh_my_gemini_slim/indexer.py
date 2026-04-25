# Developer: Vishal Raj V, Senior Engineer
import os
import json
import sqlite3
import re
from pathlib import Path

DB_PATH = Path("memory/memory.db")
MEMORY_DIR = Path("memory")

def init_db(conn):
    cursor = conn.cursor()
    # Create tables for the Knowledge Graph
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nodes (
            id TEXT PRIMARY KEY,
            type TEXT,
            label TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS edges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_id TEXT,
            to_id TEXT,
            type TEXT,
            UNIQUE(from_id, to_id, type)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            title TEXT,
            date TEXT,
            agent TEXT
        )
    """)
    conn.commit()

def extract_json(content):
    # Regex to find the JSON block at the end of the file
    match = re.search(r"```json\s*(\{.*?\})\s*```", content, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            return None
    return None

def index_memory():
    if not MEMORY_DIR.exists():
        print(f"Memory directory {MEMORY_DIR} not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    init_db(conn)
    cursor = conn.cursor()

    for log_file in MEMORY_DIR.glob("*.md"):
        content = log_file.read_text(encoding="utf-8")
        data = extract_json(content)
        
        if not data:
            continue

        session_id = str(data.get("session_id"))
        
        # 1. Index Session
        cursor.execute(
            "INSERT OR REPLACE INTO sessions (id, title, date, agent) VALUES (?, ?, ?, ?)",
            (session_id, data.get("title"), data.get("date"), data.get("agent"))
        )

        # 2. Index Nodes
        for node in data.get("nodes", []):
            cursor.execute(
                "INSERT OR REPLACE INTO nodes (id, type, label) VALUES (?, ?, ?)",
                (node["id"], node["type"], node["label"])
            )

        # 3. Index Edges
        for edge in data.get("edges", []):
            try:
                cursor.execute(
                    "INSERT OR IGNORE INTO edges (from_id, to_id, type) VALUES (?, ?, ?)",
                    (edge["from"], edge["to"], edge["type"])
                )
            except sqlite3.Error as e:
                print(f"Error indexing edge {edge}: {e}")

    conn.commit()
    conn.close()
    print(f"Knowledge Graph updated in {DB_PATH}")

if __name__ == "__main__":
    index_memory()
