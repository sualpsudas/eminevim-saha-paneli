# Tasarruf Yanımda

Tek proje: **Tasarruf Yanımda** (klasör adı `eminevim-saas`, depo `sualpsudas/eminevim-saha-paneli` eski adlardır).
**Amaç (2026-10-22, kullanıcı onaylı; eski "cumartesi yığılmasını hafta içine yaymak" tanımının yerine):** İlke (kaynak yönetimi) "Saha gücümüzün bir bölümü bizi çağıran müşteriye ayrılır; diğerleri sahada çalışır; dağılım talebe göre ayarlanır" (2026-10-23: saha personeli = **SPY** (Saha Portföy Yöneticisi), "SPY'ler" diye yazılır; ayrı ekip adı YOK, talepleri "Tasarruf Yanımda'da aktif SPY'ler" karşılar; ilk aşamada en başarılı SPY'ler, "teşvik" olarak (ödül değil); sonra kimlerin aktif olacağı belirsiz; atamada ilk ölçüt başarı, yöntem sonra (anlık hizmet/çağrı uygulamaları referans, marka adı yazma); "pilot" değil "pilot bölge denemesi"; "ayağına gitmek" yerine "dilediği yerde ve saatte ulaşmak"; Finansman Aracı + isteğe bağlı bilgiler (meslek) = SPY için görüşme öncesi ön bilgi; aynı gün talepleri de; taşmada takım lideri atar. Düzenleme claude.ai belgesinde (https://claude.ai/artifact/WBKdRt8hzNXjTymiJzqG9p, oturum ister); paylaşım için sitede rapor/proje-cercevesi.html (linkler.html alt satırı) — belge değişince bu sayfa ve md kopyası da güncellenir; md kopyası rapor/tasarruf-yanimda-proje-calismasi/00-proje-cercevesi.md; prototip takvimi henüz yarından başlıyor) (var olan talebe yetişmek talep yaratmaktan verimli — varsayım; ana ölçü temsilci saati başına görüşme/satış). Yani mevcut saha
satış gücüne **müşteriden doğrudan gelen talep kanalı** eklemek — ekip müşteriyi bulmaya devam eder, görüşmek isteyen müşteri
de temsilci (SPY) çağırabilir; temsilci uygun yer/saatte gider, müşteri kimin geleceğini önceden görür, görüşme günü takip eder.
"Talebe ulaşan saha gücümüzü, talebin bize ulaştığı bir kanalla tamamlıyoruz." Cumartesi yoğunluğu ana amaç değil; satış
artışı kanıtlanmış değil, pilotta ölçülecek. Ayrıntı ve araştırma: `rapor/tasarruf-yanimda-proje-calismasi/`.
Uygulama ve web formu bu fikrin ilk aşamalarıdır. İkisi **aynı marka görünümünü** kullanır (aşağıdaki Ürün kuralları);
senaryoları birebir aynı olmak zorunda değil.

## Ürün kuralları (2026-10-21, kullanıcıyla konuşarak yazıldı — bundan sonraki işlerin dayanağı)

### 2026-10-22 güncellemesi — randevu odaklı akış

- Web başvurusu ve uygulamadan yeni kayıt aynı randevu modeline bağlanır. Randevum'da saat doğrudan onaylanır; sonuç sohbete düşer.
- Randevu durumları: `alindi → atandi → netlesti → yolda → gorusmede → tamamlandi`; iptal `iptal` olarak saklanır. Yeni randevuda önceki kayıt müşteri geçmişine taşınır. Puan vermek yeni randevu şartı değildir.
- Değişiklik `degisiklik` alanında bekler; eski kesin saat korunur. Personel yeni öneriyi onaylayınca gün/saat/konum güncellenir. Yoldayken de değişiklik/iptal erişimi vardır.
- Personelin Yola çık / gecikme / QR / bitir işlemleri seçili randevuya bağlıdır. Kod randevu, temsilci ve revizyonla eşleşir, 10 dakika geçerlidir ve kullanıldığında tüketilir. Gerçek kamera ve sunucuda kimlik doğrulama henüz yoktur; demo tarama düğmesi ve kod girişi korunmuştur.
- Takipte son bilinen temsilci ve görüşme noktası, tahmini varış ve eski konum uyarısı görünür. Haritadaki çizgi yol ağına göre hesaplanmış navigasyon rotası değildir. Gerçek GPS/ETA için canlı servis gerekir.
- Personel görüşmeyi bitirince aynı müşteriye özet/not/sonraki adım gider. Puan penceresi kendiliğinden açılmaz. Müşteri düzeltme açıklaması yazabilir; destek talebi ASK panelinde incelenip yanıtlanır, durum müşteride görünür.
- Çalışma durumu ve yaş aralığı **ilk başvuruda zorunlu değildir**. Başvurudan sonra isteğe bağlı, atlanabilir; sonra düzenlenebilir. Webde başarı ekranında seçilen bilgiler uygulama bağlantısıyla aktarılır. Kesin yaş/doğum tarihi istenmez.
- Randevu ve hesaplar bu tarayıcı sekmesinin `sessionStorage` alanında saklanır. Gerçek hesap güvenliği, cihazlar arası eşitleme ve kalıcı sunucu kaydı henüz yoktur.
- Web kaynak formu değişince `python web-basvuru/olustur.py`; native paket için `npm run web:sync`. Yeni `appointment.js`, konum seçimi, rota ve QR kitaplığı native/PWA paketlerine dahil edilmiştir.
- **SMS kodu ve telefonla giriş (2026-10-22):** Web'de temsilci çağırma seçiliyse başarı ekranında telefona giden SMS
  önizlenir: 6 haneli **uygulama giriş kodu** (24 saat) + "Uygulamayı indirip randevu takibi, temsilciyle sohbet ve finansman
  aracı hizmetlerimizden faydalanabilirsiniz" + uygulama linki. Web → uygulama linki artık doğrudan giriş YAPMAZ: kod ekranı
  (telefon dolu) → kod → **parola oluştur** → randevu açılır (onaylar web'de alındı, KVKK sorulmaz). Giriş ekranında seçenekler
  **Giriş Yap / Kayıt Ol** (2026-10-22). "Kayıt Ol": telefon (başlıksız) → kod (10 dk) → ad soyad + parola → KVKK → Hoş geldiniz.
  **Test aşaması: telefon, kod, ad soyad ve parola (test123) hazır dolu gelir.** "Giriş Yap": telefon + parola; "Parolamı unuttum ·
  SMS koduyla gir" → kod → yeni parola. Demo: kod gerçek SMS yerine aynı sitedeki `localStorage` "ty-sms-kod"da; kod
  ekranında "Demo: … Kodunuz" görünür. Gerçek yayında kod sunucuda üretilip SMS'le gönderilmeli, parola sunucuda saklanmalı.
- Doğrulama: `npm test`; yerel 8799 sunucusunda `tests/browser-flows.py` ve `tests/web-flows.py` (Playwright + Chrome). Senaryo sayfası bu geliştirmeden sonra ayrıca ele alınacak.

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
- **Personel (2026-10-22): tablet düzeni.** Personel girişi (SPY, Takım Lideri, SGL, ASK) `isPersonel` → yeni `.tp` düzeni:
  üstte yeşil bant (logo; sağda kişi: ad, rol · durum, fotoğraf ya da baş harf → Profil), **sekmeler her cihazda ALTTA,
  müşteri uygulamasındaki gibi** (kullanıcı isteği): Görüşmeler / Performans / Saha Canlı / Profil (SPY'da Saha Canlı yok,
  SGL-ASK'ta Görüşmeler yok). Profil: Müsait/Molada (görüşmede iken otomatik "Görüşmede"), Çıkış yap. Senaryo'daki tablet de aynı. Önizleme (linkler.html) uygulamadan
  `postMessage {tip:"ty-cihaz", cihaz:"tablet"}` alınca çerçeveyi yatay tablete (1180×820) çevirir, çıkışta telefona döner.
  Dar ekranda (<900 px) tek sütun; seçilen görüşmenin ayrıntısı listenin üstünde açılır.
  - **Görüşmeler** (SPY ve TL; takım liderleri de görüşme yapar): tarih sırası, gruplar Yeni talepler · Bugün · Yarın ·
    Sonraki günler · Geçmiş; durumlar **Bekleyen** (yeni talep / yoldasınız alt hâlleri) → **Şu an görüşülüyor** (QR ile
    doğrulanınca, görüşme bitene kadar) → **Gerçekleşti**; süzgeç Tümü/Bekleyen/Şu an/Gerçekleşti. Sağda ayrıntı ve
    eylemler: Kabul et / Devret · Yola çık · Vardım: QR okut · Görüşmeyi bitir · özeti gönder. Veri `tpTohum` (demo) +
    uygulamadan gelen talepler `tpEkGorusmeler`. Ayşe K. satırı müşteri uygulamasıyla bağlı (`demoDogrulama`,
    `gorusmeBittiDemo`, `demoPuan`).
  - **Bugünkü rota**: `rota.html?b=şube&n=lat,lng,etiket,durum|…` (Leaflet; numaralı iğneler, saat sırası). Ayrı Harita sekmesi yok.
  - **Saha Canlı** (TL/SGL/ASK): 3 sayı (Şu an görüşmede · Yolda · Bugün gerçekleşen) + personel listesi (durum, şube,
    sıradaki randevu, süzgeç). Mesai dışında örnek olarak son iş gününün 15:30 durumu gösterilir (başlıkta yazar).
  - **Performans** eski ekranlardan aynen taşındı.
  - Eski telefon personel ekranları (`isSpy`/`isManager`: geri arama sayaçlı liste, eski harita akışı Kabul/Geliyorum/Ulaştım,
    Geçmiş) artık gösterilmiyor; kod duruyor, temizlenebilir. Uydurma "Yeni Başvuru" bildirim zamanlayıcısı kapatıldı.
  - **Fotoğraflar:** `TEMSILCI_DETAY[*].foto` (boşsa baş harf). Sentetik portre komutu ve dosya adları `assets/temsilci/OKUBENI.md`;
    kullanıcı üretip gönderecek (gerçek kişi fotoğrafı yok; açık lisanslı uygun hazır görsel bulunamadı).
- `senaryo.html` — **Senaryo** sekmesi (linkler.html'de üçüncü üst sekme "Senaryo", `#senaryo-telefon`; kendi sayfası
  `senaryo.html#adim-5-bilgisayar`). Senaryo tasarım tahtası: solda müşteri (Telefon / Bilgisayar seçimi; bilgisayarda
  site + uygulamasız **takip sayfası** `eminevim.com/takip/…`, kapıda SMS linkiyle telefon), sağda personel **hep tablet,
  yatay** (sol yeşil menü + iki sütun). Alt bantta adım açıklaması, İleri/Geri, adım noktaları, otomatik oynat (6 sn), ok tuşları.
  Etkin taraf turuncu etiket + vurgulu düğme; telefonda tek cihaz, etkin taraf öne gelir. Ekranlar SABİT çizimdir (gerçek
  uygulama değil): kullanıcıyla konuşarak senaryo geliştirmek için; onaylanan ekranlar sonra uygulamaya taşınır.
  Üstte senaryo seçimi (kullanıcı isteği 2026-10-22: ana akış UYGULAMADAN):
  **Senaryo 1 · Uygulamadan** (19 adım, müşteri hep telefon): uygulamayı açar → telefon → SMS kodu → ad soyad + parola →
  Hoş geldiniz → Randevularım'dan "Temsilci iste" → harita → gün/saat → talep tablete düşer → temsilci kabul eder →
  müşteri Randevularım'da "Saati onayla" → isteğe bağlı hazırlık bilgileri → Finansman Aracı tercihi SPY tabletinde
  "ÖN BİLGİ" kartı (2026-10-23; değerler uygulamadaki örnekle aynı: Konut · ~3.500.000 ₺ · %10 · 72 ay · ~43.750 ₺)
  → bir gün önce bilgilendirme formu (ÖNERİ, uygulamada
  yok) → yola çıkar → kapıda QR → yeşil → tablette plan + özet → müşteri özeti inceler (puan isteğe bağlı).
  **Senaryo 2 · Web'den** (12 adım, eski akış; müşteri Telefon/Bilgisayar seçilir, bilgisayarda uygulamasız takip sayfası).
  Adres: `senaryo.html#uyg-adim-5`, `#web-adim-9-bilgisayar` (eski `#adim-N-…` = web). Ekranlar uygulamanın güncel görünümünü
  taklit eder (başlıkta logo yok, Geri; Randevularım · Sohbetler · Finansman · Ayarlar); uygulama değişince senaryo da güncellenmeli.
  Yeni senaryo = `SENARYOLAR` + adım dizisi + ekran işlevleri (TEL / BIL / TAB).
- `video/` — **tanıtım videosu** (2026-10-23 v4, SESLİ; içeride izlenecek PROJE TANITIMI, reklam havası yok; 16:9, ~2 dk 28 sn):
  seslendirme (edge-tts `fr-FR-RemyMultilingualNeural` +4% = kullanıcının seçtiği "Ses 4"; ücretsiz Türkçe Ahmet sesi
  servis tarafında çalışmadı) + kodla üretilen sakin müzik (`muzik_uret.py`) + videoya gömülü açılıp kapanabilen Türkçe
  altyazı izi ve ayrı `.srt`. Ekranda yalnız ANAHTAR KELİMELER. Bölümler: 01 Gözlem (İstanbul haritası → yeşil hizmet
  bölgeleri + ilçe balonları, "pilot" yazılmaz → Ataşehir'e yakınlaşma → işyeri sokağı; tek yönlü temas, kanal yok,
  cumartesi takvimi, dilediği yer/zaman) · "Tasarruf Yanımda ile" sokağı (kapı kapı SPY + hafta içi çağrıya giden yeşil
  Aktif SPY; gün şeridinde Pzt/Sal/Per) · 02 İşleyiş (senaryo ekranları + uygulamanın Finansman ekranları + ön bilgi) ·
  03 Yol haritası (4 aşama + Anadolu yakası komşu ilçeler tek tek hizmete katılır, adları belirir) · 04 Hedeflenen düzen
  (çift yönlü temas; ön bilgi = YAN kazanç; SPY kaynağı önceliklendirilir). Kullanıcı kuralları: satış cümlesi yok,
  "Amacımız" yazılmaz, "SPY'ler", konuşmada "işyeri" değil "müşteri", tekrar yok, hızlı geçiş.
  Üretim: `python video/ses_uret.py` (konuşma metni METIN sözlüğünde; SPY/QR Türkçe okunsun diye OKU dönüşümü) →
  `python video/kaydet.py` (sahne süreleri ses süresinden; SES_PLAN). imageio-ffmpeg, edge-tts, numpy gerekir (conda
  `scrapling`de yok). `video/kareler/`: senaryo görüntüleri, `fin1-3` uygulamanın Finansman ekranları, `harita_z10-16`
  OpenStreetMap gri (merkez 40.9866, 29.1225; köşede atıf zorunlu); ilçe sınırları Nominatim. Linkte `?v=N` sürüm
  parametresi (telefon eski kopyayı gösteriyordu) — videoyu her güncellemede linkler.html'de N'i artır.
  Müşteriye yönelik reklam videosu çerçevenin kapsamı dışında.
- `rapor/benzer-uygulamalar.html` — Türkiye + dünya benzer uygulamalar, yenilik fikirleri, uyarılar (2026-10-21 taslak; kullanıcıyla
  konuşulup ortak rapora dönüşecek). linkler.html'de "Araştırma raporu".
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
- Proje adı Tasarruf Yanımda; amaç 2026-10-22'de değişti (yukarıdaki "Amaç"; eskiden cumartesi yığılmasını yaymak). Müşteriye uygulama indirtilmez, önce **web**.
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

## Müşteri uygulaması yerleşimi ve gezinme (2026-10-22)
- Telefon yerleşimi: animasyonların inline stil adlarına bağlı seçiciler kullanma. `app-stage` → `customer-shell` → `customer-screen` → `customer-panel` yüksekliği taşır; başlık/alt menü küçülmez, orta alan kayar. Görünür yükseklik `--app-height` ile güncellenir. `tests/phone-layout.py` müşteri/personel sekmeleri, kısa ekran ve önizleme çerçevesini kontrol eder.

- İsteğe bağlı hazırlık bilgileri sayfa içi kart değildir: müşteri saati onayladıktan sonra alt pencerede sorulur; daha önce paylaşılmışsa otomatik açılmaz. Şimdi değil randevuyu değiştirmez. `tests/preparation-popup.py` bu akışı kontrol eder.

- Randevularım varsayılan olarak iki sütunlu liste açar. `mSeciliRandevuId` ayrıntıyı seçer; `mOkunanRandevular` id/revizyonla okunmayı tutar. Aktif kayıt eylemleri yalnız aktif ayrıntıda; geçmiş ayrıntı kendi verisini salt okunur gösterir. Finansman yönlendirmesi randevu ayrıntısındadır.
- Masaüstü linkler önizlemesi `iphonePreview=1` ile iframe içinde iPhone 15 sistem alanını canlandırır (59 px üst, 34 px alt); gerçek cihazda `env(safe-area-inset-*)` kullanılır, sahte kamera çizilmez. `tests/appointment-list.py` liste, okunma, gezinme ve güvenli alan regresyonlarını doğrular.

- Saat onayı bekleyen (atandi) randevu kartında başlık/yönerge yazısı yok ("Randevu saatinizi onaylayın" vb. kaldırıldı, 2026-10-22): yalnız tarih, yer,
  temsilci ve "Saati onayla"; üst başlıkta "Temsilciniz atandı". Finansman ön tercihi saat onaylandıktan sonra (netlesti/yolda)
  randevu kartının altında tek satır: "Beklerken finansman ön tercihlerinizi oluşturun." + "Ön tercihler"; ayrı kart yok.
- Randevu ayrıntısında ileri/geri çubuğu veya Tüm randevular metni yoktur. Başlıktaki logo yerine Geri gelir; listeye döner. Temsilci adı aktif randevu kartında tarih/adres altındadır; ayrı temsilci kartı yoktur. Bekleyen randevu okunmuş olsa da ünlem taşır.
- Sohbetler → Konuşmalar → temsilci satırı → konuşma; `mKonusmaAcik` bu ayrımı tutar. Sekmeye basmak konuşma listesini açar; üst Geri aynı listeye döner.

- Müşteri üst başlığı: solda logo yok, sağda fotoğraf/baş harf yok; başlık simetrik hizalanır. Dönüş gereken ekranda sol üstte yalnız Geri metni; ok/chevron yok. İçerikte/kartta ve finansman formunun altında tekrar dönüş düğmesi kullanma; finansman adım dönüşü de üst Geri üzerinden yapılır.

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
