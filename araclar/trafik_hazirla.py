"""İBB saatlik trafik yoğunluğu verisinden pilot bölge için "tipik trafik çarpanı" üretir → veri/trafik-carpan.json

Kaynak: İBB Açık Veri Portalı, "Saatlik Trafik Yoğunluk Veri Seti" (aylık CSV, geohash-6 kareleri; İBB Açık Veri Lisansı, kaynak gösterilir).
  https://data.ibb.gov.tr/dataset/hourly-traffic-density-data-set
Kullanım: python araclar/trafik_hazirla.py <indirilen CSV'ler...>   (CSV'ler depoya girmez; her biri ~140 MB)

Hesap: her karede serbest akış hızı = gece 02:00-05:00 ortalama hızlarının medyanı; o kare, gün tipi (hafta içi / cumartesi / pazar)
ve saat için çarpan = serbest akış hızı / o saatteki ortalama hızların medyanı (1 ile 3 arasında). Atamada yol servisinin trafiksiz
süresi bu çarpanla çarpılır (merkez/ty/trafik.py). Anlık trafik DEĞİL: o gün ve saatin geçmiş aylardaki tipik trafiği.
"""
import csv
import json
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
SINIR = KOK / "assets" / "pilot-sinirlar.js"
CIKTI = KOK / "veri" / "trafik-carpan.json"
GUN = ("hi", "cmt", "pzr")  # hafta içi, cumartesi, pazar
TATIL = {"2024-10-29", "2025-01-01"}  # resmî tatil günleri hesaba katılmaz
PAY = 0.02  # pilot sınırının çevresinde ek pay (derece): sınırdaki yollar da girsin
EN_AZ = 6   # bir saat diliminde bu kadardan az ölçüm varsa o saat genel değere bırakılır


def kutu():
    m = re.search(r"window\.TY_SINIRLAR\s*=\s*(\{.*\});?\s*$", SINIR.read_text(encoding="utf-8"), re.S)
    nk = [p for i in json.loads(m.group(1))["ilceler"] for h in i["halkalar"] for p in h]
    return (min(p[0] for p in nk) - PAY, max(p[0] for p in nk) + PAY, min(p[1] for p in nk) - PAY, max(p[1] for p in nk) + PAY)


def gun_tipi(tarih):
    import datetime
    g = datetime.date.fromisoformat(tarih).weekday()
    return "hi" if g < 5 else ("cmt" if g == 5 else "pzr")


def main(dosyalar):
    sys.stdout.reconfigure(encoding="utf-8")
    la0, la1, lo0, lo1 = kutu()
    hiz = defaultdict(list)  # (gh, gun, saat) -> [ortalama hız]
    donem = set()
    for d in dosyalar:
        with open(d, encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                lat, lng = float(r["LATITUDE"]), float(r["LONGITUDE"])
                if not (la0 <= lat <= la1 and lo0 <= lng <= lo1):
                    continue
                tarih, saat = r["DATE_TIME"][:10], int(r["DATE_TIME"][11:13])
                if tarih in TATIL:
                    continue
                donem.add(tarih[:7])
                hiz[(r["GEOHASH"], gun_tipi(tarih), saat)].append(float(r["AVERAGE_SPEED"]))
        print("okundu", d, flush=True)

    kareler = sorted({k[0] for k in hiz})
    hucre, genel_carpan = {}, defaultdict(list)
    for gh in kareler:
        gece = [v for g in GUN for s in (2, 3, 4) for v in hiz.get((gh, g, s), [])]
        if len(gece) < EN_AZ:
            continue
        serbest = statistics.median(gece)
        tablo = {}
        for g in GUN:
            satir = []
            for s in range(24):
                v = hiz.get((gh, g, s), [])
                c = round(min(3.0, max(1.0, serbest / max(statistics.median(v), 1))), 2) if len(v) >= EN_AZ else None
                satir.append(c)
                if c is not None:
                    genel_carpan[(g, s)].append(c)
            tablo[g] = satir
        hucre[gh] = tablo
    genel = {g: [round(statistics.median(genel_carpan[(g, s)]), 2) if genel_carpan[(g, s)] else 1.0 for s in range(24)] for g in GUN}
    for t in hucre.values():  # eksik saatleri pilot bölge geneliyle doldur
        for g in GUN:
            t[g] = [genel[g][s] if c is None else c for s, c in enumerate(t[g])]
    CIKTI.write_text(json.dumps({"kaynak": "İBB Açık Veri · Saatlik Trafik Yoğunluk Veri Seti", "donem": sorted(donem),
                                 "aciklama": "çarpan = serbest akış hızı / o saatin tipik hızı (1-3); gün: hi=hafta içi, cmt, pzr; dizi 0-23. saat",
                                 "genel": genel, "hucre": hucre}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"→ {CIKTI.relative_to(KOK)}: {len(hucre)} kare, dönem {', '.join(sorted(donem))}")
    for g in GUN:
        print(g, " ".join(f"{s:02d}:{genel[g][s]}" for s in range(7, 22)))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
