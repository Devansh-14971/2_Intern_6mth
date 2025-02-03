# CropStreetView

from pathlib import Path
from PIL import Image
import cv2

class ProcessFiles:
    def __init__(self, frame, download_window, notebook, config, supported_files=[".jpg", ".png"]):
        self.frame = frame
        self.config = config
        self.download_window = download_window
        self.supported_files = supported_files
        notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)
    
    def get_current_folder(self):
        """
        Gets the current folder in download_window
        """
        return self.download_window.folder
    
    def display_image(self, file_path, preview_frame, preview_size=(300, 300)):
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
    
    def parts_of_img(self, img, x, y):
        return [
            img[0:y, 0:x//2],
            img[0:y, x//2:x]
        ]
    
    def save_as_numbered(self):
        pass

    def process_image(self, path: Path):
        img = cv2.imread(str(path))
        coord, num = 0, 0
        save_path = path.parent / f'{coord}__{num}.jpg'
        cv2.imwrite(str(save_path), img)
    
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


def find_raw(path=None):
    if path is None:
        global foldr_src
        path = foldr_src
    path = Path(path)
    return path.glob('**/*.jpg')
