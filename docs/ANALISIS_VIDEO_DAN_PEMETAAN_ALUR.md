# Analisis video "Cara Jual Gambar Vector AI di Microstock" (26:41) dan pemetaan ke alur kita

Sumber: 80 frame dari video (1 frame per 20 detik). **Narasinya tidak bisa gue transkrip** dari cloud (model speech-to-text diblokir proxy), jadi semua di bawah ini dari apa yang terlihat di layar. Alasan pilihan yang dia ucapkan di video belum gue dengar.

## Alur yang dia pakai (urutan di layar)

| Menit | Tahap | Alat yang terlihat |
|---|---|---|
| 0:00–3:00 | Cari ide: pilih tab Vector, gaya Flat Design, klik "Generate", dapat daftar ide asset + indikator demand/kompetisi | **StockScope AI** (app buatan sendiri di Google AI Studio) |
| 3:00–5:00 | Tempel daftar ide ke ChatGPT dengan instruksi: ubah jadi prompt text-to-image, tambahkan "isolated on white background" di akhir, 1 prompt 1 baris, 1 objek saja, keluarkan dalam code block | ChatGPT |
| 5:00–10:00 | Generate gambar massal dari file prompt | "Imagen Generator" (aplikasi desktop) memakai **kredensial lab Google Cloud Skills Boost** (akun `student-…@qwiklabs.net`, project sementara, service account JSON) |
| 9:20–13:00 | Trace massal ke vector | Illustrator + script "AutoTrace Microstock" (batch folder → AI/EPS/SVG) |
| 12:00–17:40 | Isi metadata massal (judul, deskripsi, keyword) lewat LLM lalu tanam ke file | "Metacraft" + ffmpeg/exiftool/ghostscript, API lewat SumoPod |
| 20:00–26:20 | Upload dan submit | Adobe Stock (halaman upload, tombol Upload CSV) dan **Dreamstime** (FTP FileZilla + ekstensi auto-submit) |

## Yang gue tiru, yang gue ganti, yang gue tolak

| Tahap video | Keputusan | Pengganti di alur kita |
|---|---|---|
| Cari ide + cek demand | **Tiru** idenya, ganti alatnya | Gue yang riset niche dan cek kepadatan di Adobe Stock (sudah dilakukan untuk 10 prompt pertama). StockScope AI nggak dibagikan di video, dan skor demand-nya cuma tebakan model. |
| ChatGPT jadi prompt 1 baris | **Tiru persis** | Gue yang tulis prompt, jadi di xlsx harian. Aturannya sama: 1 prompt 1 objek, akhiri dengan latar putih terisolasi. |
| Generate massal pakai kredensial Skills Boost | **Tolak** | Lab Skills Boost memberi kredensial sementara untuk belajar, bukan untuk produksi komersial. Memakainya buat bulk generate melanggar tujuan lab-nya dan bisa bikin akun Google lu ditutup. Ganti: Google Flow di akun lu sendiri (sesuai rencana lu), atau API berbayar kalau mau otomatis. |
| Trace massal pakai Illustrator | **Ganti** | `badge-tool` (vtracer + Inkscape). Lu nggak punya Illustrator. Tinggal ditambah mode batch satu folder, belum gue bikin. |
| Metadata massal lewat LLM | **Tiru** | Gue tulis title dan keyword, keluar sebagai CSV untuk tombol Upload CSV di portal Adobe. Nggak perlu Metacraft atau SumoPod. |
| Upload FTP + ekstensi auto-submit Dreamstime | **Tolak untuk sekarang** | Ekstensi pihak ketiga yang ngisi form otomatis di akun lu itu risiko akun. Dreamstime juga marketplace lain dengan aturan sendiri. Fokus Adobe dulu. |

## Yang gue lihat tapi nggak bisa gue pastikan

- Video ini menjual workflow volume. Hasil yang dia tampilkan di layar (orang di kursi, bohlam, hati+perisai) generik. Gue nggak lihat angka penjualan dia, jadi nggak ada bukti workflow ini menghasilkan.
- Dia submit ke Dreamstime dengan kategori "Generative AI" tercentang. Jadi dia disclose AI di sana, bukan menyembunyikan. Ini mematahkan dugaan lu soal klaim non-AI, setidaknya untuk video ini.
- Tool yang dia pakai adalah buatan dia sendiri, tidak bisa gue tiru persis. Yang bisa ditiru adalah urutannya.
