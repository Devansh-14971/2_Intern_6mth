import configparser
from pathlib import Path
from AppLogger import Logger
from utils import current_w_folder


class Config:
    def __init__(self):
        """
        Initializes the config object by reading the configuration file and ensuring its validity.
        Sets up a Logger for logging configuration issues.
        """
        self.config_file = Path("config_.ini")
        self.logger = Logger(__name__)
        self.parser = configparser.ConfigParser()

        # Read the config file if it exists or create a default one if missing
        if not self.config_file.exists():
            self.logger.log_status(f"Configuration file {self.config_file} not found, creating default.", "WARNING")
            self.create_default_config()
        else:
            self.read_config()

    def create_default_config(self):
        """
        Creates a default configuration file with necessary sections and settings.
        Contains the log file path hardcoded
        """
        try:
            self.parser["DEFAULT"] = {
                "AppName": "Placeholder",
                "Version": "0.1"
            }
            self.parser["Paths"] = {
                "Log_file": str(current_w_folder() / "app_logs.json"),
                "Current_folder": str(current_w_folder())
            }

            with open(self.config_file, "w") as configfile:
                self.parser.write(configfile)
            self.logger.log_status(f"Default config file created at {self.config_file}", "INFO")
        except Exception as e:
            self.logger.log_exception(e)

    def read_config(self):
        """
        Reads the configuration file.
        """
        try:
            self.parser.read(self.config_file)
        except Exception as e:
            self.logger.log_exception(e)
            raise

    def get(self, section, option, fallback=None):
        """
        Get the value of a configuration option, with a fallback value if the option is missing.
        
        Args:
            section (str): The section name in the config file.
            option (str): The option name within the section.
            fallback: The default value to return if the option doesn't exist.
        
        Returns:
            str: The value of the option or the fallback value.
        """
        try:
            return self.parser.get(section, option, fallback=fallback)
        except configparser.NoOptionError:
            self.logger.log_status(f"Option {option} in section {section} not found. Using fallback value.", "WARNING")
            return fallback
    
    def get_all(self, section):
        """
        Get the values of all values in a configuration section.
        
        Args:
            section (str): The section name in the config file.
        
        Returns:
            dict[name:value]: A dict storing name-value pairs of items in the section
        """
        try:
            return dict(self.parser.items(section))
        except configparser.NoSectionError:
            self.logger.log_status(f"Section {section} not found.", "ERROR")


    def set(self, section, option, value):
        """
        Set the value of a configuration option.
        
        Args:
            section (str): The section name in the config file.
            option (str): The option name within the section.
            value (str): The new value to set.
        """
        try:
            if not self.parser.has_section(section):
                self.parser.add_section(section)
            self.parser.set(section, option, value)
            self.save_config()
        except Exception as e:
            self.logger.log_exception(e)

    def save_config(self):
        """
        Save the current configuration to the config file.
        """
        try:
            with open(self.config_file, "w") as configfile:
                self.parser.write(configfile)
            self.logger.log_status(f"Configuration saved to {self.config_file}", "INFO")
        except Exception as e:
            self.logger.log_exception(e)

    def get_log_file(self):
        """
        Get the log file path from the config.
        """
        return self.get("Paths", "Log_file", str(Path.home() / "app_logs.json"))

    def get_current_folder(self) -> Path:
        """
        Get the current folder path from the config.
        """
        return Path(self.get("Paths", "Current_folder", str(current_w_folder())))

    def get_config_detection(self) -> dict:
        """
        Get the configuration of the Building detection program
        """
        
        section_name = "BUILDING_DETECTION"
        return self.get_all(section=section_name)

# # Example Usage:
# config = Config()
# log_file = config.get_log_file()
# config.set("Paths", "Current_folder", str(Path.home() / "new_folder"))
