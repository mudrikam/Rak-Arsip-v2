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

import tkinter as tk
from tkinter import ttk
import os
from tkinter import messagebox

class CategorySelector(ttk.LabelFrame):
    def __init__(self, parent, x, y, width, height, BASE_DIR, main_window):
        """
        Inisialisasi CategorySelector.
        """
        super().__init__(parent, text="Pilih Kategori :")  # LabelFrame sebagai widget induk
        self.place(x=x, y=y, width=width, height=height)  # Atur posisi dan ukuran
        self.BASE_DIR = BASE_DIR
                
        self.main_window = main_window
                
        self.category_value = tk.StringVar()
        self.new_category_value = tk.StringVar()
        self.categories = []
        self._load_categories()

        # Buat LabelFrames untuk kategori dan subkategori
        self.category_label_frame = ttk.LabelFrame(self, text="Kategori :", padding="10")
        self.category_label_frame.pack(fill="x", padx=10, pady=5)

        self.subcategory_label_frame = ttk.LabelFrame(self, text="Sub Kategori :", padding="10")
        self.subcategory_label_frame.pack(fill="x", padx=10, pady=5)

        # Tambahkan dropdown kategori dan input field
        self._add_category_dropdown(self.category_label_frame)
        self._add_category_input(self.category_label_frame)

        # Tambahkan dropdown subkategori dan input field
        self._add_subcategory_dropdown(self.subcategory_label_frame)
        self._add_subcategory_input(self.subcategory_label_frame)

        # Tombol reset ditempatkan di bawah frame subkategori
        self.reset_button = ttk.Button(self, text="Reset Kategori", command=self._reset, state=tk.DISABLED)
        self.reset_button.pack(fill=tk.X, padx=10, pady=5)  # Pack setelah frame subkategori

        # Inisialisasi waktu terakhir modifikasi untuk Category.txt
        self.category_file_path = os.path.join(self.BASE_DIR, "Database", "Category.txt")
        try:
            self.last_modified_time = os.path.getmtime(self.category_file_path)
        except FileNotFoundError:
            self.last_modified_time = None

        # Inisialisasi waktu terakhir modifikasi untuk file subkategori yang dipilih
        self.selected_subcategory_file_path = None
        self.last_subcategory_modified_time = None

        # Mulai memonitor Category.txt untuk perubahan
        self.check_for_updates()
        self._update_subcategory_state()

    def _load_categories(self):
        """
        Muat kategori dari file Category.txt jika ada.
        """
        category_file_path = os.path.join(self.BASE_DIR, "Database", "Category.txt")
        try:
            with open(category_file_path, "r") as file:
                self.categories = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print("Category.txt tidak ditemukan. Memulai dengan daftar kategori kosong.")
            self.categories = ["Tambahkan Kategori Baru"]  # Default jika file tidak ditemukan

    def _add_category_dropdown(self, parent_frame):
        """
        Buat dan tempatkan dropdown kategori (ComboBox).
        """
        # Buat dropdown (ComboBox) untuk kategori
        self.category_dropdown = ttk.Combobox(
            parent_frame,
            textvariable=self.category_value,
            font=("Arial", 10),
            state="readonly",  # Buat dropdown hanya-baca
        )
        self.category_dropdown["values"] = self.categories
        self.category_dropdown.pack(fill=tk.X, pady=(10, 0))  # Tempatkan dropdown dengan padding

        # Set kategori default ke None (kosong) awalnya
        self.category_value.set("")  # Pastikan tidak ada pilihan default

        # Bind event <ComboboxSelected> untuk memicu aksi pemilihan kategori
        self.category_dropdown.bind("<<ComboboxSelected>>", self._on_category_selected)
        self.category_value.trace("w", self._update_subcategory_state)

    def _add_category_input(self, parent_frame):
        """
        Tambahkan input field dan tombol untuk menambah kategori baru.
        """
        # Buat StringVar baru khusus untuk input kategori
        self.new_category_value = tk.StringVar()

        # Entry untuk kategori baru dengan validasi input
        self.new_category_entry = ttk.Entry(parent_frame, textvariable=self.new_category_value, font=("Arial", 10))
        self.new_category_entry.pack(fill=tk.X, pady=(10, 0))
        self.new_category_entry.bind("<Return>", lambda event: self._add_new_category())

        # Bind event untuk mengganti spasi dengan underscore secara otomatis
        def on_key_release(event):
            current_value = self.new_category_value.get()

            if event.keysym not in ['BackSpace', 'Delete']:
                # Filter karakter yang diizinkan (huruf, angka, underscore, dan spasi)
                filtered_value = ''.join(char for char in current_value if char.isalnum() or char == '_' or char == ' ')

                # Ganti spasi dengan underscore
                updated_value = filtered_value.replace(" ", "_")

                self.new_category_value.set(updated_value)

        self.new_category_entry.bind("<KeyRelease>", on_key_release)

        # Tombol untuk menambah kategori baru
        add_button = ttk.Button(parent_frame, text="Tambah", command=self._add_new_category)
        add_button.pack(fill=tk.X, pady=(10, 0))

    def _add_new_category(self):
        """
        Tambahkan kategori baru ke file dan perbarui dropdown.
        """
        new_category = self.new_category_value.get().strip()
        new_category = new_category.replace(" ", "_")  # Ganti spasi dengan underscore
        
        if new_category:
            category_file_path = os.path.join(self.BASE_DIR, "Database", "Category.txt")
            
            # Periksa apakah kategori sudah ada di file
            if os.path.exists(category_file_path):
                with open(category_file_path, "r") as file:
                    existing_categories = [line.strip() for line in file if line.strip()]
                    if new_category in existing_categories:
                        messagebox.showwarning("Peringatan", "Kategori sudah ada!")
                        self.new_category_entry.delete(0, tk.END)  # Reset input field
                        return
            
            # Buat file jika tidak ada
            if not os.path.exists(category_file_path):
                with open(category_file_path, "w") as file:
                    print(f"Created new file: {category_file_path}")

            # Tambahkan kategori baru ke file
            with open(category_file_path, "a") as file:
                file.write(f"{new_category}\n")

            # Perbarui dropdown kategori
            self.categories.append(new_category)
            self.category_dropdown["values"] = self.categories
            self.category_value.set(new_category)  # Set kategori baru sebagai default
            print(f"New category added: {new_category}")

            # Bersihkan field entry
            self.new_category_entry.delete(0, tk.END)
        else:
            print("Invalid input. Category name cannot be empty.")
            messagebox.showwarning("Peringatan", "Kategori tidak boleh kosong!")

    def _add_subcategory(self):
        """
        Tambahkan subkategori baru ke file subkategori kategori yang dipilih.
        """
        selected_category = self.category_value.get()
        new_subcategory = self.new_subcategory_value.get().strip()  # Gunakan StringVar baru untuk input

        if new_subcategory:
            subcategory_file_path = os.path.join(self.BASE_DIR, "Database", f"{selected_category}.txt")
            with open(subcategory_file_path, "a") as file:
                file.write(f"{new_subcategory}\n")
            print(f"Added new subcategory: {new_subcategory}")
            # Muat ulang subkategori
            self._on_category_selected(None)  # Trigger pemuatan ulang daftar

            # Bersihkan field entry
            self.new_subcategory_entry.delete(0, tk.END)
        else:
            print("Invalid input. Subcategory name cannot be empty.")
            messagebox.showwarning("Peringatan", "Sub Kategori tidak boleh kosong!")

    def _on_category_selected(self, event):
        """
        Event handler untuk pemilihan kategori.
        Ini akan membuat SubCategorySelector berdasarkan kategori yang dipilih.
        """
        selected_category = self.category_value.get()  # Dapatkan kategori yang dipilih
        self.main_window.update_value("category", selected_category)  # Perbarui kategori di MainWindow
        # Perbarui status bar dengan kategori yang dipilih
        
        self.main_window.update_status(f"Kategori utama: {selected_category}")
        print(f"Selected Category: {selected_category}")  # Cetak kategori yang dipilih ke konsol
        
        self.reset_button.config(state=tk.NORMAL)

        # Buat path ke file subkategori yang sesuai
        subcategory_file_path = os.path.join(self.BASE_DIR, "Database", f"{selected_category}.txt")

        # Periksa apakah file ada
        if os.path.exists(subcategory_file_path):
            try:
                with open(subcategory_file_path, "r") as file:
                    subcategories = [line.strip() for line in file if line.strip()]
                    if subcategories:
                        self.subcategory_dropdown["values"] = subcategories
                        self.subcategory_value.set(subcategories[0])  # Set subkategori default dari daftar
                    else:
                        print(f"The file {subcategory_file_path} is empty.")
                        self.subcategory_dropdown["values"] = [""]
            except Exception as e:
                print(f"Error reading {subcategory_file_path}: {e}")
        else:
            print(f"File {subcategory_file_path} not found.")
            # Buat file dengan daftar default atau izinkan penambahan subkategori baru
            self.subcategory_dropdown["values"] = ["Tambah"]

        # Reset field input subkategori ke keadaan kosong
        self.subcategory_value.set("")  # Bersihkan field input subkategori

        # Perbarui waktu terakhir modifikasi untuk file subkategori yang dipilih
        self.selected_subcategory_file_path = subcategory_file_path
        try:
            self.last_subcategory_modified_time = os.path.getmtime(subcategory_file_path)
        except FileNotFoundError:
            self.last_subcategory_modified_time = None

        self._update_subcategory_state()

    def _add_subcategory_dropdown(self, parent_frame):
        """
        Buat dan tempatkan dropdown subkategori (ComboBox).
        """
        self.subcategory_value = tk.StringVar()
        self.subcategory_dropdown = ttk.Combobox(
            parent_frame,
            textvariable=self.subcategory_value,
            font=("Arial", 10),
            state="readonly",  # Buat dropdown hanya-baca
        )
        self.subcategory_dropdown.pack(fill=tk.X, pady=(10, 0))  # Tempatkan dropdown dengan padding

        # Set subkategori default (atau nilai default lainnya)
        self.subcategory_value.set("Pilih kategori dulu")

        # Bind event <ComboboxSelected> untuk memuat daftar subkategori yang sesuai
        self.subcategory_dropdown.bind("<<ComboboxSelected>>", self._on_subcategory_selected)
        self.subcategory_dropdown.config(state="disabled")

    def _add_subcategory_input(self, parent_frame):
        """
        Tambahkan input field dan tombol untuk menambah subkategori baru.
        """
        # Buat StringVar baru khusus untuk input subkategori
        self.new_subcategory_value = tk.StringVar()

        # Entry untuk subkategori baru dengan validasi input
        self.new_subcategory_entry = ttk.Entry(parent_frame, textvariable=self.new_subcategory_value, font=("Arial", 10))
        self.new_subcategory_entry.pack(fill=tk.X, pady=(10, 0))
        self.new_subcategory_entry.bind("<Return>", lambda event: self._add_subcategory())

        # Bind event untuk mengganti spasi dengan underscore secara otomatis
        def on_key_release(event):
            current_value = self.new_subcategory_value.get()

            if event.keysym not in ['BackSpace', 'Delete']:
                # Filter karakter yang diizinkan (huruf, angka, underscore, dan spasi)
                filtered_value = ''.join(char for char in current_value if char.isalnum() or char == '_' or char == ' ')

                # Ganti spasi dengan underscore
                updated_value = filtered_value.replace(" ", "_")

                self.new_subcategory_value.set(updated_value)

        self.new_subcategory_entry.bind("<KeyRelease>", on_key_release)  # Bind event key release

        # Tombol untuk menambah subkategori baru
        self.add_subcategory_button = ttk.Button(parent_frame, text="Tambah", command=self._add_subcategory)
        self.add_subcategory_button.pack(fill=tk.X, pady=(10, 0))
        self.add_subcategory_button.config(state="disabled")
        self.new_subcategory_entry.config(state="disabled")

    def _on_subcategory_selected(self, event):
        """
        Event handler untuk pemilihan subkategori.
        """
        selected_category = self.category_value.get()  # Dapatkan kategori yang dipilih
        selected_subcategory = self.subcategory_value.get()  # Dapatkan subkategori yang dipilih
        selected_subcategory = self.subcategory_value.get()  # Dapatkan subkategori yang dipilih
        self.main_window.update_value("sub_category", selected_subcategory)
        # Perbarui status bar dengan kategori dan subkategori yang dipilih
        self.main_window.update_status(f"Kategori dipilih: {selected_category}\\{selected_subcategory}")
        print(f"Selected Subcategory: {selected_subcategory}")  # Cetak subkategori yang dipilih ke konsol

    def _reset(self):
        """
        Reset semua nilai ke keadaan awal.
        """
        self.category_value.set("")
        self.new_category_value.set("")
        self.subcategory_value.set("")
        self.new_subcategory_value.set("")
        self.reset_button.config(state=tk.DISABLED)
        self.main_window.update_value("category", "")
        self.main_window.update_value("sub_category", "")
        self.main_window.update_status(f"Silakan pilih kategori.")

        # Reset dropdown kategori jika diperlukan (pertimbangkan logika berdasarkan implementasi)
        self.category_dropdown["values"] = self.categories

        # Reset dropdown subkategori jika diperlukan (pertimbangkan logika berdasarkan implementasi)
        self.subcategory_dropdown["values"] = ["Pilih kategori dulu"]

        # Cetak pesan untuk konfirmasi (opsional)
        print("Semua nilai kategori telah direset.")

    def check_for_updates(self):
        """
        Periksa pembaruan di Category.txt dan muat ulang kategori jika dimodifikasi.
        """
        try:
            current_modified_time = os.path.getmtime(self.category_file_path)
            if current_modified_time != self.last_modified_time:
                self.last_modified_time = current_modified_time
                self._load_categories()
                self.category_dropdown["values"] = self.categories
                self.category_value.set("")  # Reset kategori yang dipilih
                self.subcategory_dropdown["values"] = ["Pilih kategori dulu"]  # Reset dropdown subkategori
                self.subcategory_value.set("")  # Reset subkategori yang dipilih
        except FileNotFoundError:
            messagebox.showwarning("Gawat...!", "Waduh databasenya belum ada! (o_O)")
            messagebox.showinfo("Hehehe...", "Tenang jangan panik, aku buatin dulu nih")
            self.create_csv_if_not_exists()
            messagebox.showinfo("Tolong diingat...!", "Database dapat berisi file penting seperti Daftar Pustaka, Template dan Daftar Kategori!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

        # Periksa pembaruan di file subkategori yang dipilih jika ada
        if self.selected_subcategory_file_path:
            try:
                current_subcategory_modified_time = os.path.getmtime(self.selected_subcategory_file_path)
                if current_subcategory_modified_time != self.last_subcategory_modified_time:
                    self.last_subcategory_modified_time = current_subcategory_modified_time
                    self._on_category_selected(None)  # Muat ulang subkategori
            except FileNotFoundError:
                # Jika file dihapus, reset dropdown subkategori
                self.subcategory_dropdown["values"] = ["Pilih kategori dulu"]
                self.subcategory_value.set("")
            except Exception as e:
                messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

        # Jadwalkan pemeriksaan berikutnya
        self.after(1000, self.check_for_updates)

    def create_csv_if_not_exists(self):
        """
        Buat Category.txt jika tidak ada.
        """
        if not os.path.exists(self.category_file_path):
            with open(self.category_file_path, "w") as file:
                pass

    def _update_subcategory_state(self, *args):
        """
        Update state of subcategory input, dropdown, and button based on category selection.
        """
        if self.category_value.get():
            self.subcategory_dropdown.config(state="readonly")
            self.new_subcategory_entry.config(state="normal")
            self.add_subcategory_button.config(state="normal")
        else:
            self.subcategory_dropdown.config(state="disabled")
            self.new_subcategory_entry.config(state="disabled")
            self.add_subcategory_button.config(state="disabled")