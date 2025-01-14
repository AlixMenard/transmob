import os
import subprocess
from pathlib import Path
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES

import os
import subprocess
from pathlib import Path

def repair_videos_in_folder(folder_path):
    folder_path = Path(folder_path)
    if not folder_path.is_dir():
        print(f"Error: {folder_path} is not a valid directory.")
        return

    # Supported video file extensions
    video_extensions = {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"}

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = Path(root) / file

            if file_path.suffix.lower() in video_extensions:
                repaired_file_path = file_path.with_suffix(".r.mkv")

                # Check if the repaired file already exists
                if repaired_file_path.exists():
                    print(f"Skipping {file_path}: Repaired file already exists.")
                    continue

                # Run the FFmpeg command
                command = [
                    "ffmpeg",
                    "-i", str(file_path),
                    "-map", "0",
                    "-c", "copy",
                    "-loglevel", "quiet",  # Suppress verbose output
                    str(repaired_file_path)
                ]

                try:
                    print(f"Processing {file_path}...")
                    subprocess.run(command, check=True)
                    print(f"Repaired file saved as {repaired_file_path}")

                    # Preserve the original file's timestamps
                    original_stat = file_path.stat()
                    os.utime(repaired_file_path, (original_stat.st_atime, original_stat.st_mtime))
                    print(f"Preserved timestamps for {repaired_file_path}")
                    os.remove(file_path)

                except subprocess.CalledProcessError as e:
                    print(f"Error processing {file_path}: {e}")
                except Exception as e:
                    print(f"Unexpected error with {file_path}: {e}")

if __name__ == "__main__":
    folder_to_scan = input("Enter the path to the folder containing videos: ")
    repair_videos_in_folder(folder_to_scan)


def window():
    root = TkinterDnD.Tk()

    file_lab = tk.Label(root, text = "Dossier des vidéos à réparer : ")
    file_lab.grid(row = 0, column = 0, pady=10, padx=5)
    file_path = tk.StringVar()
    file_entry = tk.Entry(root, textvariable = file_path)
    file_entry.grid(row = 0, column = 1, pady=10, padx=5)

    def validate():
        path = file_path.get()
        path = path.strip('"{}')
        repair_videos_in_folder(path)
        root.destroy()

    def create_bt():
        bt = tk.Button(root, text = "Valider", command = validate)
        bt.grid(row = 1, column = 0, columnspan = 2, pady=10, padx=5)

    def on_drop(event):
        # When a file is dropped, set the file path into the entry widget
        file_path.set(event.data)  # event.data contains the file path
        create_bt()

    # Initialize the main window with drag-and-drop support
    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', on_drop)
    root.mainloop()

if __name__ == '__main__':
    window()