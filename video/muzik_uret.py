"""Sakin arka plan müziği (telifsiz, kodla üretilir): yumuşak akor dokusu + hafif arpej, 72 vuruş/dk.

  python video/muzik_uret.py 160   → video/ses/muzik.wav (saniye)
Gerekenler: numpy.
"""
import pathlib
import sys
import wave

import numpy as np

SR = 44100
SURE = float(sys.argv[1]) if len(sys.argv) > 1 else 160
VURUS = 60 / 72
AKOR_SURE = VURUS * 8  # iki ölçü
# Cmaj7 · Am7 · Fmaj7 · G6 (MIDI)
AKORLAR = [[48, 64, 67, 71], [45, 64, 67, 72], [41, 65, 69, 72], [43, 62, 67, 71]]


def hz(n):
    return 440 * 2 ** ((n - 69) / 12)


t = np.arange(int(SURE * SR)) / SR
pad = np.zeros_like(t)
arp = np.zeros_like(t)
i = 0
while i * AKOR_SURE < SURE:
    a0 = i * AKOR_SURE
    akor = AKORLAR[i % 4]
    # akor dokusu: yavaş giriş/çıkış, komşu akorlarla örtüşür
    bas, son = int(max(0, a0 - 1.2) * SR), int(min(SURE, a0 + AKOR_SURE + 1.2) * SR)
    yt = t[bas:son] - (a0 - 1.2)
    zarf = np.clip(yt / 1.6, 0, 1) * np.clip((AKOR_SURE + 2.4 - yt) / 1.6, 0, 1)
    for k, n in enumerate(akor):
        f = hz(n)
        ses = np.sin(2 * np.pi * f * t[bas:son]) + 0.5 * np.sin(2 * np.pi * f * 1.003 * t[bas:son] + k)
        pad[bas:son] += zarf * ses * (0.55 if k == 0 else 0.32)
    # arpej: akor seslerinden çeyrek notalar, yumuşak sönüm
    desen = [akor[1] + 12, akor[2] + 12, akor[3] + 12, akor[2] + 12, akor[1] + 12, akor[2] + 12, akor[3], akor[2] + 12]
    for j, n in enumerate(desen):
        n0 = a0 + j * VURUS
        if n0 >= SURE:
            break
        b, s = int(n0 * SR), int(min(SURE, n0 + 2.5) * SR)
        nt = t[b:s] - n0
        f = hz(n)
        arp[b:s] += np.exp(-nt * 2.2) * (1 - np.exp(-nt * 60)) * (np.sin(2 * np.pi * f * nt) + 0.18 * np.sin(4 * np.pi * f * nt))
    i += 1

karisim = pad * 0.5 + arp * 0.32
karisim *= np.clip(t / 2.5, 0, 1) * np.clip((SURE - t) / 4, 0, 1)
karisim = karisim / np.max(np.abs(karisim)) * 0.5

hedef = pathlib.Path(__file__).resolve().parent / "ses" / "muzik.wav"
with wave.open(str(hedef), "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((karisim * 32767).astype(np.int16).tobytes())
print("muzik:", hedef, f"{SURE:.0f} sn")
