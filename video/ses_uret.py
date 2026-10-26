"""Seslendirme: her parçayı edge-tts ile üretir; süre ve KELİME ZAMANLARINI ses/plan.js'e yazar.

  python video/ses_uret.py          → video/ses/*.mp3 + video/ses/plan.js (hepsi)
  python video/ses_uret.py sorun    → yalnız bu parçalar yeniden; diğerleri plan.js’ten aynen kalır
Gerekenler: edge-tts, imageio-ffmpeg. Ses: fr-FR-RemyMultilingualNeural (deneme sayfasındaki "Ses 4").
METIN altyazıda görünen yazıdır; oku() seslendiriciye gideni üretir (SPY "Seğpeğyeğ" yazımıyla okutulur; kullanıcı telaffuz denemesinde seçti).
Çok dilli ses kısa/yarım cümlede dili yanlış tahmin ediyor: kısa cümleleri ve "Tasarruf Yanımda"yı tek başına okutma,
uzun cümleyle aynı parçada tut; görüntü geçişleri tanitim.html'de kelime zamanına bağlanır.
"""
import asyncio
import json
import pathlib
import re
import subprocess
import sys

import edge_tts
import imageio_ffmpeg

KLASOR = pathlib.Path(__file__).resolve().parent / "ses"
SES, HIZ = "fr-FR-RemyMultilingualNeural", "+8%"

METIN = {
    "ac": "Yeni projemiz Tasarruf Yanımda, müşterilerimizle saha ekibimiz arasında yeni bir iletişim kanalı açıyor.",
    "bugun": "Bugün Alternatif Satış Kanalı'nda Saha Portföy Yöneticileri kapı kapı dolaşır ve aday müşterileri kendileri bulur.",
    "sorun": "İlk adımı çoğunlukla biz atarız. Görüşmek isteyen müşterinin doğrudan temsilci çağırabileceği bir kanal yok. "
             "Hafta içi çalışan biri için yüz yüze görüşme de çoğu zaman cumartesiye kalıyor.",
    "cozum": "Bu kez ilk adımı müşteri atıyor. Tasarruf Yanımda bu düzene ikinci bir temas yolu ekleyecek: "
             "saha ziyaretleri sürerken, uygulamadan gelen çağrıları bölgedeki Saha Portföy Yöneticileri karşılayacak.",
    "talep": "Müşteri telefon numarasıyla kaydolup haritadan yerini işaretler, uygun gün ve saati kendisi seçer.",
    "esles": "Çağrı, bölgedeki Saha Portföy Yöneticisinin tabletine iletilir; kabul edildiğinde temsilcinin adı ve kesin saat uygulamada görünür.",
    "hazir": "Beklerken Finansman Aracı'yla ihtiyacını ve bütçesini belirleyebilecek; temsilci de görüşmeye bu ön bilgiyle hazırlıklı gidecek.",
    "guven": "Ziyaret günü temsilci haritadan izlenebilir; kapıda kimliği QR kodla doğrulanır, görüşmenin yazılı özeti de telefonda kalır.",
    "yol": "Proje önce belirlenecek bir pilot bölgede başlayacak; çağrı sayısı, yanıt süresi ve gerçekleşen görüşmeler izlenecek. "
           "Sonuçlara göre hizmet alanını uygun görülen ilçelere genişletmek mümkün.",
    "cift": "Böylece iletişim çift yönlü hâle gelir; her çağrı, ön bilgisiyle birlikte bize ek veri de kazandırır.",
    "oncelik": "Önceliği bizi çağırana vermek, saha gücümüzü doğru yere yönlendirmeyi kolaylaştırır.",
}


def oku(m):
    m = re.sub(r"\bSPY'", "Seğpeğyeğ'", m)
    m = re.sub(r"\bSPY\b", "Seğpeğyeğ", m)
    return m.replace("QR kod", "kuar kod")


def sure(dosya):
    r = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-i", str(dosya)], capture_output=True, text=True, errors="ignore")
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)


async def parca(k, m):
    for deneme in range(5):
        try:
            ses, kelime = bytearray(), []
            async for c in edge_tts.Communicate(oku(m), SES, rate=HIZ, boundary="WordBoundary").stream():
                if c["type"] == "audio":
                    ses += c["data"]
                elif c["type"] == "WordBoundary":
                    kelime.append([round(c["offset"] / 1e7, 3), c["text"]])
            if not ses:
                raise RuntimeError("ses gelmedi")
            (KLASOR / f"{k}.mp3").write_bytes(bytes(ses))
            return kelime
        except Exception as e:  # servis arada bir boş döner
            print("yeniden", k, e)
            await asyncio.sleep(3)
    raise SystemExit(f"{k} üretilemedi")


async def uret():
    KLASOR.mkdir(exist_ok=True)
    secili = sys.argv[1:]
    plan = {}
    if secili:   # yalnız seçilen parçalar; diğerleri eski plan.js’ten
        eski = (KLASOR / "plan.js").read_text(encoding="utf-8")
        plan = json.loads(eski[eski.index("{"):eski.rindex("}") + 1])
    else:
        for eski in KLASOR.glob("*.mp3"):
            eski.unlink()
    for k, m in METIN.items():
        if secili and k not in secili:
            continue
        kelime = await parca(k, m)
        plan[k] = {"sure": round(sure(KLASOR / f"{k}.mp3"), 2), "metin": m, "kelime": kelime}
        print(k, plan[k]["sure"], len(kelime))
    (KLASOR / "plan.js").write_text("/* ses_uret.py üretir */\nvar SES = " + json.dumps(plan, ensure_ascii=False) + ";\n", encoding="utf-8")


asyncio.run(uret())
