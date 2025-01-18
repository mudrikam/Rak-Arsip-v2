# ---------------------------------------------------------------
# Hak Cipta (C) 2025 M. Mudrikul Hikam
# ---------------------------------------------------------------
# Program ini adalah perangkat lunak bebas: Anda dapat 
# mendistribusikan ulang dan/atau memodifikasinya di bawah 
# ketentuan Lisensi Publik Umum GNU (GNU GPL v3) sebagaimana 
# diterbitkan oleh Free Software Foundation, baik versi 3 dari 
# Lisensi, atau (sesuai pilihan Anda) versi yang lebih baru.
# 
# Program ini didistribusikan dengan harapan bahwa itu akan 
# berguna, tetapi TANPA JAMINAN; bahkan tanpa jaminan tersirat
# tentang DIPERDAGANGKAN atau KESESUAIAN UNTUK TUJUAN TERTENTU. 
# Lihat Lisensi Publik Umum GNU untuk lebih jelasnya.
# 
# Anda seharusnya telah menerima salinan Lisensi Publik Umum GNU
# bersama dengan program ini. Jika tidak, lihat 
# <https://www.gnu.org/licenses/>.
# 
# ---------------------------------------------------------------
# Mohon untuk tidak menghapus header ini.
# Jika ingin berkontribusi, tuliskan namamu di sini.
# ---------------------------------------------------------------
# | Nama Kontributor       | Kontribusi                         |
# |------------------------|------------------------------------|
# |                        |                                    |
# |                        |                                    |
# |                        |                                    |
# ---------------------------------------------------------------

import csv
import datetime
import os
import re
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from datetime import datetime
from PIL import Image, ImageTk


class AIMetadataGenerator(ttk.LabelFrame): 
    def __init__(self, parent, BASE_DIR, main_window):
        super().__init__(parent, text="Generate Metadata", padding=5)
        self.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.current_file_path = None
        self.root_path = None
        self.BASE_DIR = BASE_DIR
        self.main_window = main_window
        
        # Make main frame expandable
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # Create canvas and scrollable components first
        self.canvas = tk.Canvas(self, bg='#f0f0f0', highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        # Configure scrollable frame after creation
        self.scrollable_frame.columnconfigure(0, weight=1)
        self.scrollable_frame.rowconfigure(0, weight=1)
        
        # Create window and bind configurations
        self.canvas_window = self.canvas.create_window(
            (0, 0), 
            window=self.scrollable_frame, 
            anchor="nw",
            tags='frame'
        )
        
        # Configure canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        
        # Create cards frame
        self.cards_frame = ttk.Frame(self.scrollable_frame)
        self.cards_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.cards_frame.columnconfigure(tuple(range(3)), weight=1, uniform='col')
        
        # Bind events
        self.scrollable_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        self.bind('<Enter>', self._bind_mousewheel)
        self.bind('<Leave>', self._unbind_mousewheel)
        
        # Create cards
        self.create_cards()
        
        # Add helper mapping
        self.helper_map = {
            "Image Metadata": "_ai_image_metadata.py",  # Changed to image metadata
            "Smart Extractor": "_ai_smart_extractor.py",
            "Data Analyzer": "_ai_data_analyzer.py"
        }
        
    def _bind_mousewheel(self, event):
        """Bind mousewheel when mouse enters the widget"""
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, event):
        """Unbind mousewheel when mouse leaves the widget"""
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        """Enhanced scroll handling"""
        if self.canvas.yview() != (0.0, 1.0):  # Only scroll if there's something to scroll
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def _on_frame_configure(self, event):
        """Handle frame resizing"""
        # Update the scroll region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def _on_canvas_configure(self, event):
        """Handle canvas resizing"""
        width = event.width
        # Update both canvas window and frame width
        self.canvas.itemconfig('frame', width=width)
        self.scrollable_frame.configure(width=width)
        
        # Force cards update when canvas resizes
        self.after(100, self._update_cards_layout)
        
    def _update_cards_layout(self):
        """Update card layouts when parent resizes"""
        available_width = self.winfo_width()
        if available_width > 1:  # Ensure valid width
            for widget in self.cards_frame.winfo_children():
                widget.configure(width=available_width//3 - 20)  # Account for padding
        
    def create_cards(self):
        cards_data = [
            ("Image Metadata", 
             "Buat metadata untuk foto atau desain.",
             "image.png"),  # Kembalikan ke icon original
            ("Smart Extractor", 
             "Ut enim ad minim veniam, quis nostrud exercitation.",
             "video.png"),
            ("Data Analyzer", 
             "Duis aute irure dolor in reprehenderit in voluptate.",
             "video.png")
        ]
        
        # Set minimum width for cards
        MIN_CARD_WIDTH = 200  # Minimal width sebelum turun ke bawah
        
        def update_grid():
            # Get actual frame width
            parent_width = self.winfo_width()
            if parent_width <= 1:  # Initial call
                self.after(100, update_grid)
                return
            
            # Calculate available width accounting for padding
            available_width = parent_width - 20  # Total padding (left+right)
            
            # Calculate columns based on minimum width
            if available_width < (MIN_CARD_WIDTH * 3 + 20):  # Check if we need to reduce columns
                if available_width < (MIN_CARD_WIDTH * 2 + 10):
                    max_cols = 1
                    card_width = available_width - 10
                else:
                    max_cols = 2
                    card_width = (available_width - 15) // 2
            else:
                max_cols = 3  # Default to 3 columns
                card_width = (available_width - 20) // 3  # Distribute space equally
            
            # Reset column configurations
            for i in range(max_cols):
                self.cards_frame.columnconfigure(i, weight=1, uniform='col')
            
            # Update all cards
            for idx, widget in enumerate(self.cards_frame.winfo_children()):
                row = idx // max_cols
                col = idx % max_cols
                widget.grid_forget()
                widget.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                widget.configure(width=card_width)
        
        # Create cards
        for idx, (title, desc, img_file) in enumerate(cards_data):
            # Card frame
            card = tk.Frame(self.cards_frame, bg='white', relief='flat')
            card.grid(row=0, column=idx, padx=5, pady=5, sticky="nsew")
            
            # Force card to maintain size
            card.grid_propagate(False)
            card.configure(height=300)
            
            # Inner frame dengan padding 10
            inner_frame = tk.Frame(card, bg='white')
            inner_frame.pack(fill='both', expand=True, padx=10, pady=10)  # Ubah padding ke 10
            
            try:
                # Load thumbnail image and create label
                img_path = os.path.join(self.BASE_DIR, "img", "Icon", "ui", img_file)
                img = Image.open(img_path)
                img = img.resize((64, 64), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                # Center the image
                img_label = tk.Label(inner_frame, image=photo, bg='white')
                img_label.image = photo
                img_label.pack(pady=(0, 10), anchor='center')
            except Exception as e:
                print(f"Failed to load image {img_file}: {e}")
                tk.Label(inner_frame, text="No Image", bg='white').pack(pady=(0, 10))
            
            # Center-aligned text
            tk.Label(inner_frame, 
                    text=title,
                    font=('Segoe UI', 12, 'bold'),
                    bg='white').pack(pady=(0, 5), anchor='center')
            
            # Center-aligned description
            tk.Label(inner_frame,
                    text=desc,
                    wraplength=200,
                    font=('Segoe UI', 10),
                    bg='white').pack(pady=(0, 10), anchor='center')
            
            try:
                # Load launch icon for button
                launch_icon_path = os.path.join(self.BASE_DIR, "img", "Icon", "ui", "launch.png")
                launch_icon = Image.open(launch_icon_path)
                launch_icon = launch_icon.resize((16, 16), Image.LANCZOS)
                launch_photo = ImageTk.PhotoImage(launch_icon)
                
                # Button with icon
                btn = ttk.Button(inner_frame,
                               text="Buka",
                               padding=5,
                               image=launch_photo,
                               compound='right',
                               command=lambda t=title: self.open_tool(t))
                btn.image = launch_photo  # Keep reference
                btn.pack(anchor='center')
            except Exception as e:
                print(f"Failed to load launch icon: {e}")
                ttk.Button(inner_frame,
                          text="Buka",
                          padding=5,
                          command=lambda t=title: self.open_tool(t)).pack(anchor='center')
            
            # Remove fixed size constraints
            card.grid_propagate(True)
        
        # Ensure cards_frame expands properly
        self.cards_frame.columnconfigure(tuple(range(3)), weight=1, uniform='col')
        
        # Bind resize event
        self.bind('<Configure>', lambda e: update_grid())
        
        # Initial grid update
        self.after(100, update_grid)
            
    def open_tool(self, title):
        """Load and display the appropriate helper UI"""
        helper_file = self.helper_map.get(title)
        if not helper_file:
            messagebox.showerror("Error", "Helper not implemented")
            return
            
        # Clear the main frame
        for widget in self.winfo_children():
            widget.destroy()
            
        # Import and load the helper dynamically
        try:
            helper_path = os.path.join(self.BASE_DIR, "ui", "Ai", helper_file)
            if os.path.exists(helper_path):
                # Import the module from file path
                import importlib.util
                spec = importlib.util.spec_from_file_location("helper", helper_path)
                helper_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(helper_module)
                
                # Get the helper class (assumed to be the only class in the module)
                helper_class = next(obj for name, obj in helper_module.__dict__.items() 
                                  if isinstance(obj, type) and name.startswith('AI'))
                
                # Create helper instance
                helper = helper_class(self, self.BASE_DIR, self.main_window)
                helper.grid(row=0, column=0, sticky="nsew")
                
            else:
                messagebox.showerror("Error", f"Helper file {helper_file} not found")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load helper: {str(e)}")