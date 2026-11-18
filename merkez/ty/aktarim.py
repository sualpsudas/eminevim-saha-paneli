"""ŞİRKET SİSTEMİNE AKTARIM KAPISI — Tasarruf Yanımda çağrılarını şirketin kendi kayıt biçiminde dışarı verir.

Alan adları şirket dosyalarındaki sütun adlarıyla aynıdır (randevu listesi ve müşteri kartı, örnek: veri/kaynak/randevu.csv).
Şu an: her değişiklikte merkez/aktarim/ altına bir satır eklenir (JSON Lines; aynı Id'nin EN SON satırı geçerlidir):
    randevu.jsonl       çağrı → randevu kaydı (SPY kabul edince, yola çıkınca, görüşme bitince / iptalde güncellenir)
    musteri_karti.jsonl yeni çağrının müşterisi → aday müşteri kartı
Gerçek sistemde: yaz() şirketin randevu/müşteri servisine gönderir (IT_DEVIR.md → Aktarım). Kart No'yu şirket sistemi verir.
Aktarım hatası çağrı akışını durdurmaz.
"""
import json
import time
from datetime import datetime

from .ayarlar import AKTARIM

GUN_ADI = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
DURUM = {"tamamlandi": "Randevu Gerçekleşti", "iptal": "Randevu İptal"}
TR_BUYUK = str.maketrans("iıçğöşü", "İIÇĞÖŞÜ")


def _buyuk(s):
    return str(s or "").translate(TR_BUYUK).upper()


def _tarih(ms, saatli=True):
    return time.strftime("%d.%m.%Y %H:%M:%S" if saatli else "%d.%m.%Y", time.localtime(ms / 1000)) if ms else ""


def _sube(spy):
    return str(spy.get("sube") or "").replace(" Şubesi", " Şb.")


def yaz(ad, satir):
    try:
        AKTARIM.mkdir(parents=True, exist_ok=True)
        with open(AKTARIM / ad, "a", encoding="utf-8") as f:
            f.write(json.dumps(satir, ensure_ascii=False) + "\n")
    except OSError:
        pass


def randevu_satiri(veri, k):
    spy = veri["spyler"].get(k.get("repId")) or {}
    planlanan = ""
    if k.get("tarih") and k.get("saat"):
        try:
            g = datetime.strptime(f"{k['tarih']} {k['saat']}", "%Y-%m-%d %H:%M")
            planlanan = f"{g.day}.{g.month}.{g.year} {g:%H:%M:%S}"
        except ValueError:
            pass
    cumartesi = bool(k.get("tarih")) and GUN_ADI[datetime.strptime(k["tarih"], "%Y-%m-%d").weekday()] == "Cumartesi"
    return {
        "Şube": _sube(spy), "Kart No": None, "Kart Kategori": "Aday Müşteri", "Planl. Tarih": planlanan,
        "Görü. Tarihi": _tarih(k.get("guncelleme")) if k.get("durum") == "tamamlandi" else "",
        "Randevu Turu": "Cumartesi Randevu" if cumartesi else "Haftaiçi Randevu",
        "Randevu Sonucu": k.get("sonrakiAdim") or "", "Randevu Durumu": DURUM.get(k.get("durum"), "Planlandı"),
        "Randevu Yeri": k.get("yer") or "", "Sorumlu Personel": _buyuk(spy.get("ad")), "Firma": "EminEvim",
        "Oluşt. Tar.": _tarih(k.get("olusma"), False), "Tim Adı": _sube(spy).replace("Şb.", "Şube"), "Konu": "Tasarruf Yanımda çağrısı",
        "Id": k["id"], "Katılımcı Sayısı": 1,
        # Şirket dosyasında olmayan, eşleştirmeyi kolaylaştıran alanlar (önerilen):
        "Sorumlu Personel Sicil": spy.get("sicil") or "", "Kaynak": "Tasarruf Yanımda · " + ("Web formu" if k.get("kaynak") == "web" else "Uygulama"),
    }


def musteri_karti(k):
    m = k.get("musteri") or {}
    ad = str(m.get("ad") or "").split()
    adi = m.get("adi") or " ".join(ad[:-1]) or (ad[0] if ad else "")
    soyadi = m.get("soyadi") or (ad[-1] if len(ad) > 1 else "")
    return {"Kart No": None, "Adı": adi, "Soyadı": soyadi,
            "Kategori": "Aday Müşteri", "Referans Grubu": "DİJİTAL KANALI", "Referans (Nereden Duydun)": "TASARRUF YANIMDA",
            "Kaynak": "Tasarruf Yanımda", "Oluşturma Tarihi": _tarih(k.get("olusma"), False), "Semt / Mahalle": k.get("yer") or "",
            "İl": "İstanbul", "Telefon": m.get("tel") or "", "Ticari İleti İzni": "Evet" if k.get("kampanya") else "Hayır", "Id": k["id"]}


def yeni_cagri(k):
    try:
        yaz("musteri_karti.jsonl", musteri_karti(k))
    except (KeyError, TypeError, ValueError):
        pass


def cagri_degisti(veri, k, onceki_durum):
    """Randevu kaydı SPY belli olunca açılır; sonra her durum değişikliğinde güncellenir."""
    if k.get("repId") and k.get("durum") != onceki_durum and k.get("durum") != "alindi":
        try:
            yaz("randevu.jsonl", randevu_satiri(veri, k))
        except (KeyError, TypeError, ValueError):
            pass
