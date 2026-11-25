"""PERSONEL KAPISI — merkezin SPY listesi.

Şu an: veri/spyler.js (uygulama da aynı dosyayı okur). Bu dosya şirket verisinden üretilir:
    python araclar/veri_hazirla.py   (personel + şube/klasman + hedef + satış + randevu → H/G, otomatik liste)
Gerçek sistemde: spyleri_oku() IT'nin personel servisine bağlanır; dönen her SPY'de en az
    id, sicil, ad, sube, ilce, mahalle, lat, lng, randevuHG, ciroHG   (ayrıntı IT_DEVIR.md → Personel)
Liste değişince merkez yeniden başlatılır.
"""
import json

from .ayarlar import SPY_DOSYASI


def spyleri_oku():
    metin = SPY_DOSYASI.read_text(encoding="utf-8")
    liste = json.loads(metin[metin.index("["):metin.rindex("]") + 1])
    return [{**x, "yer": f"{x['mahalle']}, {x['ilce']}"} for x in liste]


# Hareketli örnek SPY'ler (sunum): kendi ilçelerinde rastgele dolaşır, atamaya gerçek SPY'ler gibi katılır ve teklifi kendiliğinden kabul eder
# (konum.py gezi_konum, sunum.py sim_kabul). Gerçek personel listesinde yoktur; uygulamada yalnız müşteri tarafı bilgi kartı için
# TY_SPYLER_SIM olarak sunulur (api.py), SPY girişinde görünmez. Dolaşma kutusu ilçe sınırı içinde kalır (taban ±0,005° enlem, ±0,007° boylam).
_SIM = [  # id, ad, cinsiyet, ilçe, mahalle, şube, klasman, lat, lng, foto, deneyim, puan, görüşme, randevuHG, ciroHG, dolaşma periyodu (sn) enlem/boylam, faz
    ("h1", "Burak Yıldız", "E", "Ümraniye", "Atatürk Mah.", "Ümraniye Şubesi", 4, 41.0295, 29.1326, "burak-yildiz.jpg", 3, "4,6", 143, 108, 112, (330, 410), (0.3, 1.7)),
    ("h2", "Büşra Kılıç", "K", "Üsküdar", "Acıbadem Mah.", "Üsküdar Şubesi", 3, 41.0335, 29.0605, "busra-kilic.jpg", 4, "4,7", 188, 121, 104, (360, 450), (2.1, 0.4)),
    ("h3", "Can Erdem", "E", "Ataşehir", "Barbaros Mah.", "Ataşehir Şubesi", 2, 40.9845, 29.1256, "can-erdem.jpg", 5, "4,5", 227, 117, 131, (300, 390), (4.0, 2.6)),
    ("h4", "Damla Bulut", "K", "Ümraniye", "Çakmak Mah.", "Ümraniye Şubesi", 4, 41.0105, 29.1578, "damla-bulut.jpg", 2, "4,8", 96, 102, 109, (390, 340), (5.1, 3.3)),
    ("h5", "Emre Doğan", "E", "Üsküdar", "Kuzguncuk Mah.", "Üsküdar Şubesi", 3, 41.0155, 29.0724, "emre-dogan.jpg", 6, "4,6", 264, 125, 118, (345, 420), (1.2, 5.6)),
]
SIM_SPYLER = [{"id": i, "sicil": "49" + i[1:].zfill(3), "ad": ad, "cinsiyet": c, "gorev": "SPY1", "ilce": ilce, "mahalle": mah, "sube": sube,
               "bolge": "İstanbul Anadolu Bölge 1", "klasman": kl, "lat": la, "lng": ln, "foto": "assets/temsilci/" + foto, "deneyim": den,
               "puan": puan, "gorusme": gor, "randevuHG": rh, "ciroHG": ch, "yer": f"{mah}, {ilce}", "sim": True,
               "gezi": {"hiz": 8.0, "faz": round(faz[0] / 6.3, 3)}}
              for i, ad, c, ilce, mah, sube, kl, la, ln, foto, den, puan, gor, rh, ch, per, faz in _SIM]

SPYLER = spyleri_oku() + SIM_SPYLER
SPY_IDLER = {s["id"] for s in SPYLER}
