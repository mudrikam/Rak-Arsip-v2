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
import csv
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import webbrowser

class ProjectLibrary(ttk.LabelFrame):
    def __init__(self, parent, x, y, width, height, BASE_DIR, main_window):
        super().__init__(parent, text="Daftar Arsip yang telah dibuat :", padding=10)
        self.place(x=x, y=y, width=width, height=height)  # Atur posisi dan ukuran
        self.main_window = main_window

        self.BASE_DIR = os.path.join(BASE_DIR, "Database", "Library")
        os.makedirs(self.BASE_DIR, exist_ok=True)

        self.csv_file_path = os.path.join(self.BASE_DIR, "project_library.csv")
        self.create_csv_if_not_exists()

        self.last_modified_time = os.path.getmtime(self.csv_file_path)

        # Frame untuk tombol pencarian dan buka
        self.search_frame = ttk.Frame(self)
        self.search_frame.pack(pady=5, fill=tk.X)

        # Label "Cari :"
        self.search_label = ttk.Label(self.search_frame, text="Cari :")
        self.search_label.grid(row=0, column=0, padx=(0,5))

        # Entry untuk pencarian
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_var, width=45, font=("Lato Medium", 14))
        self.search_entry.grid(row=0, column=1, padx=(0,5), sticky="ew")
        self.search_entry.bind("<KeyRelease>", self.search_library)
        self.search_entry.bind("<Double-Button-1>", self.clear_search)

        self.open_button = ttk.Button(self.search_frame, text="Buka di Explorer", command=self.open_file, state=tk.DISABLED, padding=5)
        self.open_button.grid(row=0, column=2, sticky="ew", padx=(0,0))  # sticky ew dan padx 0

        self.search_frame.columnconfigure(2, weight=1)  # memberikan weight pada kolom 2
        

        self.tree = ttk.Treeview(self, columns=("No", "Tanggal", "Nama", "Lokasi"), show="headings", height=6)
        self.tree.heading("No", text="No")
        self.tree.heading("Tanggal", text="Tanggal")
        self.tree.heading("Nama", text="Nama")
        self.tree.heading("Lokasi", text="Lokasi")
        self.tree.column("No", width=50, anchor="center")
        self.tree.column("Tanggal", width=120, anchor="center")
        self.tree.column("Nama", width=200, anchor="w")
        self.tree.column("Lokasi", width=300, anchor="w")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)
        self.tree.bind("<Double-Button-1>", self.on_double_click)
        self.load_library()
        self.selected_file = None
        self.check_for_upDates()

        self.backup_button = ttk.Button(self, text="Cadangkan", command=self.backup_library, padding=5)
        self.backup_button.pack(side=tk.LEFT, pady=10)
        
        self.import_button = ttk.Button(self, text="Impor", command=self.import_existing_library, padding=5)
        self.import_button.pack(side=tk.LEFT, pady=10, padx=(10,0))

        self.reminder_label = ttk.Label(self, text="Buatlah cadangan berkala untuk menghindari kehilangan akses daftar pustaka.", foreground="#999999")
        self.reminder_label.pack(side=tk.LEFT, pady=10, padx=10)


    def create_csv_if_not_exists(self):
        if not os.path.exists(self.csv_file_path):
            with open(self.csv_file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["No", "Tanggal", "Nama", "Lokasi"])

    def load_library(self):
        self.tree.delete(*self.tree.get_children())
        rows = []
        with open(self.csv_file_path, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)
            rows = [row for row in reader]
        rows.sort(key=lambda x: int(x[0]), reverse=True)
        for row in rows:
            self.tree.insert("", "end", values=row)

    def on_row_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item[0])
            self.selected_file = item["values"][3]
            self.open_button.config(state=tk.NORMAL)
            file_dir=self.selected_file
            self.main_window.update_status(f"Buka di Explorer : {file_dir}")

    def open_file(self):
        if self.selected_file and os.path.exists(self.selected_file):
            try:
                webbrowser.open(self.selected_file)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file:\n{e}")
        else:
            messagebox.showwarning("Periksa!", "Sepertinya ada masalah pada lokasi file")

    def check_for_upDates(self):
        try:
            current_modified_time = os.path.getmtime(self.csv_file_path)
            if current_modified_time != self.last_modified_time:
                self.last_modified_time = current_modified_time
                self.load_library()
        except FileNotFoundError:
            self.create_csv_if_not_exists()
            self.main_window.update_status(f"Daftar Pustaka baru telah dibuat.")
            self.load_library()
        else:
            self.after(1000, self.check_for_upDates)

    def search_library(self, event=None):
        """Cari baris dalam file CSV yang sesuai dengan kata kunci."""
        keyword = self.search_var.get().strip().lower()
        self.tree.delete(*self.tree.get_children())  # Hapus semua baris dari Treeview

        if not keyword:
            self.load_library()  # Muat ulang semua data jika entri pencarian kosong
            return

        matching_rows = []
        with open(self.csv_file_path, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)  # Lewati baris header
            for row in reader:
                if any(keyword in field.lower() for field in row):  # Periksa apakah kata kunci ada di bidang mana pun
                    matching_rows.append(row)

        for row in matching_rows:
            self.tree.insert("", "end", values=row)
            
    def clear_search(self, event=None):
        self.search_var.set("")  # Setel StringVar menjadi kosong
        self.search_library()  # Panggil search_library agar data kembali semula
            
    def on_double_click(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item[0])
            self.selected_file = item["values"][3]
            self.open_file()
            self.clear_search()
            
    def backup_library(self):
        try:
            if os.name == 'nt':  # Windows
                initialdir = "::{20D04FE0-3AEA-1069-A2D8-08002B30309D}"
            # Tampilkan dialog untuk memilih lokasi penyimpanan file backup
            backup_file_path = filedialog.asksaveasfilename(
                initialdir=initialdir,
                initialfile="project_library_backup.csv",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            if not backup_file_path:
                return  # Jika pengguna membatalkan dialog, keluar dari fungsi

            with open(self.csv_file_path, mode="r", encoding="utf-8") as source_file:
                with open(backup_file_path, mode="w", newline="", encoding="utf-8") as backup_file:
                    reader = csv.reader(source_file)
                    writer = csv.writer(backup_file)
                    for row in reader:
                        writer.writerow(row)
            messagebox.showinfo(f"Daftar Pustaka telah dicadangkan.", f"Pastikan simpan file {os.path.basename(backup_file_path)} ke tempat aman.\n\nDaftar Pustaka dapat dikembalikan ke :\n\nRak Arsip\\App\\Database\\Library \n\nJika aplikasi Rak Arsip mengalami masalah.")
            self.main_window.update_status(f"Amaannn...., daftar Pustaka sudah dicadangkan (^_^)")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mencadangkan arsip:\n{e}")


    def import_existing_library(self):
        try:
            # Tampilkan dialog untuk memilih file CSV yang akan diimpor
            import_file_path = filedialog.askopenfilename(
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            if not import_file_path:
                return  # Jika pengguna membatalkan dialog, keluar dari fungsi

            # Baca data dari file CSV yang dipilih
            with open(import_file_path, mode="r", encoding="utf-8") as import_file:
                reader = csv.reader(import_file)
                next(reader, None)  # Lewati baris header
                import_rows = [row for row in reader]

            # Baca data dari project_library.csv
            with open(self.csv_file_path, mode="r", encoding="utf-8") as existing_file:
                existing_reader = csv.reader(existing_file)
                existing_rows = [row for row in existing_reader]

            # Jika project_library.csv kosong, gantikan dengan data dari file yang diimpor
            if len(existing_rows) <= 1:  # <= 1 karena baris pertama adalah header
                with open(self.csv_file_path, mode="w", newline="", encoding="utf-8") as existing_file:
                    writer = csv.writer(existing_file)
                    writer.writerow(["No", "Tanggal", "Nama", "Lokasi"])
                    for row in import_rows:
                        writer.writerow(row)
            else:
                # Jika project_library.csv sudah ada isinya, tambahkan data dari file yang diimpor
                last_no = int(existing_rows[-1][0])  # Ambil nomor terakhir dari project_library.csv
                with open(self.csv_file_path, mode="a", newline="", encoding="utf-8") as existing_file:
                    writer = csv.writer(existing_file)
                    for row in import_rows:
                        last_no += 1
                        new_name = f"{row[2]}_import"  # Tambahkan suffix _import pada nama file
                        new_row = [last_no, row[1], new_name, row[3]]
                        writer.writerow(new_row)

            messagebox.showinfo("Berhasil", "Daftar Pustaka telah diimpor dengan sukses.")
            self.main_window.update_status("Daftar Pustaka telah diimpor dengan sukses.")
            self.load_library()  # Muat ulang data di Treeview
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengimpor Daftar Pustaka:\n{e}")

