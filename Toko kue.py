class Kue:
  def __init__(self, nama, harga, rasa, stok):
    self.nama = nama
    self.harga = harga
    self.rasa = rasa
    self.stok = stok

class TokoKue:
  def __init__(self, nama_toko):
    self.nama_toko = nama_toko
    self.daftar_kue = []

  def tambah_kue(self, kue):
    self.daftar_kue.append(kue)

  def hapus_kue(self, nama_kue):
    for kue in self.daftar_kue:
      if kue.nama == nama_kue:
        self.daftar_kue.remove(kue)
        break

  def ubah_stok(self, nama_kue, stok_baru):
    for kue in self.daftar_kue:
      if kue.nama == nama_kue:
        kue.stok = stok_baru
        break

  def tampilkan_daftar_kue(self):
    print("Daftar Kue:")
    for kue in self.daftar_kue:
      print(f"- {kue.nama} (Rasa: {kue.rasa}, Harga: {kue.harga}, Stok: {kue.stok})")

  def jual_kue(self, nama_kue, jumlah):
    for kue in self.daftar_kue:
      if kue.nama == nama_kue:
        if kue.stok >= jumlah:
          kue.stok -= jumlah
          total_harga = jumlah * kue.harga
          print(f"Kue {kue.nama} ({jumlah} buah) terjual dengan total harga Rp{total_harga:,}")
          return True
        else:
          print(f"Maaf, stok kue {kue.nama} tidak cukup. Stok tersedia: {kue.stok}")
          return False