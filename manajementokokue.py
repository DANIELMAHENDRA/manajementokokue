import tkinter as tk
from tkinter import messagebox, ttk
import csv

# Baca data dari CSV
def readData():
    arr = []
    with open("datakue.csv", "r") as filename:
        csvfile = csv.reader(filename)
        next(csvfile)
        for row in csvfile:
            arr.append(row)
    return arr

# Kelas Kue dengan atribut dasar
class Kue:
    def __init__(self, nama, jenis, harga, stok):
        self.nama = nama
        self.jenis = jenis
        self.harga = harga
        self.stok = stok
    
    def tolist(self):
        return [self.nama, self.jenis, self.harga, self.stok]

# Node untuk Linked List
class Node:
    def __init__(self, kue):
        self.kue = kue
        self.next = None

# Linked List untuk mengurutkan kue berdasarkan harga
class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, kue):
        new_node = Node(kue)
        if self.head is None or self.head.kue.harga >= new_node.kue.harga:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            while current.next is not None and current.next.kue.harga < new_node.kue.harga:
                current = current.next
            new_node.next = current.next
            current.next = new_node

    def to_list(self):
        result = []
        current = self.head
        while current is not None:
            result.append(current.kue)
            current = current.next
        return result

# Kelas untuk Manajemen Toko Kue
class ManajemenTokoKue:
    def __init__(self):
        self.kue = []  # Array/List untuk menyimpan kue
        arr = readData()
        for i in arr:
            self.kue.append(Kue(i[0], i[1], int(i[2]), int(i[3])))
        self.antrian_pesanan = []  # List untuk antrian pesanan
        
    def updateFileCsv(self):
        with open("datakue.csv", "w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Nama Kue", "Jenis", "Harga", "Stok"])  # Add header row
            for i in self.kue:
                writer.writerow(i.tolist())
                
    def tambah_kue(self, kue):
        self.kue.append(kue)
        self.updateFileCsv()

    # Sorting Quick Sort
    def quick_sort(self, low, high):
        if low < high:
            pi = self.partition(low, high)
            self.quick_sort(low, pi - 1)
            self.quick_sort(pi + 1, high)

    def partition(self, low, high):
        pivot = self.kue[high].nama.lower()
        i = low - 1
        for j in range(low, high):
            if self.kue[j].nama.lower() < pivot:
                i += 1
                self.kue[i], self.kue[j] = self.kue[j], self.kue[i]
        self.kue[i + 1], self.kue[high] = self.kue[high], self.kue[i + 1]
        return i + 1

    def urutkan_kue_berdasarkan_nama(self):
        self.quick_sort(0, len(self.kue) - 1)

    # Sorting menggunakan Linked List berdasarkan harga
    def urutkan_kue_berdasarkan_harga(self):
        ll = LinkedList()
        for kue in self.kue:
            ll.append(kue)
        self.kue = ll.to_list()

    def lihat_kue(self):
        for kue in self.kue:
            print(f"Nama Kue: {kue.nama}, Jenis Kue: {kue.jenis}, Harga Kue: {kue.harga}, Stok: {kue.stok}")

    def cari_kue_dengan_nama(self, nama):
        for kue in self.kue:
            if kue.nama.lower() == nama.lower():
                return kue
        return None

    def hapus_kue(self, nama):
        kue = self.cari_kue_dengan_nama(nama)
        if kue:
            self.kue.remove(kue)
            self.updateFileCsv()
            print(f"Kue '{nama}' telah dihapus.")
        else:
            print(f"Kue '{nama}' tidak ditemukan.")

    def update_kue(self, nama, nama_baru=None, jenis_baru=None, harga_baru=None, stok_tambah=None):
        kue = self.cari_kue_dengan_nama(nama)
        if kue:
            if nama_baru:
                kue.nama = nama_baru
            if jenis_baru:
                kue.jenis = jenis_baru
            if harga_baru:
                kue.harga = harga_baru
            if stok_tambah is not None:
                kue.stok += stok_tambah
            self.updateFileCsv()
            print(f"Detail kue '{nama}' telah diperbarui.")
        else:
            print(f"Kue '{nama}' tidak ditemukan.")

    def tambah_pesanan_ke_antrian(self, pesanan):
        self.antrian_pesanan.append(pesanan)
        print(f"Pesanan untuk {pesanan.nama} ditambahkan ke dalam antrian.")

    #queue
    def proses_antrian_pesanan(self, nama_kue, status_pesanan):
        for pesanan in self.antrian_pesanan:
            if pesanan.nama.lower() == nama_kue.lower():
                if status_pesanan.lower() == 'selesai':
                    kue = self.cari_kue_dengan_nama(nama_kue)
                    if kue and kue.stok >= pesanan.jumlah:
                        kue.stok -= pesanan.jumlah
                        self.antrian_pesanan.remove(pesanan)
                        self.updateFileCsv()
                        print(f"Pesanan untuk {pesanan.nama} telah diproses dan dihapus dari antrian.")
                    else:
                        print(f"Stok untuk {nama_kue} tidak cukup untuk diproses.")
                    return
                else:
                    print("Status pemesanan tidak valid.")
                    return
        print(f"Pesanan untuk {nama_kue} tidak ditemukan dalam antrian.")

    def lihat_daftar_antrian(self):
        if not self.antrian_pesanan:
            print("Antrian pesanan kosong.")
        else:
            print("Daftar Antrian Pesanan:")
            for idx, pesanan in enumerate(self.antrian_pesanan):
                print(f"{idx + 1}. {pesanan.nama} - Jumlah: {pesanan.jumlah}")

    def hapus_antrian(self, nama_kue):
        for pesanan in self.antrian_pesanan:
            if pesanan.nama.lower() == nama_kue.lower():
                self.antrian_pesanan.remove(pesanan)
                print(f"Pesanan untuk {pesanan.nama} telah dihapus dari antrian.")
                return
        print(f"Pesanan untuk {nama_kue} tidak ditemukan dalam antrian.")

# Kelas Pesanan untuk mengelola pesanan kue
class Pesanan:
    def __init__(self, nama, jumlah):
        self.nama = nama
        self.jumlah = jumlah

# Fungsi untuk mengatur tampilan warna dan gaya
def apply_style(widget, bg_color, fg_color, font=("Arial", 12)):
    widget.configure(bg=bg_color, fg=fg_color, font=font)

# Fungsi untuk membuat dan menampilkan menu staff dalam Tkinter
def menu_staff(sistem_kue):
    root = tk.Tk()
    root.title("Menu Staff")
    root.geometry("800x600")
    root.configure(bg="#E0F7FA")  # Background color light blue

    # Frame untuk menu
    menu_frame = tk.Frame(root, bg="#E0F7FA")
    menu_frame.pack(pady=20)

    title_label = tk.Label(menu_frame, text="Menu Staff", font=("Arial", 16), bg="#E0F7FA")
    title_label.pack()

    # Buttons for the menu
    btn_tambah_kue = tk.Button(menu_frame, text="Tambah Kue", command=lambda: tambah_kue(sistem_kue), bg="#0288D1", fg="white", font=("Arial", 12), width=25)
    btn_tambah_kue.pack(pady=5)

    btn_lihat_kue = tk.Button(menu_frame, text="Lihat Kue", command=lambda: lihat_kue(sistem_kue), bg="#0288D1", fg="white", font=("Arial", 12), width=25)
    btn_lihat_kue.pack(pady=5)

    btn_hapus_kue = tk.Button(menu_frame, text="Hapus Kue", command=lambda: hapus_kue(sistem_kue), bg="#0288D1", fg="white", font=("Arial", 12), width=25)
    btn_hapus_kue.pack(pady=5)

    btn_cari_kue = tk.Button(menu_frame, text="Cari Kue", command=lambda: cari_kue(sistem_kue), bg="#0288D1", fg="white", font=("Arial", 12), width=25)
    btn_cari_kue.pack(pady=5)

    btn_tambah_pesanan = tk.Button(menu_frame, text="Tambah Pesanan ke Antrian", command=lambda: tambah_pesanan(sistem_kue), bg="#0288D1", fg="white", font=("Arial", 12), width=25)
    btn_tambah_pesanan.pack(pady=5)

    btn_lihat_daftar_antrian = tk.Button(menu_frame, text="Lihat Daftar Antrian", command=lambda: lihat_daftar_antrian(sistem_kue), bg="#0288D1", fg="white", font=("Arial", 12), width=25)
    btn_lihat_daftar_antrian.pack(pady=5)

    btn_proses_antrian_pesanan = tk.Button(menu_frame, text="Proses Antrian Pesanan", command=lambda: proses_antrian_pesanan(sistem_kue), bg="#0288D1", fg="white", font=("Arial", 12), width=25)
    btn_proses_antrian_pesanan.pack(pady=5)

    btn_hapus_antrian = tk.Button(menu_frame, text="Hapus Antrian", command=lambda: hapus_antrian(sistem_kue), bg="#0288D1", fg="white", font=("Arial", 12), width=25)
    btn_hapus_antrian.pack(pady=5)

    btn_urutkan_kue_nama = tk.Button(menu_frame, text="Urutkan Kue Berdasarkan Nama", command=lambda: urutkan_kue_berdasarkan_nama(sistem_kue), bg="#0288D1", fg="white", font=("Arial", 12), width=25)
    btn_urutkan_kue_nama.pack(pady=5)

    btn_urutkan_kue_harga = tk.Button(menu_frame, text="Urutkan Kue Berdasarkan Harga", command=lambda: urutkan_kue_berdasarkan_harga(sistem_kue), bg="#0288D1", fg="white", font=("Arial", 12), width=25)
    btn_urutkan_kue_harga.pack(pady=5)

    btn_update_kue = tk.Button(menu_frame, text="Update Kue", command=lambda: update_kue(sistem_kue), bg="#0288D1", fg="white", font=("Arial", 12), width=25)
    btn_update_kue.pack(pady=5)

    btn_keluar = tk.Button(menu_frame, text="Keluar", command=root.destroy, bg="#0288D1", fg="white", font=("Arial", 12), width=25)
    btn_keluar.pack(pady=5)

    root.mainloop()

# Fungsi untuk menambah kue
def tambah_kue(sistem_kue):
    def simpan_kue():
        nama = entry_nama.get()
        jenis = entry_jenis.get()
        harga = int(entry_harga.get())
        stok = int(entry_stok.get())
        kue_baru = Kue(nama, jenis, harga, stok)
        sistem_kue.tambah_kue(kue_baru)
        messagebox.showinfo("Info", "Kue berhasil ditambahkan.")
        tambah_kue_win.destroy()

    tambah_kue_win = tk.Toplevel()
    tambah_kue_win.title("Tambah Kue")
    tambah_kue_win.geometry("400x300")
    tambah_kue_win.configure(bg="#E0F7FA")

    tk.Label(tambah_kue_win, text="Nama Kue:", bg="#E0F7FA").pack(pady=5)
    entry_nama = tk.Entry(tambah_kue_win)
    entry_nama.pack(pady=5)

    tk.Label(tambah_kue_win, text="Jenis Kue:", bg="#E0F7FA").pack(pady=5)
    entry_jenis = tk.Entry(tambah_kue_win)
    entry_jenis.pack(pady=5)

    tk.Label(tambah_kue_win, text="Harga Kue:", bg="#E0F7FA").pack(pady=5)
    entry_harga = tk.Entry(tambah_kue_win)
    entry_harga.pack(pady=5)

    tk.Label(tambah_kue_win, text="Stok Kue:", bg="#E0F7FA").pack(pady=5)
    entry_stok = tk.Entry(tambah_kue_win)
    entry_stok.pack(pady=5)

    tk.Button(tambah_kue_win, text="Simpan", command=simpan_kue, bg="#0288D1", fg="white").pack(pady=20)

# Fungsi untuk melihat kue
def lihat_kue(sistem_kue):
    lihat_kue_win = tk.Toplevel()
    lihat_kue_win.title("Daftar Kue")
    lihat_kue_win.geometry("600x400")
    lihat_kue_win.configure(bg="#E0F7FA")

    tree = ttk.Treeview(lihat_kue_win, columns=("Nama", "Jenis", "Harga", "Stok"), show="headings")
    tree.heading("Nama", text="Nama")
    tree.heading("Jenis", text="Jenis")
    tree.heading("Harga", text="Harga")
    tree.heading("Stok", text="Stok")
    tree.pack(fill=tk.BOTH, expand=True)

    for kue in sistem_kue.kue:
        tree.insert("", tk.END, values=(kue.nama, kue.jenis, kue.harga, kue.stok))

# Fungsi untuk menghapus kue
def hapus_kue(sistem_kue):
    def hapus():
        nama = entry_nama.get()
        sistem_kue.hapus_kue(nama)
        messagebox.showinfo("Info", f"Kue '{nama}' telah dihapus.")
        hapus_kue_win.destroy()

    hapus_kue_win = tk.Toplevel()
    hapus_kue_win.title("Hapus Kue")
    hapus_kue_win.geometry("300x200")
    hapus_kue_win.configure(bg="#E0F7FA")

    tk.Label(hapus_kue_win, text="Nama Kue yang akan dihapus:", bg="#E0F7FA").pack(pady=10)
    entry_nama = tk.Entry(hapus_kue_win)
    entry_nama.pack(pady=10)
    tk.Button(hapus_kue_win, text="Hapus", command=hapus, bg="#0288D1", fg="white").pack(pady=10)

# Fungsi untuk mencari kue
def cari_kue(sistem_kue):
    def cari():
        nama = entry_nama.get()
        kue = sistem_kue.cari_kue_dengan_nama(nama)
        if kue:
            result_label.config(text=f"Nama: {kue.nama}, Jenis: {kue.jenis}, Harga: {kue.harga}, Stok: {kue.stok}")
        else:
            result_label.config(text=f"Kue '{nama}' tidak ditemukan.")

    cari_kue_win = tk.Toplevel()
    cari_kue_win.title("Cari Kue")
    cari_kue_win.geometry("400x300")
    cari_kue_win.configure(bg="#E0F7FA")

    tk.Label(cari_kue_win, text="Nama Kue yang dicari:", bg="#E0F7FA").pack(pady=10)
    entry_nama = tk.Entry(cari_kue_win)
    entry_nama.pack(pady=10)
    tk.Button(cari_kue_win, text="Cari", command=cari, bg="#0288D1", fg="white").pack(pady=10)
    result_label = tk.Label(cari_kue_win, text="", bg="#E0F7FA")
    result_label.pack(pady=10)

# Fungsi untuk mengupdate kue
def update_kue(sistem_kue):
    def update():
        nama = entry_nama.get()
        nama_baru = entry_nama_baru.get()
        jenis_baru = entry_jenis_baru.get()
        harga_baru = int(entry_harga_baru.get()) if entry_harga_baru.get() else None
        stok_tambah = int(entry_stok_tambah.get()) if entry_stok_tambah.get() else None
        sistem_kue.update_kue(nama, nama_baru, jenis_baru, harga_baru, stok_tambah)
        messagebox.showinfo("Info", f"Kue '{nama}' telah diperbarui.")
        update_kue_win.destroy()

    update_kue_win = tk.Toplevel()
    update_kue_win.title("Update Kue")
    update_kue_win.geometry("400x400")
    update_kue_win.configure(bg="#E0F7FA")

    tk.Label(update_kue_win, text="Nama Kue yang akan diupdate:", bg="#E0F7FA").pack(pady=5)
    entry_nama = tk.Entry(update_kue_win)
    entry_nama.pack(pady=5)

    tk.Label(update_kue_win, text="Nama Baru:", bg="#E0F7FA").pack(pady=5)
    entry_nama_baru = tk.Entry(update_kue_win)
    entry_nama_baru.pack(pady=5)

    tk.Label(update_kue_win, text="Jenis Baru:", bg="#E0F7FA").pack(pady=5)
    entry_jenis_baru = tk.Entry(update_kue_win)
    entry_jenis_baru.pack(pady=5)

    tk.Label(update_kue_win, text="Harga Baru:", bg="#E0F7FA").pack(pady=5)
    entry_harga_baru = tk.Entry(update_kue_win)
    entry_harga_baru.pack(pady=5)

    tk.Label(update_kue_win, text="Tambah Stok:", bg="#E0F7FA").pack(pady=5)
    entry_stok_tambah = tk.Entry(update_kue_win)
    entry_stok_tambah.pack(pady=5)

    tk.Button(update_kue_win, text="Update", command=update, bg="#0288D1", fg="white").pack(pady=20)

# Fungsi untuk mengurutkan kue berdasarkan nama
def urutkan_kue_berdasarkan_nama(sistem_kue):
        sistem_kue.urutkan_kue_berdasarkan_nama()
        lihat_kue(sistem_kue)

# Fungsi untuk mengurutkan kue berdasarkan harga
def urutkan_kue_berdasarkan_harga(sistem_kue):
        sistem_kue.urutkan_kue_berdasarkan_harga()
        lihat_kue(sistem_kue)

# Fungsi untuk menambah pesanan
def tambah_pesanan(sistem_kue):
    def simpan_pesanan():
        nama = entry_nama.get()
        jumlah = int(entry_jumlah.get())
        pesanan_baru = Pesanan(nama, jumlah)
        sistem_kue.tambah_pesanan_ke_antrian(pesanan_baru)
        messagebox.showinfo("Info", "Pesanan berhasil ditambahkan ke antrian.")
        tambah_pesanan_win.destroy()

    tambah_pesanan_win = tk.Toplevel()
    tambah_pesanan_win.title("Tambah Pesanan")
    tambah_pesanan_win.geometry("400x300")
    tambah_pesanan_win.configure(bg="#E0F7FA")

    tk.Label(tambah_pesanan_win, text="Nama Kue:", bg="#E0F7FA").pack(pady=5)
    entry_nama = tk.Entry(tambah_pesanan_win)
    entry_nama.pack(pady=5)

    tk.Label(tambah_pesanan_win, text="Jumlah:", bg="#E0F7FA").pack(pady=5)
    entry_jumlah = tk.Entry(tambah_pesanan_win)
    entry_jumlah.pack(pady=5)

    tk.Button(tambah_pesanan_win, text="Simpan", command=simpan_pesanan, bg="#0288D1", fg="white").pack(pady=20)

# Fungsi untuk melihat antrian pesanan
def lihat_daftar_antrian(sistem_kue):
    lihat_antrian_win = tk.Toplevel()
    lihat_antrian_win.title("Antrian Pesanan")
    lihat_antrian_win.geometry("600x400")
    lihat_antrian_win.configure(bg="#E0F7FA")

    tree = ttk.Treeview(lihat_antrian_win, columns=("Nama", "Jumlah"), show="headings")
    tree.heading("Nama", text="Nama")
    tree.heading("Jumlah", text="Jumlah")
    tree.pack(fill=tk.BOTH, expand=True)

    for pesanan in sistem_kue.antrian_pesanan:
        tree.insert("", tk.END, values=(pesanan.nama, pesanan.jumlah))

# Fungsi untuk memproses antrian pesanan
def proses_antrian_pesanan(sistem_kue):
    def proses():
        nama_kue = entry_nama.get()
        status_pesanan = entry_status.get()
        sistem_kue.proses_antrian_pesanan(nama_kue, status_pesanan)
        messagebox.showinfo("Info", f"Pesanan untuk '{nama_kue}' dengan status '{status_pesanan}' telah diproses.")
        proses_antrian_win.destroy()

    proses_antrian_win = tk.Toplevel()
    proses_antrian_win.title("Proses Antrian")
    proses_antrian_win.geometry("400x300")
    proses_antrian_win.configure(bg="#E0F7FA")

    tk.Label(proses_antrian_win, text="Nama Kue:", bg="#E0F7FA").pack(pady=5)
    entry_nama = tk.Entry(proses_antrian_win)
    entry_nama.pack(pady=5)

    tk.Label(proses_antrian_win, text="Status Pesanan (selesai/batal):", bg="#E0F7FA").pack(pady=5)
    entry_status = tk.Entry(proses_antrian_win)
    entry_status.pack(pady=5)

    tk.Button(proses_antrian_win, text="Proses", command=proses, bg="#0288D1", fg="white").pack(pady=20)

# Fungsi untuk menghapus pesanan dari antrian
def hapus_antrian(sistem_kue):
    def hapus():
        nama_kue = entry_nama.get()
        sistem_kue.hapus_antrian(nama_kue)
        messagebox.showinfo("Info", f"Pesanan untuk '{nama_kue}' telah dihapus dari antrian.")
        hapus_antrian_win.destroy()

    hapus_antrian_win = tk.Toplevel()
    hapus_antrian_win.title("Hapus Antrian")
    hapus_antrian_win.geometry("400x300")
    hapus_antrian_win.configure(bg="#E0F7FA")

    tk.Label(hapus_antrian_win, text="Nama Kue:", bg="#E0F7FA").pack(pady=5)
    entry_nama = tk.Entry(hapus_antrian_win)
    entry_nama.pack(pady=5)

    tk.Button(hapus_antrian_win, text="Hapus", command=hapus, bg="#0288D1", fg="white").pack(pady=20)

# Contoh inisialisasi sistem dan menjalankan menu
sistem_kue = ManajemenTokoKue()
menu_staff(sistem_kue)
