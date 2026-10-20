# Tasarruf Yanımda — web başvuru formu önizlemesi

Tasarruf Yanımda'nın web kolu. eminevim.com ana sayfasının kopyasında yalnızca **Hızlı Başvuru formu**
değiştirilmiştir; amaç cumartesi yoğunluğunu hafta içine yaymak ve müşteriye "temsilcimiz size gelsin"
seçeneğini sunmaktır.

## Formdaki akış (uygulamayla aynı 3 adım)
1. **Temsilcimiz size gelsin**: ad soyad, telefon (altta "Telefonla görüşmeyi tercih ederim")
2. **Ne zaman, nerede?**: gün (hafta içi önce, cumartesi "yoğun"), saat (öğle arası / akşam), yer (iş yeri / ev), ilçe
3. **Talebiniz alındı**: özet, temsilci kartı, isteğe bağlı e-posta + e-posta önizlemesi,
   "Finansman tercihlerinizi uygulamamızdan değerlendirebilirsiniz → Uygulamayı açın" (sayfadaki tek çalışan link, `data-ty-dis`)

## Dosyalar
| Dosya | Ne işe yarar |
|---|---|
| `form_bolumu.html` | Formun kendisi (CSS + HTML + JS). Değişiklikler burada yapılır. |
| `olustur.py` | Canlı ana sayfayı indirir, formu yerleştirir, izleme kodlarını çıkarır → `index.html` |
| `index.html` | Üretilmiş önizleme. Tarayıcıda açın; telefonda alttaki "Hızlı Başvuru"ya dokunun. |

Yeniden üretmek: `python olustur.py` (yalnızca standart kütüphane).

Önizleme hiçbir yere veri göndermez; temsilci bilgileri örnektir. Görseller ve site stilleri
`<base href="https://www.eminevim.com/">` ile canlı siteden yüklenir.
