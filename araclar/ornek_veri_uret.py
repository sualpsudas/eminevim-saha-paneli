"""Örnek şirket verisi üretir (yalnız gösteri için): veri/kaynak/*.csv

Sütun adları şirket sistemlerinden alınan örnek dosyadaki (tf_orn.xlsx, 2026-11-18) adlarla BİREBİR aynıdır;
değerler UYDURMADIR (depo herkese açık: gerçek kişi, hedef ya da satış bilgisi buraya girmez).
Gerçek sistemde bu dosyalar şirketten gelir; bu betik o zaman kullanılmaz.

Çalıştır:  python araclar/ornek_veri_uret.py      → ardından  python araclar/veri_hazirla.py
"""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
HEDEF_KLASOR = KOK / "veri" / "kaynak"
BITIS = date(2026, 10, 31)            # örnek verinin son günü (H/G için gereken son 3 tamamlanmış ay)
AYLAR = [(2026, 8), (2026, 9), (2026, 10)]
rnd = random.Random(20261118)

# (sicil, ad, soyad, şube, görev, işe giriş, randevu H/G hedefi, ciro H/G hedefi)
# İlk 7 kişi son 3 ayda iki H/G'si de >= %100 olanlar (uygulamada görünür); diğerleri kuralı sağlamaz (otomatik liste dışı).
KISILER = [
    ("48213", "Onur", "Kaya", "Ataşehir Şb.", 1, date(2020, 9, 1), 115, 129),
    ("48350", "Derya", "Aksoy", "Üsküdar Şb.", 1, date(2022, 6, 1), 126, 130),
    ("48487", "Berk", "Cengiz", "Ümraniye Şb.", 2, date(2018, 3, 1), 105, 105),
    ("48562", "Selin", "Arslan", "Üsküdar Şb.", 1, date(2021, 5, 1), 120, 100),
    ("48655", "Ece", "Yalçın", "Ümraniye Şb.", 1, date(2024, 8, 1), 114, 113),
    ("48877", "Burcu", "Avcı", "Ümraniye Şb.", 1, date(2021, 2, 1), 127, 115),
    ("48951", "Barış", "Çelik", "Ataşehir Şb.", 1, date(2021, 7, 1), 117, 116),
    ("48359", "Murat", "Şahin", "Üsküdar Şb.", 2, date(2018, 4, 1), 94, 103),
    ("48470", "Merve", "Tunç", "Üsküdar Şb.", 1, date(2024, 6, 1), 101, 91),
    ("48618", "Serkan", "Öztürk", "Ümraniye Şb.", 1, date(2022, 10, 1), 104, 92),
    ("48729", "Pınar", "Çakır", "Ümraniye Şb.", 1, date(2020, 11, 1), 88, 95),
    ("49099", "Can", "Erdem", "Ataşehir Şb.", 2, date(2016, 5, 1), 90, 104),
    ("49173", "Okan", "Polat", "Ataşehir Şb.", 1, date(2026, 9, 1), 99, 99),   # yeni başlayan: YSPY hedefi
]
# Uygulamaya özel bilgiler (şirket sisteminde yok): uygulama kimliği, fotoğraf, sabit test konumu, müşteri puanı, görüşme sayısı
EK = {
    "48213": ("s1", "E", "Atatürk Mah.", "Ataşehir", 40.9923, 29.1244, "onur-kaya.jpg", "4,8", 312),
    "48350": ("s2", "K", "Mimar Sinan Mah.", "Üsküdar", 41.0255, 29.016, "derya-aksoy.jpg", "4,9", 205),
    "48487": ("s3", "E", "Namık Kemal Mah.", "Ümraniye", 41.0256, 29.11, "berk-cengiz.jpg", "4,7", 468),
    "48562": ("s4", "K", "Bulgurlu Mah.", "Üsküdar", 41.018, 29.06, "selin-arslan.jpg", "4,8", 251),
    "48655": ("s15", "K", "Çakmak Mah.", "Ümraniye", 41.013, 29.124, "ece-yalcin.jpg", "4,7", 275),
    "48877": ("s21", "K", "Madenler Mah.", "Ümraniye", 41.009, 29.178, "burcu-avci.jpg", "4,6", 403),
    "48951": ("s23", "E", "İçerenköy Mah.", "Ataşehir", 40.975, 29.108, "baris-celik.jpg", "4,8", 251),
    "48359": ("s7", "E", "Valide-i Atik Mah.", "Üsküdar", 41.017, 29.03, "murat-sahin.jpg", "4,9", 162),
    "48470": ("s10", "K", "Çengelköy Mah.", "Üsküdar", 41.056, 29.06, "merve-tunc.jpg", "4,8", 312),
    "48618": ("s14", "E", "Tantavi Mah.", "Ümraniye", 41.0215, 29.102, "serkan-ozturk.jpg", "4,8", 316),
    "48729": ("s17", "K", "İnkılap Mah.", "Ümraniye", 41.04, 29.105, "pinar-cakir.jpg", "4,5", 288),
    "49099": ("s27", "E", "Ferhatpaşa Mah.", "Ataşehir", 40.987, 29.175, "can-erdem.jpg", "4,9", 187),
    "49173": ("s29", "E", "Örnek Mah.", "Ataşehir", 40.976, 29.14, "okan-polat.jpg", "4,7", 0),
}
SUBELER = [  # Şube Adı, Bolge Adı, Saha, Klasman (klasman UYDURMA; gerçeği şirketten gelecek)
    ("Ataşehir Şb.", "İstanbul Anadolu Bölge 1", "İstanbul Saha", 2),
    ("Üsküdar Şb.", "İstanbul Anadolu Bölge 1", "İstanbul Saha", 3),
    ("Kadıköy Şb.", "İstanbul Anadolu Bölge 1", "İstanbul Saha", 1),
    ("Ümraniye Şb.", "İstanbul Anadolu Bölge 3", "İstanbul Saha", 4),
    ("Ümraniye Çarşı Şb.", "İstanbul Anadolu Bölge 3", "İstanbul Saha", 6),
]
HEDEF_TABAN = {"YSPY1": 12_000_000, "YSPY2": 15_000_000, "YSPY3": 18_000_000, "SPY1": 22_000_000, "SPY2": 26_000_000, "TL": 20_000_000}
KIDEM = [("SPY1", 1, 3, "YSPY1"), ("SPY1", 4, 6, "YSPY2"), ("SPY1", 7, 9, "YSPY3")]
GOREV_ADI = {1: "Saha Portföy Yöneticisi (1)", 2: "Saha Portföy Yöneticisi (2)"}
TR_BUYUK = str.maketrans("iıçğöşü", "İIÇĞÖŞÜ")


def buyuk(s):
    return s.translate(TR_BUYUK).upper()


def excel_seri(g):
    return (g - date(1899, 12, 30)).days


def is_gunleri(y, m):
    g = date(y, m, 1)
    while g.month == m:
        if g.weekday() < 6 and g <= BITIS:
            yield g
        g += timedelta(days=1)


def kidem_ay(ise, y, m):
    return (y * 12 + m) - (ise.year * 12 + ise.month) + 1


def hesap_gorevi(gorev, kidem):
    for kural, bas, bit, hesap in KIDEM:
        if gorev == kural and bas <= kidem <= bit:
            return hesap
    return gorev


def hedef(klasman, gorev):
    return round(HEDEF_TABAN[gorev] * (1.0 if klasman <= 4 else 0.9), -5)


def yaz(ad, basliklar, satirlar):
    with open(HEDEF_KLASOR / ad, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(basliklar)
        w.writerows(satirlar)
    print(f"{ad}: {len(satirlar)} satır")


def main():
    HEDEF_KLASOR.mkdir(parents=True, exist_ok=True)
    klasman = {s[0]: s[3] for s in SUBELER}
    bolge = {s[0]: s[1] for s in SUBELER}

    yaz("personel.csv", ["Personel Adı", "Personel Soyadı", "Firma", "Bölge", "Şube", "Departman", "Görev", "E-Posta", "Sicil Numarası",
                         "Sanal Santral Kısa Kod", "Sanal Santral Gsm", "Prim İşe Giriş Tarihi", "Id", "İmza Sirküleri"],
        [(ad, soyad, "EminEvim", bolge[sube], sube, "Alternatif Satış Ekibi", GOREV_ADI[g],
          f"{ad.lower()}.{soyad.lower()}@ornek.com".translate(str.maketrans("çğıöşü", "cgiosu")), sicil, "", "", ise.strftime("%d.%m.%Y"), i + 1, "True")
         for i, (sicil, ad, soyad, sube, g, ise, _, _) in enumerate(KISILER)])

    yaz("sube_bolge_saha.csv", ["Şube Adı", "Bolge Adı", "Saha", "Klasman"], SUBELER)

    hedef_satir = []
    for gorev in HEDEF_TABAN:
        for k in range(1, 8):
            hedef_satir.append([k, gorev, int(hedef(k, gorev)), "", "", "", ""])
    for i, (kural, bas, bit, hesap) in enumerate(KIDEM):  # örnek dosyadaki gibi kıdem kuralı ilk satırların sağında
        hedef_satir[i][3:] = [kural, bas, bit, hesap]
    yaz("spy_hedef.csv", ["Klasman", "Görev", "Hedef", "Kural uygulanan Görev", "Kıdem (ay) başlangıç", "Kıdem (ay) bitiş",
                          "Hesapta kullanılacak Görev"], hedef_satir)

    satis, randevu = [], []
    uye_no, kart_no, rid = 2_000_000, 70_000_000, 1
    for sicil, ad, soyad, sube, g, ise, p_r, p_c in KISILER:
        gorev = f"SPY{g}"
        aktif = [(y, m) for y, m in AYLAR if date(y, m, 1) >= date(ise.year, ise.month, 1)]
        tam = aktif
        sapma = [-3, 2, 1][-len(tam):] if len(tam) >= 3 else [-1, 1][:len(tam)]
        for (y, m) in aktif:
            ofs = sapma[tam.index((y, m))]
            gunler = list(is_gunleri(y, m))
            # Ciro: o ayın hedefi × oran, satışlar Kayıt Tarihi'ne göre
            hg = hesap_gorevi(gorev, kidem_ay(ise, y, m))
            kalan = round(hedef(klasman[sube], hg) * (p_c + ofs) / 100)
            while kalan > 0:
                tutar = rnd.randrange(400_000, 2_400_001, 50_000)
                if kalan - tutar < 300_000:
                    tutar = kalan
                kalan -= tutar
                tur = rnd.choice(["GAYRİMENKUL", "GAYRİMENKUL", "ARAÇ"])
                sistem = "Çekilişli Finansman" if rnd.random() < .5 else "Bireysel Finansman - Peşinatsız"
                satis.append([len(satis) + 1, uye_no, sube, buyuk(f"{ad} {soyad}"), excel_seri(rnd.choice(gunler)), tur, sistem,
                              rnd.choice([15, 24, 36, 40, 60]), "Tahsilat Kontrolü Bekleniyor", tutar, sicil])
                uye_no += 1
            # Randevu: günlük 10 × iş günü; yalnız "Randevu Gerçekleşti" sayılır, birkaç gerçekleşmeyen de eklenir
            adet = round(10 * len(gunler) * (p_r + ofs) / 100)
            for j in range(adet + max(1, adet // 15)):
                gun = gunler[j * len(gunler) // (adet + 1) if j < adet else rnd.randrange(len(gunler))]
                saat = f"{rnd.randint(10, 19)}:{rnd.choice(['00', '15', '30', '45'])}:00"
                oldu = j < adet
                randevu.append([sube, kart_no, "", rnd.choice(["Aday Müşteri", "Kayıtlı Müşteri Aktif"]),
                                f"{gun.day}.{gun.month}.{gun.year} {saat}", f"{gun.day}.{gun.month}.{gun.year} {saat}" if oldu else "",
                                "Cumartesi Randevu" if gun.weekday() == 5 else "Haftaiçi Randevu",
                                rnd.choice(["Kayıt Oldu", "Uzun Vade Durum İçin Takip", "Bilgi Verildi"]) if oldu else "Müşteri Gelmedi",
                                "Randevu Gerçekleşti" if oldu else "Randevu Gerçekleşmedi", sube, buyuk(f"{ad} {soyad}"), "EminEvim", "",
                                (gun - timedelta(days=rnd.randint(1, 10))).strftime("%d.%m.%Y"), sube.replace("Şb.", "Şube"), "", rid, 1])
                kart_no += 1
                rid += 1

    yaz("satis_kaydi.csv", ["Sıra No", "Üye No", "Şube ", "Üye Satış Temsilcisi", "Kayıt \nTarihi", "Org Türü", "Org Sistemi",
                            "Taksit \nSayısı", "Kayıt Türü", "Org Tutar", "UyeSatisTemsilciSicilNo"], satis)
    yaz("randevu.csv", ["Şube", "Kart No", "Kart", "Kart Kategori", "Planl. Tarih", "Görü. Tarihi", "Randevu Turu", "Randevu Sonucu",
                        "Randevu Durumu", "Randevu Yeri", "Sorumlu Personel", "Firma", "Oluşt. Kul.", "Oluşt. Tar.", "Tim Adı", "Konu", "Id",
                        "Katılımcı Sayısı"], randevu)
    yaz("spy_ek.csv", ["Sicil Numarası", "Uygulama Id", "Cinsiyet", "Mahalle", "İlçe", "Enlem", "Boylam", "Fotoğraf", "Müşteri Puanı",
                       "Görüşme Sayısı"],
        [(s, *v) for s, v in EK.items()])


if __name__ == "__main__":
    main()
