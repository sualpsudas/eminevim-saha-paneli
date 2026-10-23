"""tanitim.html → MP4 (1920×1080, 25 kare/sn) + seslendirme + müzik + açılıp kapanabilen altyazı.

Her kare için sayfadaki cizim(t) çağrılır ve ekran görüntüsü ffmpeg'e verilir; süre tarayıcı hızından bağımsızdır.
Ses parçalarının yeri sayfanın SES_PLAN listesinden gelir (önce: python video/ses_uret.py).
Gerekenler: Playwright (Chrome), imageio-ffmpeg, numpy (müzik için).

  python video/kaydet.py                    → video/tasarruf-yanimda-tanitim.mp4 (+ .srt)
  python video/kaydet.py --kare 12 40.5     → yalnız o saniyelerin PNG'leri (video/onizleme/)
"""
import argparse
import pathlib
import subprocess
import sys

import imageio_ffmpeg
from playwright.sync_api import sync_playwright

KLASOR = pathlib.Path(__file__).resolve().parent
FPS = 25
MUZIK_SES = 0.13  # konuşmanın altında kısık

ap = argparse.ArgumentParser()
ap.add_argument("--kare", nargs="*", type=float, help="yalnız bu saniyelerin görüntüsünü al")
ap.add_argument("--cikti", default=str(KLASOR / "tasarruf-yanimda-tanitim.mp4"))
arg = ap.parse_args()
FF = imageio_ffmpeg.get_ffmpeg_exe()


def zaman(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


with sync_playwright() as p:
    tarayici = p.chromium.launch(channel="chrome")
    sayfa = tarayici.new_page(viewport={"width": 1920, "height": 1080})
    sayfa.goto((KLASOR / "tanitim.html").as_uri() + "?kayit=1")
    sayfa.evaluate("Promise.all([...document.images].map(i => i.decode().catch(() => {})))")
    sure = sayfa.evaluate("SURE")
    plan = sayfa.evaluate("SES_PLAN")

    if arg.kare is not None:
        hedef = KLASOR / "onizleme"
        hedef.mkdir(exist_ok=True)
        for t in arg.kare:
            sayfa.evaluate("t => cizim(t)", t)
            sayfa.screenshot(path=str(hedef / f"kare_{t:06.2f}.png"))
        print(f"{len(arg.kare)} kare: {hedef}  (toplam {sure:.1f} sn)")
        tarayici.close()
        sys.exit()

    gecici = KLASOR / "_goruntu.mp4"
    ffmpeg = subprocess.Popen([
        FF, "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
        "-vf", "scale=out_range=tv,format=yuv420p", "-c:v", "libx264", "-preset", "slow", "-crf", "20",
        "-pix_fmt", "yuv420p", str(gecici),
    ], stdin=subprocess.PIPE)
    toplam = int(sure * FPS)
    for i in range(toplam):
        sayfa.evaluate("t => cizim(t)", i / FPS)
        ffmpeg.stdin.write(sayfa.screenshot(type="jpeg", quality=95))
        if i % (FPS * 10) == 0:
            print(f"{i / FPS:5.0f} / {sure:.0f} sn", flush=True)
    ffmpeg.stdin.close()
    ffmpeg.wait()
    tarayici.close()

# altyazı
srt = pathlib.Path(arg.cikti).with_suffix(".srt")
srt.write_text("\n".join(f"{i + 1}\n{zaman(x['t'])} --> {zaman(x['t'] + x['sure'])}\n{x['metin']}\n" for i, x in enumerate(plan)), encoding="utf-8")

# müzik
subprocess.run([sys.executable, str(KLASOR / "muzik_uret.py"), f"{sure + 1:.1f}"], check=True)

# birleştirme: görüntü + konuşma parçaları (yerinde) + müzik + altyazı izi
girdi = ["-i", str(gecici)]
filtre = []
for k, x in enumerate(plan):
    girdi += ["-i", str(KLASOR / "ses" / f"{x['id']}.mp3")]
    filtre.append(f"[{k + 1}:a]aresample=44100,adelay={int(x['t'] * 1000)}:all=1[s{k}]")
m = len(plan) + 1
girdi += ["-i", str(KLASOR / "ses" / "muzik.wav"), "-i", str(srt)]
filtre.append(f"[{m}:a]aresample=44100,volume={MUZIK_SES}[muz]")
filtre.append("".join(f"[s{k}]" for k in range(len(plan))) + f"[muz]amix=inputs={len(plan) + 1}:normalize=0:duration=longest,alimiter=limit=0.95[a]")
subprocess.run([
    FF, "-y", "-loglevel", "error", *girdi, "-filter_complex", ";".join(filtre),
    "-map", "0:v", "-map", "[a]", "-map", f"{m + 1}:s",
    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-c:s", "mov_text", "-metadata:s:s:0", "language=tur", "-disposition:s:0", "-default",
    "-t", f"{sure:.2f}", "-movflags", "+faststart", arg.cikti,
], check=True)
gecici.unlink()
print("bitti:", arg.cikti)
