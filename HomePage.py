import tkinter as tk
import subprocess
import sys

def start_script(script_name):
    # Start the script in a new process
    subprocess.Popen([sys.executable, script_name])
    # Close the window and exit the current script
    root.destroy()
    sys.exit()

# Create the main window
root = tk.Tk()
root.title("AI")

# Configure the window size
root.geometry("300x100")

# Add buttons for each script
button1 = tk.Button(root, text="Analyse vidéo", command=lambda: start_script("GUI.py"))
button2 = tk.Button(root, text="Outils additionnels", command=lambda: start_script("Tools.py"))

# Position buttons
button1.pack(pady=10)
button2.pack(pady=10)

# Start the GUI event loop
root.mainloop()
