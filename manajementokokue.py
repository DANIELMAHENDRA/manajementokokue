import csv

def readData():    
    arr = []
    with open("datakue.csv","r") as filename:
        csvfile =csv.reader(filename)
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

# Kelas untuk Manajemen Toko Kue
class ManajemenTokoKue:
    def __init__(self):
        self.kue = []  # Array/List untuk menyimpan kue
        arr = readData()
        for i in arr:
            self.kue.append(Kue(i[0], i[1], i[2], i[3]))
        self.antrian_pesanan = []  # Stack untuk antrian pesanan
        
    def updateFileCsv(self):
        with open("datakue.csv", "w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Nama Kue","jenis" ,"Harga","Stock"])  # Add header row
            for i in self.kue:
                writer.writerow(i.tolist())
                
    def tambah_kue(self, kue):
        self.kue.append(kue)
        self.updateFileCsv()
        # self.urutkan_kue_berdasarkan_nama()  # Sorting kue berdasarkan nama

    def urutkan_kue_berdasarkan_nama(self):
        for i in range(len(self.kue) - 1):
            for j in range(len(self.kue) - 1 - i):
                if self.kue[j].nama.lower() > self.kue[j + 1].nama.lower():
                    self.kue[j], self.kue[j + 1] = self.kue[j + 1], self.kue[j]

    def lihat_kue(self):
        # for idx, kue in enumerate(self.kue):
        #     print(f"{idx + 1}. {kue.nama} ({kue.jenis}) - Harga: {kue.harga}, Stok: {kue.stok}")
        i = 1
        for kue in self.kue:
            print(i, ". Nama Kue : ", kue.nama, " , Jenis Kue : ", kue.jenis, " , Harga Kue : ", kue.harga, " , Stock : ", kue.stok)
            i += 1

    def cari_kue_dengan_nama(self, nama):
        for kue in self.kue:
            if kue.nama.lower() == nama.lower():
                return kue
        return None

    def perbarui_stok_kue(self, nama, stok_baru):
        kue = self.cari_kue_dengan_nama(nama)
        if kue:
            kue.stok = stok_baru
            print(f"Stok untuk {nama} telah diperbarui menjadi {stok_baru}.")
        else:
            print(f"Kue '{nama}' tidak ditemukan.")

    def hapus_kue(self, nama):
        kue = self.cari_kue_dengan_nama(nama)
        if kue:
            self.kue.remove(kue)
            print(f"Kue '{nama}' telah dihapus.")
        else:
            print(f"Kue '{nama}' tidak ditemukan.")

    def simpan_kue_ke_csv(self, datakue):
        with open(datakue, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Nama', 'Jenis', 'Harga', 'Stok'])
            for kue in self.kue:
                writer.writerow([kue.nama, kue.jenis, kue.harga, kue.stok])
        print(f"Data kue telah disimpan ke {datakue}.")

    def muat_kue_dari_csv(self, datakue):
        try:
            with open(datakue, 'r') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header
                self.kue = []
                for row in reader:
                    if row:
                        nama, jenis, harga, stok = row
                        self.kue.append(Kue(nama, jenis, int(harga), int(stok)))
            print(f"Data kue telah dimuat dari {datakue}.")
        except FileNotFoundError:
            print(f"File {datakue} tidak ditemukan. Mulai dengan data kue kosong.")

    # Fungsi untuk menambahkan pesanan ke stack
    def tambah_pesanan_ke_antrian(self, pesanan):
        self.antrian_pesanan.append(pesanan)
        print(f"Pesanan untuk {pesanan.nama} ditambahkan ke dalam antrian.")

    # Fungsi untuk memproses antrian pesanan dari stack
    def proses_antrian_pesanan(self):
        if self.antrian_pesanan:
            pesanan = self.antrian_pesanan.pop()
            kue = self.cari_kue_dengan_nama(pesanan.nama)
            if kue and kue.stok >= pesanan.jumlah:
                kue.stok -= pesanan.jumlah
                print(f"Pesanan untuk {pesanan.nama} telah diproses.")
                return pesanan
            else:
                print(f"Stok untuk {pesanan.nama} tidak cukup untuk diproses.")
        else:
            print("Tidak ada pesanan dalam antrian.")
        return None

# Kelas Pesanan untuk mengelola pesanan kue
class Pesanan:
    def __init__(self, nama, jumlah):
        self.nama = nama
        self.jumlah = jumlah

# Fungsi menu staff dengan opsi yang relevan
def menu_staff(sistem_kue):
    while True:
        print("\nMenu Staff:")
        print("1. Tambah Kue")
        print("2. Lihat Kue")
        print("3. Perbarui Stok Kue") #hapus
        print("4. Hapus Kue")
        print("5. Tambah Pesanan ke Antrian")
        print("6. Proses Antrian Pesanan")
        print("7. Keluar")

        pilihan = input("Masukkan pilihan Anda: ")

        if pilihan == '1':
            nama = input("Masukkan nama kue: ")
            jenis = input("Masukkan jenis kue: ")
            harga = int(input("Masukkan harga kue: "))
            stok = int(input("Masukkan stok kue: "))
            sistem_kue.tambah_kue(Kue(nama, jenis, harga, stok))

        elif pilihan == '2':
            print("\nDaftar Kue:")
            sistem_kue.lihat_kue()

        elif pilihan == '3':
            nama = input("Masukkan nama kue: ")
            stok_baru = int(input("Masukkan stok baru: "))
            sistem_kue.perbarui_stok_kue(nama, stok_baru)
        elif pilihan == '4':
            nama = input("Masukkan nama kue untuk dihapus: ")
            sistem_kue.hapus_kue(nama)
        elif pilihan == '5':
            nama = input("Masukkan nama kue untuk dipesan: ")
            jumlah = int(input("Masukkan jumlah: "))
            pesanan = Pesanan(nama, jumlah)
            sistem_kue.tambah_pesanan_ke_antrian(pesanan)
        elif pilihan == '6':
            sistem_kue.proses_antrian_pesanan()
        elif pilihan == '9':
            break
        else:
            print("Pilihan tidak valid. Silakan masukkan opsi yang benar.")

def main():
    # Inisialisasi sistem manajemen toko kue
    sistem_kue = ManajemenTokoKue()

    # # Muat data kue dari file CSV saat program dimulai
    # sistem_kue.muat_kue_dari_csv('File csv.csv')

    # Langsung masuk ke menu staff
    menu_staff(sistem_kue)

    # # Simpan data kue ke file CSV saat program selesai
    # sistem_kue.simpan_kue_ke_csv('File csv.csv')

if __name__ == "__main__":
    main()
