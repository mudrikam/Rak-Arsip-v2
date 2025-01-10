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

import os
import zipfile
from datetime import date
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time

class DatabaseBackup(ttk.LabelFrame):
    def __init__(self, parent, BASE_DIR, main_window):
        super().__init__(parent, text="Cadangkan Database", padding=10)
        self.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.BASE_DIR = BASE_DIR
        self.main_window = main_window

        # Frame for buttons
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))  # Moved to bottom

        # Backup button
        self.backup_button = ttk.Button(self.button_frame, text="Cadangkan", command=self.export_database, padding=5)
        self.backup_button.pack(side=tk.LEFT, padx=(0, 10), pady=5)

        # Import button
        self.import_button = ttk.Button(self.button_frame, text="Impor", command=self.import_database, padding=5)
        self.import_button.pack(side=tk.LEFT, pady=5)
        
        self.reminder_label = ttk.Label(self.button_frame, text="Buatlah cadangan berkala untuk menghindari kehilangan Database.", foreground="#999999")
        self.reminder_label.pack(side=tk.LEFT, pady=10, padx=10)

        # Scrollable Treeview for files
        self.file_treeview = ttk.Treeview(self, columns=("No", "Direktori", "File"), show="headings")
        self.file_treeview.heading("No", text="No")
        self.file_treeview.heading("Direktori", text="Direktori")
        self.file_treeview.heading("File", text="File")
        
        # Set fixed column widths
        self.file_treeview.column("No", width=50, anchor="center")
        self.file_treeview.column("Direktori", width=200, anchor="w")
        self.file_treeview.column("File", width=200, anchor="w")
        
        self.file_treeview.pack(side=tk.LEFT, fill="both", expand=True)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.file_treeview.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        self.file_treeview.config(yscrollcommand=self.scrollbar.set)
        self.update_file_list()

        # Start a thread to monitor the database directory
        self.monitor_thread = threading.Thread(target=self.monitor_database_directory, daemon=True)
        self.monitor_thread.start()

        # Bind the configure event to adjust widget sizes dynamically
        self.bind("<Configure>", self.on_resize)

    def update_file_list(self):
        """Update the Treeview with the list of files to be backed up."""
        for item in self.file_treeview.get_children():
            self.file_treeview.delete(item)
        database_dir = os.path.join(self.BASE_DIR, "Database")
        file_no = 1
        for root, dirs, files in os.walk(database_dir):
            for file in files:
                if not file.endswith(".old"):
                    directory = os.path.relpath(root, self.BASE_DIR)
                    self.file_treeview.insert("", "end", values=(file_no, directory, file))
                    file_no += 1

    def export_database(self):
        """Export the database to a zip file."""
        default_filename = f"Rak-Arsip-DB-{date.today().strftime('%Y-%m-%d')}.zip"
        zip_filepath = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("Zip files", "*.zip")], initialfile=default_filename)
        if not zip_filepath:
            return

        database_dir = os.path.join(self.BASE_DIR, "Database")
        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(database_dir):
                for file in files:
                    if not file.endswith(".old"):
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, self.BASE_DIR))

        messagebox.showinfo("Sukses", f"Database berhasil dicadangkan ke {zip_filepath}")
        self.main_window.update_status(f"Database berhasil dicadangkan ke {zip_filepath}")

    def import_database(self):
        """Import a zip file into the database directory."""
        zip_filepath = filedialog.askopenfilename(filetypes=[("Zip files", "*.zip")])
        if not zip_filepath:
            return

        database_dir = os.path.join(self.BASE_DIR)
        with zipfile.ZipFile(zip_filepath, 'r') as zipf:
            for file_info in zipf.infolist():
                extracted_path = os.path.join(database_dir, file_info.filename)
                if os.path.exists(extracted_path):
                    os.rename(extracted_path, f"{extracted_path}.old")
                zipf.extract(file_info, database_dir)

        messagebox.showinfo("Sukses", "Database berhasil diimport. Data lama telah digantikan dan ditambahkan ekstensi .old")
        self.main_window.update_status("Database berhasil diimport. Data lama telah digantikan dan ditambahkan ekstensi .old")
        self.update_file_list()

    def monitor_database_directory(self):
        """Monitor the database directory for changes and update the file list."""
        database_dir = os.path.join(self.BASE_DIR, "Database")
        previous_files = set()

        while True:
            current_files = set()
            for root, dirs, files in os.walk(database_dir):
                for file in files:
                    if not file.endswith(".old"):
                        current_files.add(os.path.join(root, file))

            if current_files != previous_files:
                self.update_file_list()
                previous_files = current_files

            time.sleep(5)  # Check for changes every 5 seconds

    def on_resize(self, event):
        """Adjust column widths dynamically based on window size."""
        width = self.winfo_width()
        self.file_treeview.column("No", width=int(width * 0.1))
        self.file_treeview.column("Direktori", width=int(width * 0.45))
        self.file_treeview.column("File", width=int(width * 0.45))
