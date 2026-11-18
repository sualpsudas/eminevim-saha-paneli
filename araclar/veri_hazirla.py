"""Şirket verisinden uygulamanın SPY listesini üretir: veri/kaynak/*.csv + veri/ayarlar.json → veri/spyler.js (+ veri/hg_ozet.json)

Adımlar (her biri ayrı fonksiyon; gerçek sistemde IT yalnız ilgili okuma fonksiyonunu kendi kaynağına bağlar):
  1. personel_oku   Personel listesi (departman + görev süzülür; kimlik = sicil no)
  2. sube_oku       Şube → bölge, saha, klasman (personelin klasmanı şubesinden)
  3. hedef_oku      Görev × klasman → aylık ciro hedefi; kıdem kuralı (yeni SPY ilk aylarda YSPY hedefi)
  4. satis_oku      Ciro gerçekleşen: satış kayıtları, sicil no + Kayıt Tarihi ayı
  5. randevu_oku    Randevu gerçekleşen: sayılan durumdaki randevular, ad soyad + ay; hedef = günlük hedef × iş günü
  6. ek_oku         Uygulamaya özel bilgiler (uygulama id, fotoğraf, sabit konum, müşteri puanı) — şirket sisteminde yok
  7. hesapla        Son N tamamlanmış ayın H/G ortalaması; iki H/G de eşik ve üzeriyse listede

Çalıştır:  python araclar/veri_hazirla.py [--tarih 2026-11-18]
Yalnız Python standart kütüphanesi kullanır.
"""
import argparse
import csv
import json
from datetime import date, datetime, timedelta
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
VERI = KOK / "veri"
KAYNAK = VERI / "kaynak"
GUNLER = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
TR_BUYUK = str.maketrans("iıçğöşü", "İIÇĞÖŞÜ")


def anahtar(ad):
    """Ad soyad eşleştirme anahtarı: Türkçe büyük harf, tek boşluk."""
    return " ".join(str(ad or "").translate(TR_BUYUK).upper().split())


def tablo(ad):
    with open(KAYNAK / ad, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def tarih_coz(deger):
    """Şirket dosyalarındaki tarih biçimleri: Excel gün sayısı (46329), 17.11.2026, 29.8.2026 13:19:56, 2026-11-17."""
    s = str(deger or "").strip()
    if not s:
        return None
    try:
        return date(1899, 12, 30) + timedelta(days=int(float(s.replace(",", "."))))
    except ValueError:
        pass
    for bicim in ("%d.%m.%Y %H:%M:%S", "%d.%m.%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, bicim).date()
        except ValueError:
            pass
    raise ValueError(f"Tarih anlaşılamadı: {s}")


def sayi(deger):
    s = str(deger or "0").strip().replace(" ", "")
    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    return float(s or 0)


def ay_ekle(y, m, n):
    t = y * 12 + (m - 1) + n
    return t // 12, t % 12 + 1


# ---- 1-6: okuma (kaynak kapıları) ----
def personel_oku(ayar):
    p = ayar["personel"]
    liste = []
    for r in tablo("personel.csv"):
        gorev = p["gorev_eslesme"].get((r.get("Görev") or "").strip())
        if not gorev or (r.get("Departman") or "").strip() != p["departman"]:
            continue
        liste.append({"sicil": r["Sicil Numarası"].strip(), "ad": f"{r['Personel Adı'].strip()} {r['Personel Soyadı'].strip()}",
                      "sube": r["Şube"].strip(), "gorev": gorev, "iseGiris": tarih_coz(r["Prim İşe Giriş Tarihi"])})
    return liste


def sube_oku():
    return {r["Şube Adı"].strip(): {"bolge": r["Bolge Adı"].strip(), "saha": r["Saha"].strip(), "klasman": int(r["Klasman"])}
            for r in tablo("sube_bolge_saha.csv")}


def hedef_oku():
    hedefler, kidem = {}, []
    for r in tablo("spy_hedef.csv"):
        hedefler[(int(r["Klasman"]), r["Görev"].strip())] = sayi(r["Hedef"])
        if (r.get("Kural uygulanan Görev") or "").strip():
            kidem.append((r["Kural uygulanan Görev"].strip(), int(r["Kıdem (ay) başlangıç"]), int(r["Kıdem (ay) bitiş"]),
                          r["Hesapta kullanılacak Görev"].strip()))
    return hedefler, kidem


def satis_oku(ayar):
    c = ayar["ciro"]
    turler = set(c["sayilan_kayit_turleri"])
    toplam = {}  # (sicil, yıl, ay) -> tutar
    for r in tablo("satis_kaydi.csv"):
        if turler and r.get("Kayıt Türü", "").strip() not in turler:
            continue
        g = tarih_coz(r[c["tarih_sutunu"]])
        if g:
            k = (str(r[c["sicil_sutunu"]]).strip(), g.year, g.month)
            toplam[k] = toplam.get(k, 0) + sayi(r[c["tutar_sutunu"]])
    return toplam


def randevu_oku(ayar):
    a = ayar["randevu"]
    durumlar = set(a["sayilan_durumlar"])
    sayi_ = {}  # (AD SOYAD, yıl, ay) -> adet
    for r in tablo("randevu.csv"):
        if r.get("Randevu Durumu", "").strip() not in durumlar:
            continue
        g = tarih_coz(r[a["tarih_sutunu"]])
        if g:
            k = (anahtar(r[a["kisi_sutunu"]]), g.year, g.month)
            sayi_[k] = sayi_.get(k, 0) + 1
    return sayi_


def ek_oku():
    ek = {}
    for r in tablo("spy_ek.csv"):
        ek[r["Sicil Numarası"].strip()] = {
            "id": r["Uygulama Id"].strip() or "p" + r["Sicil Numarası"].strip(), "cinsiyet": r["Cinsiyet"].strip(),
            "mahalle": r["Mahalle"].strip(), "ilce": r["İlçe"].strip(), "lat": sayi(r["Enlem"]), "lng": sayi(r["Boylam"]),
            "foto": "assets/temsilci/" + r["Fotoğraf"].strip(), "puan": r["Müşteri Puanı"].strip(), "gorusme": int(sayi(r["Görüşme Sayısı"]))}
    return ek


# ---- 7: hesap ----
def is_gunu_sayisi(y, m, bas, gunler):
    g, n = date(y, m, 1), 0
    while g.month == m:
        if g >= bas and GUNLER[g.weekday()] in gunler:
            n += 1
        g += timedelta(days=1)
    return n


def hesapla(ayar, bugun):
    personel, subeler = personel_oku(ayar), sube_oku()
    hedefler, kidem = hedef_oku()
    ciro, randevu, ek = satis_oku(ayar), randevu_oku(ayar), ek_oku()
    h, ra = ayar["hg"], ayar["randevu"]
    aylar = [ay_ekle(bugun.year, bugun.month, -i) for i in range(h["donem_ay"], 0, -1)]  # son N tamamlanmış ay
    sonuc = []
    for p in personel:
        sube = subeler.get(p["sube"])
        if not sube:
            raise ValueError(f"{p['ad']} ({p['sicil']}): şube '{p['sube']}' şube listesinde yok")
        satirlar = []
        for y, m in aylar:
            ise = p["iseGiris"] or date(2000, 1, 1)
            if date(y, m, 1) < date(ise.year, ise.month, 1):
                continue  # o ay henüz çalışmıyordu
            kidem_ay = (y * 12 + m) - (ise.year * 12 + ise.month) + 1
            hesap_gorev = next((x[3] for x in kidem if x[0] == p["gorev"] and x[1] <= kidem_ay <= x[2]), p["gorev"])
            ciro_h = hedefler.get((sube["klasman"], hesap_gorev))
            if ciro_h is None:
                raise ValueError(f"Hedef yok: klasman {sube['klasman']}, görev {hesap_gorev}")
            randevu_h = ra["gunluk_hedef"] * is_gunu_sayisi(y, m, max(ise, date(y, m, 1)), ra["is_gunleri"])
            # randevu kişi sütunu ad soyad ya da sicil no olabilir (ayarlar.json → randevu.kisi_sutunu)
            ciro_g = ciro.get((p["sicil"], y, m), 0)
            randevu_g = randevu.get((anahtar(p["ad"]), y, m), 0) + randevu.get((anahtar(p["sicil"]), y, m), 0)
            satirlar.append({"ay": f"{y}-{m:02d}", "kidemAy": kidem_ay, "hesapGorevi": hesap_gorev,
                             "randevuH": randevu_h, "randevuG": randevu_g, "ciroH": ciro_h, "ciroG": ciro_g,
                             "randevuHG": round(randevu_g / randevu_h * 100, 1) if randevu_h else 0,
                             "ciroHG": round(ciro_g / ciro_h * 100, 1) if ciro_h else 0})
        ort = lambda a: round(sum(x[a] for x in satirlar) / len(satirlar)) if satirlar else 0
        r_hg, c_hg = ort("randevuHG"), ort("ciroHG")
        listede = bool(satirlar) and r_hg >= h["liste_esik"] and c_hg >= h["liste_esik"]
        neden = "" if listede else ("hesaplanacak ay yok" if not satirlar else f"H/G eşiği %{h['liste_esik']} altında")
        if listede and p["sicil"] not in ek:
            listede, neden = False, "uygulama bilgisi yok (spy_ek.csv)"
        sonuc.append({**p, **sube, "subeAdi": p["sube"], "randevuHG": r_hg, "ciroHG": c_hg, "listede": listede, "neden": neden,
                      "aylar": satirlar})
    return sonuc, aylar


def uygulama_kaydi(x, ek, bugun):
    e = ek[x["sicil"]]
    ise = x["iseGiris"]
    yil = (bugun.year - ise.year - ((bugun.month, bugun.day) < (ise.month, ise.day))) if ise else 0
    return {"id": e["id"], "sicil": x["sicil"], "ad": x["ad"], "cinsiyet": e["cinsiyet"], "gorev": x["gorev"],
            "ilce": e["ilce"], "mahalle": e["mahalle"], "sube": x["subeAdi"].replace(" Şb.", " Şubesi"), "bolge": x["bolge"],
            "klasman": x["klasman"], "lat": e["lat"], "lng": e["lng"], "foto": e["foto"], "deneyim": yil, "puan": e["puan"],
            "gorusme": e["gorusme"], "randevuHG": x["randevuHG"], "ciroHG": x["ciroHG"]}


def main():
    ap = argparse.ArgumentParser(description="Şirket verisinden SPY listesini üretir")
    ap.add_argument("--tarih", help="hesap tarihi (YYYY-AA-GG); verilmezse bugün")
    arg = ap.parse_args()
    bugun = datetime.strptime(arg.tarih, "%Y-%m-%d").date() if arg.tarih else date.today()
    ayar = json.loads((VERI / "ayarlar.json").read_text(encoding="utf-8"))
    sonuc, aylar = hesapla(ayar, bugun)
    ek = ek_oku()
    sira = list(ek)  # uygulamadaki sıra spy_ek.csv sırası
    liste = sorted((x for x in sonuc if x["listede"]), key=lambda x: sira.index(x["sicil"]))
    kayitlar = [uygulama_kaydi(x, ek, bugun) for x in liste]
    baslik = (f"/* ÜRETİLEN DOSYA — elle düzenlemeyin. Kaynak: veri/kaynak/*.csv + veri/ayarlar.json → python araclar/veri_hazirla.py\n"
              f"   Hesap tarihi {bugun.isoformat()}, H/G dönemi {aylar[0][0]}-{aylar[0][1]:02d} … {aylar[-1][0]}-{aylar[-1][1]:02d} "
              f"(son {ayar['hg']['donem_ay']} tamamlanmış ay ortalaması). Listede yalnız iki H/G'si de >= %{ayar['hg']['liste_esik']} olan SPY'ler.\n"
              f"   Uygulama (window.TY_SPYLER) ve merkez (merkez/ty/personel.py) bu dosyayı okur. */\n")
    (VERI / "spyler.js").write_text(baslik + "window.TY_SPYLER = " + json.dumps(kayitlar, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
    ozet = {"hesapTarihi": bugun.isoformat(), "aylar": [f"{y}-{m:02d}" for y, m in aylar],
            "kisiler": [{k: (v.isoformat() if isinstance(v, date) else v) for k, v in x.items()} for x in sonuc]}
    (VERI / "hg_ozet.json").write_text(json.dumps(ozet, ensure_ascii=False, indent=1), encoding="utf-8")
    for x in sonuc:
        print(f"{'LİSTEDE ' if x['listede'] else 'dışarıda'} {x['sicil']} {x['ad']:<16} randevu %{x['randevuHG']:<4} ciro %{x['ciroHG']:<4} {x['neden']}")
    print(f"→ veri/spyler.js: {len(kayitlar)} SPY · ayrıntı veri/hg_ozet.json")


if __name__ == "__main__":
    main()
