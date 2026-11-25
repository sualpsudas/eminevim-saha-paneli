"""Hareketli örnek SPY'lerin (merkez/ty/personel.py SIM_SPYLER) yol üzerindeki dolaşma rotalarını üretir → veri/sim-yollar.js.
Her SPY için kendi ilçesinde tabanı çevresinde 3 rastgele (sabit tohumlu) durak seçilir, OSRM genel sunucusundan sürüş rotası (taban→durak→…→taban) alınır.
Çalıştırma (internet gerekir; bir kez, rota değişecekse yeniden):  python araclar/sim_yol_uret.py   (merkez klasöründen ya da depo kökünden)
Merkez ve takip sayfası bu dosyayı okur (konum.gezi_konum / takip.html animKonum)."""
import json
import random
import sys
import urllib.request
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK / "merkez"))
from ty.bolge import ilce_bul  # noqa: E402
from ty.personel import SIM_SPYLER  # noqa: E402

sonuc = {}
for s in SIM_SPYLER:
    rnd = random.Random(s["id"])
    duraklar = []
    while len(duraklar) < 3:
        la, ln = s["lat"] + rnd.uniform(-0.012, 0.012), s["lng"] + rnd.uniform(-0.016, 0.016)
        if ilce_bul(la, ln) == s["ilce"] and ((la - s["lat"]) ** 2 + ((ln - s["lng"]) * 0.76) ** 2) ** 0.5 > 0.006:
            duraklar.append((la, ln))
    noktalar = [(s["lat"], s["lng"])] + duraklar + [(s["lat"], s["lng"])]
    url = "https://router.project-osrm.org/route/v1/driving/" + ";".join(f"{ln:.6f},{la:.6f}" for la, ln in noktalar) + "?overview=full&geometries=geojson"
    j = json.loads(urllib.request.urlopen(url, timeout=40).read())
    yol = [[round(c[1], 5), round(c[0], 5)] for c in j["routes"][0]["geometry"]["coordinates"]]
    sonuc[s["id"]] = yol
    print(s["id"], len(yol), "nokta", round(j["routes"][0]["distance"] / 1000, 1), "km")
(KOK / "veri" / "sim-yollar.js").write_text(
    "/* ÜRETİLEN DOSYA — araclar/sim_yol_uret.py. Hareketli örnek SPY'lerin yol üstü dolaşma rotaları [enlem, boylam]. */\nwindow.TY_SIM_YOL = "
    + json.dumps(sonuc, separators=(",", ":")) + ";\n", encoding="utf-8")
