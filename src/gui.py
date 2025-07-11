import customtkinter as ctk
import threading
from tkinter import filedialog, messagebox

from file_processor import FileProcessor
from settings_manager import SettingsManager
from settings_window import SettingsWindow

# Constants
APP_NAME = "Image Organizer"
SETTINGS_FILE = "settings.json"
DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 400

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title(APP_NAME)
        self.geometry(f"{DEFAULT_WIDTH}x{DEFAULT_HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self._on_delete_window)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        ctk.set_widget_scaling(1.2)
        ctk.set_window_scaling(1.2)
        
        # Initialize manager and create UI
        self.settings_manager = SettingsManager(SETTINGS_FILE)
        self._create_widgets()
        self._load_settings()
        
        # Update window size
        self.update_idletasks()
        self.geometry(f"{DEFAULT_WIDTH}x{self.winfo_reqheight()}")

    
    def _select_folder(self, entry_widget: ctk.CTkEntry) -> None:
        path = filedialog.askdirectory(title="Select Folder")
        if path:
            entry_widget.delete(0, ctk.END)
            entry_widget.insert(0, path)
            
    
    def _select_file(self, entry_widget: ctk.CTkEntry) -> None:
        path = filedialog.askopenfilename(title="Select File", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if path:
            entry_widget.delete(0, ctk.END)
            entry_widget.insert(0, path)
            
    
    def _select_source_folder(self) -> None:
        self._select_folder(self.source_folder_entry)
        
        
    def _select_destination_folder(self) -> None:
        self._select_folder(self.destination_folder_entry)
        
        
    def _select_number_file(self) -> None:
        self._select_file(self.number_file_entry)
        
        
    def _create_path_selector(self, parent, label_text, row, command) -> ctk.CTkEntry:
        ctk.CTkLabel(parent, text=label_text, anchor="e", justify="right").grid(row=row, column=0, padx=10, sticky="e")
        entry = ctk.CTkEntry(parent)
        entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        button = ctk.CTkButton(parent, text="Browse", command=command, width=10)
        button.grid(row=row, column=2, padx=5, pady=5)
        return entry
        
        
    def _create_widgets(self) -> None:
        self.grid_columnconfigure(0, weight=1)

        # App name label at the top
        app_name_label = ctk.CTkLabel(self, text=APP_NAME, font=ctk.CTkFont(size=24, weight="bold"))
        app_name_label.grid(row=0, column=0, pady=(20, 10), sticky="n")
        
        # Controls frame (label / entry / button)
        controls_frame = ctk.CTkFrame(self)
        controls_frame.grid(row=1, column=0, padx=20, pady=(0, 0), sticky="ew")
        controls_frame.grid_columnconfigure(1, weight=1)
        
        # Source folder
        self.source_folder_entry = self._create_path_selector(
            controls_frame, "Source Folder:", 0, 
            self._select_source_folder
        )
        
        # Destination folder
        self.destination_folder_entry = self._create_path_selector(
            controls_frame, "Destination Folder:", 1, 
            self._select_destination_folder
        )
        
        # Number list file
        self.number_file_entry = self._create_path_selector(
            controls_frame, "Number List File:", 2, 
            self._select_number_file
        )
        
        # Prefix
        ctk.CTkLabel(controls_frame, text="File Prefix:", anchor="e", justify="right").grid(
            row=3, column=0, padx=10, sticky="e"
        )
        self.prefix_entry = ctk.CTkEntry(controls_frame)
        self.prefix_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        
        # Extension
        ctk.CTkLabel(controls_frame, text="File Extension:", anchor="e", justify="right").grid(
            row=4, column=0, padx=10, sticky="e"
        )
        self.extension_combobox = ctk.CTkComboBox(
            controls_frame,
            values=["ARW", "CR3", "DNG", "NEF", "ORF", "RAF", "RW2", "JPG", "PNG"],
            width=120
        )
        self.extension_combobox.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        
        # Actions Frame
        actions_frame = ctk.CTkFrame(controls_frame)
        actions_frame.grid(row=5, column=0, columnspan=3, padx=10, pady=(20, 10), sticky="ew")
        
        # Make all columns for buttons have equal weight for even spacing
        for i in range(4):
            actions_frame.grid_columnconfigure(i, weight=1)
        
        self.copy_button = ctk.CTkButton(
            actions_frame, text="Copy Files", 
            command=lambda: self._start_processing("copy")
        )
        self.copy_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.move_button = ctk.CTkButton(
            actions_frame, text="Move Files", 
            command=lambda: self._start_processing("move")
        )
        self.move_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        self.rename_button = ctk.CTkButton(
            actions_frame, text="Rename Files",
            command=lambda: self._start_processing("rename")
        )
        self.rename_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        
        self.delete_button = ctk.CTkButton(
            actions_frame, text="Delete Files",
            command=lambda: self._start_processing("delete")
        )
        self.delete_button.grid(row=0, column=3, padx=10, pady=10, sticky="ew")
        
        # Settings button
        bottom_frame = ctk.CTkFrame(self)
        bottom_frame.grid(row=2, column=0, sticky="sw", padx=20, pady=(20, 0))
        bottom_frame.grid_columnconfigure(0, weight=1)
        settings_button = ctk.CTkButton(bottom_frame, text="Settings", command=self._open_settings_window, width=10)
        settings_button.grid(row=0, column=0, sticky="w")
        
        
    def _start_processing(self, operation_type: str) -> None:
        self._save_settings()
        
        def _run_processor():
            processor = FileProcessor()
            try:
                result = processor.process(
                    operation_type,
                    self.source_folder_entry.get(),
                    self.destination_folder_entry.get(),
                    self.prefix_entry.get(),
                    self.extension_combobox.get(),
                    self.number_file_entry.get()
                )
                
                if operation_type == "copy":
                    if result > 0:
                        msg = f"Copy operation completed:  {result} file{'s' if result != 1 else ''} copied"
                    else:
                        msg = "No files copied"
                elif operation_type == "move":
                    if result > 0:
                        msg = f"Move operation completed: {result} file{'s' if result != 1 else ''} moved"
                    else:
                        msg = "No files moved"
                elif operation_type == "rename":
                    if result > 0:
                        msg = f"Rename operation completed: {result} file{'s' if result != 1 else ''} renamed"
                    else:
                        msg = "No files renamed"
                else:  # delete
                    if result > 0:
                        msg = f"Delete operation completed: {result} file{'s' if result != 1 else ''} deleted"
                    else:
                        msg = "No files deleted"
                
                self.after(0, lambda: messagebox.showinfo("Done", msg))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Error", str(e)))
        
        pthread = threading.Thread(target=_run_processor)
        pthread.daemon = True
        pthread.start()
        
        
    def _load_settings(self) -> None:
        settings = self.settings_manager.load_settings()
        self.source_folder_entry.insert(0, settings.get("source_folder", ""))
        self.destination_folder_entry.insert(0, settings.get("destination_folder", ""))
        self.prefix_entry.insert(0, settings.get("prefix", ""))
        self.extension_combobox.set(settings.get("extension", ""))
        
        # Apply appearance mode if present
        appearance = settings.get("appearance_mode", "System")
        ctk.set_appearance_mode(appearance.lower())
        
        
    def _save_settings(self) -> None:
        settings = self.settings_manager.load_settings()
        settings.update({
            "source_folder": self.source_folder_entry.get(),
            "destination_folder": self.destination_folder_entry.get(),
            "prefix": self.prefix_entry.get(),
            "extension": self.extension_combobox.get(),
        })
        self.settings_manager.save_settings(settings)
        
        
    def _on_delete_window(self) -> None:
        settings = self.settings_manager.load_settings()
        retain_fields = settings.get("retain_fields", True)
        
        if retain_fields:
            self._save_settings()
        else:
            # Clear fields in settings
            self.settings_manager.save_settings({
                "appearance_mode": settings.get("appearance_mode", "System"),
                "retain_fields": False
            })
            
        self.destroy()
        
        
    def _open_settings_window(self) -> None:
        SettingsWindow(self)
