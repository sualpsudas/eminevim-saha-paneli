"""Tek parça dış seslendirmeyi (ElevenLabs) 11 bölüme ayırır: video/ses-<ad>/*.mp3 + plan.js (ses_uret.py çıktısıyla aynı biçim).

Kelime zamanları Whisper'dan gelir (ElevenLabs sitesi vermez); METIN'le hizalanır, kesim yeri bölüm arasındaki en sessiz andır.
  python video/ses_bol.py <kaynak.mp3> <whisper.json> ses-ahmet
whisper.json: [{"w": [[baş, son, kelime], ...]}, ...] (faster-whisper medium, word_timestamps; klasöre kelime_ham.json diye kopyalanır)
"""
import ast
import difflib
import json
import pathlib
import re
import shutil
import subprocess
import sys

import imageio_ffmpeg
import numpy as np

KLASOR = pathlib.Path(__file__).resolve().parent
FF = imageio_ffmpeg.get_ffmpeg_exe()
ORNEK = 16000


def metin_al():
    for n in ast.parse((KLASOR / "ses_uret.py").read_text(encoding="utf-8")).body:
        if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "METIN":
            return ast.literal_eval(n.value)


def sade(w):
    w = w.replace("I", "ı").replace("İ", "i").lower().replace("â", "a")
    return re.sub(r"[^a-zçğıöşü]", "", w)


def sessiz_an(ses, bas, son):
    """[bas, son] içinde en düşük enerjili 20 ms'nin ortası"""
    a, b, p = int(bas * ORNEK), int(son * ORNEK), int(.02 * ORNEK)
    if b - a <= p:
        return (bas + son) / 2
    enerji = [float(np.mean(ses[i:i + p] ** 2)) for i in range(a, b - p, p // 2)]
    return (a + int(np.argmin(enerji)) * (p // 2) + p / 2) / ORNEK


kaynak, ham, ad = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3]
hedef = KLASOR / ad
hedef.mkdir(exist_ok=True)
METIN = metin_al()
kaynak_kelime = [w for s in json.loads(ham.read_text(encoding="utf-8")) for w in s["w"]]
beklenen = [(k, w) for k, m in METIN.items() for w in m.split()]

# hizalama: eşleşmeyen kelimeye (Whisper yanlış duyduysa) komşularından zaman verilir
eslesme = difflib.SequenceMatcher(None, [sade(w) for _, w in beklenen], [sade(w[2]) for w in kaynak_kelime], autojunk=False)
zaman = [None] * len(beklenen)
for blok in eslesme.get_matching_blocks():
    for i in range(blok.size):
        zaman[blok.a + i] = kaynak_kelime[blok.b + i][:2]
bilinen = [i for i, z in enumerate(zaman) if z]
eksik = [beklenen[i][1] for i, z in enumerate(zaman) if not z]
for i, z in enumerate(zaman):
    if not z:
        once = max(j for j in bilinen if j < i)
        sonra = min(j for j in bilinen if j > i)
        o = zaman[once][1] + (zaman[sonra][0] - zaman[once][1]) * (i - once) / (sonra - once)
        zaman[i] = [o, o]
print("eşleşen", len(bilinen), "/", len(beklenen), "| Whisper'ın farklı duyduğu:", eksik)

ham_ses = subprocess.run([FF, "-v", "error", "-i", str(kaynak), "-f", "f32le", "-ac", "1", "-ar", str(ORNEK), "-"], capture_output=True, check=True).stdout
ses = np.frombuffer(ham_ses, np.float32)
toplam = len(ses) / ORNEK

sira = list(METIN)
ilk = {k: min(i for i, (x, _) in enumerate(beklenen) if x == k) for k in sira}
son = {k: max(i for i, (x, _) in enumerate(beklenen) if x == k) for k in sira}
kesim = [0.0]
for a, b in zip(sira, sira[1:]):
    kesim.append(sessiz_an(ses, zaman[son[a]][1] - .08, zaman[ilk[b]][0] + .08))
kesim.append(toplam)

plan = {}
for n, k in enumerate(sira):
    bas, bit = kesim[n], kesim[n + 1]
    subprocess.run([FF, "-y", "-v", "error", "-ss", f"{bas:.3f}", "-t", f"{bit - bas:.3f}", "-i", str(kaynak), "-af",
                    f"afade=t=in:d=0.01,afade=t=out:st={bit - bas - .01:.3f}:d=0.01", "-c:a", "libmp3lame", "-b:a", "192k", str(hedef / f"{k}.mp3")], check=True)
    kelime = [[round(max(0, zaman[i][0] - bas), 3), beklenen[i][1]] for i in range(ilk[k], son[k] + 1)]
    plan[k] = {"sure": round(bit - bas, 2), "metin": METIN[k], "kelime": kelime}
    print(k, plan[k]["sure"], len(kelime))
(hedef / "plan.js").write_text("/* ses_bol.py üretir */\nvar SES = " + json.dumps(plan, ensure_ascii=False) + ";\n", encoding="utf-8")
if ham.resolve() != (hedef / "kelime_ham.json").resolve():
    shutil.copy(ham, hedef / "kelime_ham.json")
