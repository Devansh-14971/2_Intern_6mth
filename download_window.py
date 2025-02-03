import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from AppLogger import Logger
from Downloader import Downloader


class DownloadWindow:
    """
    Class to create and handle the download window UI and invoke file downloads.
    """
    # This has merged the UI of the pop up and the UI of the Download Tab. I have to seperate the two and shift the popup to the download() and create_ui should have the UI that triggers download and the select folder button
    # The logics have been merged and distributed messily between Downloader and DownloadWindow. We need to clarify and separate this clearly
    def __init__(self, destination_folder: Path, parent_frame):
        self.destination_folder = destination_folder
        self.parent_frame = parent_frame
        self.logger = Logger(__name__)
        self.downloader = Downloader(self.destination_folder, self.logger)  # Use the Downloader class
        self.create_ui()

    def create_ui(self):
        """
        Sets up the UI elements for the download window within the parent frame.
        """
        # Clear the parent frame
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        self.parent_frame.grid_columnconfigure(0, weight=1)
        self.parent_frame.grid_rowconfigure(0, weight=1)

        # Create UI elements
        progress_bar_frame = tk.Frame(self.parent_frame)
        progress_bar_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")
        progress_bar_frame.grid_columnconfigure(0, weight=1)

        self.progress_bar = ttk.Progressbar(progress_bar_frame)
        self.progress_bar.grid(row=0, column=0, padx=25, pady=10, sticky="ew")

        self.progress_bar_sVar = tk.StringVar(progress_bar_frame, value=f"{self.progress_bar['value']}%")
        progress_bar_label = tk.Label(progress_bar_frame, textvariable=self.progress_bar_sVar)
        progress_bar_label.grid(row=1, column=0, padx=10, pady=10)

        files_found_frame = tk.Frame(self.parent_frame)
        files_found_frame.grid(row=1, column=0, padx=10, sticky="nsew")
        files_found_frame.grid_columnconfigure(0, weight=1)

        self.files_found_text = tk.Text(files_found_frame, wrap=tk.WORD, width=30, state="disabled")
        self.files_found_text.grid(row=0, column=0, padx=10, pady=20)

        files_found_scrollbar = ttk.Scrollbar(files_found_frame, orient=tk.VERTICAL, command=self.files_found_text.yview)
        files_found_scrollbar.grid(row=0, column=1, sticky="ns")
        self.files_found_text.config(yscrollcommand=files_found_scrollbar.set)

        files_downloaded_frame = tk.Frame(self.parent_frame)
        files_downloaded_frame.grid(row=1, column=1, padx=10, sticky="nsew")
        files_downloaded_frame.grid_columnconfigure(0, weight=1)

        self.files_downloaded_text = tk.Text(files_downloaded_frame, wrap=tk.WORD, width=30, state="disabled")
        self.files_downloaded_text.grid(row=0, column=0, padx=10, pady=20)

        files_downloaded_scrollbar = ttk.Scrollbar(files_downloaded_frame, orient=tk.VERTICAL, command=self.files_downloaded_text.yview)
        files_downloaded_scrollbar.grid(row=0, column=1, sticky="ns")
        self.files_downloaded_text.config(yscrollcommand=files_downloaded_scrollbar.set)


        ## I believe we don't need this here as the action of closing is not needed in a tab of a ttk.Notebook
        # close_button = tk.Button(self.parent_frame, text="Close", command=lambda: self.clear_ui())
        # close_button.grid(row=2, column=1, pady=20)

    def clear_ui(self):
        """
        Clears all widgets from the parent frame.
        """
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

    def download(self):
        """
        Handles the file download process using the Downloader class.
        """
        files = self.downloader.get_files()
        if not files:
            messagebox.showwarning("No Files", "No files found in the repository to download.")
            return

        total_files = len(files)
        self.files_found_text.config(state="normal")
        self.files_found_text.insert("end", "Files Found:\n")
        self.files_found_text.config(state="disabled")

        past_progress = 0

        for file in files:
            self.files_found_text.config(state="normal")
            self.files_found_text.insert("end", f"{file['name']}\n")
            self.files_found_text.config(state="disabled")

            success = self.downloader.download_file(file["download_url"], file["name"])
            if success:
                self.files_downloaded_text.config(state="normal")
                self.files_downloaded_text.insert("end", f"Downloaded: {file['name']}\n")
                self.files_downloaded_text.config(state="disabled")

            past_progress += 1
            progress = (past_progress / total_files) * 100
            self.progress_bar['value'] = progress
            self.progress_bar_sVar.set(f"{int(progress)}%")

            self.parent_frame.update_idletasks()

        self.logger.log_info(f"Downloaded {past_progress} files successfully.")
        messagebox.showinfo("Download Complete", "Download complete.")