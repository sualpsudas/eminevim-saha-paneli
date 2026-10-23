"""Seslendirme: her sahne parçasını edge-tts ile üretir, sürelerini ölçer, ses/plan.js yazar.

  python video/ses_uret.py          → video/ses/*.mp3 + video/ses/plan.js
Gerekenler: edge-tts, imageio-ffmpeg. Ses: fr-FR-RemyMultilingualNeural (deneme sayfasındaki "Ses 4"), hız +4%.
METIN altyazıda görünen yazıdır; OKU seslendiriciye giden yazıdır (SPY ve QR Türkçe okunsun diye).
"""
import asyncio
import json
import pathlib
import re
import subprocess

import edge_tts
import imageio_ffmpeg

KLASOR = pathlib.Path(__file__).resolve().parent / "ses"
SES, HIZ = "fr-FR-RemyMultilingualNeural", "+4%"

METIN = {
    "s1": "Alternatif Satış Kanalı'ndan yeni bir proje: Tasarruf Yanımda.",
    "s2a": "İstanbul'da Üsküdar, Ümraniye ve Ataşehir'den başlıyoruz.",
    "s2b": "Bugün SPY'ler sahada müşterileri kapı kapı, tek tek ziyaret ediyor.",
    "s3": "Yani sahadaki temas tek yönlü: ilk adımı her zaman biz atıyoruz.",
    "s4": "Bizimle görüşmek isteyen bir müşterinin ise bizi çağırabileceği bir kanal yok.",
    "s5": "Müşterinin gözünden bakınca, yüz yüze görüşme çoğu zaman cumartesiye kalıyor; hafta içi mesai buna fırsat vermiyor.",
    "s6": "Oysa müşteriye, dilediği yerde ve dilediği zamanda ulaşabilmeliyiz.",
    "s6ba": "Tasarruf Yanımda ile ikisi bir arada yürür.",
    "s6bb": "SPY'ler kapı kapı çalışmayı sürdürürken, bizi çağıran müşteriye aktif SPY'ler gider; pazartesi, salı ya da perşembe, hangi günü seçerse.",
    "b1": "Peki nasıl işliyor? Müşteri uygulamaya telefon numarasıyla kaydoluyor,",
    "b2": "Randevularım'dan temsilci istiyor,",
    "b3": "görüşme yerini haritada işaretliyor",
    "b4": "ve uygun gün ile saati seçiyor; aynı gün bile olabilir.",
    "b5": "Talep, bölgedeki aktif SPY'nin tabletine anında düşüyor.",
    "b6": "SPY kabul ettiği anda müşteri, kimin geleceğini adıyla görüyor.",
    "b7": "Saat onaylanınca randevu iki tarafta da kesinleşiyor.",
    "b8": "Müşteri beklerken Finansman Aracı'yla ihtiyacını ve bütçesini netleştirebiliyor.",
    "b9": "Bu tercihler SPY'nin tabletine ön bilgi olarak geçiyor; görüşme hazırlıklı başlıyor.",
    "b10": "Görüşme günü müşteri, SPY'nin yolda olduğunu haritadan izliyor.",
    "b11": "Kapıda QR kod okutuluyor ve doğrulama müşterinin kendi ekranında beliriyor.",
    "b12": "Görüşme bitince yazılı özet doğrudan telefona geliyor.",
    "s19a": "Bu düzeni önce pilot bölgede deneyip her adımını ölçeceğiz.",
    "s19b": "Sonuçlara göre hizmet alanı, komşu ilçelere doğru adım adım genişleyebilir.",
    "s20": "Böylece müşteri ile SPY ekibi arasında çift yönlü bir temas kuruluyor. Her talep, ön bilgisiyle birlikte bize ek bir veri de kazandırıyor.",
    "s21a": "SPY kaynağını önceliklendirerek saha gücümüzü daha doğru yönetiyoruz.",
    "s21b": "Tasarruf Yanımda.",
}


def oku(m):
    m = re.sub(r"\bSPY'", "Es-Pe-Ye'", m)
    m = re.sub(r"\bSPY\b", "Es-Pe-Ye", m)
    return m.replace("QR kod", "kuar kod")


def sure(dosya):
    r = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-i", str(dosya)], capture_output=True, text=True, errors="ignore")
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)


async def uret():
    KLASOR.mkdir(exist_ok=True)
    plan = {}
    for k, m in METIN.items():
        hedef = KLASOR / f"{k}.mp3"
        for deneme in range(4):
            try:
                await edge_tts.Communicate(oku(m), SES, rate=HIZ).save(str(hedef))
                break
            except Exception as e:  # servis arada bir boş döner
                print("yeniden", k, e)
                await asyncio.sleep(3)
        plan[k] = {"sure": round(sure(hedef), 2), "metin": m}
        print(k, plan[k]["sure"])
    (KLASOR / "plan.js").write_text("/* ses_uret.py üretir */\nvar SES = " + json.dumps(plan, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")


asyncio.run(uret())
