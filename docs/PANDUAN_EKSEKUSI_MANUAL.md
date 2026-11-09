# Panduan Eksekusi Manual: Logo Vector EPS untuk Adobe Stock

Target batch pertama: **10 aset, 10 konsep berbeda, 1 file per konsep.**
Stack: Windows, Adobe Firefly, Inkscape 1.3+ (gratis), Vectorizer.AI (opsional), Adobe Stock Contributor Portal.
Contoh hasil akhir yang lolos QC teknis: folder `/mnt/project-files/logo-001/` (EPS 5000×3000 pt, 0 raster, tanpa font).

Dicek ke halaman resmi Adobe pada 7 Nov 2026. Apa pun yang ditandai **[CEK ULANG]** belum gue verifikasi; buka halamannya sendiri sebelum produksi.

---

## A. Koreksi terhadap tutorial yang lu tempel

| # | Klaim di tutorial | Fakta / masalah | Yang harus lu lakukan |
|---|---|---|---|
| 1 | Artboard 3000 × 5000 px | Itu **portrait**, padahal prompt background minta "wide horizontal". Komposisinya bakal bentrok. | Pakai **landscape**. |
| 2 | "3000×5000 px = 15 MP, sesuai minimum" | **Jebakan unit.** Inkscape pakai 96 px/inch, EPS pakai point (72/inch). 3000×5000 **px** di Inkscape jadi 2250×3750 **pt** di EPS = **8,4 MP**. Di bawah minimum, ditolak. Selain itu 15,0 MP pas-pasan, tanpa margin. | Set unit dokumen ke **pt**, ukuran **5334 × 3000 pt** (16:9, ±16 MP). |
| 3 | "Upload atau pastikan preview JPEG tersedia" | Halaman resmi: **lu tidak upload JPEG preview**, Adobe yang bikin otomatis. Vector di dalam ZIP **tidak diterima**. Format yang diterima: AI, EPS, SVG. | Upload EPS saja. JPEG cuma buat QC dan contact sheet pribadi. |
| 4 | "Persyaratan diperbarui September 2026" | Halaman resmi tertanggal **11 Juni 2026**. Angkanya benar: 15–65 MP, maks 45 MB, RGB, offset artboard (0,0) pojok kiri atas. | Pakai angka itu, abaikan tanggal versi tutorial. |
| 5 | "Simpan sebagai master SVG, lalu Save As EPS" | Save As mengganti file aktif ke EPS. Edit berikutnya bisa nyasar ke EPS. | Pakai **File → Save a Copy** (Shift+Ctrl+Alt+S) untuk EPS. |
| 6 | "Periksa opsi transparency dan rasterization" | Kurang tegas. Di Inkscape, **opacity < 100%, blur, filter, drop shadow** bakal di-rasterize diam-diam waktu export EPS. Hasilnya EPS ada bitmap tertanam. | Larangan keras: tidak ada opacity, blur, filter. Warna "transparan" diganti warna solid hasil campuran. |
| 7 | Standalone + presentation = 2 aset | Tutorial sendiri sudah kasih peringatan, tapi buat akun baru ini risiko utama: penolakan **similar content**. | Batch 1: **jangan** upload 2 versi dari logo yang sama. 10 konsep, 10 file. |
| 8 | Trace bitmap sebagai langkah utama | Adobe minta vector AI "di-rework sampai semudah diedit seperti vector organik". Hasil trace mentah biasanya ratusan node acak: gagal di kriteria itu. | Default: **rebuild manual** pakai shape + Boolean. Trace hanya jadi panduan bentuk. |

---

## B. Persiapan sekali jalan (±1 jam)

- [ ] Daftar / login **contributor.stock.adobe.com** pakai Adobe ID.
- [ ] Lengkapi profil, data pajak, dan metode payout di portal. **[CEK ULANG]** form pajak untuk kontributor Indonesia (biasanya W-8BEN) dan metode payout yang tersedia.
- [ ] Install **Inkscape 1.3 atau lebih baru** dari inkscape.org (installer .msi 64-bit).
- [ ] Login **firefly.adobe.com**. **[CEK ULANG]** ketentuan penggunaan komersial dan sisa kredit generatif di akun lu.
- [ ] (Opsional) Vectorizer.AI: **[CEK ULANG]** harga, batas gratis, dan lisensi output. Jangan andalkan versi trial untuk produksi.
- [ ] Bikin struktur folder di laptop:

```
D:\stock-logo\
  00_riset\          konsep.xlsx (daftar 10 konsep)
  01_ai_raw\         PNG dari Firefly
  02_master_svg\     logo-002_master.svg ...
  03_eps_submit\     logo-002.eps ...
  04_qc_jpg\         logo-002_qc.jpg (buat cek, bukan upload)
  05_metadata\       metadata.csv
```

- [ ] Penamaan file: `logo-002`, `logo-003`, ... huruf kecil, tanpa spasi. (logo-001 sudah ada.)

---

## C. Alur per aset (ulangi 10×)

### Tahap 1. Pilih konsep (5 menit/aset)

Isi `konsep.xlsx` dengan kolom: ID, industri target, ide simbol, palet (3 hex), tipe background (A geometris / B organik / C premium).

Aturan pemilihan:
- [ ] Sebar 10 konsep ke minimal 4 industri (tech, wellness, sustainability, finance, creative studio, food, education).
- [ ] Simbol bisa dijelaskan dalam satu kalimat ("tiga busur saling mengunci"). Kalau tidak bisa, terlalu rumit untuk di-vector.
- [ ] Sebelum generate, cari di **stock.adobe.com** pakai kata kunci konsep lu. Kalau hasil halaman pertama penuh simbol yang mirip, ganti konsep.

**QC gate 1:** 10 baris terisi, tidak ada dua konsep dengan bentuk dasar yang sama.

### Tahap 2. Generate konsep di Firefly (10 menit/aset)

1. Buka firefly.adobe.com → **Text to Image**.
2. Aspect ratio **Square (1:1)** untuk simbol.
3. Tempel prompt logo dari tutorial, ganti bagian industri, bentuk, dan warna sesuai baris konsep.
4. Generate 4 variasi, ulangi maksimal 2–3 kali.
5. Pilih **satu** yang paling sederhana. Download PNG ke `01_ai_raw\logo-00X_raw.png`.
6. Background: **jangan generate gambar background lalu di-trace.** Hasilnya kotor. Pakai prompt background cuma sebagai referensi komposisi; bangun shape-nya sendiri di Tahap 5.

**QC gate 2 (originalitas, wajib):**
- [ ] Upload PNG ke **Google Lens** (images.google.com → ikon kamera) dan **TinEye**. Kalau ada logo merek nyata yang mirip, buang.
- [ ] Tidak ada huruf, angka, atau bentuk yang bisa dibaca sebagai inisial.
- [ ] Simbol masih kebaca kalau lu kecilkan ke ukuran ikon (zoom out browser ke 25%).

### Tahap 3. Setup dokumen Inkscape (2 menit, sekali per file)

1. Inkscape → **File → New**.
2. **File → Document Properties** (Shift+Ctrl+D).
3. Tab **Display/Page**: *Display units* = **pt**, *Format* = Custom, *Width* = **5334**, *Height* = **3000**, *Units* = **pt**. Scale = 1.0.
4. Tutup dialog. Simpan langsung: **File → Save As** → `02_master_svg\logo-00X_master.svg` (Inkscape SVG).

**QC gate 3:** pojok kanan bawah status bar menunjukkan unit pt; Document Properties terbaca 5334 × 3000 pt.

### Tahap 4. Bangun logo vector (30–60 menit/aset, ini tahap terberat)

**Jalur utama: rebuild manual (direkomendasikan untuk logo geometris)**
1. **File → Import** (Ctrl+I) PNG dari Firefly → pilih *Embed* → OK.
2. Klik gambar, buka **Object → Layers and Objects**, kunci (ikon gembok) gambar itu. Turunkan opacity *gambar referensi* ke 30% supaya enak dijiplak (ini dihapus nanti, jadi aman).
3. Gambar ulang pakai **Circle (E)**, **Rectangle (R)**, **Bezier (B)**. Pegang Ctrl saat drag supaya proporsional.
4. Gabung/potong bentuk: pilih 2 objek → **Path → Union** (Ctrl++), **Difference** (Ctrl+-), **Intersection** (Ctrl+*), **Division** (Ctrl+/).
5. Stroke yang jadi bagian logo diubah ke shape: **Path → Stroke to Path** (Ctrl+Alt+C).
6. Isi warna dari palet: **Object → Fill and Stroke** (Shift+Ctrl+F) → Flat color → ketik hex. **Alpha harus 255 (100%).**
7. Hapus gambar referensi: buka kunci, klik, Delete.

**Jalur cadangan: trace (untuk bentuk organik yang susah digambar)**
1. Klik gambar → **Path → Trace Bitmap** (Shift+Alt+B).
2. Pilih **Multiple scans** → mode **Colors** → Scans **3–6**. Centang **Smooth**, **Remove background**, **Stack scans** dimatikan.
3. Apply. Geser hasil trace ke samping, hapus PNG asli.
4. **Object → Ungroup** (Shift+Ctrl+G), hapus serpihan kecil.
5. Pilih tiap shape → **Path → Simplify** (Ctrl+L) sekali atau dua kali sampai kurva masih rapi tapi node berkurang.
6. Tekan **N** (Node tool) dan lihat jumlah node di status bar. Kalau satu bentuk sederhana masih ratusan node, rebuild manual saja.
7. Vectorizer.AI: upload PNG → download **SVG** → File → Import ke Inkscape → lanjut langkah 4–6 yang sama.

**QC gate 4:**
- [ ] **Edit → Select All in All Layers** (Ctrl+Alt+A), lihat status bar: tidak boleh ada kata "Image".
- [ ] Zoom 400% di tepi bentuk: tidak ada gigi gergaji, celah putih antar warna, atau serpihan.
- [ ] Jumlah warna = palet yang direncanakan (biasanya 2–4).
- [ ] Logo di-group (Ctrl+G) dan diberi nama di Layers and Objects, misal "logo".

### Tahap 5. Background vector (15–30 menit/aset)

1. Buat persegi panjang seukuran halaman: Rectangle tool, lalu di toolbar isi X=0, Y=0, W=5334, H=3000 (pt). Isi warna dasar.
2. Tambah 2–5 shape besar (lingkaran raksasa terpotong, pita lengkung, bidang diagonal) dengan warna solid dari palet yang sama.
3. Potong yang keluar halaman: pilih semua shape background + satu kotak seukuran halaman → **Path → Intersection** per shape. **Jangan pakai clipping mask** kalau bisa dihindari, karena area tersembunyi di luar artboard bikin file kotor.
4. Area tengah (±40% lebar) dibiarkan tenang untuk logo.
5. Taruh logo: tengah, tinggi logo ±35–45% tinggi halaman. Align: **Object → Align and Distribute** (Shift+Ctrl+A), relative to Page, center both.
6. Background di-group, beri nama "background", taruh di bawah logo.
7. **Ctrl+S** simpan master SVG.

**QC gate 5:**
- [ ] Kontras logo vs background jelas. Tes cepat: **View → Display mode → Outline** lalu kembali **Normal**; tes kedua, zoom out sampai logo selebar ±2 cm di layar, masih kebaca.
- [ ] Tidak ada objek di luar halaman: **Edit → Select All** (Ctrl+A), bounding box tidak melewati batas halaman.
- [ ] Tidak ada opacity < 100%, blur, filter, atau gradient mesh. Cek di Fill and Stroke tiap group.

### Tahap 6. Export EPS (2 menit)

1. **File → Save a Copy** (Shift+Ctrl+Alt+S).
2. Format: **Encapsulated PostScript (*.eps)**. Simpan ke `03_eps_submit\logo-00X.eps`.
3. Di dialog opsi:
   - Restrict to PostScript level: **PostScript level 3**.
   - Text output: **Embed fonts** tidak relevan kalau tidak ada teks; kalau ada teks, sebelumnya sudah **Path → Object to Path** (Shift+Ctrl+C).
   - **Rasterize filter effects**: tidak boleh ada filter, jadi opsi ini tidak berpengaruh. Kalau berpengaruh, berarti masih ada filter: kembali ke Tahap 5.
   - Export area: **Use document's page size**.
   - Bleed/margin: **0**.
4. OK.

### Tahap 7. QC file EPS (5 menit/aset, jangan dilewati)

- [ ] **Ukuran file** di Explorer: logo sederhana harusnya puluhan KB sampai beberapa ratus KB (contoh logo-001: 5–7 KB). Kalau tiba-tiba beberapa MB, hampir pasti ada raster tertanam.
- [ ] **Cek raster pakai Notepad:** klik kanan EPS → Open with → Notepad → Ctrl+F cari `DataSource` dan `ImageType`. Harus **tidak ketemu**. Kalau ketemu, ada bitmap tertanam: cari objek dengan opacity/filter, perbaiki, export ulang. Catatan: kata `image` **pasti** muncul di dua baris awal (`/cairo_image ... def`). Itu definisi bawaan Inkscape/cairo, bukan gambar, abaikan.
- [ ] **Cek ukuran artboard di Notepad:** baris `%%BoundingBox:` harus `0 0 5334 3000`. Kalau angkanya 4000 × 2250 atau sejenisnya, unit dokumen salah (balik ke Tahap 3).
- [ ] Buka EPS di Inkscape (File → Open, pilih *Poppler/Cairo import*). Tampilan sama dengan master, path bisa diklik per bentuk.
- [ ] Export JPEG untuk arsip QC: buka master SVG → **File → Export** (Shift+Ctrl+E) → Page → PNG → buka di Paint → Save As JPEG ke `04_qc_jpg\`. File ini **tidak di-upload**.

**Yang belum terverifikasi dan bisa bikin gagal teknis:** EPS dari Inkscape dibuat lewat cairo, bukan format "Illustrator EPS". **[CEK ULANG]** apakah portal menerima EPS cairo tanpa masalah. Cara paling murah: upload 1–2 file dulu sebelum produksi 10 (lihat Bagian D). Alternatif yang juga resmi diterima: upload **SVG**, tapi **[CEK ULANG]** ketentuan SVG di halaman teknis vector sebelum memilih jalur ini.

### Tahap 8. Metadata (10 menit/aset)

Format per aset di `metadata.csv`: Filename, Title, Keywords.

- [ ] **Title**: deskriptif, bahasa Inggris, tanpa kata "vector", "stock", nama merek, atau kata promosi. Pola: `[gaya] [bentuk] logo [fungsi/industri] on [background]`. Contoh: `Abstract Woven Arc Logo Emblem on Geometric Navy Teal Background`. **[CEK ULANG]** batas panjang title di portal.
- [ ] **Keywords**: maksimal 49 **[CEK ULANG]**. Adobe resmi menyatakan **10 keyword pertama diprioritaskan** di pencarian, jadi urutan penting: subjek dulu (logo, emblem, symbol, bentuk spesifik), lalu industri, lalu gaya/warna.
- [ ] Jangan pakai keyword yang tidak terlihat di gambar. Keyword spam = alasan penolakan.
- [ ] Kalau title/keyword dikosongkan, portal kasih saran otomatis (title + sampai 25 keyword). Pakai sebagai bahan, edit, jangan terima mentah.

### Tahap 9. Upload dan submit

1. contributor.stock.adobe.com → **Upload** → pilih file `.eps` (bukan ZIP, bukan JPEG).
2. Tunggu proses (bisa beberapa menit sampai thumbnail muncul).
3. Tab **Not submitted**: klik file.
4. Isi:
   - File type: **Vectors** (atau **Illustrations** sesuai pilihan yang muncul).
   - Category: **Graphic Resources** **[CEK ULANG]** nama kategori di dropdown.
   - Language: English.
   - Title, Keywords: tempel dari CSV, urutkan ulang kalau perlu (drag).
   - **Centang "Created using generative AI tools"** kalau konsep berasal dari Firefly/AI apa pun. Tidak centang = risiko akun di-flag, jauh lebih mahal daripada risiko ditolak.
   - Kalau muncul pertanyaan orang/properti: pilih bahwa konten fiksi/tidak ada merek nyata sesuai opsi yang ada.
5. **Submit**.
6. Catat tanggal submit di `konsep.xlsx`.

---

## D. Urutan eksekusi batch pertama (yang realistis)

| Hari | Pekerjaan | Output |
|---|---|---|
| 1 | Bagian B + Tahap 1 untuk 10 konsep + Tahap 2 untuk 3 konsep | Akun siap, konsep.xlsx, 3 PNG |
| 2 | Tahap 3–7 untuk **2 aset** | 2 EPS lolos QC |
| 2 | **Upload 2 EPS itu (plus logo-001 kalau mau) sebagai uji coba** | Tahu EPS Inkscape diterima portal atau tidak |
| 3–5 | Tunggu hasil review uji coba. Sambil itu Tahap 2–7 untuk 7–8 aset sisanya, **jangan di-submit dulu**. | 8 EPS siap |
| 6+ | Kalau uji coba lolos: submit sisanya. Kalau ditolak: baca alasannya, perbaiki semua file sebelum submit. | 10 aset ter-submit |

Estimasi waktu kerja: **1–2 jam per aset** di 3 aset pertama, turun ke ±45 menit setelah lancar. 10 aset = ±10–15 jam kerja. Kalau lu dapat angka jauh lebih cepat, kemungkinan besar lu melewati QC.

Lama review Adobe tidak pasti, bisa beberapa hari sampai beberapa minggu. **[CEK ULANG]** di portal.

---

## E. Risiko nyata yang tidak bisa dihilangkan oleh workflow ini

1. **Kejenuhan niche.** "Abstract geometric logo" adalah salah satu kategori vector paling padat di Adobe Stock. Cek sendiri: cari kata itu di stock.adobe.com dan lihat jumlah hasilnya. 10 aset di niche ini hampir pasti tenggelam. Penjualan realistis batch pertama: nol sampai segelintir dalam beberapa bulan. Diferensiasi lu harus datang dari konsep per industri yang spesifik, bukan dari "lebih rapi".
2. **Similar content.** Dua file yang cuma beda warna/background dari logo yang sama sering ditolak sebagai mirip. Untuk akun baru, rasio tolak yang tinggi di awal tidak membantu.
3. **Trademark/IP.** Simbol geometris sederhana (busur, segitiga, daun, infinity) punya peluang besar mirip logo terdaftar. Google Lens bukan jaminan. Kalau pembeli kena masalah merek, yang tercatat adalah file lu.
4. **Kualitas trace.** Reviewer melihat jumlah node dan kebersihan path. Hasil auto-trace mentah adalah alasan penolakan klasik untuk vector AI.
5. **Raster tersembunyi.** Satu objek opacity 90% cukup untuk bikin EPS berisi bitmap. Tahap 7 ada untuk ini.
6. **Kebijakan AI berubah.** Halaman generative AI Adobe diperbarui berkala (terakhir 11 Juni 2026). Baca ulang tiap bulan.
7. **Logo sebagai produk stock.** Pembeli logo stock tidak mendapat hak eksklusif, jadi sebagian bisnis serius tidak akan memakainya sebagai identitas utama. Pasar realistisnya: template, mockup, presentasi, UMKM. Sesuaikan konsep ke pembeli itu.

---

## F. Hitungan realistis menuju $1000 pertama

### Angka yang sudah pasti (halaman resmi Adobe, diperbarui 27 Okt 2026)
- Royalti kontributor untuk vector: **33% dari harga net** per lisensi.
- Royalti minimum per download dari paket langganan besar: **$0,33** (0–999 lisensi seumur hidup akun), $0,36 (1.000–9.999), $0,38 (10.000+).
- Satu download dari paket langganan kecil atau pembelian kredit bisa membayar lebih tinggi, tapi porsinya tidak bisa lu kontrol.
- **[CEK ULANG]** batas minimum payout dan metode payout untuk Indonesia.

### Angka yang masih asumsi (bukan data Adobe, ganti dengan data lu sendiri setelah 3 bulan)
- Rata-rata royalti per download: pesimis **$0,35**, moderat **$0,50**, optimis **$0,80**.
- Download per aset yang diterima per bulan, di niche logo yang sangat jenuh: pesimis **0,02**, moderat **0,05**, optimis **0,15**. Artinya pada skenario moderat, 100 aset menghasilkan ±5 download per bulan.

### Download yang dibutuhkan untuk $1000
| Skenario | Royalti/download | Download yang dibutuhkan |
|---|---|---|
| Pesimis | $0,35 | ±2.860 |
| Moderat | $0,50 | 2.000 |
| Optimis | $0,80 | 1.250 |

### Pendapatan per bulan berdasarkan ukuran portofolio (aset yang **diterima**)
| Portofolio | Pesimis (0,02 × $0,35) | Moderat (0,05 × $0,50) | Optimis (0,15 × $0,80) |
|---|---|---|---|
| 100 aset | $0,70 | $2,50 | $12 |
| 300 aset | $2,10 | $7,50 | $36 |
| 500 aset | $3,50 | $12,50 | $60 |
| 1.000 aset | $7 | $25 | $120 |

Kesimpulan yang tidak enak: pada skenario moderat, **1.000 aset diterima butuh ±40 bulan untuk mencapai $1000 kumulatif.** Pada skenario optimis, 1.000 aset butuh ±8–9 bulan. Pada skenario pesimis, target ini praktis tidak tercapai dari niche logo saja.

### Biaya waktu
- 45 menit/aset (setelah lancar) × 1.000 aset = **±750 jam kerja**, belum termasuk aset yang ditolak.
- Kalau acceptance rate 60%, untuk dapat 1.000 aset diterima lu harus produksi ±1.670 aset = ±1.250 jam.
- Pada skenario moderat, $1000 / 1.250 jam = **±$0,80 per jam.** Ini angka yang harus lu bandingkan dengan alternatif penggunaan waktu lu.

### Milestone dan titik keputusan
| Milestone | Target | Yang diukur | Keputusan |
|---|---|---|---|
| M1 | 10 aset submit (Bagian D) | Acceptance rate, alasan penolakan | < 50% diterima: perbaiki proses dulu, jangan scale up |
| M2 | 50 aset diterima | Waktu produksi rata-rata per aset | > 90 menit/aset: workflow belum layak di-scale |
| M3 | 100 aset diterima + 3 bulan online | **Download per aset per bulan** (data nyata lu) | < 0,02: niche logo saja tidak akan sampai $1000, pindah fokus (lihat bawah) |
| M4 | 300 aset diterima | Pendapatan per bulan, aset terlaris | Gandakan produksi hanya di kategori yang terbukti laku |
| M5 | $25–$50 pertama tercairkan | Payout benar-benar masuk rekening | Bukti bahwa jalur pajak dan payout jalan |

### Kalau M3 gagal, pindah ke mana
Tetap pakai skill dan workflow yang sama (Inkscape, vector bersih, EPS), tapi geser ke format yang biasanya lebih sering di-download daripada logo tunggal: **icon set, seamless pattern, background abstrak, dan elemen desain untuk template.** Ini juga asumsi; validasi dengan 20–30 aset uji sebelum pindah total.

### Aturan supaya target ini tidak menipu diri sendiri
1. Catat setiap aset di `konsep.xlsx`: tanggal submit, status, tanggal diterima, jumlah download per bulan.
2. Hitung ulang tabel di atas tiap bulan pakai angka lu sendiri. Buang asumsi gue begitu data lu ada.
3. Jangan beli tool berbayar (Vectorizer.AI, Illustrator) sebelum M3 lolos. Biaya tetap memakan target $1000 lu.
4. Jangan upload variasi berlebihan demi menaikkan angka portofolio. Itu jalan tercepat ke penolakan massal dan akun bermasalah.

Sumber royalti: https://helpx.adobe.com/stock/contributor/payments-earnings/royalties-pricing/royalty-rates-assets.html

---

## G. Daftar [CEK ULANG] di halaman resmi

- Persyaratan teknis vector (15–65 MP, 45 MB, RGB, offset 0,0; sudah dicek 7 Nov 2026):
  https://helpx.adobe.com/stock/contributor/submit-your-content/submit-vectors/technical-requirements-for-vector-submissions.html
- Format yang diterima, preview otomatis, ZIP tidak diterima:
  https://helpx.adobe.com/stock/contributor/help/vector-requirements.html
- Aturan vector generative AI:
  https://helpx.adobe.com/stock/contributor/submit-your-content/submit-generative-ai-content/generative-ai-vector-submission-guidelines.html
- Aturan konten generative AI (disclosure, IP pihak ketiga):
  https://helpx.adobe.com/stock/contributor/submit-your-content/submit-generative-ai-content/generative-ai-content-guidelines.html
- Design requirements vector (gagal gue buka dari sini; baca sendiri, terutama soal raster, clipping mask, stray points):
  https://helpx.adobe.com/stock/contributor/submit-your-content/submit-vectors/design-requirements-for-vector-submissions.html
- Royalti (33%, minimum $0,33 per download langganan besar; dicek 7 Nov 2026):
  https://helpx.adobe.com/stock/contributor/payments-earnings/royalties-pricing/royalty-rates-assets.html
- Belum dicek sama sekali: versi EPS yang diterima (cairo vs Illustrator EPS), batas panjang title, batas jumlah keyword, nama kategori di dropdown, form pajak Indonesia, minimum payout, lisensi Firefly dan Vectorizer.AI.
