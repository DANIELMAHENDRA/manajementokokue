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
        self.kue = sorted(self.kue, key=lambda x: x.nama.lower())  # Sort by name

    def lihat_kue(self):
        for idx, kue in enumerate(self.kue):
            print(f"{idx + 1}. {kue.nama} ({kue.jenis}) - Harga: {kue.harga}, Stok: {kue.stok}")

    def cari_kue_dengan_nama(self, nama):
        # Binary search for efficiency
        low = 0
        high = len(self.kue) - 1
        while low <= high:
            mid = (low + high) // 2
            if self.kue[mid].nama.lower() == nama.lower():
                return self.kue[mid]
            elif self.kue[mid].nama.lower() < nama.lower():
                low = mid + 1
            else:
                high = mid - 1
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
        kue = self.cari_kue_dengan_nama(pesanan.nama)
        if kue:
            if kue.stok >= pesanan.jumlah:
                self.antrian_pesanan.append(pesanan)
                print(f"Pesanan untuk {pesanan.nama} ditambahkan ke dalam antrian.")
            else:
                print(f"Stok untuk {pesanan.nama} tidak cukup.")
        else:
            print(f"Kue '{pesanan.nama}' tidak ditemukan.")

    def proses_antrian_pesanan(self):
        if self.antrian_pesanan:
            pesanan = self.antrian_pesanan.pop(0)
            kue = self.cari_kue_dengan_nama(pesanan.nama)
            if kue and kue.stok >= pesanan.jumlah:
                kue.stok -= pesanan.jumlah
                print(f"Pesanan untuk {pesanan.nama} telah diproses dan dihapus dari antrian.")
                return pesanan
            else:
                print(f"Stok untuk {pesanan.nama} tidak cukup untuk diproses.")
        else:
            print("Tidak ada pesanan dalam antrian.")
        return None

class Pesanan:
    def __init__(self, nama, jumlah):
        self.nama = nama
        self.jumlah = jumlah

# Sistem Login dan Registrasi
class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

class UserManagement:
    def __init__(self):
        self.users = {}

    def register(self):
        print("Register Akun Baru")
        while True:
            username = input("Masukkan username: ")
            if username in self.users:
                print("Username sudah ada, silakan coba lagi.")
            else:
                password = input("Masukkan password: ")
                role = input("Pilih peran (staff/pengunjung): ").lower()
                if role == 'staff' or role == 'pengunjung':
                    self.users[username] = User(username, password, role)
                    print(f"Akun untuk {username} berhasil dibuat sebagai {role}.")
                    break
                else:
                    print("Peran tidak valid. Silakan pilih antara 'staff' atau 'pengunjung'.")

    def login(self):
        print("Login")
        username = input("Masukkan username: ")
        password = input("Masukkan password: ")
        if username in self.users and self.users[username].password == password:
            print(f"Login berhasil sebagai {self.users[username].role}.")
            return self.users[username].role
        else:
            print("Login gagal. Username atau password salah.")
            return None

def menu_staff(sistem_kue):
    while True:
        print("\nMenu Staff:")
        print("1. Tambah Kue")
        print("2. Lihat Kue")
        print("3. Perbarui Stok Kue")
        print("4. Hapus Kue")
        print("5. Hapus Data Pelanggan")
        print(". Keluar")

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
            

        elif pilihan == '6':
            break

        else:
            print("Pilihan tidak valid. Silakan masukkan opsi yang benar.")

def menu_pengunjung(sistem_kue):
    while True:
        print("\nMenu Pengunjung:")
        print("1. Lihat Kue")
        print("2. Buat Pesanan")
        print("3. Proses Antrian Pesanan")
        print("4. Keluar")

        pilihan = input("Masukkan pilihan Anda: ")

        if pilihan == '1':
            print("\nDaftar Kue:")
            sistem_kue.lihat_kue()

        elif pilihan == '2':
            nama = input("Masukkan nama kue untuk dipesan: ")
            jumlah = int(input("Masukkan jumlah: "))
            pesanan = Pesanan(nama, jumlah)
            konfirmasi = input("Apakah Anda ingin melanjutkan memesan? (y/n): ").lower()
            if konfirmasi == 'y':
                sistem_kue.tambah_pesanan_ke_antrian(pesanan)
                print("Pesanan berhasil ditambahkan.")
            elif konfirmasi == 'n':
                print("Pesanan dibatalkan.")
            else:
                print("Opsi tidak valid, kembali ke menu.")

        elif pilihan == '3':
            pesanan = sistem_kue.proses_antrian_pesanan()
            if pesanan:
                print(f"Memproses pesanan: {pesanan.nama} x{pesanan.jumlah}")

        elif pilihan == '4':
            break

        else:
            print("Pilihan tidak valid. Silakan masukkan opsi yang benar.")

def main():
    # Inisialisasi sistem manajemen toko kue
    sistem_kue = ManajemenTokoKue()

    # Tambahkan beberapa kue ke dalam sistem
    sistem_kue.tambah_kue(Kue("Kue Keju", "Keju", 15000, 10))
    sistem_kue.tambah_kue(Kue("Kue Coklat", "Coklat", 12000, 15))
    sistem_kue.tambah_kue(Kue("Kue Strawberry", "Strawberry", 20000, 5))

    # Inisialisasi manajemen pengguna
    user_management = UserManagement()

    while True:
        print("\nMain Menu:")
        print("1. Login")
        print("2. Register")
        print("3. Exit")

        pilihan = input("Masukkan pilihan Anda: ")

        if pilihan == '1':
            user_type = user_management.login()
            if user_type:
                if user_type == "staff":
                    menu_staff(sistem_kue)
                else:
                    menu_pengunjung(sistem_kue)
        elif pilihan == '2':
            user_management.register()
        elif pilihan == '3':
            break
        else:
            print("Pilihan tidak valid. Silakan masukkan opsi yang benar.")

if __name__ == "__main__":
    main()
