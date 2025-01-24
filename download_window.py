from tkinter import ttk, Toplevel, messagebox, filedialog
import tkinter as tk
from pathlib import Path
from Downloader import Downloader
import utils, config_


class DownloadWindow:
    def __init__(self, frame):
        self.frame = frame
        self.default_folder = utils.get_downloads_folder()
        self.folder = self.default_folder
        self.last_saved_info = "No files saved"
        self.__setup_ui()

    def __setup_ui(self):
        # Folder selection
        folder_frame = ttk.Frame(self.frame)
        folder_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        folder_frame.grid_rowconfigure(0, weight=1)
        folder_frame.grid_columnconfigure(0, weight=1)

        folder_label = ttk.Label(folder_frame, text="Destination Folder:")
        folder_label.grid(row=0, column=0, padx=5)
        folder_entry = ttk.Entry(folder_frame, width=50)
        folder_entry.insert(0, str(self.default_folder))
        folder_entry.grid(row=0, column=1, padx=5)

        browse_button = ttk.Button(folder_frame, text="Browse", command=lambda: self.browse_folder(folder_entry))
        browse_button.grid(row=0, column=2, padx=5)

        # Download Button
        download_button = ttk.Button(self.frame, text="Start Download", command=self.start_download)
        download_button.grid(row=1, column=0, pady=10)

    def browse_folder(self, folder_entry):
        folder = filedialog.askdirectory(title="Select Destination Folder")
        if folder:
            self.folder = Path(folder)
            config_.set
            folder_entry.delete(0, tk.END)
            folder_entry.insert(0, str(folder))

    def start_download(self):
        downloader = Downloader(self.folder, self.frame)
        downloader.download()

