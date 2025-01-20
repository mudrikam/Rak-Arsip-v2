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
import json


class APIKeyManagement(ttk.LabelFrame): 
    def __init__(self, parent, BASE_DIR, main_window):
        super().__init__(parent, text="Manajemen API Key :", padding=(5, 5, 5, 5))
        self.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.current_file_path = None
        self.root_path = None
        self.BASE_DIR = BASE_DIR
        self.main_window = main_window
        
        # Load config
        self.config_path = os.path.join(BASE_DIR, "ui", "Ai", "ai_config.json")
        self.load_config()
        
        # Create frames - updated name
        self.create_model_selection_frame()
        self.create_api_key_list_frame()  # Renamed from create_prompt_management_frame
        
        # Configure main grid
        self.grid_columnconfigure(0, weight=1)
        
    def load_config(self):
        """Load AI configuration from JSON file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load AI configuration: {str(e)}")
            self.config = {"models": {}, "prompts": []}

    def save_config(self):
        """Save configuration to JSON file"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save AI configuration: {str(e)}")

    def create_model_selection_frame(self):
        """Create frame for model selection and API key management"""
        frame = ttk.LabelFrame(self, text="Input API Key :", padding=(5, 5, 5, 5))
        frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Container for all controls with consistent padding
        container = ttk.Frame(frame)
        container.pack(fill="x")
        
        # Model dropdown with consistent spacing
        self.model_var = tk.StringVar()
        models = list(self.config['models'].keys())
        model_dropdown = ttk.Combobox(container, 
                                    textvariable=self.model_var, 
                                    values=models, 
                                    state="readonly", 
                                    font=('TkDefaultFont', 14),
                                    width=15)
        model_dropdown.pack(side="left", padx=5)
        if models:
            model_dropdown.set(models[0])
            
        # API Key entry with consistent spacing and Enter binding
        self.api_key_var = tk.StringVar()
        api_key_entry = ttk.Entry(container, 
                                 textvariable=self.api_key_var,
                                 font=('TkDefaultFont', 14))
        api_key_entry.pack(side="left", fill="x", expand=True, padx=5)
        api_key_entry.bind('<Return>', lambda e: self.save_api_key())
        
        # Load plus icon
        plus_icon_path = os.path.join(self.BASE_DIR, "Img", "icon", "ui", "plus.png")
        if os.path.exists(plus_icon_path):
            plus_img = Image.open(plus_icon_path)
            # Resize to 16x16
            plus_img = plus_img.resize((16, 16), Image.Resampling.LANCZOS)
            self.plus_icon = ImageTk.PhotoImage(plus_img)
        else:
            self.plus_icon = None
        
        # Save button with plus icon
        save_button = ttk.Button(container, 
                                text="Simpan",
                                image=self.plus_icon if self.plus_icon else None,
                                compound='left',
                                command=self.save_api_key,
                                padding=5)
        save_button.pack(side="right", padx=5)

    def create_api_key_list_frame(self):  # Renamed from create_prompt_management_frame
        frame = ttk.LabelFrame(self, text="Daftar API Key Model :", padding=(5, 5, 5, 5))
        frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        
        # Make frame expandable
        self.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        
        # Left frame with padding
        left_frame = ttk.Frame(frame)
        left_frame.grid(row=0, column=0, sticky="nsew")
        left_frame.grid_rowconfigure(0, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)
        
        # Tree container with padding
        tree_container = ttk.Frame(left_frame)
        tree_container.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)
        
        # Treeview tanpa header dan dynamic sizing
        self.model_tree = ttk.Treeview(tree_container, 
                                      columns=("model",), 
                                      show="tree",
                                      selectmode="browse")
        self.model_tree.column("#0", width=0, stretch=False)
        self.model_tree.column("model", width=200, stretch=True)
        
        # Scrollbar yang langsung menempel
        scrollbar = ttk.Scrollbar(tree_container, 
                                 orient="vertical", 
                                 command=self.model_tree.yview)
        
        # Konfigurasi treeview dan scrollbar
        self.model_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack digunakan untuk membuat scrollbar menempel
        scrollbar.pack(side='right', fill='y')
        self.model_tree.pack(side='left', fill='both', expand=True)
        
        # Load delete icon
        delete_icon_path = os.path.join(self.BASE_DIR, "Img", "icon", "ui", "delete.png")
        if os.path.exists(delete_icon_path):
            delete_img = Image.open(delete_icon_path)
            # Resize to 16x16
            delete_img = delete_img.resize((16, 16), Image.Resampling.LANCZOS)
            self.delete_icon = ImageTk.PhotoImage(delete_img)
        else:
            self.delete_icon = None

        # Delete button with icon
        delete_button = ttk.Button(left_frame, 
                                 text="Hapus API Key",
                                 image=self.delete_icon if self.delete_icon else None,
                                 compound='left',
                                 command=self.delete_api_key,
                                 padding=5)
        delete_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        
        # Right frame with padding
        right_frame = ttk.Frame(frame)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        right_frame.grid_rowconfigure(0, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)
        
        # Text editor with padding and modified binding
        self.api_keys_editor = tk.Text(right_frame, wrap="word")
        self.api_keys_editor.grid(row=0, column=0, sticky="nsew")

        # Remove KeyRelease binding and use TextModified instead
        self.api_keys_editor.bind("<<Modified>>", self.update_model_api_keys)

        # Bind selection event
        self.model_tree.bind('<<TreeviewSelect>>', self.on_model_select)
        
        # Load initial models
        self.load_models()

    def load_models(self):
        """Load models into treeview"""
        self.model_tree.delete(*self.model_tree.get_children())
        for model_id, model_data in self.config['models'].items():
            self.model_tree.insert("", "end", values=(model_data['name'],), tags=(model_id,))

    def on_model_select(self, event):
        """Load API keys for selected model"""
        selected = self.model_tree.selection()
        if not selected:
            return
            
        model_id = self.model_tree.item(selected[0], "tags")[0]
        api_keys = self.config['models'][model_id]['api_key']
        
        # Clear editor and insert API keys with line breaks
        self.api_keys_editor.delete(1.0, tk.END)
        if isinstance(api_keys, list):
            # Display as separate lines
            self.api_keys_editor.insert(1.0, "\n".join(api_keys))
        elif isinstance(api_keys, str) and api_keys:
            # Convert comma to newline for display
            api_keys = [k.strip() for k in api_keys.split(',')]
            self.api_keys_editor.insert(1.0, "\n".join(api_keys))
            
        # Reset modified flag
        self.api_keys_editor.edit_modified(False)

    def update_model_api_keys(self, event):
        """Update API keys for selected model"""
        if not self.api_keys_editor.edit_modified():
            return
            
        selected = self.model_tree.selection()
        if not selected:
            return
            
        model_id = self.model_tree.item(selected[0], "tags")[0]
        text = self.api_keys_editor.get(1.0, tk.END).strip()
        
        # Split by newlines and clean up
        api_keys = [key.strip() for key in text.splitlines() if key.strip()]
        
        # Update config
        if len(api_keys) == 1:
            self.config['models'][model_id]['api_key'] = api_keys[0]
        else:
            self.config['models'][model_id]['api_key'] = api_keys
            
        self.save_config()
        
        # Reset modified flag
        self.api_keys_editor.edit_modified(False)

    def delete_api_key(self):
        """Delete API keys for selected model"""
        selected = self.model_tree.selection()
        if not selected:
            return
            
        model_id = self.model_tree.item(selected[0], "tags")[0]
        self.config['models'][model_id]['api_key'] = ""
        self.save_config()
        
        # Clear editor
        self.api_keys_editor.delete(1.0, tk.END)

    def save_api_key(self):
        """Save API key for selected model from entry field"""
        model = self.model_var.get()
        api_key = self.api_key_var.get()
        
        if not model or not api_key:
            return
            
        # Get existing API keys
        existing_keys = self.config['models'][model]['api_key']
        if isinstance(existing_keys, list):
            if api_key not in existing_keys:
                existing_keys.append(api_key)
        else:
            if existing_keys:
                existing_keys = [existing_keys, api_key]
            else:
                existing_keys = [api_key]
                
        # Update config
        self.config['models'][model]['api_key'] = existing_keys
        self.save_config()
        
        # Clear entry
        self.api_key_var.set("")
        
        # Update display if model is selected in treeview
        selected = self.model_tree.selection()
        if selected and self.model_tree.item(selected[0], "tags")[0] == model:
            self.api_keys_editor.delete(1.0, tk.END)
            # Display as separate lines
            if isinstance(existing_keys, list):
                self.api_keys_editor.insert(1.0, "\n".join(existing_keys))
            else:
                self.api_keys_editor.insert(1.0, existing_keys)