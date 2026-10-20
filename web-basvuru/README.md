# Tasarruf Yanımda — web başvuru formu önizlemesi

Tasarruf Yanımda'nın web kolu. eminevim.com ana sayfasının kopyasında yalnızca **Hızlı Başvuru formu**
değiştirilmiştir; amaç cumartesi yoğunluğunu hafta içine yaymak ve müşteriye "temsilcimiz size gelsin"
seçeneğini sunmaktır.

## Formdaki akış
- Ad, soyad, telefon (mevcut formla aynı)
- **Nasıl görüşelim?** Temsilcimiz size gelsin / Beni arayın / Şubeye geleceğim
- *Temsilci gelsin*: konu, yer (iş yeri / ev), il-ilçe (veya konum), gün, saat aralığı, e-posta
- Cumartesi seçilirse hafta içi öğle arasına yönlendiren uyarı
- Gönderim sonrası özet + **e-posta önizlemesi** (temsilci kartı, sicil no, randevu, canlı takip linki, güven notları)

## Dosyalar
| Dosya | Ne işe yarar |
|---|---|
| `form_bolumu.html` | Formun kendisi (CSS + HTML + JS). Değişiklikler burada yapılır. |
| `olustur.py` | Canlı ana sayfayı indirir, formu yerleştirir, izleme kodlarını çıkarır → `index.html` |
| `index.html` | Üretilmiş önizleme. Tarayıcıda açın; telefonda alttaki "Hızlı Başvuru"ya dokunun. |

Yeniden üretmek: `python olustur.py` (yalnızca standart kütüphane).

Önizleme hiçbir yere veri göndermez; temsilci bilgileri örnektir. Görseller ve site stilleri
`<base href="https://www.eminevim.com/">` ile canlı siteden yüklenir.
