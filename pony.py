#!/usr/bin/env python3
import urllib.request
import json
import os
from PIL import Image

HEADERS = {'User-Agent': 'Mozilla/5.0'}
URL = 'https://derpibooru.org/api/v1/json/search/images?q=safe,pony&sf=random&per_page=2'


def buka(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=10) as r:
        return r.read()


def buat_kecil(path_asli, path_kecil):
    img = Image.open(path_asli)
    img.thumbnail((800, 800))

    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
        latar = Image.new("RGB", img.size, (255, 255, 255))
        latar.paste(img, mask=img.split()[-1])
        img = latar
    else:
        img = img.convert("RGB")
    img.save(path_kecil)
    return img


def tampilkan(img):
    import tkinter as tk
    from PIL import ImageTk
    root = tk.Tk()
    foto = ImageTk.PhotoImage(img)
    tk.Label(root, image=foto).pack()
    root.mainloop()


def fetch_pony():
    try:
        os.makedirs("lib", exist_ok=True)
        data = json.loads(buka(URL).decode())
        if not data.get('images'):
            print("FAILED: tidak ada hasil")
            return
        gambar = data['images'][0]
        ext = gambar.get('format', 'jpg')
        path_asli = f"lib/pony_{gambar['id']}.{ext}"
        path_kecil = "lib/kecil.jpg"
        with open(path_asli, 'wb') as f:
            f.write(buka(gambar['representations']['large']))
        img = buat_kecil(path_asli, path_kecil)
        print("SUCCESS")
        print("Disimpan di:", os.path.abspath(path_kecil))
        tampilkan(img)
    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == '__main__':
    fetch_pony() 
    
    