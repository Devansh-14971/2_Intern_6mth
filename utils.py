from tkinter import messagebox
from pathlib import Path


def current_path():
    return Path(__file__).resolve()

def show_error(error):
    messagebox.showerror(f"error in {current_path()}", error)
    return 

def get_downloads_folder():
    return Path.home() / "Downloads"