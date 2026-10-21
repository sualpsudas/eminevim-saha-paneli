# Tasarruf Yanımda

Tek proje: **Tasarruf Yanımda** (klasör adı `eminevim-saas`, depo `sualpsudas/eminevim-saha-paneli` eski adlardır).
Ana konu **müşteri teması**: hafta içi çalışan müşteri cumartesi şubeye yığılmasın, temsilci (SPY) uygun yer/saatte
müşterinin yanına gitsin; müşteri kimin geleceğini önceden görsün ve görüşme günü temsilcinin yolda olduğunu izlesin.
Uygulama ve web formu bu fikrin ilk aşamalarıdır; ikisi **aynı ekranları ve aynı dili** kullanmalı.

## Klasörler
- `index.html`, `assignment.js`, `org-data.js`, `map.html`, `sw.js` — uygulama (web/PWA). Aynı kod Capacitor ile iPhone'a
  paketlenir (`scripts/prepare-web.mjs`, `IOS_TESTFLIGHT.md`, Codemagic).
- `web-basvuru/` — eminevim.com ana sayfa kopyasında yeni Hızlı Başvuru formu (`form_bolumu.html` düzenlenir,
  `python olustur.py` → `index.html`). Sayfadaki tüm linkler etkisizdir; bu kural korunmalı.
- `taslak/` — sunuma eklenebilir ekran taslakları (aşağıya bakın).
- `backup/2026-10-21-eski-uygulama/` — sade akıştan önceki uygulama (açılır hâlde; git etiketi `eski-uygulama-2026-10-21`).
  Geri dönmek gerekirse: `git checkout eski-uygulama-2026-10-21 -- "Eminevim Saha Paneli.dc.html"`.
- `PROJE_ILERLEME.md` — her çalışmadan sonra tarihli kısa not eklenir.

Yayın: GitHub Pages `master` dalından → https://sualpsudas.github.io/eminevim-saha-paneli/ (depo public; kullanıcı izinli).
Paylaşım için tek sayfa: `linkler.html` — Uygulama / Web formu × Telefon / Bilgisayar seçmeli önizleme (iframe, ekrana sığdırır;
`#web-telefon` gibi adreslenebilir), altta taslak ve eski sürüm linkleri — yeni sayfa eklenince güncelle.

## Müşteri ekranı ilkeleri
- Olabildiğince basit; gereksiz yazı yok, her ekranda tek soru grubu ve tek ana buton.
- İlk temasta üyelik, şifre, konum izni, sohbet yok. Alanlar: ad, telefon, gün, saat, yer (+ilçe); e-posta isteğe bağlı.
- Korkutmayan dil: "Temsilciniz önce sizi arar", "Ücretsiz", "Görüşmede ödeme alınmaz", "Sicil numarası aynıdır".
  "Takip" müşteriyi değil temsilciyi anlatır ("Temsilcinizin nerede olduğunu görürsünüz").
- Cumartesi engellenmez; hafta içi günler önce gelir, cumartesi "yoğun" etiketiyle durur.
- Temsilci bilgileri ve takip linki **e-postayla** gider (SMS değil).
- Yeni müşteri üye olmadan sade akışla ilerler (uygulamada giriş ekranı → "Yeni Müşteri", `ya*` durumları).
  Finansman/bütçe hesabı yalnız **üyelere**, "Finansmanlarım" sekmesinde; web formu bunun için uygulama linki verir.
- **Web formu gerçek sitedeki gibi görünmeli** (kullanıcı isteği, 2026-10-21): sitenin başlığı, gri kutucukları
  (`tk-inputGri` / mobilde `tk-inputMobilGri`), onay kutuları ve turuncu "Gönder". Formda "Tasarruf Yanımda" adı, açıklama
  simgeleri, adım çubuğu ya da "bilgiler gönderilmez" gibi önizleme yazısı YOK; sayfa sitenin kendi başlığıyla en üstten açılır.
  Temsilci çağırma resmî görünen **isteğe bağlı** kutu: "Temsilcimiz size gelsin · İsteğe bağlı — Dilerseniz temsilcimizi
  konumunuza çağırabilirsiniz"; işaretlenince gün/saat/yer seçimi, ilçe, e-posta (isteğe bağlı) açılır.

## Taslak isteği gelirse (web ya da uygulama)
Kullanıcı "taslak göster" dediğinde çalışan kod değil, **sunuma eklenebilir ekran taslağı** hazırla:
1. `taslak/<konu>.html` olarak tek dosya; şablon `taslak/uygulama-akisi.html` (telefon çerçeveleri, her ekranın altında
   kalın başlık + bir iki cümle açıklama, sonda "Bu taslağın kuralları"). Webde masaüstü görünümü gerekiyorsa aynı
   sayfada geniş çerçeve kullan.
2. Aynı renkler ve bileşenler (yeşil `#00724c`, turuncu buton `#ea803f`, çipler, ilerleme çizgileri); dış kütüphane yok.
3. Örnek kişi/veri kullan (ör. Ayşe Yılmaz, Sicil 48213); Eminevim logosu taslakta yok, "Tasarruf Yanımda" yazısı var.
4. Chrome ile ekran görüntüsü alıp kontrol et (390 px'te yatay taşma olmasın), `master`'a commit + push, Pages linkini ver.
5. `taslak/README.md` ve `linkler.html` listelerine ekle.
