class Kue:
    def __init__(self, nama, jenis, harga, stok):
        self.nama = nama
        self.jenis = jenis
        self.harga = harga
        self.stok = stok

class ManajemenTokoKue:
    def __init__(self):
        self.kue = []
        self.antrian_pesanan = []

    def tambah_kue(self, kue):
        self.kue.append(kue)

    def lihat_kue(self):
        for idx, kue in enumerate(self.kue):
            print(f"{idx + 1}. {kue.nama} ({kue.jenis}) - Harga: {kue.harga}, Stok: {kue.stok}")

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

    def tambah_pesanan_ke_antrian(self, pesanan):
        self.antrian_pesanan.append(pesanan)
        print(f"Pesanan untuk {pesanan.nama} ditambahkan ke dalam antrian.")

    def proses_antrian_pesanan(self):
        if self.antrian_pesanan:
            pesanan = self.antrian_pesanan.pop(0)
            print(f"Pesanan untuk {pesanan.nama} telah diproses dan dihapus dari antrian.")
            return pesanan
        else:
            print("Tidak ada pesanan dalam antrian.")

def impor_kue_dari_csv(nama_file):
    sistem_kue = ManajemenTokoKue()
    with open(nama_file, 'r') as file:
        next(file)  # Lewati baris header
        for line in file:
            nama, jenis, harga, stok = line.strip().split(',')
            kue = Kue(nama, jenis, float(harga), int(stok))
            sistem_kue.tambah_kue(kue)
    return sistem_kue

def ekspor_kue_ke_csv(nama_file, sistem_kue):
    with open(nama_file, 'w') as file:
        file.write('Nama Kue,Jenis Kue,Harga,Stok\n')
        for kue in sistem_kue.kue:
            file.write(f"{kue.nama},{kue.jenis},{kue.harga},{kue.stok}\n")

class Pesanan:
    def __init__(self, nama, jumlah):
        self.nama = nama
        self.jumlah = jumlah

def main():
    # Inisialisasi sistem manajemen toko kue
    nama_file_csv = 'manajementokokue.csv'
    sistem_kue = impor_kue_dari_csv(nama_file_csv)

    # Tampilkan menu
    print("Selamat datang di Sistem Manajemen Toko Kue")
    while True:
        print("\nMenu:")
        print("1. Lihat Kue")
        print("2. Perbarui Stok Kue")
        print("3. Hapus Kue")
        print("4. Tambah Pesanan")
        print("5. Proses Antrian Pesanan")
        print("6. Keluar")

        pilihan = input("Masukkan pilihan Anda: ")

        if pilihan == '1':
            print("\nDaftar Kue:")
            sistem_kue.lihat_kue()

        elif pilihan == '2':
            nama = input("Masukkan nama kue: ")
            stok_baru = int(input("Masukkan stok baru: "))
            sistem_kue.perbarui_stok_kue(nama, stok_baru)

        elif pilihan == '3':
            nama = input("Masukkan nama kue untuk dihapus: ")
            sistem_kue.hapus_kue(nama)

        elif pilihan == '4':
            nama = input("Masukkan nama kue untuk dipesan: ")
            jumlah = int(input("Masukkan jumlah: "))
            pesanan = Pesanan(nama, jumlah)
            sistem_kue.tambah_pesanan_ke_antrian(pesanan)

        elif pilihan == '5':
            pesanan = sistem_kue.proses_antrian_pesanan()
            if pesanan:
                print(f"Memproses pesanan: {pesanan.nama} x{pesanan.jumlah}")

        elif pilihan == '6':
            ekspor_kue_ke_csv('D:/KULEAH/SEMESTER 2/SDA/manajementokokue/managementokokue.csv', sistem_kue)
            print("Terima kasih telah menggunakan Sistem Manajemen Toko Kue.")
            break

        else:
            print("Pilihan tidak valid. Silakan masukkan opsi yang benar.")

if __name__ == "__main__":
    main()