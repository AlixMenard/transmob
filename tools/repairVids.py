import os
import subprocess
from pathlib import Path
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES

import os
import subprocess
from pathlib import Path

import os
import subprocess
from pathlib import Path

def get_video_duration(file_path):
    command = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
        return float(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"Error getting duration for {file_path}: {e}")
        return None

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
                repaired_file_path = file_path.with_suffix(".r.mp4")

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

                    # Get the original file's duration
                    original_duration = get_video_duration(file_path)
                    if original_duration is None:
                        print(f"Skipping timestamp adjustment for {file_path} due to missing duration.")
                        continue

                    # Calculate the new last modified time
                    original_stat = file_path.stat()
                    original_start_time = original_stat.st_mtime - original_duration

                    repaired_duration = get_video_duration(repaired_file_path)
                    if repaired_duration is None:
                        print(f"Skipping timestamp adjustment for {repaired_file_path} due to missing duration.")
                        continue

                    new_modified_time = original_start_time + repaired_duration

                    # Set the repaired file's timestamps
                    os.utime(repaired_file_path, (original_stat.st_atime, new_modified_time))
                    print(f"Adjusted timestamps for {repaired_file_path}")
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