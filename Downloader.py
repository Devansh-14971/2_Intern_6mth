## We need to optimize the space used when downloading 
import os
import requests
import tkinter as tk



from tkinter import ttk, Toplevel, messagebox
from pathlib import Path
from AppLogger import Logger

from dotenv import load_dotenv
load_dotenv()

class Downloader:
    """
    Class to handle downloading files from GitHub using its API.

    Attributes:
        destination_folder (Path): The destination folder where files will be saved.
        ui_frame (tk.Frame): The UI frame for displaying progress and messages.
        logger (AppLogger): The logger instance for logging events.
    """
    def __init__(self, destination_folder: Path, ui_frame):
        self.destination_folder = destination_folder
        self.ui_frame = ui_frame
        self.logger = Logger(__name__)

    def download(self):
        """
        Downloads files from a GitHub repository using the GitHub API and updates the GUI with progress.
        """
        github_repo = os.getenv("REPO_NAME")
        github_username = os.getenv("USERNAME")
        github_token = os.getenv("GITHUB_ACCESS_TOKEN")
        github_foldr_name = os.getenv("GITHUB_FOLDER_NAME")
        ALLOWED_FILE_TYPES = os.getenv("ALLOWED_FILE_TYPES").split(',')
        ALLOWED_FILE_TYPES = [i.strip() for i in ALLOWED_FILE_TYPES]

        if not github_username or not github_repo:
            self.logger.log_exception("GitHub username or repository name not found in environment variables.")
            return

        if not github_token:
            self.logger.log_exception("GitHub token not found in environment variables.")
            return


        # See if we need to forcefully make a folder


        # Check if the destination folder exists
        if not self.destination_folder.exists():
            self.logger.log_warning("Destination folder does not exist.")
            return

        # Initialize UI for the download process
        ui_frame = self.ui_frame

        window_width = 800 #ui_frame.winfo_screenwidth() 
        window_height = 600 #ui_frame.winfo_screenheight()
        screen_width = (ui_frame.winfo_screenwidth() // 2) - (window_width // 2) - 60
        screen_height = (ui_frame.winfo_screenheight() // 2) - (window_height // 2)

        window = Toplevel(ui_frame)
        window.geometry(f"{window_width}x{window_height}+{screen_width}+{screen_height}")
        window.title("Download Window")
        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(0, weight=1)
        window.resizable(False, False)

        # Create UI elements
        progress_bar_frame = tk.Frame(window)
        progress_bar_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")
        progress_bar_frame.grid_columnconfigure(0, weight=1)

        progress_bar = ttk.Progressbar(progress_bar_frame)
        progress_bar.grid(row=0, column=0, padx=25, pady=10, sticky="ew")

        progress_bar_sVar = tk.StringVar(progress_bar_frame, value=f"{progress_bar['value']}%")
        progress_bar_label = tk.Label(progress_bar_frame, textvariable=progress_bar_sVar)
        progress_bar_label.grid(row=1, column=0, padx=10, pady=10)

        files_found_frame = tk.Frame(window)
        files_found_frame.grid(row=1, column=0, padx=10, sticky="nsew")
        files_found_frame.grid_columnconfigure(0, weight=1)

        files_found_text = tk.Text(files_found_frame, wrap=tk.WORD, width=30, state="disabled")
        files_found_text.grid(row=0, column=0, padx=10, pady=20)

        files_found_scrollbar = ttk.Scrollbar(files_found_frame, orient=tk.VERTICAL, command=files_found_text.yview)
        files_found_scrollbar.grid(row=0, column=1, sticky="ns")
        files_found_text.config(yscrollcommand=files_found_scrollbar.set)

        files_downloaded_frame = tk.Frame(window)
        files_downloaded_frame.grid(row=1, column=1, padx=10, sticky="nsew")
        files_downloaded_frame.grid_columnconfigure(0, weight=1)

        files_downloaded_text = tk.Text(files_downloaded_frame, wrap=tk.WORD, width=30, state="disabled")
        files_downloaded_text.grid(row=0, column=0, padx=10, pady=20)

        files_downloaded_scrollbar = ttk.Scrollbar(files_downloaded_frame, orient=tk.VERTICAL, command=files_downloaded_text.yview)
        files_downloaded_scrollbar.grid(row=0, column=1, sticky="ns")
        files_downloaded_text.config(yscrollcommand=files_downloaded_scrollbar.set)

        close_button = tk.Button(window, text="Close", command=window.destroy)
        close_button.grid(row=2, column=1, pady=20)

        # Fetch files from GitHub API
        url = f"https://api.github.com/repos/{github_username}/{github_repo}/{github_foldr_name}/"
        headers = {"Authorization": f"token {github_token}"}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            files = response.json()

            if not files:
                self.logger.log_info("The repository is empty or no files are available.")
                return

            # Filter for valid files
            files = [item for item in files if item["type"] == "file" and item["name"].lower().endswith(ALLOWED_FILE_TYPES)]
            total_files = len(files)

            files_found_text.config(state="normal")
            files_found_text.insert("end", "Files Found:\n")
            files_found_text.config(state="disabled")

            past_progress = 0

            # Download files and update progress
            for item in files:
                files_found_text.config(state="normal")
                files_found_text.insert("end", f"{item['name']}\n")
                files_found_text.config(state="disabled")

                self._download_file(item["download_url"], item["name"], files_downloaded_text)
                past_progress += 1
                progress = (past_progress / total_files) * 100
                progress_bar['value'] = progress
                progress_bar_sVar.set(f"{int(progress)}%")

                window.update_idletasks()

            self.logger.log_info(f"Downloaded {past_progress} files successfully.")

        except requests.exceptions.RequestException as e:
            self.logger.log_exception(f"Error while fetching repository data: {e}")
        response = messagebox.askokcancel("Download Complete", "Download complete. \n Close window?")
        if response: window.destroy()
    def _download_file(self, url, filename, files_downloaded_text):
        """
        Downloads an individual file from a URL.

        Args:
            url (str): The URL of the file to download.
            filename (str): The name of the file to save.
            files_downloaded_text (tk.Text): Text widget to display downloaded files.
        """
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            filepath = self.destination_folder / filename

            with open(filepath, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            files_downloaded_text.config(state="normal")
            files_downloaded_text.insert("end", f"Downloaded: {filename}\n")
            files_downloaded_text.config(state="disabled")
            self.logger.log_info(f"Downloaded file: {filename} to {self.destination_folder}")

        except requests.exceptions.RequestException as e:
            self.logger.log_exception(f"Error downloading file {filename}: {e}")