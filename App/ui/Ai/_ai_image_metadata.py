import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk

class AIImageMetadata(ttk.Frame):
    def __init__(self, parent, BASE_DIR, main_window):
        super().__init__(parent)
        self.BASE_DIR = BASE_DIR
        self.main_window = main_window
        
        # Configure grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        # Header frame with back button
        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        try:
            back_icon_path = os.path.join(BASE_DIR, "img", "Icon", "ui", "back.png")
            back_icon = Image.open(back_icon_path)
            back_icon = back_icon.resize((16, 16), Image.LANCZOS)
            back_photo = ImageTk.PhotoImage(back_icon)
            
            back_btn = ttk.Button(header_frame, 
                                text="Kembali",
                                image=back_photo,
                                compound='left',
                                command=self.go_back)
            back_btn.image = back_photo
        except:
            back_btn = ttk.Button(header_frame, 
                                text="Kembali",
                                command=self.go_back)
        
        back_btn.pack(side="left", padx=5)
            
    def go_back(self):
        """Return to the AI Metadata Generator view"""
        from App.ui.Ai.ai_metadata_generator import AIMetadataGenerator
        
        # Dapatkan parent frame yang benar (2 level ke atas)
        parent = self.master.master
        
        # Hapus semua widget di parent
        for widget in parent.winfo_children():
            widget.destroy()
            
        # Buat generator baru di parent yang benar menggunakan grid
        generator = AIMetadataGenerator(parent, self.BASE_DIR, self.main_window)
        generator.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Konfigurasi grid di parent
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)
