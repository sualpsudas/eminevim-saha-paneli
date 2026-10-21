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
Paylaşım için tek sayfa: `linkler.html` → https://sualpsudas.github.io/eminevim-saha-paneli/linkler.html — yeni sayfa eklenince güncelle.
- Telefonda: yalnız sol üstte küçük "Uyg / Web" tuşları, sayfa gerçek boyutunda tam ekran.
- Bilgisayarda: iPhone 15 çerçevesi (393×852); uygulamanın bilgisayar görünümü YOK, Telefon/Bilgisayar seçimi yalnız Web'de;
  sağda "Yapılacaklar" paneli. Adreslenebilir: `#uygulama-telefon`, `#web-telefon`, `#web-bilgisayar`.
- Yapılacaklar ortak olacak: kullanıcı Google E-Tablo açıp "Bağlantıya sahip herkes · Düzenleyen" linkini verecek →
  `linkler.html` içinde `var TABLO = ""` doldurulur, panel tabloyu gömer. Link gelene kadar liste yalnız tarayıcıda (localStorage).
  (Drive bağlayıcısının yazma izni yok; üyeliksiz dış JSON servisleri denenmedi/çalışmadı — kullanıcı Google E-Tablo'yu seçti.)

## Kararlar (2026-10-20 / 21)
- Proje adı Tasarruf Yanımda; amaç cumartesi yığılmasını hafta içine yaymak. Müşteriye uygulama indirtilmez, önce **web**.
- Uygulama ve web formu ilk aşamalar; aynı akış/dil. Yeni müşteri üyeliksiz; finansman/bütçe yalnız üyelere ("Finansmanlarım").
- Web formunda **e-posta istenmez** (2026-10-21 akşam); temsilci bilgisi ve takip linki telefona mesajla gider (önizleme "Gelecek mesajı önizle").
  Web formu **gerçek site formu gibi**, temsilci çağırma **isteğe bağlı** seçenek.
- Web formu demo: her açılışta ve "Yeni başvuru"da örnek bilgilerle dolu gelir (Mehmet Demir, 532 123 45 67; takvimde ilk hafta içi günü + 18:00, haritada Caferağa/Kadıköy, Ev).
- Bütçe hesabı (kaba formül) ilk temasta gösterilmez; rakamlar müşteriye açılacaksa şirketin onaylı hesabı + uyum/hukuk onayı şart.
- Uygulama dosyası (`Eminevim Saha Paneli.dc.html`) 2026-10-21'den beri değiştirilmedi; kullanıcı "şimdilik HTML'den
  (web formu, taslak, önizleme) devam" dedi — uygulamaya dokunmadan önce sor.

## Açık işler
- Google E-Tablo linki (yukarıda) → yapılacaklar ortak hâle gelsin.
- iPhone (TestFlight) derlemesi yapılmadı; web hâli güncel. Codemagic ile yeni derleme gerekiyor (`IOS_TESTFLIGHT.md`).
- Finansmanlarım rakamları için Eminevim uyum/hukuk onayı.
- Klasör/depo adı eski (eminevim-saas / eminevim-saha-paneli) — yeniden adlandırma kararı verilmedi (Pages adresi değişir).
- Öneri olarak bekliyor: cumartesi yığılmasını rakamla gösteren analiz (SPY raporları), yönetime kısa sunum.

## Teknik notlar
- Uygulama: tek dosya `Eminevim Saha Paneli.dc.html` (şablon `{{ }}`, `<sc-if>`, `<sc-for>`; durum `state`, görüntü değerleri
  `renderVals()`), `support.js` çalışma zamanı. `?native=1` telefon düzeni ve service worker kapalı.
- Web formu: `web-basvuru/form_bolumu.html` (TY_CSS / TY_FORM / TY_TAKIP / TY_JS blokları) → `python olustur.py` canlı
  eminevim.com'u indirir, formu masaüstü paneline ve mobil pencereye koyar (mobilde `tk-input*Mobil*` sınıfları), izleme
  kodlarını çıkarır, tüm `<a>`'ları etkisizleştirir (`data-ty-dis` hariç). Değişiklikten sonra mutlaka yeniden üret.
- Test: conda `scrapling` Python + Playwright `channel="chrome"` (sunucuda Chromium indirme yok); yerel sunucu
  `python -m http.server 8799`. Pages yayını ~1 dk; `curl ...?t=$RANDOM` ile kontrol.
- Bu depoda git kimliği yerel ayarlı: `sualpsudas <sualpsudas@users.noreply.github.com>`.

## Müşteri ekranı ilkeleri
- Olabildiğince basit; gereksiz yazı yok, her ekranda tek soru grubu ve tek ana buton.
- İlk temasta üyelik, şifre, konum izni, sohbet yok. Alanlar: ad, soyad, telefon; temsilci istenirse gün, saat, haritadan yer (İş yeri/Ev). E-posta yok.
- Korkutmayan dil: "Temsilciniz önce sizi arar", "Ücretsiz", "Görüşmede ödeme alınmaz", "Sicil numarası aynıdır".
  "Takip" müşteriyi değil temsilciyi anlatır ("Temsilcinizin nerede olduğunu görürsünüz").
- Cumartesi engellenmez; hafta içi günler önce gelir, cumartesi "yoğun" etiketiyle durur.
- Temsilci bilgileri ve takip linki telefona **mesajla** gider (e-posta istenmez; 2026-10-21 kararıyla değişti).
- Yeni müşteri üye olmadan sade akışla ilerler (uygulamada giriş ekranı → "Yeni Müşteri", `ya*` durumları).
  Finansman/bütçe hesabı yalnız **üyelere**, "Finansmanlarım" sekmesinde; web formu bunun için uygulama linki verir.
- **Web formu gerçek sitedeki gibi görünmeli** (kullanıcı isteği, 2026-10-21): sitenin başlığı, gri kutucukları
  (`tk-inputGri` / mobilde `tk-inputMobilGri`), onay kutuları ve turuncu "Gönder". Formda "Tasarruf Yanımda" adı, açıklama
  simgeleri, adım çubuğu ya da "bilgiler gönderilmez" gibi önizleme yazısı YOK; sayfa sitenin kendi başlığıyla en üstten açılır.
  Sıra: Ad, Soyad, Telefon → iki onay kutusu → **"Temsilcimiz size gelsin" düğmesi** (yalnız konum simgesi + yazı) → Gönder.
  Formun altında açılan uzun alan YOK. Düğmeye basınca **takvim penceresi** (yarından 3 hafta, pazar kapalı, cumartesi turuncu
  nokta "yoğun", saat 10:00–20:00) → "Onayla" → **harita penceresi** (Leaflet + OpenStreetMap, ortadaki iğne; adres Nominatim'den;
  İş yeri / Ev) → "Onayla" → düğme seçimi gösterir ("Pzt 26 Eki, 14:00 · Kadıköy", × ile kaldırılır).
  Pencereler telefonda tam ekran ve **dvh** ile görünür alana oturur (tarayıcının üst/alt çubuğu); bilgisayarda ortada.
  Site modalının içindeyse pencereler modalın içine eklenir (Bootstrap odak kilidi) ve açıkken modal z-index 10000'e çıkar
  (sitenin solda gizli mobil menüsü z 9999, gölge düşürüyordu).
  Eksik kutu sitenin turuncu hata renginde (`--tdk_turuncuHata`) ve uyarı altında; telefonda "Gönder" pencere altında sabit.
- Önizlemede (`linkler.html`) web formu telefon görünümü Safari çubuklarıyla: iPhone 15 görünür alan 393×659 (üst 59, alt 134 px).
  Test de bu boyutta yapılmalı.

## Taslak isteği gelirse (web ya da uygulama)
Kullanıcı "taslak göster" dediğinde çalışan kod değil, **sunuma eklenebilir ekran taslağı** hazırla:
1. `taslak/<konu>.html` olarak tek dosya; şablon `taslak/uygulama-akisi.html` (telefon çerçeveleri, her ekranın altında
   kalın başlık + bir iki cümle açıklama, sonda "Bu taslağın kuralları"). Webde masaüstü görünümü gerekiyorsa aynı
   sayfada geniş çerçeve kullan.
2. Aynı renkler ve bileşenler (yeşil `#00724c`, turuncu buton `#ea803f`, çipler, ilerleme çizgileri); dış kütüphane yok.
3. Örnek kişi/veri kullan (ör. Ayşe Yılmaz, Sicil 48213); Eminevim logosu taslakta yok, "Tasarruf Yanımda" yazısı var.
4. Chrome ile ekran görüntüsü alıp kontrol et (390 px'te yatay taşma olmasın), `master`'a commit + push, Pages linkini ver.
5. `taslak/README.md` ve `linkler.html` listelerine ekle.
