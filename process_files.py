import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from PIL import Image, ImageTk
import config_
from CropStreetView import ProcessFiles

class CropWindow:
    def __init__(self, root, download_window, config):
        self.root = root
        self.config = config
        self.download_window = download_window
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")
        
        self.frame = ttk.Frame(self.notebook)
        self.notebook.add(self.frame, text="Process Files")
        
        self.processor = ProcessFiles(self.frame, self.download_window, self.notebook, self.config)
        
        self.setup_ui()
    
    def setup_ui(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Files Canvas
        files_canvas = tk.Canvas(self.frame, bg="lightgrey")
        files_canvas.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        files_scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=files_canvas.yview)
        files_scrollbar.grid(row=0, column=1, sticky="ns")
        files_canvas.configure(yscrollcommand=files_scrollbar.set)

        # Files Frame inside Files Canvas
        files_frame = ttk.Frame(files_canvas)
        files_frame.bind("<Configure>", lambda e: files_canvas.configure(scrollregion=files_canvas.bbox("all")))
        files_canvas.create_window((0, 0), window=files_frame, anchor="nw")
        
        # Preview Canvas
        preview_canvas = tk.Canvas(self.frame, bg="white")
        preview_canvas.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        preview_scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=preview_canvas.yview)
        preview_scrollbar.grid(row=0, column=3, sticky="ns")
        preview_canvas.configure(yscrollcommand=preview_scrollbar.set)

        # Preview Frame inside Preview Canvas
        preview_frame = ttk.Frame(preview_canvas)
        preview_canvas.create_window((0, 0), window=preview_frame, anchor="nw")

        # Make the main frame expandable
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(2, weight=2)
        self.frame.grid_rowconfigure(0, weight=1)

        # Populate file buttons using backend
        self.processor.populate_files(files_frame, preview_frame)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Crop Window Application")
    config = config_.config_()
    download_window = None  # Define your download_window accordingly
    app = CropWindow(root, download_window, config)
    root.mainloop()
