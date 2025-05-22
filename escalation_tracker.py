import os
import sys
from datetime import datetime
import glob
import re
import subprocess

ESCALATION_DIR = os.path.expanduser("~/.escalations")

if not os.path.exists(ESCALATION_DIR):
    os.makedirs(ESCALATION_DIR)

def sanitize_filename(text):
    text = re.sub(r'[|/\\:*?"<>]', '', text)  # remove unsafe characters
    return "_".join(text.lower().split())

def find_escalation_file(esc_id):
    files = glob.glob(os.path.join(ESCALATION_DIR, f"{esc_id}_*.txt"))
    return files[0] if files else None

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

def update_escalation(esc_id):
    path = find_escalation_file(esc_id)
    if not path:
        print(f"Escalation {esc_id} not found.")
        return
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    updated_lines = []
    inserted = False
    with open(path, "r") as f:
        for line in f:
            updated_lines.append(line)
            if line.strip() == "Status Updates:" and not inserted:
                updated_lines.append(f"[{timestamp}]\n")
                inserted = True
    with open(path, "w") as f:
        f.writelines(updated_lines)
    editor = os.environ.get('EDITOR', 'vim')
    subprocess.call([editor, path])

def search_escalations(term):
    matches = glob.glob(os.path.join(ESCALATION_DIR, "*.txt"))
    for file in matches:
        with open(file) as f:
            lines = f.readlines()
            content = "".join(lines).lower()
            if term.lower() in content:
                esc_id = next((l.split(': ')[1].strip() for l in lines if l.startswith("Escalation:")), "")
                title = next((l.split(': ')[1].strip() for l in lines if l.startswith("Title:")), "")
                print(f"{esc_id}: {title}")
                for line in lines:
                    if term.lower() in line.lower():
                        print(f"  > {line.strip()}")
                print()
def list_escalations():
    for file in sorted(glob.glob(os.path.join(ESCALATION_DIR, "*.txt"))):
        with open(file) as f:
            lines = f.readlines()
            esc_id = next((l.strip().split(': ')[1] for l in lines if l.startswith("Escalation:")), "")
            title = next((l.strip().split(': ')[1] for l in lines if l.startswith("Title:")), "")
            print(f"{esc_id}: {title}")

def show_escalation(esc_id):
    path = find_escalation_file(esc_id)
    if not path:
        print(f"Escalation {esc_id} not found.")
        return
    with open(path) as f:
        print(f.read())

def delete_escalation(esc_id):
    path = find_escalation_file(esc_id)
    if not path:
        print(f"Escalation {esc_id} not found.")
        return
    confirm = input(f"Are you sure you want to delete escalation {esc_id}? [y/N]: ").strip().lower()
    if confirm == 'y':
        os.remove(path)
        print(f"Deleted escalation {esc_id}.")
    else:
        print("Aborted.")

def help():
    print("""
Usage:
  esc start <id> <title>
  esc update <id>
  esc search <term>
  esc list
  esc show <id>
  esc delete <id>
    """)

def main():
    if len(sys.argv) < 2:
        help()
    elif sys.argv[1] == "start" and len(sys.argv) >= 4:
        esc_id = sys.argv[2]
        title = " ".join(sys.argv[3:])
        start_escalation(esc_id, title)
    elif sys.argv[1] == "update" and len(sys.argv) == 3:
        esc_id = sys.argv[2]
        update_escalation(esc_id)
    elif sys.argv[1] == "search" and len(sys.argv) == 3:
        search_escalations(sys.argv[2])
    elif sys.argv[1] == "list":
        list_escalations()
    elif sys.argv[1] == "show" and len(sys.argv) == 3:
        esc_id = sys.argv[2]
        show_escalation(esc_id)
    elif sys.argv[1] == "delete" and len(sys.argv) == 3:
        esc_id = sys.argv[2]
        delete_escalation(esc_id)
    else:
        help()

if __name__ == "__main__":
    main()
