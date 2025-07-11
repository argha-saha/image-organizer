import customtkinter as ctk

class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Settings")
        self.geometry("300x200")
        self.parent = parent
        self.resizable(False, False)
        self.grab_set()

        # Centering frame
        center_frame = ctk.CTkFrame(self)
        center_frame.pack(expand=True)
        center_frame.grid_columnconfigure(0, weight=1)
        center_frame.grid_columnconfigure(1, weight=1)

        # Appearance mode
        ctk.CTkLabel(center_frame, text="Appearance Mode:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.appearance_combobox = ctk.CTkComboBox(
            center_frame, values=["System", "Dark", "Light"], width=120
        )
        self.appearance_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.appearance_combobox.set(self.parent.settings_manager.load_settings().get("appearance_mode", "System"))

        # Field retention
        ctk.CTkLabel(center_frame, text="On Close:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.retain_combobox = ctk.CTkComboBox(
            center_frame, values=["Retain Fields", "Clear Fields"], width=120
        )
        self.retain_combobox.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        retain_val = self.parent.settings_manager.load_settings().get("retain_fields", True)
        self.retain_combobox.set("Retain Fields" if retain_val else "Clear Fields")

        # Save button
        save_btn = ctk.CTkButton(center_frame, text="Save", command=self._save_settings)
        save_btn.grid(row=2, column=0, columnspan=2, pady=20)


    def _save_settings(self) -> None:
        appearance = self.appearance_combobox.get()
        retain = self.retain_combobox.get() == "Retain Fields"
        
        # Save to settings
        settings = self.parent.settings_manager.load_settings()
        settings["appearance_mode"] = appearance
        settings["retain_fields"] = retain
        self.parent.settings_manager.save_settings(settings)
        
        # Apply appearance
        ctk.set_appearance_mode(appearance.lower())
        self.destroy()