---
name: proses-png
description: Ubah PNG hasil Google Flow (diupload Nathan) jadi EPS vector 5334x3000 pt + preview + QC + contact sheet. Pakai saat ada PNG logo-0XX baru di inbox atau thread.
---

# Proses PNG → EPS

## Langkah
1. Pastikan dependensi: `./setup.sh` (vtracer, fonttools, Inkscape, Ghostscript).
2. Taruh PNG di `inbox/` dengan nama `logo-0XX.png` (ID dari xlsx). PNG asli, bukan screenshot.
3. Jalankan `python -m agent_vector.batch inbox --registry data/registry.json`.
4. **Lihat sendiri** `hasil/contact_sheet.jpg` dan tiap `hasil/logo-0XX/logo-0XX_preview.jpg` (Read gambarnya). Cek: bentuk lingkaran/perisai bersih, tidak ada serpihan, warna sesuai palet, tidak ada teks sampah AI.
5. Tolak dan minta generate ulang kalau gambar sumber bertekstur, bergradasi, ada bayangan, atau detail halus (trace akan kotor). Jangan "memperbaiki" gambar jelek dengan trik yang menyembunyikan masalah.
6. Pasang teks placeholder: buat `inbox/logo-0XX.json` berisi `texts` (kind `arc_top` / `arc_bottom` / `line`, font OFL dari `fonts/`, posisi dalam pecahan 0..1 ukuran gambar) dan `masks` (menutup teks sampah AI di raster SEBELUM trace). Jalankan ulang batch, cek preview lagi. Opsional `variant_map` untuk varian satu warna di kanan artboard.
7. QC wajib lolos: `raster_tertanam: false`, BoundingBox `0 0 5334 3000`, 15–65 MP, < 45 MB. Tandai "perlu tinjau" bila node > 6000, > 6 warna, atau mirip gambar lain (dHash).
8. Buka EPS keluaran dengan Ghostscript (`gs -sDEVICE=png16m -dEPSCrop`) dan bandingkan dengan preview.

## Catatan jujur
- QC teknis lolos ≠ lolos review Adobe. Belum ada file dari pipeline ini yang lolos review (jangan klaim sebaliknya sampai ada bukti).
- Node ±2.000–4.600 per badge; belum diketahui apakah reviewer menganggap wajar.
- Latar artboard harus putih; tanpa latar, cairo memotong BoundingBox ke area bertinta.

## Catatan dari C-Vector Day 1 (9 Nov 2026)
- Flow memberi JPG 1024 px ("1K Original size"), bukan PNG; konversi ke PNG tidak menaikkan kualitas. Opsi 2K/4K Upscaled tidak dipakai.
- Job override per badge ada di `data/jobs/logo-0XX.json` (colors=8, speckle=8, posisi teks placeholder). Salin ke `inbox/` untuk render ulang persis.
- Teks placeholder dipasang hanya di ribbon lurus dan cincin lebar; ribbon melengkung (017) dan cincin tipis (020) dibiarkan tanpa teks.
- Cek visual zoom wajib: teks di band melengkung sering menyentuh garis tepi; geser baseline lalu render ulang.
- Upload ke portal Adobe lewat sesi Remote Control di Chrome Nathan: pastikan file dikirim sebagai `application/postscript` (tipe `octet-stream` ditolak "invalid file type"). Sesi berhenti sebelum "Submit for review"; Nathan yang konfirmasi.
