"""Siapkan paket upload Dreamstime dari folder hasil Adobe (EPS + metadata_adobe.csv).

Dreamstime tidak menerima EPS sebagai file utama: file utama = JPG resolusi tinggi,
EPS ditempel sebagai "additional format". Skrip ini:
  1. render tiap EPS jadi JPG 5334x3000 (Ghostscript, -dEPSCrop, 72 dpi = 1 px/pt),
  2. menanam title, description (dengan kalimat disclosure AI) dan keyword ke IPTC/XMP JPG (exiftool),
  3. menyalin EPS dan menulis metadata_dreamstime.csv.

Pakai:
  python tools/dreamstime_prep.py OUT_DIR SRC_DIR [SRC_DIR ...] [--only logo-022,logo-023]
SRC_DIR berisi eps/*.eps dan metadata_adobe.csv (format keluaran batch Adobe).
Butuh: gs (ghostscript), exiftool.
"""
import argparse
import csv
import shutil
import subprocess
import sys
from pathlib import Path

AI_SENTENCE = "This image is generated using an AI (generative AI tool) and vectorized."
CATEGORIES = [
    "Illustrations & Clipart > AI-generated",  # WAJIB, tanpa ini langsung ditolak
    "Illustrations & Clipart > Vector",
    "Business > Logos/Signs (pilih yang paling dekat di portal)",
]


def need(tool):
    if not shutil.which(tool):
        sys.exit(f"butuh '{tool}' (apt-get install ghostscript libimage-exiftool-perl)")


def render(eps: Path, jpg: Path):
    subprocess.run([
        "gs", "-q", "-dSAFER", "-dBATCH", "-dNOPAUSE", "-dEPSCrop", "-sDEVICE=jpeg",
        "-dJPEGQ=95", "-r72", "-dTextAlphaBits=4", "-dGraphicsAlphaBits=4",
        f"-sOutputFile={jpg}", str(eps),
    ], check=True)


def embed(jpg: Path, title: str, desc: str, kws):
    args = ["exiftool", "-q", "-overwrite_original", "-codedcharacterset=utf8",
            f"-IPTC:ObjectName={title[:64]}", f"-XMP-dc:Title={title}",
            f"-IPTC:Caption-Abstract={desc}", f"-XMP-dc:Description={desc}"]
    args += [f"-IPTC:Keywords={k}" for k in kws] + [f"-XMP-dc:Subject={k}" for k in kws]
    subprocess.run(args + [str(jpg)], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("src", nargs="+")
    ap.add_argument("--only", default="", help="ID dipisah koma, mis. logo-022,logo-023")
    a = ap.parse_args()
    need("gs")
    need("exiftool")
    only = {s.strip() for s in a.only.split(",") if s.strip()}
    out = Path(a.out)
    (out / "jpg").mkdir(parents=True, exist_ok=True)
    (out / "eps").mkdir(exist_ok=True)
    rows = []
    for src in map(Path, a.src):
        with open(src / "metadata_adobe.csv", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                b = Path(r["Filename"]).stem
                if only and b not in only:
                    continue
                title = r["Title"].strip()
                kws = [k.strip() for k in r["Keywords"].split(",") if k.strip()]
                if "ai generated" not in kws:
                    kws.append("ai generated")
                desc = f"{title}. Editable vector badge logo template. {AI_SENTENCE}"
                eps = src / "eps" / f"{b}.eps"
                jpg = out / "jpg" / f"{b}.jpg"
                render(eps, jpg)
                embed(jpg, title, desc, kws)
                shutil.copy(eps, out / "eps" / eps.name)
                rows.append({"Filename": jpg.name, "Additional format": eps.name, "Title": title,
                             "Description": desc, "Keywords": ", ".join(kws),
                             "Category 1": CATEGORIES[0], "Category 2": CATEGORIES[1],
                             "Category 3": CATEGORIES[2]})
    if not rows:
        sys.exit("tidak ada file yang diproses")
    with open(out / "metadata_dreamstime.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} file siap di {out}")


if __name__ == "__main__":
    main()
