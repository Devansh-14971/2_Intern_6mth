# main_app.py

import tkinter as tk
from tkinter import ttk
from download_window import DownloadWindow
from process_files import ProcessFiles
import config_


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


config = config_.config_()

root = tk.Tk()
root.title("Main Application")
center_window(root, 650, 300)
root.config(bg="grey")
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, sticky="nsew", pady=5)

# Create tabs
download_frame = ttk.Frame(notebook)
download_frame.grid(row=0, column=0, sticky='nsew')
download_frame.grid_columnconfigure(0, weight=1)
download_frame.grid_rowconfigure(0, weight=1)

process_frame = ttk.Frame(notebook)
process_frame.grid(row=0, column=0, sticky='nsew')
process_frame.grid_rowconfigure(0, weight=1)
process_frame.grid_columnconfigure(0, weight=1)


notebook.add(download_frame, text="Download")
notebook.add(process_frame, text="Process Files")

# Initialize modules
download_window = DownloadWindow(download_frame, config)
ProcessFiles(process_frame, download_window, notebook, config)

root.mainloop()
