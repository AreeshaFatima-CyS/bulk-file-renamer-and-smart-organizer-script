import os
import shutil
import csv
from datetime import datetime
LOG_FILE = "operations_log.csv"
IMAGE_EXT = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]
VIDEO_EXT = [".mp4", ".mov", ".avi", ".mkv", ".wmv"]
DOC_EXT = [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".ppt", ".pptx"]
AUDIO_EXT = [".mp3", ".wav", ".flac", ".aac"]
def write_log(entries):
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["old_name", "new_name", "timestamp"])
        for old_name, new_name in entries:
            writer.writerow([old_name, new_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
def get_files(folder):
    return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
def make_unique_name(folder, name):
    base, ext = os.path.splitext(name)
    counter = 1
    new_name = name
    while os.path.exists(os.path.join(folder, new_name)):
        new_name = f"{base}_{counter}{ext}"
        counter += 1
    return new_name
def build_rename_plan(folder, mode, value):
    files = get_files(folder)
    plan = []
    if mode == "prefix":
        for f in files:
            plan.append((f, value + f))
    elif mode == "suffix":
        for f in files:
            base, ext = os.path.splitext(f)
            plan.append((f, base + value + ext))
    elif mode == "replace":
        old_word, new_word = value
        for f in files:
            if old_word in f:
                plan.append((f, f.replace(old_word, new_word)))
            else:
                plan.append((f, f))
    elif mode == "number":
        for i, f in enumerate(files, start=1):
            ext = os.path.splitext(f)[1]
            plan.append((f, f"{value}_{i}{ext}"))
    return plan
def preview_plan(plan):
    if not plan:
        print("Nothing to rename.")
        return
    print("\nPreview of changes:")
    print("-" * 50)
    for old_name, new_name in plan:
        print(f"{old_name}  -->  {new_name}")
    print("-" * 50)
def apply_rename(folder, plan):
    log_entries = []
    for old_name, new_name in plan:
        old_path = os.path.join(folder, old_name)
        if not os.path.exists(old_path):
            print(f"Skipped (missing): {old_name}")
            continue
        if old_name == new_name:
            continue
        safe_new_name = new_name
        if os.path.exists(os.path.join(folder, new_name)):
            safe_new_name = make_unique_name(folder, new_name)
        try:
            os.rename(old_path, os.path.join(folder, safe_new_name))
            log_entries.append((old_name, safe_new_name))
        except PermissionError:
            print(f"Permission denied for: {old_name}")
        except FileNotFoundError:
            print(f"File not found: {old_name}")
    write_log(log_entries)
    print(f"\nRenamed {len(log_entries)} file(s).")
def category_for(ext):
    ext = ext.lower()
    if ext in IMAGE_EXT:
        return "Images"
    if ext in VIDEO_EXT:
        return "Videos"
    if ext in DOC_EXT:
        return "Documents"
    if ext in AUDIO_EXT:
        return "Audio"
    return "Others"
def organize_by_type(folder):
    files = get_files(folder)
    log_entries = []
    for f in files:
        ext = os.path.splitext(f)[1]
        category = category_for(ext)
        dest_folder = os.path.join(folder, category)
        os.makedirs(dest_folder, exist_ok=True)
        src = os.path.join(folder, f)
        dest_name = f
        if os.path.exists(os.path.join(dest_folder, f)):
            dest_name = make_unique_name(dest_folder, f)
        try:
            shutil.move(src, os.path.join(dest_folder, dest_name))
            log_entries.append((f, f"{category}/{dest_name}"))
        except PermissionError:
            print(f"Permission denied for: {f}")
    write_log(log_entries)
    print(f"\nMoved {len(log_entries)} file(s) into category folders.")
def organize_by_extension(folder):
    files = get_files(folder)
    log_entries = []
    for f in files:
        ext = os.path.splitext(f)[1].replace(".", "").lower() or "no_extension"
        dest_folder = os.path.join(folder, ext)
        os.makedirs(dest_folder, exist_ok=True)
        src = os.path.join(folder, f)
        dest_name = f
        if os.path.exists(os.path.join(dest_folder, f)):
            dest_name = make_unique_name(dest_folder, f)
        try:
            shutil.move(src, os.path.join(dest_folder, dest_name))
            log_entries.append((f, f"{ext}/{dest_name}"))
        except PermissionError:
            print(f"Permission denied for: {f}")
    write_log(log_entries)
    print(f"\nMoved {len(log_entries)} file(s) by extension.")
def organize_by_date(folder):
    files = get_files(folder)
    log_entries = []
    for f in files:
        path = os.path.join(folder, f)
        modified_time = os.path.getmtime(path)
        date_folder = datetime.fromtimestamp(modified_time).strftime("%Y-%m-%d")
        dest_folder = os.path.join(folder, date_folder)
        os.makedirs(dest_folder, exist_ok=True)
        dest_name = f
        if os.path.exists(os.path.join(dest_folder, f)):
            dest_name = make_unique_name(dest_folder, f)
        try:
            shutil.move(path, os.path.join(dest_folder, dest_name))
            log_entries.append((f, f"{date_folder}/{dest_name}"))
        except PermissionError:
            print(f"Permission denied for: {f}")
    write_log(log_entries)
    print(f"\nMoved {len(log_entries)} file(s) by date.")
def view_logs():
    if not os.path.isfile(LOG_FILE):
        print("No log file yet.")
        return
    with open(LOG_FILE) as f:
        reader = csv.reader(f)
        rows = list(reader)
    if len(rows) <= 1:
        print("Log file is empty.")
        return
    print("\nOperations log:")
    print("-" * 60)
    for row in rows[1:]:
        print(f"{row[0]:30} -> {row[1]:25} ({row[2]})")
    print("-" * 60)
def rename_menu(folder):
    print("\n1. Add prefix")
    print("2. Add suffix")
    print("3. Replace word in filenames")
    print("4. Auto numbering")
    choice = input("Choose an option: ").strip()
    if choice == "1":
        value = input("Enter prefix: ")
        plan = build_rename_plan(folder, "prefix", value)
    elif choice == "2":
        value = input("Enter suffix: ")
        plan = build_rename_plan(folder, "suffix", value)
    elif choice == "3":
        old_word = input("Word to replace: ")
        new_word = input("Replace with: ")
        plan = build_rename_plan(folder, "replace", (old_word, new_word))
    elif choice == "4":
        base_name = input("Base name (e.g. file): ")
        plan = build_rename_plan(folder, "number", base_name)
    else:
        print("Invalid choice.")
        return
    preview_plan(plan)
    confirm = input("\nApply these changes? (y/n): ").strip().lower()
    if confirm == "y":
        apply_rename(folder, plan)
    else:
        print("Cancelled.")
def organize_menu(folder):
    print("\n1. By file type (Images, Videos, Documents...)")
    print("2. By extension")
    print("3. By date modified")
    choice = input("Choose an option: ").strip()
    if choice == "1":
        organize_by_type(folder)
    elif choice == "2":
        organize_by_extension(folder)
    elif choice == "3":
        organize_by_date(folder)
    else:
        print("Invalid choice.")
def main():
    folder = None
    while True:
        print("\n===== Bulk File Renamer & Organizer =====")
        print("1. Select Folder")
        print("2. Rename Files")
        print("3. Organize Files")
        print("4. View Logs")
        print("5. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            path = input("Enter folder path: ").strip()
            if os.path.isdir(path):
                folder = path
                print(f"Folder set to: {folder}")
            else:
                print("That folder doesn't exist.")
        elif choice == "2":
            if not folder:
                print("Select a folder first.")
            else:
                rename_menu(folder)
        elif choice == "3":
            if not folder:
                print("Select a folder first.")
            else:
                organize_menu(folder)
 
        elif choice == "4":
            view_logs()
 
        elif choice == "5":
            print("Goodbye.")
            break
        else:
            print("Invalid choice, try again.")
if __name__ == "__main__":
    main()