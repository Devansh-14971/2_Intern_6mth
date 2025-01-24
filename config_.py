import configparser 
from pathlib import Path
from utils import current_path


class config_:
    def __init__(self):
        parser = configparser.ConfigParser()
        self.config_file = Path("config_.ini")

        if not self.config_file.exists():
            self.config_file.touch()
        # Create file if it doesn't exist
        File = parser.read(self.config_file)
        File.set("Paths", "Current_folder", current_path())
        with open(self.config_file.name) as file:
            parser.write(file)

    def set_curr_dep_foldr(self, path):
        parser = configparser.ConfigParser()
        parser.read(self.config_file)
        parser.set("Paths", "Current_folder", path)
        self.save(parser)
        

    def save(self, parser):
        with open(self.config_file, "w") as f:
            parser.write(f)

    def read_log_file_path(self):
        parser = configparser.ConfigParser()
        return parser.read(self.config_file)["Paths"]["Log_file"]
    
    def read_all(self):
        parser = configparser.ConfigParser()
        return parser.read(self.config_file)
    
    def read_defaults(self):
        return self.read_all()["DEFAULT"]
    
    def main_folder(self):
        parser = configparser.ConfigParser()
        return parser.read(self.config_file)["Paths"]["main_folder"]
    
config_()



    
