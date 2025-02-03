from tkinter import messagebox
from pathlib import Path
from AppLogger import Logger
import os

# Configure logger for utility functions
logger = Logger(__name__)

def current_w_folder():
    return Path(os.getcwd())

def current_path():
    """
    Returns the absolute path of the currently executing script.
    
    Returns:
        Path: The absolute path of the script.
    """
    try:
        path = Path(__file__).resolve()
        logger.debug(f"Current script path resolved: {path}")
        return path
    except Exception as e:
        logger.error(f"Error resolving current script path: {e}")
        raise


def get_downloads_folder():
    """
    Gets the path to the user's default downloads folder.
    
    Returns:
        Path: Path to the Downloads folder.
    """
    try:
        downloads_path = Path.home() / "Downloads"
        logger.debug(f"Downloads folder path resolved: {downloads_path}")
        return downloads_path
    except Exception as e:
        logger.error(f"Error resolving Downloads folder path: {e}")
        raise

def validate_path(path):
    """
    Validates whether the provided path exists and is accessible.
    
    Args:
        path (Path or str): Path to validate.
    
    Returns:
        bool: True if the path exists and is accessible, False otherwise.
    """
    path = Path(path)
    if path.exists():
        logger.debug(f"Validated path exists: {path}")
        return True
    else:
        logger.warning(f"Path does not exist: {path}")
        return False

def ensure_directory_exists(directory):
    """
    Ensures the given directory exists. Creates it if it doesn't.
    
    Args:
        directory (Path or str): The directory to check or create.
    
    Returns:
        Path: The validated or newly created directory path.
    """
    directory = Path(directory)
    if not directory.exists():
        try:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Directory created: {directory}")
        except Exception as e:
            logger.error(f"Error creating directory: {directory} - {e}")
            raise
    else:
        logger.debug(f"Directory already exists: {directory}")
    return directory
