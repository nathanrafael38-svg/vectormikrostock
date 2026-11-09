# Agent Vector Microstock

Agen produksi badge/emblem logo vector EPS untuk Adobe Stock. Dibuat untuk non-desainer: Nathan generate gambar di Google Flow, agen mengurus sisanya sampai file siap upload.

Alur harian ("C-Vector Day N"):
1. `riset-niche-harian` → 10 prompt dalam xlsx.
2. Nathan generate di Google Flow, upload PNG (`logo-0XX.png`).
3. `proses-png` → EPS 5334×3000 pt + QC + contact sheet.
4. `metadata-qc-submit` → title/keyword/CSV + checklist. Nathan upload dan submit manual, dengan centang generative AI.

Lihat `CLAUDE.md` untuk aturan keras dan spesifikasi, `docs/` untuk panduan dan hitungan menuju $1000 (skenario moderat: ±40 bulan untuk 1.000 aset diterima).

Setup: `./setup.sh`. Jalankan: `python -m agent_vector.batch inbox --registry data/registry.json`.
Font: hanya SIL OFL. Status: belum ada file yang lolos review Adobe.
