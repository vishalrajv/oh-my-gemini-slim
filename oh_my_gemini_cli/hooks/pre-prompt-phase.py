#!/usr/bin/env python3
# Developer: Vishal Raj V, Senior Engineer
import os
import sys

def main():
    phase_file = "PHASE.txt"
    if os.path.exists(phase_file):
        with open(phase_file, "r") as f:
            phase = f.read().strip()
        print(f"\n[SYSTEM HOOK] Current Phase: {phase}. Ensure your actions align with this phase.")

if __name__ == "__main__":
    main()
