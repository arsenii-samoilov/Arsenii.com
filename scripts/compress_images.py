#!/usr/bin/env python3
"""Compress site images: optimize JPEG/PNG in place and refresh WebP companions."""
import os
import subprocess
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("pip install Pillow")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRS = ["images", "food", "photos"]
MAX_WIDTH = 1920
JPEG_QUALITY = 82
WEBP_QUALITY = 82
MIN_BYTES = 200 * 1024  # only recompress files >= 200KB (or missing webp)
CWEBP = "/opt/homebrew/bin/cwebp"


def human(n):
    for u in ("B", "KB", "MB"):
        if n < 1024:
            return "%.1f%s" % (n, u)
        n /= 1024
    return "%.1fGB" % n


def optimize_image(path):
    before = os.path.getsize(path)
    ext = os.path.splitext(path)[1].lower()
    with Image.open(path) as im:
        if im.mode in ("RGBA", "P"):
            im = im.convert("RGB")
            ext = ".jpg"
            out_path = os.path.splitext(path)[0] + ".jpg"
        else:
            out_path = path
        w, h = im.size
        if w > MAX_WIDTH:
            nh = int(h * MAX_WIDTH / w)
            im = im.resize((MAX_WIDTH, nh), Image.Resampling.LANCZOS)
        if ext in (".jpg", ".jpeg") or out_path != path:
            im.save(out_path, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
        elif ext == ".png":
            im.save(path, "PNG", optimize=True)
        else:
            return before, before, None
    after = os.path.getsize(out_path)
    return before, after, out_path


def make_webp(src):
    dst = os.path.splitext(src)[0] + ".webp"
    cmd = [CWEBP, "-q", str(WEBP_QUALITY), src, "-o", dst]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return dst


def main():
    if not os.path.isfile(CWEBP):
        sys.exit("cwebp not found at %s" % CWEBP)

    total_before = total_after = 0
    count = 0
    for d in DIRS:
        base = os.path.join(ROOT, d)
        if not os.path.isdir(base):
            continue
        for name in sorted(os.listdir(base)):
            if name.startswith("."):
                continue
            low = name.lower()
            if not low.endswith((".jpg", ".jpeg", ".png")):
                continue
            path = os.path.join(base, name)
            size = os.path.getsize(path)
            webp = os.path.splitext(path)[0] + ".webp"
            need = size >= MIN_BYTES or not os.path.isfile(webp)
            if not need:
                continue
            try:
                b, a, out = optimize_image(path)
                src = out or path
                make_webp(src)
                total_before += b
                total_after += os.path.getsize(src)
                count += 1
                print("%s  %s -> %s" % (os.path.relpath(path, ROOT), human(b), human(os.path.getsize(src))))
            except Exception as e:
                print("SKIP", path, e)

    print("\nCompressed %d files: %s -> %s (saved %s)" % (
        count, human(total_before), human(total_after), human(total_before - total_after)))


if __name__ == "__main__":
    main()
