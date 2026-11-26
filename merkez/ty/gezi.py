"""Hareketli örnek SPY'lerin "dur-kalk" saha günü (2026-11-26).

Her hareketli SPY kendi ilçesinde rastgele bir hedef seçer → oraya en hızlı rotayla, yoldaki İBB anlık hızıyla gider
(atama.en_hizli_rota + trafik.zamanli_rota, sunumdaki yola çıkışla aynı) → varınca 10-30 dk durur ("ziyarette") → yeni hedef.
Süreler sunumdaki gibi hızlandırılmış: gerçek 1 dk = 3 sn (sunum.YOL_SN_DK). Plan yalnız bellekte tutulur (veri.json'a yazılmaz);
merkez yeniden başlayınca SPY bulunduğu yerden yeniden başlar. Çağrı alıp yola çıkınca (don/yolda/görüşme) ya da yönetici haritada
taşıyınca gezi biter; çağrı kapanınca SPY son yerinden (müşterinin adresi) devam eder. Konum: konum.py konum_ve_kaynak → gezi.konum;
takip sayfası aynı rotayı spy_ozet'teki geziRota ile aynı formülle canlandırır.
"""
import math
import random
import threading
import time

from . import bolge
from .yardim import simdi

HIZ_SN_DK = 3                 # gerçek 1 dk = sunumda 3 sn (sunum.YOL_SN_DK ile aynı)
DURAK_DK = (10, 30)           # hedefte bekleme (gerçek dk)
HEDEF_M = (1200, 5000)        # yeni hedef bulunduğu yerden bu kadar uzakta (kuş uçuşu)
TUR_SN = 2                    # planlayıcı bu sıklıkla bakar
_durum = {}                   # id → {"r": [[enlem, boylam, varış sn]…], "bas": ms, "sure": ms, "bit": ms (durak sonu)}
_kilit = threading.Lock()


def _m(a, b):
    return math.hypot((b[0] - a[0]) * 110540, (b[1] - a[1]) * 111320 * math.cos(math.radians(a[0])))


def konum(spy_id, t_ms=None):
    """Planı olan hareketli SPY'nin o anki yeri {"lat", "lng"} ya da None (plan yoksa çağıran eski düzene düşer)."""
    with _kilit:
        d = _durum.get(spy_id)
    if not d:
        return None
    r = d["r"]
    p = min(1.0, max(0.0, ((t_ms if t_ms is not None else simdi()) - d["bas"]) / (d["sure"] or 1)))
    hedef = p * r[-1][2]
    i = next((j for j in range(1, len(r)) if r[j][2] >= hedef), len(r) - 1)
    a, b = r[i - 1], r[i]
    f = (hedef - a[2]) / (b[2] - a[2]) if b[2] > a[2] else 1
    return {"lat": a[0] + (b[0] - a[0]) * f, "lng": a[1] + (b[1] - a[1]) * f}


def ozet(spy_id):
    """Takip sayfası için: {"r", "bas", "sure", "bit"} ya da None."""
    with _kilit:
        d = _durum.get(spy_id)
        return dict(d) if d else None


def _hedef(ilce, bas):
    bolge._yukle()
    halkalar = dict(bolge._ilceler or []).get(ilce)
    if not halkalar:
        return None
    nok = [p for h in halkalar for p in h]
    a0, a1 = min(p[0] for p in nok), max(p[0] for p in nok)
    b0, b1 = min(p[1] for p in nok), max(p[1] for p in nok)
    for _ in range(60):
        h = (random.uniform(a0, a1), random.uniform(b0, b1))
        if any(bolge._icinde(h[0], h[1], x) for x in halkalar) and HEDEF_M[0] <= _m(bas, h) <= HEDEF_M[1]:
            return {"lat": h[0], "lng": h[1]}
    return None


def _planla(s, bas):
    from . import trafik
    from .atama import en_hizli_rota
    h = _hedef(s.get("ilce"), (bas["lat"], bas["lng"]))
    if not h:
        return None
    c = en_hizli_rota(bas, h)
    if c and c.get("rota"):
        r = trafik.zamanli_rota(c["rota"], en_az_m=60, en_cok=80)
    else:  # yol servisi yoksa düz çizgi, 25 km/s
        r = [[bas["lat"], bas["lng"], 0], [h["lat"], h["lng"], round(_m((bas["lat"], bas["lng"]), (h["lat"], h["lng"])) / (25 / 3.6))]]
    if len(r) < 2:
        return None
    t = simdi()
    sure = int(max(6, r[-1][2] / 60 * HIZ_SN_DK) * 1000)
    durak = int(random.uniform(*DURAK_DK) * HIZ_SN_DK * 1000)
    return {"r": r, "bas": t, "sure": sure, "bit": t + sure + durak}


def _tur():
    from . import depo
    from .konum import konum_ve_kaynak
    from .personel import SIM_SPYLER
    with depo.kilit:
        veri = depo.oku()
    mesgul = {x.get("repId") for x in veri["kayitlar"].values() if x.get("durum") in ("yolda", "gorusme", "gorusmede") or x.get("don")}
    elle = veri.get("elleKonum") or {}
    for s in SIM_SPYLER:
        i = s["id"]
        if i in mesgul or i in elle:
            with _kilit:
                _durum.pop(i, None)
            continue
        with _kilit:
            d = _durum.get(i)
        if d and simdi() < d["bit"]:
            continue
        if d:
            bas = {"lat": d["r"][-1][0], "lng": d["r"][-1][1]}
        else:
            bas = dict(konum_ve_kaynak(veri, veri["spyler"].get(i) or s)[0])
        try:
            yeni = _planla(s, bas)
        except (OSError, ValueError, KeyError):
            yeni = None
        if yeni:
            with _kilit:
                _durum[i] = yeni


def baslat():
    def dongu():
        while True:
            try:
                _tur()
            except Exception:  # planlayıcı hiç durmasın; bir sonraki turda yeniden dener
                pass
            time.sleep(TUR_SN)
    threading.Thread(target=dongu, daemon=True).start()
