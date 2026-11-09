---
name: riset-niche-harian
description: Pilih niche badge/emblem logo untuk hari ini dan tulis 10 prompt Google Flow ("C-Vector Day N") dalam xlsx. Pakai untuk jadwal harian atau saat Nathan minta prompt baru.
---

# Riset niche harian → prompt C-Vector Day N

## Langkah
1. Baca `data/registry.json` (suffix prompt + semua konsep yang sudah dipakai) dan `data/konsep.xlsx` (status: diterima/ditolak, download). Kalau ada alasan penolakan Adobe, konsep baru harus belajar dari itu.
2. Tentukan N = nomor hari berikutnya (lihat `data/prompts/`). ID lanjutan dari ID terakhir di registry (logo-0XX).
3. Pilih 10 konsep: minimal 5 niche berbeda; tiap konsep punya bentuk badge (perisai, lingkaran, hexagon, arch-top, ...) dan ilustrasi utama yang BERBEDA dari yang sudah ada di registry. Boleh niche sama asal ilustrasi + bentuk beda.
4. Cek kepadatan manual: `WebSearch` / satu `WebFetch` pencarian biasa per niche ("<niche> logo" di stock.adobe.com). Catat jumlah hasil dan gaya dominan di `data/riset/<tanggal>.md`. Jangan scraping berulang.
5. Prioritas niche: buyer UMKM nyata (home service, food, otomotif, olahraga, pet, craft). Hindari niche yang hasil pencariannya ratusan ribu kecuali ada sudut pembeda yang spesifik; tulis jujur kalau sudut pembedanya lemah.
6. Tulis prompt Inggris: `<deskripsi badge + ilustrasi + palet hex>` + spasi + `suffix` dari registry. Pita/teks band wajib EMPTY. 1 prompt = 1 logo. Tanpa merek/IP.
7. Tulis `data/prompts/C-Vector Day N.xlsx` dengan kolom: ID, Niche, Prompt (lebar 110, wrap), Sudah generate, Sudah upload PNG (dropdown Ya/Belum). Tiru struktur `C-Vector Day 1.xlsx`.
8. Update `data/registry.json` (id, niche, prompt, date). Kirim ke Nathan: 1 pesan singkat + lampiran xlsx.

## Aturan
- Kalau 3 hari berturut-turut tidak ada PNG yang diupload, jangan bikin batch baru; tanya sekali apakah jadwal di-pause.
- Output riset harus menyebut risiko: kepadatan, kemiripan, trademark.
