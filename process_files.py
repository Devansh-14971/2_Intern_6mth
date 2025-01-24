import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from PIL import Image, ImageTk
import cv2


class ProcessFiles:

    def __init__(self, frame, download_window, notebook, supported_files=[".jpg", ".png"]):
        self.frame = frame
        self.download_window = download_window
        self.supported_files = supported_files
        notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)
    
    def get_current_folder(self):
        """
        Gets the current folder in download_window
        """
        return self.download_window.folder
    
    def display_image(self, file_path, preview_frame, preview_size = (300, 300)):
        """
        Display the selected image in the preview_frame.
        """
        for widget in preview_frame.winfo_children():
            widget.destroy()  # Clear the preview frame

        try:
            img = Image.open(file_path)
            img.thumbnail(preview_size)  # Resize image to fit
            img_tk = ImageTk.PhotoImage(img)

            img_label = tk.Label(preview_frame, image=img_tk)
            img_label.image = img_tk  # Keep reference to avoid garbage collection
            img_label.pack(pady=10)
        except Exception as e:
            tk.Label(preview_frame, text=f"Error loading file: {e}", fg="red").pack(pady=10)


    def on_tab_selected(self, event):
        notebook = event.widget
        if notebook.tab(notebook.select(), "text") == "Process Files":
            self.folder = self.get_current_folder()
            self.setup_ui()
    
    def parts_of_img(self,img,x,y):
        return [
            img[0:y,0:x//2],
            img[0:y,x//2:x]
            ]
    
    def save_as_numbered(self):
        pass

    """
    The function below is set to work with street view 360. Please check with the conventions of the new source
    """
    # def get_coords(path):
    #     path = path.split('/')[-1].split(' ')
    #     x,y = path[-2],path[-1].split('.')[0]+path[-1].split('.')[1]
    #     return x+'_'+y

    def process_image(self, path: Path):
        img = cv2.imread(Path)
        """
        Add the coords and num to this function
        """
        coord, num = 0,0
        path = path+f'/{coord}__{num}.jpg'
        cv2.imwrite(path,img)

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

        # Populate file buttons
        self.populate_files(files_frame, preview_frame)

    def populate_files(self, files_frame, preview_frame):
        """
        Add buttons for files in the files_frame.
        """
        if not self.folder.is_dir():
            tk.Label(files_frame, text="Invalid folder.", fg="red").pack(pady=10)
            return

        files = [file for ext in self.supported_files for file in self.folder.glob(f"*{ext}")]
        if not files:
            tk.Label(files_frame, text="No files found.", fg="blue").pack(pady=10)
            return

        for file in files:
            button = ttk.Button(files_frame, text=file.name, command=lambda f=file: self.display_image(f, preview_frame))
            button.pack(anchor="w", pady=5)




def find_raw(path = None):
  if path is None:
    global foldr_src
    path = foldr_src
  path = Path(path)
  return path.glob('**/*.jpg')


