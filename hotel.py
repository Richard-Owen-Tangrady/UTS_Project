from abc import ABC, abstractmethod
from datetime import datetime, date

# CUSTOM EXCEPTION
class KamarTidakDitemukanError(Exception):
    pass

class ReservasiTidakDitemukanError(Exception):
    pass

class TamuTidakDitemukanError(Exception):
    pass


# 1. CLASS KAMAR
class Kamar:
    def __init__(self, nomor_kamar, tipe_kamar, harga_per_malam):
        if not isinstance(harga_per_malam, (int, float)) or harga_per_malam < 0:
            raise ValueError("Harga kamar harus berupa angka dan tidak boleh negatif!")
        if not str(nomor_kamar).strip() or not str(tipe_kamar).strip():
            raise ValueError("Nomor dan tipe kamar wajib diisi!")

        self.__nomor_kamar = str(nomor_kamar)
        self.__tipe_kamar = tipe_kamar
        self.__harga_per_malam = harga_per_malam
        self.__status = "Tersedia"

    def get_nomor_kamar(self):
        return self.__nomor_kamar

    def get_tipe_kamar(self):
        return self.__tipe_kamar

    def get_harga_per_malam(self):
        return self.__harga_per_malam

    def get_status(self):
        return self.__status

    def set_status(self, status_baru):
        if status_baru not in ["Tersedia", "Terisi", "Perbaikan"]:
            raise ValueError("Status kamar tidak valid!")

        self.__status = status_baru

    def get_info(self):
        return (
            f"Nomor Kamar: {self.__nomor_kamar}\n"
            f"Tipe Kamar: {self.__tipe_kamar}\n"
            f"Harga per Malam: Rp{self.__harga_per_malam}\n"
            f"Status: {self.__status}"
        )


# 2. CLASS TAMU
class Tamu:
    def __init__(self, id_tamu, nama, nomor_telepon):
        if not nama.strip():
            raise ValueError("Nama tidak boleh kosong!")
        if not nomor_telepon.strip():
            raise ValueError("Nomor telepon tidak boleh kosong!")

        self.__id_tamu = id_tamu
        self.__nama = nama.strip()
        self.__nomor_telepon = nomor_telepon.strip()

    def get_id_tamu(self):
        return self.__id_tamu

    def get_nama(self):
        return self.__nama

    def get_nomor_telepon(self):
        return self.__nomor_telepon

    def set_nama(self, nama_baru):
        if not nama_baru.strip():
            raise ValueError("Nama tidak boleh kosong!")

        self.__nama = nama_baru.strip()

    def set_nomor_telepon(self, nomor_telepon_baru):
        if not nomor_telepon_baru.strip():
            raise ValueError("Nomor telepon tidak boleh kosong!")

        self.__nomor_telepon = nomor_telepon_baru.strip()

    def get_info(self):
        return (
            f"ID Tamu: {self.__id_tamu}\n"
            f"Nama: {self.__nama}\n"
            f"Nomor Telepon: {self.__nomor_telepon}"
        )


# 3. CLASS KAMAR ITERATOR
class KamarIterator:
    def __init__(self, daftar_kamar):
        self.daftar_kamar = daftar_kamar
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.daftar_kamar):
            raise StopIteration

        kamar = self.daftar_kamar[self.index]
        self.index += 1

        return kamar


# 4. CLASS MANAJEMEN KAMAR  
class ManajemenKamar:
    def __init__(self):
        self.__daftar_kamar = []
        self.inisialisasi_kamar()

    def __iter__(self):
        return KamarIterator(self.__daftar_kamar)

    def inisialisasi_kamar(self):
        for nomor in range(101, 111):
            kamar = Kamar(str(nomor), "Standard", 500000)
            self.__daftar_kamar.append(kamar)

        for nomor in range(201, 211):
            kamar = Kamar(str(nomor), "Deluxe", 800000)
            self.__daftar_kamar.append(kamar)

        for nomor in range(301, 306):
            kamar = Kamar(str(nomor), "Suite", 1000000)
            self.__daftar_kamar.append(kamar)

    def tambah_kamar(self, kamar_baru):
        iterator = iter(self)

        while True:
            try:
                kamar = next(iterator)

                if kamar.get_nomor_kamar() == kamar_baru.get_nomor_kamar():
                    raise ValueError("Nomor kamar sudah digunakan!")

            except StopIteration:
                self.__daftar_kamar.append(kamar_baru)
                return "Kamar berhasil ditambahkan!"

    def cari_kamar(self, nomor_dicari):
        for kamar in self:
            if kamar.get_nomor_kamar() == nomor_dicari:
                return kamar

        return None

    def hapus_kamar(self, nomor_dihapus, manajemen_reservasi):
        kamar = self.cari_kamar(nomor_dihapus)

        if kamar is None:
            raise KamarTidakDitemukanError("Kamar tidak ditemukan!")
        if manajemen_reservasi.kamar_punya_reservasi_aktif(nomor_dihapus):
            raise ValueError("Kamar masih memiliki reservasi aktif dan tidak dapat dihapus!")

        self.__daftar_kamar.remove(kamar)
        return "Kamar berhasil dihapus!"

    def tampilkan_kamar(self):
        if not self.__daftar_kamar:
            return "Belum ada data kamar!"

        hasil = []

        for kamar in self:
            hasil.append(kamar.get_info())

        return "\n\n".join(hasil)

    def ubah_status_kamar(self, nomor_diubah):
        kamar = self.cari_kamar(nomor_diubah)

        if kamar is None:
            raise KamarTidakDitemukanError("Kamar tidak ditemukan!")

        if kamar.get_status() == "Terisi":
            raise ValueError("Status kamar yang sedang ditempati tidak dapat diubah!")

        if kamar.get_status() == "Tersedia":
            kamar.set_status("Perbaikan")
        else:
            kamar.set_status("Tersedia")

        return "Status kamar berhasil diubah!"

# 5. CLASS MANAJEMEN TAMU
class ManajemenTamu:
    def __init__(self):
        self.__daftar_tamu = []
        self.__nomor_id = 1

    def buat_id_tamu(self):
        id_tamu = f"T{self.__nomor_id:03d}"
        self.__nomor_id += 1

        return id_tamu

    def tambah_tamu(self, nama, nomor_telepon):
        if not nama.strip() or not nomor_telepon.strip():
            raise ValueError("Nama dan nomor telepon wajib diisi!")

        tamu = Tamu(self.buat_id_tamu(), nama, nomor_telepon)
        self.__daftar_tamu.append(tamu)

        return f"Tamu berhasil ditambahkan dengan ID {tamu.get_id_tamu()}!"

    def cari_tamu(self, id_dicari):
        for tamu in self.__daftar_tamu:
            if tamu.get_id_tamu() == id_dicari:
                return tamu

        return None

    def hapus_tamu(self, id_dihapus, manajemen_reservasi):
        tamu = self.cari_tamu(id_dihapus)

        if tamu is None:
            raise TamuTidakDitemukanError("Tamu tidak ditemukan!")
        if manajemen_reservasi.tamu_punya_reservasi_aktif(id_dihapus):
            raise ValueError("Tamu masih memiliki reservasi aktif dan tidak dapat dihapus!")

        self.__daftar_tamu.remove(tamu)
        return "Data tamu berhasil dihapus!"

    def tampilkan_tamu(self):
        if not self.__daftar_tamu:
            return "Belum ada data tamu!"

        hasil = []

        for tamu in self.__daftar_tamu:
            hasil.append(tamu.get_info())

        return "\n\n".join(hasil)

    def ubah_data_tamu(self, id_diubah, nama_baru, nomor_telepon_baru):
        tamu = self.cari_tamu(id_diubah)

        if tamu is None:
            raise TamuTidakDitemukanError("Tamu tidak ditemukan!")

        # Validasi kedua input sebelum mengubah salah satu atribut.
        if not nama_baru.strip():
            raise ValueError("Nama tidak boleh kosong!")
        if not nomor_telepon_baru.strip():
            raise ValueError("Nomor telepon tidak boleh kosong!")

        tamu.set_nama(nama_baru)
        tamu.set_nomor_telepon(nomor_telepon_baru)

        return "Data tamu berhasil diubah!"


# 6. CLASS RESERVASI
class Reservasi:
    def __init__(self, id_reservasi, tamu, kamar, check_in, check_out):
        self.__id_reservasi = id_reservasi
        self.__tamu = tamu
        self.__kamar = kamar
        self.__check_in = check_in
        self.__check_out = check_out
        self.__status = "Dipesan"

    def get_id_reservasi(self):
        return self.__id_reservasi

    def get_tamu(self):
        return self.__tamu

    def get_kamar(self):
        return self.__kamar

    def get_check_in(self):
        return self.__check_in

    def get_check_out(self):
        return self.__check_out

    def get_status(self):
        return self.__status

    def set_status(self, status_baru):
        if status_baru not in ["Dipesan", "Check-in", "Selesai", "Dibatalkan"]:
            raise ValueError("Status reservasi tidak valid!")
        self.__status = status_baru

    def hitung_durasi(self):
        durasi = self.__check_out - self.__check_in
        return durasi.days

    def hitung_total_harga(self):
        durasi = self.hitung_durasi()
        harga = self.__kamar.get_harga_per_malam()

        return durasi * harga

    def get_info(self):
        return (
            f"ID Reservasi: {self.__id_reservasi}\n"
            f"Nama Tamu: {self.__tamu.get_nama()}\n"
            f"Nomor Kamar: {self.__kamar.get_nomor_kamar()}\n"
            f"Check-in: {self.__check_in}\n"
            f"Check-out: {self.__check_out}\n"
            f"Durasi: {self.hitung_durasi()} malam\n"
            f"Total Harga: Rp{self.hitung_total_harga()}\n"
            f"Status: {self.__status}"
        )


# 7. ABSTRACT CLASS PEMBAYARAN
class Pembayaran(ABC):
    def __init__(self, id_pembayaran, reservasi):
        self._id_pembayaran = id_pembayaran
        self._reservasi = reservasi
        self._jumlah_pembayaran = reservasi.hitung_total_harga()
        self._status_pembayaran = "Belum Lunas"

    @abstractmethod
    def proses_pembayaran(self, nominal):
        pass

    def get_reservasi(self):
        return self._reservasi

    def get_status_pembayaran(self):
        return self._status_pembayaran

    def get_info(self):
        return (
            f"ID Pembayaran: {self._id_pembayaran}\n"
            f"ID Reservasi: {self._reservasi.get_id_reservasi()}\n"
            f"Jumlah Tagihan: Rp{self._jumlah_pembayaran}\n"
            f"Status Pembayaran: {self._status_pembayaran}"
        )


# 8. CLASS PEMBAYARAN TUNAI
class PembayaranTunai(Pembayaran):
    def __init__(self, id_pembayaran, reservasi):
        super().__init__(id_pembayaran, reservasi)
        self.__kembalian = 0

    def proses_pembayaran(self, nominal):
        if not isinstance(nominal, int) or nominal <= 0:
            raise ValueError("Nominal pembayaran harus berupa bilangan bulat positif!")
        if nominal < self._jumlah_pembayaran:
            raise ValueError("Uang pembayaran kurang!")

        self.__kembalian = nominal - self._jumlah_pembayaran
        self._status_pembayaran = "Lunas"

        return self.__kembalian

    def get_info(self):
        return (
            super().get_info() +
            f"\nMetode: Tunai\n"
            f"Kembalian: Rp{self.__kembalian}"
        )


# 9. CLASS PEMBAYARAN TRANSFER
class PembayaranTransfer(Pembayaran):
    def __init__(self, id_pembayaran, reservasi, nama_bank):
        super().__init__(id_pembayaran, reservasi)
        self.__nama_bank = nama_bank

    def proses_pembayaran(self, nominal):
        if not isinstance(nominal, int) or nominal <= 0:
            raise ValueError("Nominal pembayaran harus berupa bilangan bulat positif!")
        if nominal != self._jumlah_pembayaran:
            raise ValueError("Nominal transfer harus sesuai tagihan!")

        self._status_pembayaran = "Lunas"

        return "Transfer berhasil diproses!"

    def get_info(self):
        return (
            super().get_info() +
            f"\nMetode: Transfer\n"
            f"Bank: {self.__nama_bank}"
        )

# 10. CLASS MANAJEMEN RESERVASI
class ManajemenReservasi:
    def __init__(self, manajemen_kamar, manajemen_tamu):
        self.__daftar_reservasi = []
        self.__daftar_pembayaran = []
        self.__nomor_reservasi = 1
        self.__nomor_pembayaran = 1

        self.__manajemen_kamar = manajemen_kamar
        self.__manajemen_tamu = manajemen_tamu

        self.__tanggal_sistem = date.today()

    def get_tanggal_sistem(self):
        return self.__tanggal_sistem

    def set_tanggal_sistem(self, tanggal_baru):
        try:
            tanggal = datetime.strptime(tanggal_baru, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Format tanggal harus YYYY-MM-DD!")

        if tanggal < self.__tanggal_sistem:
            raise ValueError("Tanggal sistem tidak boleh mundur dari tanggal saat ini!")

        self.__tanggal_sistem = tanggal
        return f"Tanggal sistem berhasil diubah menjadi {tanggal}!"

    def cari_reservasi(self, id_dicari):
        for reservasi in self.__daftar_reservasi:
            if reservasi.get_id_reservasi() == id_dicari:
                return reservasi

        return None

    def kamar_punya_reservasi_aktif(self, nomor_kamar):
        for reservasi in self.__daftar_reservasi:
            if (
                reservasi.get_kamar().get_nomor_kamar() == nomor_kamar
                and reservasi.get_status() in ["Dipesan", "Check-in"]
            ):
                return True
        return False

    def tamu_punya_reservasi_aktif(self, id_tamu):
        for reservasi in self.__daftar_reservasi:
            if (
                reservasi.get_tamu().get_id_tamu() == id_tamu
                and reservasi.get_status() in ["Dipesan", "Check-in"]
            ):
                return True
        return False

    def cek_ketersediaan_kamar(self, nomor_kamar, check_in, check_out):
        kamar = self.__manajemen_kamar.cari_kamar(nomor_kamar)

        if kamar is None:
            raise KamarTidakDitemukanError("Kamar tidak ditemukan!")
        if kamar.get_status() == "Perbaikan":
            raise ValueError("Kamar sedang dalam perbaikan!")

        for reservasi in self.__daftar_reservasi:
            if reservasi.get_kamar().get_nomor_kamar() == nomor_kamar:
                if reservasi.get_status() in ["Dipesan", "Check-in"]:
                    if (
                        check_in < reservasi.get_check_out()
                        and check_out > reservasi.get_check_in()
                    ):
                        raise ValueError(
                            "Kamar sudah dipesan pada periode tersebut!"
                        )

        return kamar

    def tambah_reservasi(self, id_tamu, nomor_kamar, tanggal_check_in, tanggal_check_out):
        tamu = self.__manajemen_tamu.cari_tamu(id_tamu)

        if tamu is None:
            raise TamuTidakDitemukanError("Tamu tidak ditemukan!")

        try:
            check_in = datetime.strptime(
                tanggal_check_in, "%Y-%m-%d"
            ).date()

            check_out = datetime.strptime(
                tanggal_check_out, "%Y-%m-%d"
            ).date()

        except ValueError:
            raise ValueError("Format tanggal harus YYYY-MM-DD!")

        if check_out <= check_in:
            raise ValueError("Tanggal check-out harus setelah check-in!")
        if check_in < self.__tanggal_sistem:
            raise ValueError("Tanggal check-in tidak boleh berada di masa lalu!")

        kamar = self.cek_ketersediaan_kamar(
            nomor_kamar, check_in, check_out
        )

        id_reservasi = f"R{self.__nomor_reservasi:03d}"

        reservasi = Reservasi(id_reservasi, tamu, kamar, check_in, check_out)

        self.__daftar_reservasi.append(reservasi)
        self.__nomor_reservasi += 1

        return f"Reservasi berhasil dibuat dengan ID {id_reservasi}!"

    def batalkan_reservasi(self, id_reservasi):
        reservasi = self.cari_reservasi(id_reservasi)

        if reservasi is None:
            raise ReservasiTidakDitemukanError("Reservasi tidak ditemukan!")

        if reservasi.get_status() != "Dipesan":
            raise ValueError("Hanya reservasi berstatus Dipesan yang dapat dibatalkan!")

        reservasi.set_status("Dibatalkan")

        return "Reservasi berhasil dibatalkan!"

    def check_in(self, id_reservasi):
        reservasi = self.cari_reservasi(id_reservasi)

        if reservasi is None:
            raise ReservasiTidakDitemukanError("Reservasi tidak ditemukan!")

        if reservasi.get_status() != "Dipesan":
            raise ValueError("Reservasi tidak dapat diproses untuk check-in!")

        hari_ini = self.__tanggal_sistem
        if hari_ini < reservasi.get_check_in():
            raise ValueError("Check-in belum dapat dilakukan sebelum tanggal reservasi!")
        if hari_ini >= reservasi.get_check_out():
            raise ValueError("Masa reservasi telah berakhir sehingga check-in tidak dapat dilakukan!")

        kamar = reservasi.get_kamar()

        if kamar.get_status() != "Tersedia":
            raise ValueError("Kamar sedang tidak tersedia untuk check-in!")

        kamar.set_status("Terisi")
        reservasi.set_status("Check-in")

        return "Check-in berhasil!"

    def bayar_reservasi(self, id_reservasi, metode, nominal, nama_bank=""):
        reservasi = self.cari_reservasi(id_reservasi)

        if reservasi is None:
            raise ReservasiTidakDitemukanError("Reservasi tidak ditemukan!")

        if reservasi.get_status() != "Check-in":
            raise ValueError("Pembayaran hanya dapat dilakukan setelah check-in!")
        if self.__tanggal_sistem < reservasi.get_check_out():
            raise ValueError("Pembayaran dilakukan pada tanggal check-out!")

        for pembayaran in self.__daftar_pembayaran:
            if pembayaran.get_reservasi() == reservasi:
                raise ValueError("Reservasi ini sudah dibayar!")

        id_pembayaran = f"P{self.__nomor_pembayaran:03d}"

        if metode == "Tunai":
            pembayaran = PembayaranTunai(id_pembayaran, reservasi)

        elif metode == "Transfer":
            if not nama_bank.strip():
                raise ValueError("Nama bank harus diisi!")

            pembayaran = PembayaranTransfer(id_pembayaran, reservasi, nama_bank)

        else:
            raise ValueError("Metode pembayaran tidak valid!")

        hasil = pembayaran.proses_pembayaran(nominal)

        self.__daftar_pembayaran.append(pembayaran)
        self.__nomor_pembayaran += 1

        return pembayaran, hasil

    def check_out(self, id_reservasi):
        reservasi = self.cari_reservasi(id_reservasi)

        if reservasi is None:
            raise ReservasiTidakDitemukanError("Reservasi tidak ditemukan!")

        if reservasi.get_status() != "Check-in":
            raise ValueError("Tamu belum melakukan check-in!")

        if self.__tanggal_sistem < reservasi.get_check_out():
            raise ValueError("Check-out belum dapat dilakukan sebelum tanggal check-out!")

        sudah_bayar = False

        for pembayaran in self.__daftar_pembayaran:
            if pembayaran.get_reservasi() == reservasi:
                if pembayaran.get_status_pembayaran() == "Lunas":
                    sudah_bayar = True
                    break

        if not sudah_bayar:
            raise ValueError("Tamu harus menyelesaikan pembayaran terlebih dahulu!")

        reservasi.get_kamar().set_status("Tersedia")
        reservasi.set_status("Selesai")

        return "Check-out berhasil!"

    def tampilkan_reservasi(self):
        if not self.__daftar_reservasi:
            return "Belum ada data reservasi!"

        hasil = []

        for reservasi in self.generator_reservasi():
            hasil.append(reservasi.get_info())

        return "\n\n".join(hasil)

    def tampilkan_pembayaran(self):
        if not self.__daftar_pembayaran:
            return "Belum ada data pembayaran!"

        hasil = []

        for pembayaran in self.__daftar_pembayaran:
            hasil.append(pembayaran.get_info())

        return "\n\n".join(hasil)

    def generator_reservasi(self):
        for reservasi in self.__daftar_reservasi:
            yield reservasi

def main():
    manajemen_kamar = ManajemenKamar()
    manajemen_tamu = ManajemenTamu()

    manajemen_reservasi = ManajemenReservasi(manajemen_kamar, manajemen_tamu)

    while True:
        print("\n========== SISTEM MANAJEMEN HOTEL ==========")
        print(f"Tanggal Sistem: {manajemen_reservasi.get_tanggal_sistem()}\n")
        print("Manajemen Kamar:")
        print("1. Tampilkan Kamar")
        print("2. Tambah Kamar")
        print("3. Hapus Kamar")
        print("4. Ubah Status Kamar")
        print("\nManajemen Tamu:")
        print("5. Tampilkan Tamu")
        print("6. Tambah Tamu")
        print("7. Ubah Data Tamu")
        print("8. Hapus Tamu")
        print("\nManajemen Reservasi:")
        print("9. Buat Reservasi")
        print("10. Tampilkan Reservasi")
        print("11. Batalkan Reservasi")
        print("12. Check-in")
        print("13. Pembayaran")
        print("14. Check-out")
        print("15. Tampilkan Pembayaran")
        print("\nLainnya:")
        print("16. Atur Tanggal Sistem")
        print("0. Keluar")

        pilihan = input("\nPilih menu: ")

        try:
            if pilihan == "1":
                print("\n", manajemen_kamar.tampilkan_kamar())

            elif pilihan == "2":
                nomor = input("Nomor kamar: ")
                tipe = input("Tipe kamar: ")
                harga = int(input("Harga per malam: "))

                kamar = Kamar(nomor, tipe, harga)
                print(manajemen_kamar.tambah_kamar(kamar))

            elif pilihan == "3":
                nomor = input("Nomor kamar: ")
                print(manajemen_kamar.hapus_kamar(nomor, manajemen_reservasi))

            elif pilihan == "4":
                nomor = input("Nomor kamar: ")
                print(manajemen_kamar.ubah_status_kamar(nomor))

            elif pilihan == "5":
                print("\n", manajemen_tamu.tampilkan_tamu())

            elif pilihan == "6":
                nama = input("Nama tamu: ")
                telepon = input("Nomor telepon: ")

                print(manajemen_tamu.tambah_tamu(nama, telepon))

            elif pilihan == "7":
                id_tamu = input("ID tamu: ")
                nama = input("Nama baru: ")
                telepon = input("Nomor telepon baru: ")

                print(manajemen_tamu.ubah_data_tamu(id_tamu, nama, telepon))

            elif pilihan == "8":
                id_tamu = input("ID tamu: ")
                print(manajemen_tamu.hapus_tamu(id_tamu, manajemen_reservasi))

            elif pilihan == "9":
                id_tamu = input("ID tamu: ")
                nomor_kamar = input("Nomor kamar: ")
                check_in = input("Tanggal check-in (YYYY-MM-DD): ")
                check_out = input("Tanggal check-out (YYYY-MM-DD): ")

                print(manajemen_reservasi.tambah_reservasi(
                    id_tamu, nomor_kamar, check_in, check_out
                ))

            elif pilihan == "10":
                print("\n", manajemen_reservasi.tampilkan_reservasi())

            elif pilihan == "11":
                id_reservasi = input("ID reservasi: ")
                print(manajemen_reservasi.batalkan_reservasi(id_reservasi))

            elif pilihan == "12":
                id_reservasi = input("ID reservasi: ")
                print(manajemen_reservasi.check_in(id_reservasi))

            elif pilihan == "13":
                id_reservasi = input("ID reservasi: ")
                metode = input("Metode (Tunai/Transfer): ")
                nominal = int(input("Nominal pembayaran: "))

                nama_bank = ""

                if metode == "Transfer":
                    nama_bank = input("Nama bank: ")

                pembayaran, hasil = manajemen_reservasi.bayar_reservasi(
                    id_reservasi, metode, nominal, nama_bank
                )

                print(pembayaran.get_info())

                if metode == "Tunai":
                    print(f"Kembalian: Rp{hasil}")
                else:
                    print(hasil)

            elif pilihan == "14":
                id_reservasi = input("ID reservasi: ")
                print(manajemen_reservasi.check_out(id_reservasi))

            elif pilihan == "15":
                print("\n", manajemen_reservasi.tampilkan_pembayaran())

            elif pilihan == "16":
                tanggal = input("Tanggal sistem baru (YYYY-MM-DD): ")
                print(manajemen_reservasi.set_tanggal_sistem(tanggal))

            elif pilihan == "0":
                print("Terima kasih telah menggunakan sistem hotel!")
                break

            else:
                print("Pilihan menu tidak valid!")

        except (
            ValueError,
            KamarTidakDitemukanError,
            TamuTidakDitemukanError,
            ReservasiTidakDitemukanError,
        ) as error:
            print(f"Terjadi kesalahan: {error}")


if __name__ == "__main__":
    main()