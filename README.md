# Bulk File Renamer & Organizer

A simple Python CLI tool to rename multiple files at once and automatically organize them into folders. Built to simulate real-world file management and automation tasks.

## Features

- **Bulk Renaming**
  - Add prefix (e.g. `HK_`)
  - Add suffix (e.g. `_2026`)
  - Replace words in filenames
  - Auto numbering (`file_1`, `file_2`, ...)

- **File Organization**
  - Sort files by type (Images, Videos, Documents, Audio, Others)
  - Sort files by extension
  - Sort files by date modified

- **Preview System**
  - Shows old name vs new name before applying any changes
  - Asks for confirmation before executing

- **Logging**
  - Every rename/move operation is saved to `operations_log.csv`
  - Includes old name, new name, and timestamp

- **Safe by Design**
  - Never overwrites existing files (auto-adds a number if a name conflict happens)
  - Handles missing files and permission errors without crashing

## Requirements

- Python 3.x
- No external libraries needed — uses only built-in modules (`os`, `shutil`, `csv`, `datetime`)

## How to Run

1. Open a terminal or command prompt.
2. Navigate to the folder containing the script:
   ```
   cd path/to/file_organizer
   ```
3. Run the script:
   ```
   python code.py
   ```
4. Use the on-screen menu:
   ```
   1. Select Folder
   2. Rename Files
   3. Organize Files
   4. View Logs
   5. Exit
   ```
5. Select a folder first (option 1), then choose rename or organize.

## Example

```
Enter folder path: C:\Users\YourName\Desktop\sample_files

1. Add prefix
2. Add suffix
3. Replace word in filenames
4. Auto numbering
Choose an option: 1
Enter prefix: HK_

Preview of changes:
--------------------------------------------------
photo1.jpg  -->  HK_photo1.jpg
report.pdf  -->  HK_report.pdf
--------------------------------------------------

Apply these changes? (y/n): y
Renamed 2 file(s).
```

## Project Structure

```
file_organizer/
├── code.py              # main script
├── operations_log.csv   # auto-generated log file
└── README.md
```

## Notes

for demo video click here
https://drive.google.com/file/d/1XeEB-uM4fFNrvOwqmcnnJ2QGm629gVTK/view?usp=drive_link

- Always run a preview before applying changes — nothing is renamed or moved without confirmation.
- The log file is created automatically in the same folder as the script.
