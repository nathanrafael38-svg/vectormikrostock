---
name: upload-dreamstime
description: Siapkan dan isi upload badge logo AI ke Dreamstime (JPG utama + EPS additional format, kategori AI-generated, disclosure AI), berhenti sebelum Submit. Pakai setelah batch Adobe (EPS + metadata_adobe.csv) siap.
---

# Upload ke Dreamstime

Kebijakan dicek 11 Nov 2026. Cek ulang sebelum dipakai, karena halaman resmi tidak bertanggal.

## Aturan Dreamstime untuk konten AI
Sumber resmi: https://www.dreamstime.com/ai-generated-images dan blog Dreamstime 4 Okt 2024 (`/blog/how-to-successfully-submit-ai-generated-images-to-dreamstime-74214`).
- Kontributor harus punya hak penuh atas gambar. Hak output Google Flow **belum terverifikasi** (Google hanya menyatakan "won't claim ownership").
- **Description wajib menyatakan gambar dibuat AI.**
- **Salah satu kategori wajib `Illustrations & Clipart > AI-generated`.** Tanpa itu langsung ditolak.
- Ditolak: wajah manusia realistis, logo/merek asli, teks salah eja atau ngawur, watermark/tanda tangan, artefak.
- Non-eksklusif: aman dijual paralel dengan Adobe Stock. Jangan centang exclusive.

## Format vektor
- File utama = **JPG resolusi tinggi** (kita pakai 5334×3000, 16 MP). EPS diupload sebagai **additional format** dan direview terpisah (lebih lama). Info ini dari forum Dreamstime (lama). **[CEK ULANG]** di portal.
- Risiko EPS Inkscape/cairo ditolak sama seperti di Adobe. Belum ada bukti lolos.
- Akun baru: uji batch kecil (3 file) dulu. Dugaan, belum terverifikasi: rasio diterima memengaruhi batas upload.

## Langkah
1. Siapkan paket (butuh `gs` dan `exiftool`):
   ```
   python tools/dreamstime_prep.py hasil/dreamstime hasil/c-vector-day-2 --only logo-022,logo-023,logo-031
   ```
   Hasil: `jpg/` (judul, description berisi kalimat AI, dan keyword tertanam di IPTC sehingga portal bisa mengisi otomatis), `eps/`, `metadata_dreamstime.csv`.
2. Cek tiap description/keyword dengan gambarnya. Hapus kata yang tidak terlihat di gambar (misalnya "ribbon banner" kalau tidak ada pita).
3. Salin paket ke PC Nathan (mis. `Downloads\Dreamstime-Pilot`).
4. Sesi Remote Control di Chrome Nathan yang sudah login: upload JPG, pastikan title/description/keyword sesuai CSV, pilih 3 kategori (AI-generated wajib), tanpa release, bukan editorial, bukan exclusive. Tempel EPS sebagai additional format kalau portal mengizinkan sebelum submit.
5. **Berhenti sebelum Submit.** Nathan klik Submit sendiri dan memastikan akun yang login benar.
6. Catat hasil review (JPG dan EPS terpisah) di `data/konsep.xlsx`. Batch berikutnya hanya setelah hasil uji keluar.

## Larangan
- Jangan buat akun, jangan isi data pajak, pembayaran, atau identitas tanpa konfirmasi Nathan.
- Jangan submit atas nama Nathan, jangan pakai ekstensi auto-submit.
- Jangan menyembunyikan status AI.
