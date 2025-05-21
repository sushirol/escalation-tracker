# escalation_tracker.py

import os
import sys
from datetime import datetime
import glob

ESCALATION_DIR = os.path.expanduser("~/.escalations")

if not os.path.exists(ESCALATION_DIR):
    os.makedirs(ESCALATION_DIR)

def sanitize_filename(text):
    return "_".join(text.lower().split())

def start_escalation(esc_id, title):
    filename = f"{esc_id}_{sanitize_filename(title)}.txt"
    path = os.path.join(ESCALATION_DIR, filename)
    if os.path.exists(path):
        print(f"Escalation {esc_id} already exists.")
        return
    with open(path, "w") as f:
        f.write(f"Escalation: {esc_id}\n")
        f.write(f"Title: {title}\n")
        f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write("\nStatus Updates:\n")
    print(f"Created: {path}")

def update_escalation(esc_id, update):
    files = glob.glob(os.path.join(ESCALATION_DIR, f"{esc_id}_*.txt"))
    if not files:
        print(f"Escalation {esc_id} not found.")
        return
    path = files[0]
    with open(path, "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {update}\n")
    print(f"Updated: {path}")

def search_escalations(term):
    matches = glob.glob(os.path.join(ESCALATION_DIR, "*.txt"))
    for file in matches:
        with open(file) as f:
            content = f.read().lower()
            if term.lower() in content:
                print(f"Found in: {file}\n")

def list_escalations():
    for file in sorted(glob.glob(os.path.join(ESCALATION_DIR, "*.txt"))):
        print(os.path.basename(file))

def help():
    print("""
Usage:
  esc start <id> <title>
  esc update <id> <status update>
  esc search <term>
  esc list
    """)

def main():
    if len(sys.argv) < 2:
        help()
    elif sys.argv[1] == "start" and len(sys.argv) >= 4:
        esc_id = sys.argv[2]
        title = " ".join(sys.argv[3:])
        start_escalation(esc_id, title)
    elif sys.argv[1] == "update" and len(sys.argv) >= 4:
        esc_id = sys.argv[2]
        update_text = " ".join(sys.argv[3:])
        update_escalation(esc_id, update_text)
    elif sys.argv[1] == "search" and len(sys.argv) == 3:
        search_escalations(sys.argv[2])
    elif sys.argv[1] == "list":
        list_escalations()
    else:
        help()

if __name__ == "__main__":
    main()
