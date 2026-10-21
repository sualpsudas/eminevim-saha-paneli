# Tasarruf Yanımda

Tek proje: **Tasarruf Yanımda** (klasör adı `eminevim-saas`, depo `sualpsudas/eminevim-saha-paneli` eski adlardır).
Ana konu **müşteri teması**: hafta içi çalışan müşteri cumartesi şubeye yığılmasın, temsilci (SPY) uygun yer/saatte
müşterinin yanına gitsin; müşteri kimin geleceğini önceden görsün ve görüşme günü temsilcinin yolda olduğunu izlesin.
Uygulama ve web formu bu fikrin ilk aşamalarıdır. İkisi **aynı marka görünümünü** kullanır (aşağıdaki Ürün kuralları);
senaryoları birebir aynı olmak zorunda değil.

## Ürün kuralları (2026-10-21, kullanıcıyla konuşarak yazıldı — bundan sonraki işlerin dayanağı)
Bu bölüm aşağıdaki eski kararlarla çelişirse **bu bölüm geçerlidir**. Uygulama adım adım, kullanıcıyla konuşarak yapılır;
her adım bitince burada "Durum" güncellenir.

1. **Rol ayrımı.** Uygulama = kapsamlı içerik (başvuru takibi, sohbet, finansman aracı, ayarlar). Web formu ve sitedeki
   yönlendirmeler = **hızlı aksiyon**: her şey yok, eksik kalan kısım uygulamaya yönlendirmeyle tamamlanır.
2. **Marka birliği.** Uygulamayı kullanan müşteri de personel de eminevim.com'a baktığında **aynı firma** olduğunu anlamalı:
   renkler, logolar, görseller, yazı tipi, düğme/kutu biçimi siteyle aynı. Kaynak her zaman eminevim.com (değerler
   "Kararlar"daki "Görünüm kaynağı" maddesinde).
3. **Web formu akışı.**
   - Formda yalnız **"Temsilci çağırmak istiyorum" için sağa-sola kaydırmalı düğme** (telefonla seçeneği yok; 2026-10-21 değişikliği).
   - Düğme açılınca **ayrı pencere** açılır: 1/2 harita (konum izni istenir, üstte WhatsApp'taki gibi adres/mekân arama,
     sağ altta **"Hizmet bölgesini göster"** → bölgeler görünürken düğme **"Konumuma dön"** olur ve seçili konuma odaklar),
     2/2 gün ve saat → "Onayla". Pencere onaysız kapanırsa düğme kapanır. Formda tek satır özet + "Değiştir".
   - Harita sade ama **mekânlar görünür** olmalı. Uzaktan bakınca yalnız harita + **hizmet bölgeleri yeşil** alan
     (kompakt görünüm). Hizmet bölgeleri şimdilik: **İstanbul Ümraniye, Ataşehir, Üsküdar**.
   - Seçilen konum hizmet bölgesinin içindeyse ilerlenir.
   - Gönderince **yeni ekran: "Başarılı"** — kurumsal ama samimi dil: talebin alındığı, temsilcinin iletişime geçeceği,
     belirlenen saatte belirtilen konumda olacağı. Ardından: "Kampanyalarımıza, Finansman Aracımıza ve size atanan
     temsilci hakkında detaylara ulaşmak için Eminevim uygulamasını kullanabilirsiniz." + uygulamaya geçiş.
4. **Web'den uygulamaya geçiş.** Uygulama, formdaki **telefon numarasıyla kayıtlı müşteri** gibi açılır; içinde **henüz
   kayıtlı finansman yoktur**. Bölümler: **Başvuru takibi, Sohbet, Ayarlar, Finansman aracı**.
5. **Hoş geldiniz penceresi.** Uygulamaya yeni gelen herkese (uygulamadan telefonla kayıt olan ya da web formundan gelen):
   küçük, **3 sayfalık**, "Hoş geldiniz" ile başlayan, uygulamayı **çok basit** anlatan pencere.
6. **Giriş ekranındaki "Kayıtlı Müşteri" (demo senaryosu).** Daha önce kayıt olmuş, **finansmanını belirlemiş**, temsilciyle
   **sohbet ederek randevusunu netleştirmiş** ve **temsilciyi beklediğini** bildiğimiz müşteri.
7. **Uygulamadan telefonla kayıt olan yeni müşteri** için de web'deki gibi **"Temsilci iste"** seçeneği olur.

8. **Kullanıcı cevapları (2026-10-21):**
   - Gün ve saat seçimi **kalır**, **haritadan sonra** gelir.
   - **Bölge dışı konum:** "Bu bölgede henüz hizmet yok, sizi telefonla arayalım" denir ve normal (telefonla) başvuruya dönülür.
   - **Web'deki finansman penceresi yedekte:** kod durur, sitedeki Konut/Araç/İşyeri kutularıyla **bağlantısı kesildi**
     (ileride dönülebilir).
   - "Temsilci çağırmak istiyorum" seçimi **onay kutularından sonra** durur.
   - Temsilci bilgisi **SMS olarak da gider** ve uygulamada da görünür. Temsilciler için **sentetik (yapay) fotoğraflar**
     üretilip SMS önizlemesinde ve uygulamada kullanılır (gerçek kişi fotoğrafı kullanılmaz).

**Durum:** Adım 1 bitti (2026-10-21, sonra pencereye taşındı): kaydırmalı düğme → pencere (Leaflet + OSM; uzaktayken soluk
gri + yeşil bölgeler ve adları, yakında renkli ve mekânlı; konum izni yoksa demo için Ataşehir örnek konumu; dokun/sürükle;
Nominatim araması İstanbul sınırlı) → gün/saat. Bölge dışı: pencerede "Telefonla görüşmeyle devam et" → formda turuncu not,
başvuru telefonla. Bölge sınırları `form_bolumu.html` içinde `BOLGELER`. CARTO sade harita anahtar istiyor — kullanılmaz.
Önizleme iframe'inde `allow="geolocation"` gerekli (linkler.html'de var).
Adım 2 bitti: "Başarılı!" ekranı (ad soyad, gün/saat/yer özeti, "Size atanan temsilcinin adını,
fotoğrafını ve sicil numarasını Eminevim uygulamasından kontrol edebilirsiniz.", yeşil kartta uygulama yazısı + turuncu
"Uygulamayı aç"; link `?kaynak=web&ad=&tel=&gun=&saat=&yer=` taşır — adım 3'te uygulama bunu okuyacak). Mesaj önizleme
düğmesi kaldırıldı (SMS biçimi ve sentetik fotoğraflar açık soru). Adım 3–6 yapıldı (2026-10-21, kullanıcı "uygulama senaryolarını kontrol et" dedi):
- **Giriş ve kayıt telefonla** (e-posta yok). "Kayıtlı Müşteri" = telefon + şifre. "Yeni Müşteri" = telefonla kayıt
  (ad soyad, telefon, şifre; adres de sorulmaz) → KVKK → Hoş geldiniz. Eski üyeliksiz "Temsilcimiz size gelsin" akışı
  girişte yok; aynı ekranlar yalnız uygulama içi "Temsilci iste" ve "Görüşme günü (örnek)" için kullanılır (`yaKaynak:"uygulama"`).
- **Web'den gelen:** `?kaynak=web&ad=&tel=&gun=&saat=&yer=` → giriş ekranı atlanır, telefonla kayıtlı, finansman yok,
  talep Başvurum'da, temsilci atanmış (bölgeye göre: Üsküdar→Derya Aksoy, Ümraniye→Berk Cengiz, diğer→Onur Kaya) ve
  Sohbet'te ilk mesajı var. Telefonla başvuruda "Sizi arayacağız" + "Temsilci iste".
- **Müşteri sekmeleri (2026-10-21 gece güncel):** **Randevum** (eski Başvurum; yeşil durum kartında gün/saat/yer, kısa adım
  listesi, temsilci tek satır + **"Bilgiler"** tuşu → alt pencerede fotoğraf/şube/sicil, Mesaj gönder; görüşme günü
  "Temsilcinizi takip edin") · Sohbet (başlıkta da "Bilgiler"; temsilci ilk mesajda saati önerir, müşteri **"Saati onayla"**
  düğmesiyle onaylar → durum `netlesti`) · Finansman ("+ Yeni", "Değiştir") · Ayarlar. Durumlar: alindi → atandi → netlesti → gorusme.
  Gereksiz/tekrarlı yazılar ayıklandı (Gün/Saat/Yer tablosu, adım alt yazıları, "Örnek görünüm" notu).
- **Randevum ek özellikler (2026-10-21 gece):** "Gün / saati değiştir" (yeni öneri sohbete düşer, temsilci onaylayınca netleşir;
  durum `degisti`) ve "İptal et" (onay penceresi); gecikme uyarısı (Ayşe: 10 dk, yeni varış 18:10); takip ekranında
  "Örnek: görüşme bitti" → durum `tamamlandi` → **puan penceresi** (1–5 yıldız) + Randevum'da **Görüşme özeti** (konu, tutar,
  peşinat, vade, aylık ödeme örnek, cayma hakkı 14 gün; "Bilgiler doğru" / "Bir sorun var" → temsilciden bağımsız müşteri
  ilişkileri arar) + "Yeni randevu iste". Temsilci "Bilgiler" penceresinde puan / deneyim / görüşme sayısı (`TEMSILCI_DETAY`).
  Finansman kaydı temsilci varsa sohbete otomatik not olarak düşer; ilk adım yazısı temsilci yoksa söz vermez.
  Bölge dışı telefon talebi (`bolgeDisi`, web'den `&bolgeDisi=1`) → "Başka adres için temsilci iste".
- **Hoş geldiniz:** 3 sayfalık alt pencere, her sayfada basit resim (satır içi SVG) + tek kısa cümle (yeni kayıt ve web'den gelen).
- **Kayıtlı Müşteri (Ayşe Kaya):** KVKK sorulmaz (önceden onaylamış); **görüşme günü** senaryosu — bugün 18:00, temsilci
  Onur Kaya yolda (~12 dk), konut finansmanı var, sohbette randevu dünden netleşmiş.
- Uygulama içi "Temsilci iste" (2026-10-21 gece): web penceresiyle aynı akış — 1/2 harita (`konum-sec.html`, iframe;
  seçimi `postMessage {tip:"ty-konum"}` ile yollar; `BOLGELER` form_bolumu.html'den kopya, bölge değişirse ikisini de
  güncelle) → 2/2 gün + saat (10:00–20:00, web'deki gibi) → "Talebiniz alındı" → Başvurumu gör. Bölge dışı → telefonla talep.
  Yalnız talebi olmayan müşteride Başvurum'da görünür. **Finansman sekmesinde temsilci bulma/iletişim yok**; eski
  "Temsilci Bul" eşleştirme ekranı (customerNav "tasarruf") kaldırıldı. Temsilci fotoğrafı yerine baş harfler.
- Önizleme telefonda `dvh` + visualViewport ile görünür alana oturur (iOS Safari alt çubuğu düğmeleri kapatıyordu).
- **Kapıda QR doğrulama (2026-10-21):** Görüşme günü Randevum'da "Kapıda kimliğini doğrula" → QR (vendor/qrcode.min.js,
  internetsiz) + 4 haneli yedek kod (`DOGRULAMA_KODU` 4821, SMS ile de gider). Personel (SPY) Görüşmeler'in üstünde
  "Bugünkü randevu · Ayşe K." kartı → "Kapıda: müşterinin QR'ını okut" (tarayıcı ekranı, "Örnek: QR okundu" ya da kod gir)
  → müşterinin ekranı yeşil: "Temsilciniz yanınızda · Kimliği 18:10'da doğrulandı"; varış kaydı. Durum `demoDogrulama`
  (oturumlar arası kalır; görüşme bitince sıfırlanır). Güvenlik mantığı: onay MÜŞTERİNİN ekranında görünür, sahte biri
  okutsa da ekran değişmez; ekran yeşile dönmezse bilgi verme, 444 36 46.
- **Personel ekranları marka birliği (2026-10-21):** kartlar düz (beyaz, #DDD çizgi, 14 px köşe; degrade/cam gölge yok),
  kırmızı/altın yerine sitenin turuncu tonları (#B25E30 / #EA803F / #FCE0D4), koyu ton lacivert #1E3856, sekme anahtarı
  hap biçimi, tek yazı tipi GOTHIC (Manrope kaldırıldı), küçük etiketler büyütüldü. Yeni personel ekranı da bu kurallarla.
Sıradakiler: açık sorular: SMS biçimi, sentetik fotoğraflar.

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
- Uygulama ve web formu ilk aşamalar; aynı marka görünümü (akış birebir aynı olmak zorunda değil, bkz. Ürün kuralları). Yeni müşteri üyeliksiz; finansman/bütçe yalnız üyelere ("Finansmanlarım").
- Web formunda **e-posta istenmez** (2026-10-21 akşam); temsilci bilgisi ve takip linki telefona mesajla gider (önizleme "Gelecek mesajı önizle").
  Web formu **gerçek site formu gibi**, temsilci çağırma **isteğe bağlı** seçenek.
- Web formu demo: her açılışta ve "Yeni başvuru"da örnek bilgilerle dolu gelir (Mehmet Demir, 532 123 45 67; takvimde ilk hafta içi günü + 18:00, haritada Caferağa/Kadıköy, Ev).
- Bütçe hesabı (kaba formül): 2026-10-21 kullanıcı kararıyla web sitesinde de var — sitedeki Konut / Araç / İşyeri kutuları
  (üst menü, Çözümlerimiz kartları, mobil menü) "Ödeme planınızı oluşturun" penceresini açar; hesap uygulamadakiyle aynı
  (`senaryoHesapla`), "Örnek hesaplamadır" notuyla. Gerçek yayında şirketin onaylı hesabı + uyum/hukuk onayı yine şart.
- **Görünüm kaynağı eminevim.com** (2026-10-21): renk/köşe/kutu/yazı tipi sitenin :root değerleri — yeşil #00724c,
  ana düğme turuncu #ea803f, gri hap kutu #EEE (köşe 22px), kart köşesi 14px, yazı #666, çizgi #DDD, açık yeşil #e9f0ed,
  yazı tipi GOTHIC → "Century Gothic" (site dosyası başka adrese izin vermiyor). Uygulama da bu değerlere çevrildi
  (tema değişkeninde `--kutu`); yeni ekran/bileşen bu değerlerle yapılır, web ve uygulama birbirine uyumlu tutulur.
- Temsilci başvurudan hemen sonra gösterilmez: "Görüşme saatinden önce temsilciniz hakkında bilgilendirileceksiniz".
  Yer türü (İş yeri / Ev) yok. Teşekkürde: "Görüşme öncesinde Çözümlerimize, Kampanyalarımıza ve Finansman aracına göz
  atmak isterseniz Eminevim uygulamasını indirebilirsiniz." (uygulamada aynı dil "üye olun" ile).
- Uygulama dosyası 2026-10-21 akşamı kullanıcı isteğiyle değişti: tüm ekranlar site görünümüne çevrildi, yeni müşteri
  akışı web kararlarına uyduruldu (yer türü ve e-posta yok, temsilci hemen gösterilmez), finansman sonuç kartı web'deki gibi.

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
- **Ödeme / ücret güvencesi cümleleri ASLA kullanılmaz** ("Görüşmede ödeme alınmaz", "hiçbir ödeme alınmaz", "Ücretsiz" vb.;
  kullanıcı kuralı 2026-10-21). Dil kurumsal ama samimi: "Temsilcimiz görüşmeden önce sizinle iletişime geçecek", "Sicil numarası aynıdır".
  "Takip" müşteriyi değil temsilciyi anlatır ("Temsilcinizin nerede olduğunu görürsünüz").
- Cumartesi engellenmez; hafta içi günler önce gelir, cumartesi "yoğun" etiketiyle durur.
- Temsilci bilgileri ve takip linki telefona **mesajla** gider (e-posta istenmez; 2026-10-21 kararıyla değişti).
- Yeni müşteri üye olmadan sade akışla ilerler (uygulamada giriş ekranı → "Yeni Müşteri", `ya*` durumları).
  Finansman/bütçe hesabı yalnız **üyelere**, "Finansmanlarım" sekmesinde; web formu bunun için uygulama linki verir.
- **Web formu gerçek sitedeki gibi görünmeli** (kullanıcı isteği, 2026-10-21): sitenin başlığı, gri kutucukları
  (`tk-inputGri` / mobilde `tk-inputMobilGri`), onay kutuları ve turuncu "Gönder". Formda "Tasarruf Yanımda" adı, açıklama
  simgeleri, adım çubuğu ya da "bilgiler gönderilmez" gibi önizleme yazısı YOK; sayfa sitenin kendi başlığıyla en üstten açılır.
  Sıra: Ad, Soyad, Telefon → iki onay kutusu → (seçildiyse tek satır finansman planı) → **"Temsilcimiz size gelsin" düğmesi** (yalnız konum simgesi + yazı) → Gönder.
  Formun altında açılan uzun alan YOK. Düğmeye basınca **takvim penceresi** (yarından 3 hafta, pazar kapalı, cumartesi turuncu
  nokta "yoğun", saat 10:00–20:00) → "Onayla" → **harita penceresi** (Leaflet + OpenStreetMap, ortadaki iğne; adres Nominatim'den;
  yer türü sorulmaz) → "Onayla" → düğme seçimi gösterir ("Pzt 26 Eki, 14:00 · Kadıköy", × ile kaldırılır).
  Pencereler telefonda tam ekran ve **dvh** ile görünür alana oturur (tarayıcının üst/alt çubuğu); bilgisayarda ortada.
  Site modalının içindeyse pencereler modalın içine eklenir (Bootstrap odak kilidi) ve açıkken modal z-index 10000'e çıkar
  (sitenin solda gizli mobil menüsü z 9999, gölge düşürüyordu).
  Eksik kutu sitenin turuncu hata renginde (`--tdk_turuncuHata`) ve uyarı altında; telefonda "Gönder" pencere altında sabit.
- Önizlemede (`linkler.html`) Safari'nin üst durum çubuğu + alt adres çubuğu **yalnız "Web formu · Telefon"** görünümünde
  (iPhone 15 görünür alan 393×659: üst 59, alt 134 px); Uygulama ve Bilgisayar görünümünde ve gerçek telefonda yok
  (kullanıcı kararı 2026-10-21). Test de bu boyutta yapılmalı.
- Web "Başarılı" ekranı: bilgisayarda "Uygulamayı aç" yerine App Store / Google Play simgeleri + kısa cümle; telefonda düğme kalır.
  Karar cihaza göre: masaüstü paneli (`.tk-desktopForm`) ya da fareyle doğrudan açılan sayfa (`html.ty-masaustu`; site 1200 px
  altında telefon düzenine geçtiği için dar pencerede de). Başarılı ekranında yan panel 280 → 460 px (`.ty-genis`), sarkmaz.

## Taslak isteği gelirse (web ya da uygulama)
Kullanıcı "taslak göster" dediğinde çalışan kod değil, **sunuma eklenebilir ekran taslağı** hazırla:
1. `taslak/<konu>.html` olarak tek dosya; şablon `taslak/uygulama-akisi.html` (telefon çerçeveleri, her ekranın altında
   kalın başlık + bir iki cümle açıklama, sonda "Bu taslağın kuralları"). Webde masaüstü görünümü gerekiyorsa aynı
   sayfada geniş çerçeve kullan.
2. Aynı renkler ve bileşenler (yeşil `#00724c`, turuncu buton `#ea803f`, çipler, ilerleme çizgileri); dış kütüphane yok.
3. Örnek kişi/veri kullan (ör. Ayşe Yılmaz, Sicil 48213); Eminevim logosu taslakta yok, "Tasarruf Yanımda" yazısı var.
4. Chrome ile ekran görüntüsü alıp kontrol et (390 px'te yatay taşma olmasın), `master`'a commit + push, Pages linkini ver.
5. `taslak/README.md` ve `linkler.html` listelerine ekle.
