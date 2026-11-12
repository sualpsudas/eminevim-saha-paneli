# Tasarruf Yanımda — ürün ve ekran kuralları

Proje amacı, kararlar ve açık işler `CLAUDE.md`'de. Bu dosya 2026-11-05'te oradan aynen taşındı; ekran ve akış işlerinden önce okunur.

## Ortak dil (kullanıcı kuralı, 2026-11-11 — proje çerçevesi ve videodaki gibi)
- **Müşterinin gördüğü her yerde "temsilci"** (uygulamanın müşteri ekranları, web formu, SMS, müşteri bildirimleri, senaryo ve taslaklardaki
  müşteri ekranları): "Temsilci iste", "Temsilciniz yolda", "Temsilcimiz size gelsin".
- **Personel, yönetici, takip sayfası ve iç belgelerde "SPY"** (Saha Portföy Yöneticisi): "Yeni çağrı", "Sıradaki SPY'ye geçer".
- İkisinde de **"çağrı"** (müşterinin temsilci isteği). Destek / düzeltme / randevu değişikliği **talebi** aynı kalır.
- "Alternatif Satış Kanalı" tam adıyla yazılır (kısaltma yok). Video değişmez (zaten "temsilci" diyor).
- Bu belgede rol adı olarak "SPY" geçer; tırnak içindeki ekran yazıları ekrandaki gibidir.

## Ürün kuralları (2026-10-21, kullanıcıyla konuşarak yazıldı — bundan sonraki işlerin dayanağı)

### 2026-10-22 güncellemesi — randevu odaklı akış

- Web başvurusu ve uygulamadan yeni kayıt aynı randevu modeline bağlanır. Randevum'da saat doğrudan onaylanır; sonuç sohbete düşer.
- Randevu durumları: `alindi → atandi → netlesti → yolda → gorusmede → tamamlandi`; iptal `iptal` olarak saklanır. Yeni randevuda önceki kayıt müşteri geçmişine taşınır. Puan vermek yeni randevu şartı değildir.
- Değişiklik `degisiklik` alanında bekler; eski kesin saat korunur. Personel yeni öneriyi onaylayınca gün/saat/konum güncellenir. Yoldayken de değişiklik/iptal erişimi vardır.
- Personelin Yola çık / gecikme / QR / bitir işlemleri seçili randevuya bağlıdır. Kod randevu, SPY ve revizyonla eşleşir, 10 dakika geçerlidir ve kullanıldığında tüketilir. Gerçek kamera ve sunucuda kimlik doğrulama henüz yoktur; demo tarama düğmesi ve kod girişi korunmuştur.
- Takipte son bilinen SPY ve görüşme noktası, tahmini varış ve eski konum uyarısı görünür. Haritadaki çizgi yol ağına göre hesaplanmış navigasyon rotası değildir. Gerçek GPS/ETA için canlı servis gerekir.
- Personel görüşmeyi bitirince aynı müşteriye özet/not/sonraki adım gider. Puan penceresi kendiliğinden açılmaz. Sorusu olursa müşteri temsilcisine sohbetten yazar (düzeltme/destek bölümü 2026-11-11 kaldırıldı).
- Çalışma durumu ve yaş aralığı **ilk başvuruda zorunlu değildir**. Başvurudan sonra isteğe bağlı, atlanabilir; sonra düzenlenebilir. Kesin yaş/doğum tarihi istenmez. 2026-11-11: bu sorular **yalnız uygulamada** (web sonuç ekranında yok), bkz. Canlı test sürümü → Görüşmeye hazırlık.
- Randevu ve hesaplar bu tarayıcı sekmesinin `sessionStorage` alanında saklanır. Gerçek hesap güvenliği, cihazlar arası eşitleme ve kalıcı sunucu kaydı henüz yoktur.
- Web kaynak formu değişince `python web-basvuru/olustur.py`; native paket için `npm run web:sync`. Yeni `appointment.js`, konum seçimi, rota ve QR kitaplığı native/PWA paketlerine dahil edilmiştir.
- **Tek müşteri girişi (2026-11-11):** “Telefon numaranızla devam edin”. Kayıtlı numara → yalnız mevcut parola;
  “Parolamı unuttum” → SMS kodu → yeni parola. Yeni numara → SMS kodu → ad soyad + parola → KVKK → Hoş geldiniz.
  **Yeni müşteri KVKK onayı olmadan hesabına giremez.** Örnek kayıtlı müşteri Ayşe Kaya (0532 145 67 89); test parolası hazır gelir.
- **Web’den uygulamaya:** temsilci çağrısının SMS önizlemesindeki bağlantı → başvuruya ait 6 haneli kod → parola → aynı çağrı.
  Web formundaki konum onayı yeniden sorulmaz. Test kodları gerçek SMS yerine ekranda gösterilir. Gerçek SMS ayrı iştir.
- **Müşteri hesabı merkezde (2026-11-11, yalnız merkezden açılan sürüm):** telefon, ad soyad, KVKK onay tarihi, web'den geldiyse konum onay
  tarihi. Parola düz metin tutulmaz (merkezde PBKDF2 özeti). Aynı numara + parola **her telefonda** çalışır; kayıtlı numaraya başka
  telefonda da yalnız parola sorulur, çağrıları Randevularım'a gelir. Art arda 5 yanlış parola → 5 dk giriş kapalı ("Parolamı unuttum" açık).
  Web'den gelen müşterinin hesabı parolayı oluşturunca açılır. Test sıfırlaması müşterileri de siler; Ayşe Kaya (parola test123) yeniden kurulur.
  GitHub Pages gösterisi eski davranışla kalır (hesap o tarayıcıda).
- **Müşteri oturumu "Çıkış yap"a kadar açık kalır:** uygulama kapanıp açılınca parola sorulmaz. Telefonda parola değil, merkezin verdiği
  oturum anahtarı saklanır. Çıkış yap ve test verisini sıfırlama oturumu telefonda ve merkezde kapatır.
- **Test sıfırlaması telefonlara da yansır:** uygulama açılınca (o sırada kapalı olsa bile) yerel randevular silinir, müşteri giriş ekranına döner.
  Yeni sürüm yüklenince üstte "Yeni sürüm hazır · Yenile" çıkar; ana ekrandan açılan uygulamada aşağı çekince sayfa yenilenir.
- **Demo modu ve koyu tema yok (2026-11-12):** otomatik kabul/yola çıkış düğmesi kaldırıldı (deneme ekip içinde gerçek akışla);
  uygulama telefon gece modunda da açık renk kalır.
- **Telefonda dokunma hissi ve geçiş (2026-11-12):** düğmeye basınca hafif küçülme (0,15 sn); randevu/konuşma ayrıntısı sağdan,
  Geri ile liste soldan kayar (0,24 sn); sekme değişiminde kayma yok; "hareketi azalt" açıksa kapalı. Temsilci iste penceresi
  telefonda tam ekran (masaüstü telefon çerçevesinin lacivert üst şeridi yok). Kartlarda çok hafif gölge, rakamlar eşit genişlikte.
- **Ekran yazıları sade:** slogan ("Emin olmak, güven demek") ve "nasıl hesaplanıyor / ne işe yarar" türü açıklamalar yok.
- Doğrulama: `npm test`; yerel 8799 sunucusunda `tests/browser-flows.py` ve `tests/web-flows.py` (Playwright + Chrome). Senaryo sayfası bu geliştirmeden sonra ayrıca ele alınacak.

Bu bölüm `CLAUDE.md`'deki eski kararlarla çelişirse **bu bölüm geçerlidir**. Uygulama adım adım, kullanıcıyla konuşarak yapılır;
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
   - Temsilci seçilince ayrı konum açık rızası işaretsiz açılır. Metin amacı kendi içinde söyler (uygulamadaki KVKK ekranında amaçlar cümlenin üstünde yazdığı için "yukarıda belirtilen" web'de kullanılmaz).
     Onaydan sonra harita açılır. Onay vermek istemeyen temsilci seçimini kapatıp normal başvuru yapabilir.
     Merkez web temsilci çağrısında onayı doğrular ve zamanını kaydeder.
   - Seçilen konum hizmet bölgesinin içindeyse ilerlenir.
   - **2026-11-11 (geçerli):** sonuç ekranı başlığı "Sayın Ad Soyad, temsilci çağrınız alındı!" + gün/saat/yer özeti + "… numarasına SMS
     gönderdik" (SMS önizlemesi kendiliğinden açılan, **Kapat'a kadar duran** pencere; "SMS'i göster" yeniden açar) + uygulama kartı
     ("Temsilcinizi ve randevunuzu uygulamadan takip edin, görüşmeye hazırlık bilgilerinizi ekleyin."). Bölge dışı ya da telefonla:
     "Sayın Ad Soyad, çağrınız alındı!" + turuncu not ("Seçtiğiniz konumda henüz temsilci hizmetimiz yok. 444 36 46 numaralı telefonumuzdan
     sizi arayacağız.") + uygulama kartı ("Çağrınızı ve Finansman Aracımızı uygulamadan takip edin."). "Başarılı!", uzun açıklamalar,
     hazırlık bölümü ve "Yeni başvuru" kalktı. Aşağıdaki eski tarif tarihçedir.
   - (eski) Gönderince **yeni ekran: "Başarılı"** — kurumsal ama samimi dil: talebin alındığı, SPY'nin iletişime geçeceği,
     belirlenen saatte belirtilen konumda olacağı. Ardından: "Kampanyalarımıza, Finansman Aracımıza ve size atanan
     SPY hakkında detaylara ulaşmak için Eminevim uygulamasını kullanabilirsiniz." + uygulamaya geçiş.
4. **Web'den uygulamaya geçiş.** Uygulama, formdaki **telefon numarasıyla kayıtlı müşteri** gibi açılır; içinde **henüz
   kayıtlı finansman yoktur**. Bölümler: **Başvuru takibi, Sohbet, Ayarlar, Finansman aracı**.
5. **Hoş geldiniz penceresi.** Uygulamaya yeni gelen herkese (uygulamadan telefonla kayıt olan ya da web formundan gelen):
   küçük, **3 sayfalık**, "Hoş geldiniz" ile başlayan, uygulamayı **çok basit** anlatan pencere.
6. **Giriş ekranındaki "Kayıtlı Müşteri" (demo senaryosu).** Daha önce kayıt olmuş, **finansmanını belirlemiş**, SPY'yle
   **sohbet ederek randevusunu netleştirmiş** ve **SPY'yi beklediğini** bildiğimiz müşteri.
7. **Uygulamadan telefonla kayıt olan yeni müşteri** için de web'deki gibi **"Temsilci iste"** seçeneği olur.

8. **Kullanıcı cevapları (2026-10-21):**
   - Gün ve saat seçimi **kalır**, **haritadan sonra** gelir.
   - **Bölge dışı konum:** "Bu bölgede henüz hizmet yok, sizi telefonla arayalım" denir ve normal (telefonla) başvuruya dönülür.
   - **Web'deki finansman penceresi yedekte:** kod durur, sitedeki Konut/Araç/İşyeri kutularıyla **bağlantısı kesildi**
     (ileride dönülebilir).
   - "Temsilci çağırmak istiyorum" seçimi **onay kutularından sonra** durur.
   - SPY bilgisi **SMS olarak da gider** ve uygulamada da görünür. SPY'ler için **sentetik (yapay) fotoğraflar**
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
  talep Başvurum'da, SPY atanmış (bölgeye göre: Üsküdar→Derya Aksoy, Ümraniye→Berk Cengiz, diğer→Onur Kaya) ve
  Sohbet'te ilk mesajı var. Telefonla başvuruda "Sizi arayacağız" + "Temsilci iste".
- **Müşteri sekmeleri (2026-10-21 gece güncel):** **Randevum** (eski Başvurum; yeşil durum kartında gün/saat/yer, kısa adım
  listesi, SPY tek satır + **"Bilgiler"** tuşu → alt pencerede fotoğraf/şube/sicil, Mesaj gönder; görüşme günü
  "Temsilcinizi takip edin") · Sohbet (başlıkta da "Bilgiler"; SPY ilk mesajda saati önerir, müşteri **"Saati onayla"**
  düğmesiyle onaylar → durum `netlesti`) · Finansman ("+ Yeni", "Değiştir") · Ayarlar. Durumlar: alindi → atandi → netlesti → gorusme.
  Gereksiz/tekrarlı yazılar ayıklandı (Gün/Saat/Yer tablosu, adım alt yazıları, "Örnek görünüm" notu).
- **Randevum ek özellikler (2026-10-21 gece):** "Gün / saati değiştir" (yeni öneri sohbete düşer, SPY onaylayınca netleşir;
  durum `degisti`) ve "İptal et" (onay penceresi); gecikme uyarısı (Ayşe: 10 dk, yeni varış 18:10); takip ekranında
  "Örnek: görüşme bitti" → durum `tamamlandi` → **puan penceresi** (1–5 yıldız) + Randevum'da **Görüşme özeti** (konu, tutar,
  peşinat, vade, aylık ödeme örnek, cayma hakkı 14 gün; "Bilgiler doğru" / "Bir sorun var" → SPY'den bağımsız müşteri
  ilişkileri arar) + "Yeni randevu iste". SPY "Bilgiler" penceresinde puan / deneyim / görüşme sayısı (`TEMSILCI_DETAY`).
  **Finansman kendiliğinden seçilmez (2026-11-12):** tutar, plan, peşinat ve vade boş başlar; kaydedilen finansman ✓ almaz,
  müşteri dokunarak seçer. Yalnız seçili finansman SPY'ye gider; seçili olan düzenlenince SPY varsa sohbete not düşer.
  İlk adım yazısı SPY yoksa söz vermez.
  Bölge dışı telefon talebi (`bolgeDisi`, web'den `&bolgeDisi=1`) → "Başka adres için temsilci iste".
- **Hoş geldiniz:** 3 sayfalık alt pencere, her sayfada basit resim (satır içi SVG) + tek kısa cümle (yeni kayıt ve web'den gelen).
- **Kayıtlı Müşteri (Ayşe Kaya):** KVKK sorulmaz (önceden onaylamış); **görüşme günü** senaryosu — bugün 18:00, SPY
  Onur Kaya yolda (~12 dk), konut finansmanı var, sohbette randevu dünden netleşmiş.
- Uygulama içi "Temsilci iste" (2026-10-21 gece): web penceresiyle aynı akış — 1/2 harita (`konum-sec.html`, iframe;
  seçimi `postMessage {tip:"ty-konum"}` ile yollar; `BOLGELER` form_bolumu.html'den kopya, bölge değişirse ikisini de
  güncelle) → 2/2 gün + saat (10:00–20:00, web'deki gibi) → "Talebiniz alındı" → Başvurumu gör. Bölge dışı → telefonla talep.
  Yalnız talebi olmayan müşteride Başvurum'da görünür. **Finansman sekmesinde SPY bulma/iletişim yok**; eski
  "Temsilci Bul" eşleştirme ekranı (customerNav "tasarruf") kaldırıldı. SPY fotoğrafı yerine baş harfler.
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


## Canlı test sürümü (merkez, 2026-11-10; 7 SPY, atama, Saha Canlı haritası 2026-11-11)
- Uygulama iki biçimde çalışır: **merkezden açılırsa canlı** (`merkez/sunucu.py` sayfaya `window.TY_CANLI` ve `canli.js` ekler; çağrı,
  durum ve mesajlar cihazlar arasında gerçek), **GitHub Pages'te gösteri** (örnek verilerle, sunucusuz). Pages kopyası bozulmamalı.
- **7 SPY** tek dosyada: `spyler.js` (uygulama ve merkez aynı dosyayı okur; değişince merkez yeniden başlatılır): Onur Kaya, Derya Aksoy,
  Berk Cengiz, Selin Arslan, Ece Yalçın, Burcu Avcı, Barış Çelik. Pilot bölge **Üsküdar, Ümraniye, Ataşehir**; her SPY farklı mahallede.
  Fotoğraflar sentetik (`assets/temsilci/OKUBENI.md`). s1-s4 video ve senaryodaki kişilerdir. Randevu H/G ve ciro H/G (son 3 ay) **uydurmadır**.
- **"Aktif değil" diye bir şey yok** (kullanıcı, 2026-11-11): uygulamada yalnız iki H/G'si de ≥ %100 olan SPY'ler bulunur. "Molada" ayrı
  bir durumdur (SPY kendisi seçer).
- **Giriş:** Müşteri tek telefon numarası ekranından devam eder. **Personel Girişi** yalnız iki seçenek: **SPY** (açılır listeden kişi, fotoğraflı
  önizleme + "Giriş yap") ve **Yönetici** (tek düğme; her yönetici hepsini görür). Cihaz SPY'nin son girişini hatırlar.
- **Atama** (ayrıntı `rapor/tasarruf-yanimda-proje-calismasi/10-atama-ve-rota.md`). Günlük sınır 4 çağrı.
  - **Hemen çağrı** (bugün, saati en geç 2 saat sonra): molada, yolda/görüşmede ve
    günlük sınırı dolan elenir. Puan: **yakınlık 50** (o anki yer: bugünkü son randevusu, yoksa kendi mahallesi), **H/G 30** (randevu 15 +
    ciro 15), **bugünkü çağrı 20** (az olan önde).
  - **İleri saat/gün:** o saatin ±90 dk'sında randevusu olan ve o gün sınırı dolan elenir. Puan: **H/G 50** (randevu 25 + ciro 25),
    **yakınlık 30** (kendi bölgesine ya da o günkü randevularına), **o günkü çağrı 20**.
  - Çağrı en yüksek puanlıya **teklif** edilir; **2 dakikada** kabul edilmezse ya da SPY **Devret** derse sıradakine. Deneme sınırı yok;
    uygun SPY kalmazsa çağrı **"kimse almadı"** olur ve Saha Canlı haritasında **kırmızı** görünür; uygun SPY çıkınca (moladan döndü,
    görüşmesi bitti) kendiliğinden ona teklif edilir. **Yöneticiye düşme, Ata ve Aktar yok.** Süresi dolmuş çağrıyı eski SPY kabul edemez.
- **SPY ekranı:** yeni çağrıda ses + titreşim + "Yeni çağrı: Ad"; ayrıntıda **kabul için kalan süre** (geri sayım; "Neden size geldi" satırı
  2026-11-11'de kaldırıldı) ve müşterinin görüşmeye hazırlık bilgileri (ne için, çalışma durumu, yaş aralığı, not).
  Performans: son 3 ay randevu ve ciro H/G çubukları, ekipteki sıra (x/7), bugünkü çağrı (en fazla 4). ("Çağrı size nasıl gelir?" kartı 2026-11-12 kaldırıldı.)
- **Yönetici ekranı:** Saha Canlı ve Performans. **Destek bölümü yok** (yönetici, müşteri ve testlerden kaldırıldı, 2026-11-11).
  - **Saha Canlı** = merkezin takip sayfası (uygulamada ve bilgisayarda aynı düzen; Pages gösterisinde örnek veriyle). Yalnız **bugün**
    (tarih seçimi yok): **Gelen Çağrı** ve **Görüşme Sayısı** (kapıda doğrulanan). Süzgeç: **Tümü / Boşta / Randevuda / Molada**.
    Harita: pilot ilçe sınırları (kalın yeşil) + mahalle sınırları ve adları (yakınlaşınca); altlık OpenStreetMap, soluk.
    SPY'ler **küçük simge, fotoğraf yok**: yeşil boşta, turuncu randevuda (yolda + görüşmede), gri molada; dokununca kısa bilgi.
    Kimsenin almadığı çağrılar **kırmızı nokta**. Haritanın altında kısa SPY listesi (dokununca haritada gösterir). Eski çağrı kartları,
    olaylar ve uzun liste kalktı. Sınırlar `assets/pilot-sinirlar.js` (OpenStreetMap, sadeleştirilmiş).
  - **Performans:** kompakt liste — sıra, ad, ort. randevu H/G, ort. ciro H/G; iki oranın ortalamasına göre yukarıdan aşağı; altta ekip ortalaması.
- **Bildirim (2026-11-11):** uygulamanın açık olması gerekmez. Yeni çağrı, o SPY'yi seçmiş **tüm telefonlara** bildirim olarak gider
  ("Yeni çağrı: Ad" · yer · saat · "2 dk içinde kabul edin"). Bir telefon tek SPY'ye bağlıdır: başka SPY seçilince bağ ona geçer,
  Çıkış yapınca kalkar; aynı SPY birden çok telefonda seçilebilir. İzin girişte (dokununca) sorulur; Profil'de **Bildirimler** kartı
  durumu gösterir, kapalıysa "Bildirimleri aç". **iPhone'da** Safari → Paylaş → **Ana Ekrana Ekle** ile açılan sayfada çalışır (iOS 16.4+).
  TestFlight uygulamasında kapalıyken bildirim için Apple bildirim anahtarı (APNs) gerekir (sonraki adım). Takip sayfasında SPY'ye
  dokununca bildirimi açık telefon sayısı görünür. Müşteri, SPY kabul edene kadar kimin geleceğini görmez.
- **Müşteri bildirimi (2026-11-11, merkez sürümü):** girişten sonra Randevularım'da "Bildirimleri açın" kartı (Şimdi değil ile kapanır);
  Ayarlar'da **Bildirimler** kartı. Giden haberler: "Temsilciniz belli oldu: Ad · saat", "Temsilciniz yola çıktı · tahmini varış SS:DD",
  temsilcinin yazdığı mesaj. Dokununca o randevu açılır (giriş gerekiyorsa girişten sonra). Çıkış yapınca bildirim kalkar.
  Yalnız web formunu kullanıp uygulamaya hiç girmeyen müşteriye bildirim gitmez (SMS işi ayrı). iPhone'da Ana Ekrana Ekle gerekir.
- **Web formu** merkezden açılırsa (`<merkez>/web-basvuru/index.html`) "Temsilci çağırmak istiyorum" çağrısı merkeze gider; SMS önizlemesindeki
  6 haneli giriş kodunu merkez verir. Uygulamada telefon + bu kodla girince aynı çağrı açılır (merkezde `api/kod`). Pages kopyasında eski
  gösteri davranışı (kod tarayıcıda üretilir).
- **Görüşmeye hazırlık yalnız uygulamada** (web'de yok): çalışma durumu, yaş aralığı, "Ne için düşünüyorsunuz?" (Konut / Araç / İşyeri /
  Henüz karar vermedim), kısa not (en çok 300 harf). Web'den gelen müşteri uygulamaya ilk girdiğinde (tanıtım penceresi kapanınca) ve saat
  onaylanınca sorulur; "Şimdi değil" → Randevum ayrıntısında "Görüşmeye hazırlık · isteğe bağlı" kartı kalır. Telefonla görüşme çağrısında sorulmaz.
- Canlıda uydurma otomatik yanıtlar kapalıdır. SMS kodu test sürümünde ekranda gösterilir.
- Merkezde atama puanı `atamaPuan` alanındadır (müşteri yıldız puanı `puan` ile karışmasın).
- **Aynı gün çağrısı:** takvim bugünü de gösterir (saat 19'a kadar); bugün için geçmiş ve bir saat içindeki saatler seçilemez.


## Personel ve Senaryo ekranları
- **Personel (2026-10-22): tablet düzeni.** (2026-11-11: girişte yalnız SPY ve Yönetici, bkz. Canlı test sürümü.) Personel girişi `isPersonel` → yeni `.tp` düzeni:
  üstte yeşil bant (logo; sağda kişi: ad, rol · durum, fotoğraf ya da baş harf → Profil), **sekmeler her cihazda ALTTA,
  müşteri uygulamasındaki gibi** (kullanıcı isteği): Görüşmeler / Performans / Saha Canlı / Profil (SPY'da Saha Canlı yok,
  SGL ve Alternatif Satış Kanalı Müdürü ekranında Görüşmeler yok). Profil: Müsait/Molada (görüşmede iken otomatik "Görüşmede"), Çıkış yap. Senaryo'daki tablet de aynı. Önizleme (linkler.html) uygulamadan
  `postMessage {tip:"ty-cihaz", cihaz:"tablet"}` alınca çerçeveyi yatay tablete (1180×820) çevirir, çıkışta telefona döner.
  Dar ekranda (<900 px) tek sütun; seçilen görüşmenin ayrıntısı listenin üstünde açılır.
  - **Görünüm ayrıntıları (2026-11-12, kozmetik):** seçili süzgeç / Müsait-Molada / Saha Canlı süzgeci aynı: açık yeşil dolgu +
    yeşil çerçeve (Müsaitlik'te ✓), telefonda 44 px. Alt menü etiketi #767676 12 px, seçili sekmede üstte 2 px yeşil çizgi.
    Sayaçlar (Görüşmeler, Saha Canlı, Performans sıra/çağrı) koyu nötr; yeşil yalnız durum ve H/G için. SPY Performans'ta
    H/G yüzdesi büyük (28/24 px), çubukta %100 hedef çizgisi (ölçek %150). Yönetici tablosunda %100 üstü yeşil, tam %100 koyu nötr.
    Sekme başlığı dar tek satır, alt yazı yok ("Tüm SPY'ler · pilot bölge", bölge, tarih kalktı; kullanıcı 2026-11-12).
    Saha Canlı mesai dışında başlığın yanında açık kehribar "Örnek: 11 Kasım 15:30" etiketi; uygulama içinde harita kısa (kişi kartları ilk ekranda). Çıkış yap gri çerçeveli.
  - **Görüşmeler** (SPY ve TL; takım liderleri de görüşme yapar): tarih sırası, gruplar Yeni talepler · Bugün · Yarın ·
    Sonraki günler · Geçmiş; durumlar **Bekleyen** (yeni talep / yoldasınız alt hâlleri) → **Şu an görüşülüyor** (QR ile
    doğrulanınca, görüşme bitene kadar) → **Gerçekleşti**; süzgeç Tümü/Bekleyen/Şu an/Gerçekleşti. Sağda ayrıntı ve
    eylemler: Kabul et / Devret · Yola çık · Vardım: QR okut · Görüşmeyi bitir · özeti gönder. Veri `tpTohum` (demo) +
    uygulamadan gelen talepler `tpEkGorusmeler`. Ayşe K. satırı müşteri uygulamasıyla bağlı (`demoDogrulama`,
    `gorusmeBittiDemo`, `demoPuan`).
  - **Bugünkü rota**: `rota.html?b=şube&n=lat,lng,etiket,durum|…` (Leaflet; numaralı iğneler, saat sırası). Ayrı Harita sekmesi yok.
  - **Saha Canlı** (TL/SGL/Alternatif Satış Kanalı Müdürü): 3 sayı (Şu an görüşmede · Yolda · Bugün gerçekleşen) + personel listesi (durum, şube,
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
  Hoş geldiniz → Randevularım'dan "Temsilci iste" → harita → gün/saat → talep tablete düşer → SPY kabul eder →
  müşteri Randevularım'da "Saati onayla" → isteğe bağlı hazırlık bilgileri → Finansman Aracı tercihi SPY tabletinde
  "ÖN BİLGİ" kartı (2026-10-23; değerler uygulamadaki örnekle aynı: Konut · ~3.500.000 ₺ · %10 · 72 ay · ~43.750 ₺)
  → bir gün önce bilgilendirme formu (ÖNERİ, uygulamada
  yok) → yola çıkar → kapıda QR → yeşil → tablette plan + özet → müşteri özeti inceler (puan isteğe bağlı).
  **Senaryo 2 · Web'den** (12 adım, eski akış; müşteri Telefon/Bilgisayar seçilir, bilgisayarda uygulamasız takip sayfası).
  Adres: `senaryo.html#uyg-adim-5`, `#web-adim-9-bilgisayar` (eski `#adim-N-…` = web). Ekranlar uygulamanın güncel görünümünü
  taklit eder (başlıkta logo yok, Geri; Randevularım · Sohbetler · Finansman · Ayarlar); uygulama değişince senaryo da güncellenmeli.
  Yeni senaryo = `SENARYOLAR` + adım dizisi + ekran işlevleri (TEL / BIL / TAB).

## Müşteri uygulaması yerleşimi ve gezinme (2026-10-22)
- Telefon yerleşimi: animasyonların inline stil adlarına bağlı seçiciler kullanma. `app-stage` → `customer-shell` → `customer-screen` → `customer-panel` yüksekliği taşır; başlık/alt menü küçülmez, orta alan kayar. Görünür yükseklik `--app-height` ile güncellenir. `tests/phone-layout.py` müşteri/personel sekmeleri, kısa ekran ve önizleme çerçevesini kontrol eder.

- İsteğe bağlı hazırlık bilgileri sayfa içi kart değildir: müşteri saati onayladıktan sonra alt pencerede sorulur; daha önce paylaşılmışsa otomatik açılmaz. Şimdi değil randevuyu değiştirmez. `tests/preparation-popup.py` bu akışı kontrol eder.

- Randevularım varsayılan olarak iki sütunlu liste açar. `mSeciliRandevuId` ayrıntıyı seçer; `mOkunanRandevular` id/revizyonla okunmayı tutar. Aktif kayıt eylemleri yalnız aktif ayrıntıda; geçmiş ayrıntı kendi verisini salt okunur gösterir. Finansman yönlendirmesi randevu ayrıntısındadır.
- Masaüstü linkler önizlemesi `iphonePreview=1` ile iframe içinde iPhone 15 sistem alanını canlandırır (59 px üst, 34 px alt); gerçek cihazda `env(safe-area-inset-*)` kullanılır, sahte kamera çizilmez. `tests/appointment-list.py` liste, okunma, gezinme ve güvenli alan regresyonlarını doğrular.

- Saat onayı bekleyen (atandi) randevu kartında başlık/yönerge yazısı yok ("Randevu saatinizi onaylayın" vb. kaldırıldı, 2026-10-22): yalnız tarih, yer,
  SPY ve "Saati onayla"; üst başlıkta "SPY'niz atandı". Finansman ön tercihi saat onaylandıktan sonra (netlesti/yolda)
  randevu kartının altında tek satır: "Beklerken finansman ön tercihlerinizi oluşturun." + "Ön tercihler"; ayrı kart yok.
- Randevu ayrıntısında ileri/geri çubuğu veya Tüm randevular metni yoktur. Başlıktaki logo yerine Geri gelir; listeye döner. SPY adı aktif randevu kartında tarih/adres altındadır; ayrı SPY kartı yoktur. Bekleyen randevu okunmuş olsa da ünlem taşır.
- Sohbetler → Konuşmalar → SPY satırı → konuşma; `mKonusmaAcik` bu ayrımı tutar. Sekmeye basmak konuşma listesini açar; üst Geri aynı listeye döner.

- Müşteri üst başlığı: solda logo yok, sağda fotoğraf/baş harf yok; başlık simetrik hizalanır. Dönüş gereken ekranda sol üstte yalnız Geri metni; ok/chevron yok. İçerikte/kartta ve finansman formunun altında tekrar dönüş düğmesi kullanma; finansman adım dönüşü de üst Geri üzerinden yapılır.

## Müşteri ekranı ilkeleri
- Olabildiğince basit; gereksiz yazı yok, her ekranda tek soru grubu ve tek ana buton.
- İlk temasta üyelik, şifre, konum izni, sohbet yok. Alanlar: ad, soyad, telefon; SPY istenirse gün, saat, haritadan yer (İş yeri/Ev). E-posta yok.
- **Ödeme / ücret güvencesi cümleleri ASLA kullanılmaz** ("Görüşmede ödeme alınmaz", "hiçbir ödeme alınmaz", "Ücretsiz" vb.;
  kullanıcı kuralı 2026-10-21). Dil kurumsal ama samimi: "SPY'miz görüşmeden önce sizinle iletişime geçecek", "Sicil numarası aynıdır".
  "Takip" müşteriyi değil SPY'yi anlatır ("SPY'nizin nerede olduğunu görürsünüz").
- Cumartesi engellenmez; hafta içi günler önce gelir, cumartesi "yoğun" etiketiyle durur.
- SPY bilgileri ve takip linki telefona **mesajla** gider (e-posta istenmez; 2026-10-21 kararıyla değişti).
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
