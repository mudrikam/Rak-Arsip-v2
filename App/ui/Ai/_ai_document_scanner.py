import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
from PIL import Image, ImageTk

class AIDocumentScanner(ttk.Frame):
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
        
        # Load back icon
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
        
        # Main content
        content_frame = ttk.LabelFrame(self, text="Document Scanner", padding=10)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Add your document scanner UI components here
        ttk.Label(content_frame, text="Document Scanner Interface").pack()
        ttk.Button(content_frame, text="Scan Document", 
                  command=lambda: messagebox.showinfo("Info", "Scanning...")).pack(pady=10)
        
    def go_back(self):
        """Return to the main metadata generator UI"""
        # Import here to avoid circular imports
        from .ai_metadata_generator import AIMetadataGenerator
        
        # Clear current frame
        for widget in self.winfo_children():
            widget.destroy()
            
        # Recreate metadata generator
        generator = AIMetadataGenerator(self, self.BASE_DIR, self.main_window)
        generator.grid(row=0, column=0, sticky="nsew")
