#!/usr/bin/env python3
# Developer: Vishal Raj V, Senior Engineer
import os
import sys

def main():
    todo_file = "TODO.md"
    if os.path.exists(todo_file):
        with open(todo_file, "r") as f:
            content = f.read()
        if "- [ ]" in content:
            print("\n[SYSTEM HOOK] Reminder: There are still unchecked items in TODO.md. Please continue working on them.")

if __name__ == "__main__":
    main()
