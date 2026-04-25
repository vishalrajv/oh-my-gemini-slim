# Developer: Vishal Raj V, Senior Engineer
import sqlite3
import json
import sys
from pathlib import Path

DB_PATH = Path("memory/memory.db")

def query_db(query, params=()):
    if not DB_PATH.exists():
        return {"error": "Knowledge Graph database not found. Run indexing first."}
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        return {"error": str(e)}
    finally:
        conn.close()

def get_file_history(file_path):
    """Find all tasks and sessions that modified a specific file."""
    query = """
        SELECT n.id as task_id, n.label as task_description, s.id as session_id, s.title as session_title, s.date
        FROM edges e
        JOIN nodes n ON e.from_id = n.id
        JOIN edges e2 ON e2.to_id = n.id
        JOIN sessions s ON e2.from_id = s.id
        WHERE e.to_id = ? AND e.type = 'MODIFIED'
        ORDER BY s.date DESC
    """
    return query_db(query, (file_path,))

def get_recent_decisions(limit=5):
    """Retrieve the most recent architectural or project decisions."""
    query = """
        SELECT n.id, n.label as decision, s.title as session, s.date
        FROM nodes n
        JOIN edges e ON e.from_id = n.id
        JOIN edges e2 ON e2.to_id = e.to_id
        JOIN sessions s ON e2.from_id = s.id
        WHERE n.type = 'Decision' AND e.type = 'RATIONALE_FOR'
        ORDER BY s.date DESC
        LIMIT ?
    """
    return query_db(query, (limit,))

def search_nodes(keyword):
    """Search for any node (Task, Decision, File) by keyword."""
    query = "SELECT * FROM nodes WHERE id LIKE ? OR label LIKE ?"
    return query_db(query, (f"%{keyword}%", f"%{keyword}%"))

def main():
    if len(sys.argv) < 2:
        print("Usage: querier.py <file-history|decisions|search> [args]")
        sys.exit(1)

    cmd = sys.argv[1]
    
    if cmd == "file-history" and len(sys.argv) > 2:
        print(json.dumps(get_file_history(sys.argv[2]), indent=2))
    elif cmd == "decisions":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        print(json.dumps(get_recent_decisions(limit), indent=2))
    elif cmd == "search" and len(sys.argv) > 2:
        print(json.dumps(search_nodes(sys.argv[2]), indent=2))
    else:
        print(f"Unknown command or missing arguments: {cmd}")

if __name__ == "__main__":
    main()
