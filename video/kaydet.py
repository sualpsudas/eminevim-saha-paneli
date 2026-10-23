"""tanitim.html → MP4 (1920×1080, 25 kare/sn, sessiz).

Her kare için sayfadaki cizim(t) çağrılır ve ekran görüntüsü ffmpeg'e verilir; süre tarayıcı hızından bağımsızdır.
Gerekenler: Playwright (Chrome) + imageio-ffmpeg (pip install imageio-ffmpeg).

  python video/kaydet.py                    → video/tasarruf-yanimda-tanitim.mp4
  python video/kaydet.py --kare 12 40.5     → yalnız o saniyelerin PNG'leri (video/onizleme/)
"""
import argparse
import pathlib
import subprocess

import imageio_ffmpeg
from playwright.sync_api import sync_playwright

KLASOR = pathlib.Path(__file__).resolve().parent
FPS = 25

ap = argparse.ArgumentParser()
ap.add_argument("--kare", nargs="*", type=float, help="yalnız bu saniyelerin görüntüsünü al")
ap.add_argument("--cikti", default=str(KLASOR / "tasarruf-yanimda-tanitim.mp4"))
arg = ap.parse_args()

with sync_playwright() as p:
    tarayici = p.chromium.launch(channel="chrome")
    sayfa = tarayici.new_page(viewport={"width": 1920, "height": 1080})
    sayfa.goto((KLASOR / "tanitim.html").as_uri() + "?kayit=1")
    sayfa.evaluate("Promise.all([...document.images].map(i => i.decode().catch(() => {})))")
    sure = sayfa.evaluate("SURE")

    if arg.kare is not None:
        hedef = KLASOR / "onizleme"
        hedef.mkdir(exist_ok=True)
        for t in arg.kare:
            sayfa.evaluate("t => cizim(t)", t)
            sayfa.screenshot(path=str(hedef / f"kare_{t:06.2f}.png"))
        print(f"{len(arg.kare)} kare: {hedef}")
    else:
        ffmpeg = subprocess.Popen([
            imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error",
            "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
            "-vf", "scale=out_range=tv,format=yuv420p", "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", arg.cikti,
        ], stdin=subprocess.PIPE)
        toplam = int(sure * FPS)
        for i in range(toplam):
            sayfa.evaluate("t => cizim(t)", i / FPS)
            ffmpeg.stdin.write(sayfa.screenshot(type="jpeg", quality=95))
            if i % (FPS * 10) == 0:
                print(f"{i / FPS:5.0f} / {sure:.0f} sn", flush=True)
        ffmpeg.stdin.close()
        ffmpeg.wait()
        print("bitti:", arg.cikti)
    tarayici.close()
