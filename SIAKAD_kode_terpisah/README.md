# SIAKAD STITEK Bontang — versi kode terpisah

## Struktur file

- `app.py` — file utama/final untuk menjalankan aplikasi.
- `config.py` — warna, style dasar, dan daftar modul.
- `core.py` — inisialisasi tampilan, style, helper query database.
- `login.py` — halaman dan proses login.
- `dashboard.py` — beranda, taskbar atas, pencarian modul, dan scroll.
- `akademik.py` — tampilan tabel dan fungsi tambah/edit/hapus/cari data.
- `logout.py` — proses logout.
- `data_mahasiswa.py` — konfigurasi modul Mahasiswa.
- `data_dosen.py` — konfigurasi modul Dosen.
- `data_mata_kuliah.py` — konfigurasi modul Mata Kuliah.
- `data_krs.py` — konfigurasi modul KRS.
- `data_jadwal_kuliah.py` — konfigurasi modul Jadwal Kuliah.
- `data_pembayaran_ukt.py` — konfigurasi modul Pembayaran UKT.

## Cara memasang

1. Ekstrak semua file ke dalam **satu folder project yang sama**.
2. Salin file `database.py` milik project lama ke folder ini. File tersebut tidak disertakan karena isi konfigurasi koneksi MySQL dan struktur tabel login tidak ada di kode yang diberikan.
3. Jika ada logo, letakkan `stitek.jpg` di folder yang sama. Logo opsional.
4. Pasang dependensi jika belum ada:
   `pip install mysql-connector-python`
5. Pastikan MySQL di XAMPP aktif dan database `siakad` sudah di-import.
6. Jalankan:
   `python app.py`

## Catatan

File `app.py` adalah titik masuk aplikasi setelah modul-modul dipisahkan. Jangan jalankan `login.py`, `dashboard.py`, atau `akademik.py` sendiri-sendiri. Semuanya dipakai oleh `app.py`.

Konfigurasi tabel saat ini mengikuti kode sumber: `mahasiswa`, `dosen`, `mata_kuliah`, `krs`, `jadwal_kuliah`, dan `pembayaran_ukt`. Nama kolom primary key mengikuti kode sumber juga. Bila skema database berbeda, sesuaikan file `data_*.py`.

Fungsi login memanggil `check_login()` dan `setup_login()` dari `database.py` lama, jadi pertahankan fungsi tersebut beserta konfigurasi database yang sudah cocok dengan project.
