---
name: metadata-qc-submit
description: Tulis title/keyword Adobe Stock per logo setelah melihat gambarnya, cek risiko mirip/merek, dan siapkan CSV + checklist submit untuk Nathan. Pakai setelah proses-png selesai.
---

# Metadata + QC submit

## Langkah
1. Buka `hasil/metadata_DRAFT_adobe.csv` (draft dari nama niche) dan **lihat tiap preview**. Title/keyword harus menggambarkan isi gambar sebenarnya, bukan niche yang direncanakan.
2. **Title**: Inggris, deskriptif, tanpa kata "vector/stock", tanpa nama merek atau teks placeholder. Pola: `<gaya> <bentuk badge> logo <ilustrasi> for <niche>`. **[CEK ULANG]** batas panjang di portal.
3. **Keyword**: 10 pertama = subjek utama yang paling relevan; sisanya industri, gaya, warna. Maks 49 **[CEK ULANG]**. Tanpa merek, tanpa kata yang tidak terlihat di gambar.
4. **Cek risiko** per file, tulis hasilnya di `data/konsep.xlsx`: (a) cari mirip di Adobe Stock secara manual (halaman pertama), (b) cari kemiripan dengan merek terdaftar (Google Lens/TinEye oleh Nathan atau pencarian teks), (c) dua file dalam batch yang sama tidak boleh hanya beda warna/ikon (similar content).
5. Kosongkan kolom Category di CSV sampai nomor kategori di portal diverifikasi. Jangan mengarang nomor.
6. Buat checklist submit untuk Nathan (satu halaman): file yang boleh diupload, file yang ditahan beserta alasannya, **centang "Created using generative AI tools" untuk semua**, upload EPS saja (preview dibuat Adobe), isi/Upload CSV, review, submit manual.
7. Perbarui `data/konsep.xlsx` (status, tanggal submit). Setelah ada keputusan Adobe, catat alasan tolak untuk bahan `riset-niche-harian`.

## Larangan
- Jangan submit atas nama Nathan, jangan pakai ekstensi auto-submit.
- Jangan menyembunyikan status AI.
