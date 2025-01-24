import os
import requests

from tkinter import Toplevel, ttk, messagebox
import tkinter as tk




class Downloader:
    # Destination folder to save images
    
    def __init__(self, folder, root):
        self.root = root
        self.folder = folder       

    def fetch_folder_contents(self,api_url):
        """
        Fetch contents of the folder from GitHub API.
        """
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()  # Returns a list of files and folders
        else:
            messagebox.showerror("No files found", f"Something went wrong. Either no files were found \n or The API gave a bad response \n Response code:{response.status_code}")
            return []

    def download_file(self, download_url, file_name, files_downloaded_text : tk.Text):
        """
        Download a file from a given URL.
        """
        response = requests.get(download_url, stream=True)
        if response.status_code == 200:
            file_path = os.path.join(self.folder, file_name)
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            files_downloaded_text.config(state="normal")
            files_downloaded_text.insert("end",f"Downloaded: {file_name}\n")    
            files_downloaded_text.config(state="disabled")        
        else:
            files_downloaded_text.config(state="normal")
            files_downloaded_text.insert("end",f"Failed to download {file_name}: {response.status_code}\n")
            files_downloaded_text.config(state="disabled")

    def download(self):
        if not self.folder.is_file:
            messagebox.showwarning("Error", "Destination folder not found")
        
        root = self.root

        window_width = 800 #root.winfo_screenwidth() 
        window_height = 600 #root.winfo_screenheight()
        screen_width = (root.winfo_screenwidth()// 2) - (window_width// 2) - 60
        screen_height = (root.winfo_screenheight()// 2) - (window_height// 2)

        window = Toplevel(root)
        window.geometry(f"{window_width}x{window_height}+{screen_width}+{screen_height}")
        window.title("Download window")
        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(0, weight=1)
        window.resizable(False,False)

        progress_bar_frame = tk.Frame(window)
        progress_bar_frame.grid_columnconfigure(0, weight=1)
        progress_bar_frame.grid_rowconfigure(0, weight=1)
        progress_bar_frame.grid(row=0, column=0, pady = 10, sticky='ew', columnspan=2)

        progress_bar = ttk.Progressbar(progress_bar_frame)
        progress_bar.grid(row=0, column=0, padx=25, pady=10, sticky='ew')

        progress_bar_sVar = tk.StringVar(progress_bar_frame, value= f"{progress_bar['value']}%" )
        progress_bar_label = tk.Label(progress_bar_frame, textvariable=progress_bar_sVar)
        progress_bar_label.grid(row=1, column=0, padx=10, pady=10)

        files_found_frame = tk.Frame(window)
        files_found_frame.grid_columnconfigure(0, weight=1)
        files_found_frame.grid_rowconfigure(0, weight=1)
        files_found_frame.grid(row = 1, column=0, padx = 10)

        files_found_text = tk.Text(files_found_frame, wrap=tk.WORD, width=30, state="disabled")
        files_found_text.grid(row = 0, column=0, padx = 10, pady=20)

        files_found_scrollbar = ttk.Scrollbar(files_found_frame, orient=tk.VERTICAL, command = files_found_text.yview)
        files_found_scrollbar.grid(row=0, column=1, sticky='w')

        files_found_text.config(yscrollcommand=files_found_scrollbar.set)


        files_downloaded_frame = tk.Frame(window)
        files_downloaded_frame.grid_columnconfigure(0, weight=1)
        files_downloaded_frame.grid_rowconfigure(0, weight=1)
        files_downloaded_frame.grid(row = 1, column=1, padx = 10)

        files_downloaded_text = tk.Text(files_downloaded_frame, wrap=tk.WORD, width=30, state="disabled")
        files_downloaded_text.grid(row = 0, column=0, padx = 10, pady=20)

        files_downloaded_scrollbar = ttk.Scrollbar(files_downloaded_frame, orient=tk.VERTICAL, command = files_downloaded_text.yview)
        files_downloaded_scrollbar.grid(row=0, column=1, sticky='w')

        files_downloaded_text.config(yscrollcommand=files_downloaded_scrollbar.set)

        close_button = tk.Button(window, text="Close")
        close_button.grid(row=2, column=1, pady = 20)
        close_button.config(command=window.destroy)

        # Fetch folder contents
        folder_contents = self.fetch_folder_contents(GITHUB_API_URL)

        if not folder_contents: return

        folder_contents = [item for item in folder_contents if item["type"] == "file" and item["name"].lower().endswith((".jpg", ".png")) ]

        total_files = len(folder_contents)
        past_progress = progress_bar['value']

        files_found_text.config(state="normal")
        files_found_text.insert("end",f"Files Found:\n")  
        files_found_text.config(state="disabled")

        # Download files and update progress bar
        for item in folder_contents:

            files_found_text.config(state="normal")       
            files_found_text.insert("end",f"{item['name']}\n")
            files_found_text.config(state="disabled")

            self.download_file(item["download_url"], item["name"], files_downloaded_text)
            past_progress += 1
            progress_bar_sVar.set(f"{(past_progress/total_files)*100}%")
            progress_bar['value'] = past_progress/total_files*100
            
            window.update_idletasks()
        
        else:
            response = messagebox.askokcancel("Download Complete", "Download complete. \n Close window?")
            if response: window.destroy()


