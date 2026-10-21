# Tasarruf Yanımda — web başvuru formu önizlemesi

Tasarruf Yanımda'nın web kolu. eminevim.com ana sayfasının kopyasında yalnızca **Hızlı Başvuru formu**
değiştirilmiştir; amaç cumartesi yoğunluğunu hafta içine yaymak ve müşteriye "temsilcimiz size gelsin"
seçeneğini sunmaktır.

## Form
Sitedeki Hızlı Başvuru formunun aynısı (başlık, Ad, Soyad, bayrak + Telefon, onay kutuları, "Gönder") ve bir ek:
**Temsilcimiz size gelsin · İsteğe bağlı** kutusu. İşaretlenince gün (hafta içi önce, cumartesi "yoğun"), saat aralığı,
görüşme yeri, ilçe ve isteğe bağlı e-posta açılır. Teşekkür ekranında özet, temsilci kartı, e-posta önizlemesi ve
"Uygulamayı açın" linki (sayfadaki tek çalışan link, `data-ty-dis`). Formda proje adı ya da önizleme yazısı yoktur.

## Dosyalar
| Dosya | Ne işe yarar |
|---|---|
| `form_bolumu.html` | Formun kendisi (CSS + HTML + JS). Değişiklikler burada yapılır. |
| `olustur.py` | Canlı ana sayfayı indirir, formu yerleştirir, izleme kodlarını çıkarır → `index.html` |
| `index.html` | Üretilmiş önizleme. Tarayıcıda açın; telefonda alttaki "Hızlı Başvuru"ya dokunun. |

Yeniden üretmek: `python olustur.py` (yalnızca standart kütüphane).

Form hiçbir yere veri göndermez; temsilci bilgileri örnektir. Görseller ve site stilleri
`<base href="https://www.eminevim.com/">` ile canlı siteden yüklenir.
