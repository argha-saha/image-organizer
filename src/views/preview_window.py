import customtkinter as ctk
import tkinter as tk

class PreviewWindow(ctk.CTkToplevel):
    def __init__(self, parent, found, missing, overwrite=None):
        super().__init__(parent)
        self.title("Preview Files")
        self.geometry("600x400")
        self.grab_set()

        main_label = ctk.CTkLabel(self, text="File Processing Summary", font=ctk.CTkFont(size=18, weight="bold"))
        main_label.pack(pady=(10, 0))

        summary_text = f"Found: {len(found)}   Missing: {len(missing)}"
        if overwrite is not None:
            summary_text += f"   Overwrite: {len(overwrite)}"
        summary_label = ctk.CTkLabel(self, text=summary_text, font=ctk.CTkFont(size=14))
        summary_label.pack()

        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        listbox = tk.Listbox(frame, selectmode="browse")
        listbox.pack(fill="both", expand=True, side="left")
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar.set)
        
        for f in found:
            listbox.insert("end", f)
        for f in missing:
            listbox.insert("end", f"[MISSING] {f}")
        if overwrite:
            for f in overwrite:
                listbox.insert("end", f"[OVERWRITE] {f}")
                
        close_button = ctk.CTkButton(self, text="Close", command=self.destroy)
        close_button.pack(pady=(10, 20))
