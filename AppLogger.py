import configparser
import config_
from pytz import timezone
from pathlib import Path
import json
from utils import show_error
from datetime import datetime


class logger:
    def __init__(self):
        """
        The log file directory is saved in the .config file as a string
        """
        parser = configparser.ConfigParser()
        self.log_path = parser.read(self.config_file)["Paths"]["Log_file"]  # Using a json for logging
        self.log_path = Path(self.log_path)
        self.log_path.touch(exist_ok=True)

    def log_status(self, info, status):        
        log_message = {
            "timestamp": datetime.now(timezone('Asia / Calcutta')),
            "level" : status,
            "message" : info,
            "module" : __name__
        }
        try:
            json.dump(log_message, self.log_path)
        except Exception as e:
            show_error(e)