import customtkinter as ctk
from tkinter import filedialog

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
        
        
    def _create_path_selector(self, parent, label_text, row, command):
        ctk.CTkLabel(parent, text=label_text).grid(row=row, column=0, padx=10, pady=(0, 10), sticky="nsew")
        entry = ctk.CTkEntry(parent)
        entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        button = ctk.CTkButton(parent, text="Browse", command=command, width=10)
        button.grid(row=row, column=2, padx=5, pady=5)
        return entry
    
    
    def _select_folder(self, entry_widget: ctk.CTkEntry):
        path = filedialog.askdirectory(title="Select Folder")
        if path:
            entry_widget.delete(0, ctk.END)
            entry_widget.insert(0, path)
            
    
    def _select_source_folder(self):
        self._select_folder(self.source_folder_entry)
        
        
    def _select_destination_folder(self):
        self._select_folder(self.destination_folder_entry)
        
        
    def _create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        controls_frame = ctk.CTkFrame(self)
        controls_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        controls_frame.grid_columnconfigure(1, weight=1)
        
        self.source_folder_entry = self._create_path_selector(controls_frame, "Source Folder", 0, self._select_source_folder)
        self.destination_folder_entry = self._create_path_selector(controls_frame, "Source Folder", 0, self._select_destination_folder)
