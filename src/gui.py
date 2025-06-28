import customtkinter as ctk

from settings_manager import SettingsManager
from file_processor import FileProcessor

APP_NAME = "Image Organizer"
SETTINGS_FILE = "settings.json"
DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 600

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry(f"{DEFAULT_WIDTH}x{DEFAULT_HEIGHT}")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.settings_manager = SettingsManager(SETTINGS_FILE)
        self._create_widgets()
        
        
    def _create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        controls_frame = ctk.CTkFrame(self)
        controls_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        controls_frame.grid_columnconfigure(1, weight=1)