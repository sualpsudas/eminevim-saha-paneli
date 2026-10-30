# Eminevim Saha Paneli - Proje İlerleme Kaydı

Bu dosya, uygulamadaki önemli geliştirmelerin kısa kaydını tutar. Yeni bir çalışma tamamlandığında tarih, kapsam ve doğrulama bilgisi eklenmelidir.

## Aktif çalışma bilgisi

- Aktif klasör: `C:\Users\SUALP\Desktop\eminevim saas geliştirme`
- Git dalı: `master`
- Uzak depo: `sualpsudas/eminevim-saha-paneli`
- Son senkron commit: `d5f7890` - `feat: unify Tasarruf Yanımda panel flows`

## Tamamlananlar

### Müşteri odaklı giriş ve ana navigasyon

- Giriş ekranı müşteri odaklı hale getirildi; `Personel Girişi` sağ üstte ayrı aksiyon olarak konumlandı.
- Giriş altında `Kayıt Ol` eklendi. Kayıt akışı ad, e-posta ve şifre belirleme adımlarını içeriyor.
- Giriş sonrası müşteri navigasyonu `Profil`, `Tasarruf Yanımda`, `Görüşmeler`, `Ayarlar` sekmelerine ayrıldı.
- Tasarruf Yanımda sekmesi mevcut konum seçimi, en yakın SPY atama ve sohbet akışını kullanmaya devam ediyor.

### Tasarruf Yanımda müşteri akışı

- Sekmesiz, doğrusal müşteri akışı eklendi: kayıt formu, temsilci arama, atama, sohbet, konum paylaşımı ve yönlendirme.
- Ad, telefon, e-posta ve adres alanlarından oluşan form eklendi.
- GPS ile adres doldurma ve yalnızca geliştirme için `TEST_MODE_SKIP_FORM` test geçişi eklendi.
- Sohbette otomatik SPY karşılama mesajı ile konum gönderme / haritadan nokta belirtme seçenekleri eklendi.
- Müşteri sohbeti kapatıp durum özetine dönebilir ve `Sohbete Dön` ile geçmişi koruyarak tekrar açabilir.
- `Ana Uygulamaya Geç` için sonraki gerçek entegrasyona hazırlanmış yer tutucu eklendi.

### SPY atama ve saha akışı

- `assignment.js` oluşturuldu: Haversine mesafe, uygun SPY seçimi, ret ve süre dolumu ile sıradaki SPY'ye aktarım.
- SPY bildirimi için kabul/ret akışı eklendi.
- Konum bekleme, konum alındı, yolda ve görüşmede durumları eklendi.
- SPY'nin yönlendirme başlatması, müşteriye ulaştığını işaretlemesi ve randevu oluşturması eklendi.
- SPY paneline oluşturulan randevuların listesi eklendi.

### Harita, Admin ve kalite

- Harita gerçek `lat/lng` verisini, rota çizimini, tıklanabilir konum seçimini ve kümelenmeyi destekliyor.
- Mesafe ve ETA Haversine hesabı üzerinden güncelleniyor; gerçek GPS/API bağlantısı için istemci katmanı hazır.
- Admin tarafına Bildirim Gönderildi, Sohbette, Konum Alındı, Yolda ve Görüşmede durumları; randevu filtresi ve aktif talep/randevu özeti eklendi.
- Pull-to-refresh, yükleme/boş durumlar, detay ekranı, devret bottom-sheet'i, tema geçişi ve erişilebilirlik iyileştirmeleri eklendi.

## Açık / sonraki işler

- Gerçek backend, kimlik doğrulama ve kalıcı veri deposu.
- WebSocket veya gerçek polling endpoint'i ile canlı SPY konumu ve mesajlaşma.
- Apple/Google Haritalar yönlendirme entegrasyonu.
- Randevu verilerinin kalıcı olarak saklanması ve gerçek takvim görünümü.
- Gerçek cihazlarda GPS, izin, erişilebilirlik ve mobil performans testleri.

## Güncelleme notu şablonu

```md
### YYYY-AA-GG - Kısa başlık

- Yapılan değişiklik
- Doğrulama / test sonucu
- Varsa takip edilecek iş
```

### 2026-09-14 - Ev Almak kaldırıldı, hikâye güçlendirildi

- "Ev Almak" sekmesi ve fiyat tabanlı bölge/semt mantığı tamamen kaldırıldı; müşteri akışı eski "Temsilci Bul → SPY" modeline döndü (4 sekme).
- Üst banner tek satır ince tasarım; alt nav hover/seçili-şerit efektleri kaldırıldı.
- Bekleme ekranlarına 5 adımlı akış göstergesi (Aranıyor → Bulundu → Bağlandı → Yolda → Ulaştı).
- Temsilci güven kartı (şube, puan, deneyim, görüşme sayısı, "Eminevim onaylı") bekleme + özet ekranında.
- Görüşme konusu çipleri (Bilgi almak / Sözleşme / Ödeme / Diğer) → SPY bildirimi ve ilk sohbet mesajına yansır.
- SPY "Görüşmeyi Tamamla" → müşteride 5 yıldız + not değerlendirme ekranı; Görüşmeler geçmişine ve SPY puanına işlenir.
- Admin özet: Ort. kabul süresi, ort. varış süresi, tamamlanma oranı, SPY puanı KPI kartları (gerçek ölçümler, veri yoksa hedef değer).
- Doğrulama: tarayıcıda uçtan uca akış (konu seç → çağır → konum → geliyorum → ulaştım → tamamla → puanla → admin KPI) hatasız.

### 2026-09-14 - İkinci tur: sohbet, randevu, müsaitlik, kapanış, kozmetik

- Sohbet: mesajlarda saat + gönderildi tiki, demo modda "temsilci yazıyor…" göstergesi ve otomatik kısa yanıt.
- Görüşmeler: temsilci avatarı, saat, durum rozeti (Onay bekliyor / Onaylandı / Tamamlandı), "Tekrar çağır" (aynı temsilci tercih edilir), boş durum ekranı, yenilemede iskelet yükleme.
- "Şimdi değil, randevu al": tarih + saat dilimi seçimli alt sayfa → SPY randevu listesine düşer, demo modda 3 sn'de onaylanır.
- SPY profil: Müsaitim / Molada / Görüşmede anahtarı; müsait değilken talepler sıradaki temsilciye gider.
- SPY "Görüşmeyi Tamamla" → kapanış notu (Sözleşme imzalandı / Takip gerekli / İlgilenmedi) → geçmiş kartında rozet.
- Koyu tema: sabit açık renkli arka planlar token'a (--tintGreen/--tintRed/--tintGold) çevrildi.
- Profil: avatara dokununca fotoğraf yükleme (header'da da görünür). Temsilci kabul edince kısa titreşim.

### 2026-09-14 - Harita yenilemesi (SPY + Admin + müşteri)

- Tile: CARTO (API anahtarı istiyor, filigran basıyordu) → OpenStreetMap standart; açık temada doygunluk düşürüldü, koyu temada tile'lar ters çevrilerek koyu harita.
- İşaretçi türleri: SPY = baş harfli renkli avatar + durum noktası; müşteri = pin; "Siz" = yeşil nokta + 4 km hizmet alanı halkası. Nabız yalnız aktif/hareket edenlerde.
- Kalıcı etiket yerine dokununca popup (şube, durum, puan/görüşme, mesafe, kritik süre); popup içerik yerinde güncellenir, her saniye kapanmaz.
- Rota: kat edilen kısım düz, kalan kısım noktalı; hareket eden avatarda ETA rozeti.
- Kontroller sağ altta büyük; "⤢ hepsini göster" butonu; harita içi lejant; admin'de SPY/Müşteri filtreleri sayaçlı çip.
- Müşteri sohbet minik haritası compact modda (kontrol/lejant yok). Iframe src'lerine ?v= önbellek kırıcı, SW cache v4.

### 2026-09-15 - Başvuru sihirbazı, giriş/KVKK, Eminevim marka dili

- Sekmeler: Profil · Başvuru · İletişim · Ayarlar (Görüşmeler kaldırıldı, geçmiş Profil'e taşındı). İletişim ekranındaki tanıtım kartları kaldırıldı.
- Giriş: Kayıtlı Müşteri / Yeni Müşteri seçimi; yeni müşteri kayıt formu (dolu demo veri, telefon alanı) → boş geçmişle başlar; hesap verisi e-postaya göre oturumda saklanır.
- KVKK: giriş/kayıt sonrası tek kutucuklu standart açık rıza ekranı ("Onaylıyorum"); Ayarlar'da sade "Çıkış yap".
- Başvuru (danışmanlık ön bilgisi) 3 adımlı sihirbaz: Ne için? (Konut/Taşıt/İşyeri, Eminevim ikonları) → Plan (Bireysel/Çekilişli) → Bütçe ve aylık ödeme (tutar, peşinat çipleri, 1'er ay vade kaydırıcısı; canlı "Aylık ödemeniz" kartı). Geri/Devam sabit alt çubukta.
- Başvurularım listesi: seçili kartta "Başvuruyu değiştir" / "Temsilciyle iletişime geç", "+ Yeni başvuru". Onay/durum süreci yok.
- Hesap: senaryoHesapla (Eminevim site örnekleri + BDDK kuralları, kaba). Reklam dili: "Ayda X ₺ taksitle bütçenizi zorlamadan ev/araba/iş yeri sahibi olun."
- Sohbet: harita 260px, yeni mesajda otomatik en alta kaydırma; temsilci kartından "Eminevim onaylı" rozeti kaldırıldı.
- Tüm sekmelerde içerik banner–nav arasında (masaüstü alt boşluk, mobil sıfırlama); ikonlar CSS mask ile (şablon 404'leri giderildi).

### 2026-10-01 - Hiyerarşik performans panelleri ve iPhone PWA testi

- `org-data.js` içinde seed'li organizasyon ve metrik veri katmanı eklendi: 4 saha, 22 bölge, 220 şube, 45 takım lideri ve 250 personel. Onur K., Derya A. ve Berk C. canlı SPY kayıtlarıyla aynı kimlikleri kullanıyor.
- TL, SGL ve ASK Müdürü için ortak Performans · Ekibim · Saha Canlı · Genel paneli; H/G, ciro, R/K/K, dönüşüm hunisi, mini trend, sıralama, dikkat filtresi, breadcrumb drill-down ve yetki kapsamı eklendi.
- SPY Profil ekranına Gün/Hafta/Ay/Yıl dönemli Performansım kartları, takım sırası ve takım ortalaması farkı eklendi.
- Personel Girişi rol seçimi ve `?rol=tl|sgl|ask|spy` doğrudan demo girişleri eklendi. Yönetici Ayarlar menüsüne tema ve çıkış eklendi.
- PWA cache `eminevim-v5` oldu ve `org-data.js` offline kabuğa eklendi. Manifest standalone, Apple meta etiketleri ve 180 px touch icon doğrulandı.
- `tests/org-data.test.js` ile hiyerarşi sayıları, referanslar, üst-alt toplamlar ve H/G'nin toplamlardan yeniden hesaplanması doğrulandı.
- 390×844 tarayıcı testinde TL/SGL/ASK/SPY rolleri, dört dönem, ekip drill-down, canlı/genel sekmeleri, koyu tema ve çıkış doğrulandı. Müşteri → temsilci → konum → yolda → ulaştı → tamamla → 5 yıldız → Admin özeti regresyon akışı hatasız geçti; tarayıcı konsolunda hata yoktu.
- QR kod `https://sualpsudas.github.io/eminevim-saha-paneli/` adresine çözümleniyor.
- Native Capacitor/Codemagic hazırlığı (Adım 7b), talimat gereği kullanıcı onayı alınana kadar başlatılmadı.

#### iPhone'a kurulum

1. iPhone'da Safari ile `https://sualpsudas.github.io/eminevim-saha-paneli/` adresini açın.
2. Safari araç çubuğundaki **Paylaş** düğmesine dokunun.
3. **Ana Ekrana Ekle** seçeneğini seçip **Ekle** ile onaylayın.
4. Ana ekrandaki **Tasarruf Yanımda** simgesinden uygulamayı standalone olarak açın.
5. Rol testi için adrese `?rol=tl`, `?rol=sgl`, `?rol=ask` veya `?rol=spy` ekleyin.

### 2026-10-02 - Performans raporları haftalık düzene sadeleştirildi

- Personel, TL, SGL ve ASK Müdürü performans raporları yalnızca haftalık gösterime geçirildi; Gün/Hafta/Ay/Yıl anahtarı kaldırıldı.
- Üstte H/G yüzdesi ve yatay gerçekleşme barı, devamında Günlük Ciro ve Haftalık Ciro satırları eklendi.
- Haftalık Randevu Sayısı ve Açılan Kart değerleri yan yana büyük kartlara taşındı.
- SPY Performans görünümü Profil içinden çıkarılarak bağımsız alt navigasyon sekmesi yapıldı.
- 390×844 mobil görünümde SPY/TL/SGL/ASK rolleri doğrulandı; dönem düğmelerinin kaldırıldığı ve tarayıcı konsolunda hata olmadığı kontrol edildi.

### 2026-10-02 - Premium dashboard ve kompakt hiyerarşi seçimi

- Yönetici ve personel performans ekranları; katmanlı kartlar, daha güçlü tipografi, ikon blokları, durum renkleri ve özet rozetleriyle premium dashboard görsel diline geçirildi.
- TL, SGL ve ASK Müdürü performans ekranlarına kompakt “Görüntülenen Kapsam” seçicisi eklendi. Üst roller yalnızca kendi yetki ağacındaki alt saha, takım ve personeli seçerek inceleyebiliyor.
- Seçilen kapsamın adı, rolü, H/G yüzdesi ve haftalık cirosu seçim listesinde birlikte gösteriliyor; seçim sonrasında breadcrumb ve üst seviyeye dönüş korunuyor.
- 390×844 mobil görünümde ASK → saha → takım ve TL → personel seçimleri ile ayrı SPY Performans sekmesi görsel olarak doğrulandı.
- Ana uygulama betiğinin sözdizimi ve `tests/org-data.test.js` organizasyon/veri bütünlüğü testleri başarıyla tamamlandı.

### 2026-10-02 - Rapor dönemleri tarih olarak gösterildi

- Performans ekranlarındaki “Bugün”, “Bu hafta”, “Günlük” ve “Haftalık” dönem metinleri dinamik tarih etiketleriyle değiştirildi.
- Günlük ciro gün/ay/yıl, haftalık metrikler ise Pazartesi–Pazar tarih aralığını gösteriyor; tarihler cihaz saatine göre otomatik yenileniyor.
- Personel, TL, SGL ve ASK Müdürü performans görünümleri aynı tarih biçimini kullanıyor.

### 2026-10-02 - Aylık performans ve SPY karşılaştırması

- Personel, TL, SGL ve ASK Müdürü performans hesapları haftalık dönemden aylık döneme geçirildi; başlıklar ve tarih rozetleri içinde bulunulan ayı gösteriyor.
- Yalnızca SPY Performans ekranına “Performans / Karşılaştırma” alt sekmeleri eklendi.
- Karşılaştırma görünümünde SPY’nin 250 personel içindeki genel sırası, kişisel ve şirket H/G değerleri, şirket ortalaması farkı ile tüm personelin H/G sıralı kompakt listesi gösteriliyor.
- Listede şube, ciro, randevu ve açılan kart değerleri yer alıyor; oturumdaki SPY “SİZ” etiketiyle vurgulanıyor.
- 390×844 mobil görünümde SPY karşılaştırması ve ASK aylık performans ekranı doğrulandı.

### 2026-10-02 - SPY aylık H/G özeti sadeleştirildi

- SPY Performans özetinin ilk kartı, gün gün biriken ciro ve hedeflerden hesaplanan aylık H/G barı olarak netleştirildi.
- Ciro alanı yalnızca tek kartta gösteriliyor; başlığı “1 Ekim Perşembe” biçiminde tarih ve gün adını içeriyor. Ayrı aylık ciro kartı kaldırıldı.
- Ciro kartının altına personelin H/G bazlı Bölge, Saha ve Genel sıralamasını gösteren üç kompakt kart eklendi.
- Aylık randevu ve açılan kart sayıları yan yana büyük kartlar olarak korundu.
- `tests/org-data.test.js` içine aylık personel cirosunun günlük kayıtların toplamı olduğunu ve H/G'nin bu birikimden hesaplandığını doğrulayan kontroller eklendi.
- 390×844 mobil görünümde yeni kart sıralaması, tarih biçimi ve hesaplanan sıralamalar doğrulandı.

### 2026-10-02 - Saha ve takım hiyerarşisi yeniden düzenlendi

- Dört saha `Orta`, `Batı`, `Doğu` ve `İstanbul` olarak yeniden adlandırıldı.
- Takımlar her saha içinde bağımsız olarak `1. Takım`dan başlayacak şekilde numaralandırıldı; takım lideri adı ayrı veri olarak korundu.
- Müdür ekranında şirket toplamı ve Sahalar/Takımlar/Personeller seçilebilir karşılaştırmaları; Saha ekranında saha toplamı, kendi takımları ve tüm sahalar karşılaştırması; Takım ekranında takım toplamı, kendi personelleri ve tüm takımlar karşılaştırması eklendi.
- Takım karşılaştırmalarında bağlı saha adı ayrı sütun bilgisi olarak gösteriliyor. Yetki dışındaki kardeş birimler karşılaştırmada okunabiliyor ancak detayına girilemiyor.
- Personel profilinde bağlı takım ve saha bilgisi dinamik olarak gösteriliyor; personel karşılaştırma satırlarına da saha ve takım eklendi.
- Saha toplamlarının takım toplamlarıyla, takım toplamlarının personel toplamlarıyla eşleştiği otomatik testlerle doğrulandı.
- PWA önbelleği `eminevim-v6` sürümüne yükseltildi ve yeni organizasyon verisi için önbellek kırıcı eklendi.
- 390×844 mobil testte Müdür, Saha, Takım karşılaştırmaları ve SPY profil hiyerarşisi doğrulandı.

### 2026-10-02 - Takım karşılaştırma hizaları düzeltildi

- Uzun takım/personel listelerinde dikey flex alanının üst filtreleri ve seçim kapsüllerini küçültmesi engellendi.
- Karşılaştırma başlığı, dönem etiketi, sıralama filtreleri ve tablo başlığı tam yükseklikte ve hizalı kalıyor.
- Liste kendi içerik alanında dikey kaydırılırken üst başlık ve alt navigasyon düzeni korunuyor.
- 390×844 görünümde “Tüm Takımlar” karşılaştırması; uzun liste, sütunlar, H/G barları ve saha bilgileriyle görsel olarak doğrulandı.

### 2026-10-05 - Karşılaştırma Performans görünümüne taşındı

- Yönetici karşılaştırması ayrı alt navigasyon sekmesinden kaldırılarak Performans içindeki `Özet / Karşılaştırma` seçimine taşındı.
- Ayrı H/G, Ciro, Randevu ve Kart filtreleri kaldırıldı; tüm değerler tek bir kompakt tabloda ayrı sütunlar halinde birleştirildi.
- Müdür, saha lideri ve takım lideri kapsam seçimleri korunurken satır yükseklikleri ve yazı boyutları mobil ekrana uygun biçimde küçültüldü.
- SPY’nin tüm personel karşılaştırması da `H/G · Ciro · Randevu · Kart` sütunlarını aynı tabloda gösterecek şekilde sadeleştirildi.
- 390×844 mobil görünümde takım lideri, müdür ve SPY tabloları doğrulandı; sütun taşması veya tarayıcı konsolu hatası görülmedi.

### 2026-10-05 - Native iOS ve TestFlight hazırlığı

- Capacitor 8.5.2 ile native iOS projesi oluşturuldu; uygulama adı `Tasarruf Yanımda`, geçici bundle kimliği `com.sualpsudas.tasarrufyanimda` olarak ayarlandı.
- Web uygulamasını native `www/` paketine deterministik biçimde kopyalayan `scripts/prepare-web.mjs` ve npm komutları eklendi.
- iOS uygulama ikonu mevcut Tasarruf Yanımda ikonuyla, açılış ekranı Eminevim yeşili ve beyaz logosuyla markalandı.
- Uygulama portre kullanımına sınırlandı; Türkçe konum izni açıklaması ve ihracat uyumluluk bilgisi eklendi.
- Codemagic macOS ortamında SPM senkronizasyonu, otomatik App Store imzalama, IPA üretimi, build numarası artırma ve TestFlight yüklemesi için `codemagic.yaml` hazırlandı.
- Apple Developer, App Store Connect ve Codemagic gizli değişkenlerinin kurulumu `IOS_TESTFLIGHT.md` dosyasında belgelendi; hiçbir sertifika veya özel anahtar repoya eklenmedi.
- Capacitor senkronizasyonu, YAML/XML doğrulaması, organizasyon testleri ve çalışma zamanı bağımlılık güvenlik taraması başarıyla tamamlandı. Windows ortamında Xcode derlemesi yapılamadığı için ilk imzalı IPA doğrulaması Codemagic üzerinde yapılacak.

### 2026-10-05 - Giriş ekranına hızlı dönüş

- Müşteri, SPY, yönetici ve admin ekranlarının sağ üst durum çubuğuna küçük `↩ Giriş` düğmesi eklendi.
- Düğme mevcut oturumu güvenli biçimde kapatıp ana giriş ekranına dönüyor; panel başlıkları ve diğer sağ üst kontrollerle çakışmıyor.
- 390×844 mobil görünümde SPY ve ASK Müdürü ekranlarında yerleşim, dönüş davranışı ve tarayıcı konsolu doğrulandı.

### 2026-10-05 - Panel geçişi sadeleştirildi

- Müşteri ana girişi ve Personel/SPY erişimi korunarak geri getirildi.
- Personel girişindeki Takım Lideri, Saha Grup Lideri ve Alternatif Satış Kanalı Müdürü rol seçenekleri korundu.
- Oturum içindeki yalnızca geliştirme amaçlı `Müşteri / SPY Paneli / Admin Paneli` üst geçiş şeridi kaldırıldı.

### 2026-10-05 - İlk TestFlight doğrulama hataları giderildi

- Uygulama portre kullanımını koruyacak şekilde yalnızca iPhone hedef ailesine sınırlandı; iPad çoklu görev yönlendirme doğrulama hatası kaldırıldı.
- 1024×1024 App Store ikonundaki alfa kanalı kaldırıldı ve ikon 24 bit RGB PNG olarak yeniden kaydedildi.
- Apple API anahtarları proje dışındaki güvenli klasörde tutuldu; sertifika ve provisioning dosyaları Git dışında bırakıldı.

### 2026-10-05 - İlk iPhone TestFlight kurulumu tamamlandı

- Codemagic üzerinden imzalı iOS IPA üretildi ve App Store Connect'e başarıyla yüklendi.
- App Store Connect API, otomatik kod imzalama ve TestFlight yapı numarası akışı doğrulandı.
- Build 1, iç test grubuna eklendi; davet kabul edilerek uygulama gerçek iPhone cihazında TestFlight üzerinden kuruldu ve açıldı.

### 2026-10-05 - Native ekran kaydırma ve sabit navigasyon

- Müşteri, SPY ve yönetici panellerinde üst durum/başlık alanları ile alt navigasyon ekranın sabit bölümleri haline getirildi; yalnızca orta içerik dikey kaydırılıyor.
- Mobil görünümde alt menüyü tüm sayfaya sabitleyen kırılgan genel CSS kaldırıldı; panel bazlı flex yerleşim ve iOS momentum kaydırması eklendi.
- SPY ve yönetici karşılaştırma tablolarının sütun başlıkları, uzun listeler kaydırılırken üst başlığın hemen altında görünür kalacak şekilde yapışkanlaştırıldı.
- Kısa içerikli performans ve müşteri ekranları gereksiz kaydırma oluşturmadan 390×844 ekrana oturtuldu; düşük ekran yükseklikleri için aralıklar kompaktlaştırıldı.
- 390×844 testinde SPY karşılaştırmasında 10.763 px uzunluğundaki içerik kaydırılırken üst başlık, tablo başlığı ve alt navigasyonun konumlarını koruduğu doğrulandı; Capacitor iOS paketi yeniden senkronize edildi.

### 2026-10-05 - Native iOS ve raporlama iyileştirmeleri (18 madde)

- Native kabuk: telefon çerçevesi native/mobilde tamamen kalkıyor; üst şerit çentik/Dynamic Island alanını panel başlığının rengiyle dolduruyor. `contentInset: never`, `@capacitor/status-bar` (ekrana göre açık/koyu yazı) ve `@capacitor/haptics` eklendi. Tüm yeşil `div`'lere üst boşluk veren hatalı güvenli alan CSS kuralı kaldırıldı.
- Service Worker native'de (`window.EMINEVIM_NATIVE`) kaydedilmiyor; tarayıcıda `?native=1` ile native düzen test edilebiliyor.
- Karşılaştırma tabloları ilk 20 satırı gösteriyor; SPY kendi satırını listenin dışındaysa altta görüyor; "Tümünü göster" ile tam liste açılıyor.
- Harita tile sağlayıcısı `map.html` içinde tek bir `MAP_TILE_PROVIDER` nesnesine taşındı (şimdilik OSM; `EMINEVIM_CONFIG.mapTiles` ile değiştirilebilir).
- Demo rapor tarihi cihaz saatinden alınıyor (`EMINEVIM_CONFIG.demoToday` ile sabitlenebilir).
- Aylık H/G artık ayın tam hedefine göre; kartta gerçekleşen, ay hedefi ve "bu hızla ay sonu tahmini" gösteriliyor. Aylık değişim geçen ayın aynı günlerine göre hesaplanıyor ve kartta açıklanıyor.
- Binlik kısaltma "B" yerine "bin".
- Özet ekranları sadeleştirildi: H/G kartı + Bugün Ciro/Randevu/Kart/Kayıt şeridi (SPY'de takım ortalaması, yöneticide kişi başı ve şirket ortalamasıyla renk) + dönüşüm hunisi.
- Saha Canlı: seçili kapsamdaki tüm personel için seed'li canlı durum ve mesai saatli olay akışı; demo SPY'ler gerçek akıştaki durumlarını koruyor.
- Yönetici panelinden Genel sekmesi kaldırıldı; alt menü SVG ikonlara geçti; tüm alt menü butonlarına `aria-label` eklendi.
- Dokunsal geri bildirim (sekme, bildirim, yenileme), iOS'ta çalışan touch tabanlı çekip yenileme (SPY ve yönetici), sistem koyu temasına uyum ve koyu temada okunur alt menü renkleri.
- SPY Harita sekmesi tam yükseklik; GPS durumu haritanın üstünde ince şerit.
- PWA önbelleği `eminevim-v7`, `org-data.js?v=7`, `map.html?v=4`.
- Doğrulama: `npm test` geçti; 390×844 native düzende SPY/TL/SGL/ASK özet, karşılaştırma, Saha Canlı, harita, çekip yenileme, açık/koyu tema ve müşteri giriş → KVKK → Başvuru akışı; masaüstü çerçeveli görünüm kontrol edildi, konsolda hata yok.

### 2026-10-05 - React uygulama içine alındı

- React ve ReactDOM 18.3.1 UMD dosyaları `vendor/` klasörüne alındı; native uygulama artık açılmak için unpkg'ye bağlı değil. Dosyaların SHA-384 özeti `support.js` içindeki SRI değerleriyle birebir aynı.
- `scripts/prepare-web.mjs` `vendor/` klasörünü native pakete kopyalıyor; PWA önbelleği `eminevim-v8` oldu ve vendor dosyalarını içeriyor.
- Doğrulama: native düzende React yerel dosyadan yükleniyor, unpkg isteği yok; `npm test` geçti.
- Not: Google Fonts (Manrope/Inter) ve haritadaki Leaflet hâlâ internetten geliyor; internet yoksa sistem fontu kullanılır, harita zaten tile için internet gerektirir.

### 2026-10-05 - Müşteri paneli native dokunma sorunları

- Başvuru sihirbazında "Devam" butonuna basılamıyordu: müşteri alt menüsünü bulan mobil CSS seçicisi (`[style*="position:absolute"]`) React'in yazdığı `position: absolute` biçimini yakalamadığı için menü yüzer kalıyor ve Devam/Geri çubuğunun üstüne biniyordu. Menüye doğrudan `app-bottom-nav` sınıfı verildi; artık akışta, içeriğin altında duruyor. Admin menüsü de aynı sınıfı aldı (home indicator boşluğu).
- Mobilde alt menünün katmanı 50'den orijinal 40'a çekildi; nokta seçme ekranındaki "Bu Konumu Gönder" artık menünün altında kalmıyor.
- SPY "Devret" ve "Görüşme sonucu" alt sayfaları menünün üstüne alındı ("Vazgeç" basılabilir). Tüm alt sayfalara ve nokta seçme onay kartına iPhone alt çubuğu için güvenli alan boşluğu eklendi.
- Doğrulama: 390×844 native düzende müşteri Profil/Başvuru/İletişim/Ayarlar, sihirbazın 3 adımı ve kayıt, sohbet, randevu ve nokta seçme ekranlarında görünen tüm butonların dokunuşu aldığı otomatik olarak kontrol edildi; SPY Devret sayfası doğrulandı. PWA önbelleği `eminevim-v9`.

### 2026-10-20 - Web kolu: Tasarruf Yanımda başvuru formu önizlemesi

- `web-basvuru/` eklendi: eminevim.com ana sayfasının kopyasında Hızlı Başvuru formu yenilendi ("Nasıl görüşelim?": temsilci gelsin / beni arayın / şubeye geleceğim).
- Temsilci gelsin akışı: konu, iş yeri/ev, il-ilçe/konum, gün, saat aralığı, e-posta; cumartesi seçilince hafta içi öğle arasına yönlendirme.
- Takip linki SMS yerine e-postayla gider; gönderim sonrası e-posta önizlemesi (temsilci kartı, sicil no, randevu, canlı takip butonu, güven notları).
- `olustur.py` canlı sayfayı indirip formu yerleştirir, GTM/Facebook/reCAPTCHA kodlarını çıkarır; form veri göndermez.
- Doğrulama: 390×844 ve 1440×900'de Chrome ile uçtan uca dolduruldu, sayfa hatası yok.

### 2026-10-21 - Sade yeni müşteri akışı, Finansmanlarım, web formu aynı akışa geçti

- Önceki uygulama yedeklendi: `backup/2026-10-21-eski-uygulama/` (açılır hâlde) + git etiketi `eski-uygulama-2026-10-21`.
- Giriş ekranındaki "Yeni Müşteri" artık üyelik istemeden 3 adımlı akışı açar: Temsilcimiz size gelsin (ad, telefon) → Ne zaman, nerede? (gün/saat/yer/ilçe) → Talebiniz alındı (özet, en yakın temsilci kartı, isteğe bağlı e-posta). "Görüşme günü" örnek ekranı ve "Telefonla görüşmeyi tercih ederim" seçeneği var; talep temsilci paneli listesine düşer.
- Bütçe/finansman sihirbazı yalnız üyelere: sekmenin adı "Finansmanlarım". Akışın sonundaki "Üye olun" kayıt formunu bilgilerle doldurur → KVKK → Finansmanlarım.
- Web formu aynı 3 adıma çevrildi; sonda uygulama linki (sayfadaki tek çalışan link).
- Doğrulama: 390×844'te Chrome ile yeni akış, telefonla seçeneği, üyelik → Finansmanlarım ve yedek sürüm uçtan uca denendi; web formu mobil ve masaüstünde denendi; sayfa hatası yok.

### 2026-10-21 (gece) - Web taslağı, Finansmanlarım taslağı, bağlantılar sayfası

- `taslak/web-akisi.html`: web formunun aynı 3 adımı (telefon ekranları + bilgisayar görünümü) ve gelen e-posta.
- `taslak/uygulama-akisi.html`: "Üye olun" bağlantısı ve 6. ekran "Finansmanlarım (yalnız üyeler)" eklendi.
- `linkler.html`: tüm taslak, önizleme ve yedek bağlantıları tek sayfada (açık/koyu tema).
- Web formu: adım değişince odak başlığa geçer; masaüstü paneli kendi aç/kapa koduyla yana gizlenir (sitenin kodu geniş panelde çalışmıyordu); e-postada "Temsilcimin yerini gör" dili.
- Uygulama dosyasına dokunulmadı.

### 2026-10-21 - Web formu gerçek sitedeki forma döndü

- Adımlı akış, "Tasarruf Yanımda" yazısı, simgeler ve önizleme etiketi kaldırıldı; sayfa sitenin kendi başlığıyla en üstten açılır.
- Form sitedeki alanlar ve sınıflarla (gri kutucuklar, bayrak + telefon, onay kutuları, turuncu Gönder); mobilde sitenin mobil sınıfları.
- Ek: kesik çizgili "Temsilcimiz size gelsin · İsteğe bağlı" kutusu → gün/saat/yer seçimi, ilçe, isteğe bağlı e-posta. Teşekkür ekranı sitenin mesajı + özet + temsilci kartı + uygulama linki.
- Onay kutularında yazıya tıklayınca da işaretlenir (sitenin iç içe etiket yapısı düzeltildi). Yazı tipi yüklenemezse tırnaklı yazıya düşmez.
- `taslak/web-akisi.html` yeni forma göre yeniden çizildi.
- Doğrulama: mobil ve masaüstünde seçenekli/seçeneksiz gönderim, e-posta önizlemesi, yeni başvuru; sayfa hatası yok.

### 2026-10-21 - Tek önizleme sayfası

- `linkler.html` artık tek sayfalık önizleme: üstte "Uygulama / Web formu" ve "Telefon / Bilgisayar" seçimi, seçilen görünüm ekrana sığdırılmış çerçevede açılır; "Tam ekran aç", taslaklar ve eski sürüm linkleri altta. Seçim adreste (`#uygulama-telefon` vb.) ve tarayıcıda hatırlanır.
- Doğrulama: 390×844 ve 1440×900'de dört görünüm açıldı, yatay taşma ve sayfa hatası yok.

### 2026-10-21 - Önizleme sayfası: telefonda tam ekran, iPhone çerçevesi, yapılacaklar

- Telefonda yalnız sol üstte küçük "Uyg / Web" tuşları; sayfa gerçek boyutunda tam ekran.
- Bilgisayarda iPhone 15 biçimi ve boyutu (393×852, Dynamic Island, yan tuşlar); uygulamanın bilgisayar görünümü kaldırıldı, Telefon/Bilgisayar seçimi yalnız Web formunda.
- Sağda "Yapılacaklar" (ekle, işaretle, sil). ŞİMDİLİK yalnız o tarayıcıda saklanıyor; herkesin yazabileceği ortak kayıt yöntemi kullanıcı kararı bekliyor.

### 2026-10-21 - Web formu görünüm iyileştirmeleri (8 madde)

1. Temsilci seçeneği: düz açık yeşil kart, konum simgesi, açma-kapama anahtarı, "İsteğe bağlı" etiketi; açıklama tam genişlikte.
2. Açılan alanlar kısaldı: gün + saat yan yana (kısa etiketler), yer iki dokunmalık seçim (İş yeri / Ev), ilçe, e-posta; kart içindeki kutular beyaz.
3. Telefonda "Gönder" açılır pencerenin altında sabit.
4. Hatalar kutu başına: eksik kutu sitenin turuncu hata renginde, kısa uyarı altında; düzeltilince kaybolur, ilk eksiğe kaydırır.
5. Okunabilirlik: eklenen bölümde yazı 9–10.5 pt, kutucuk ipuçları daha koyu.
6. Seçenek açılınca kısa kayma ile açılır (hareket azaltma ayarında kapalı).
7. Teşekkür: konum simgesi, özet + temsilci kartı tek kutuda, "Görüşmede ödeme alınmaz."
8. Bilgisayarda panel gizlenince "HIZLI BAŞVURU" yanında küçük yeşil nokta.
- `taslak/web-akisi.html` yeni görünüme uyarlandı. Doğrulama: mobil ve masaüstünde boş/eksik/tam gönderim, hata temizlenmesi, kapalı panel; sayfa hatası yok.

### 2026-10-21 - Oturum kapanışı

- Kararlar, açık işler ve teknik notlar `CLAUDE.md`'ye yazıldı (yeni oturum oradan devam eder).
- Bekleyen: Google E-Tablo linki (yapılacaklar ortak olsun), TestFlight derlemesi, finansman rakamları için uyum onayı.

### 2026-10-21 - Web formu: takvim + harita akışı, e-posta kaldırıldı, telefon çubukları

1. Telefonda tarayıcının üst/alt çubuğu: site penceresi ve yeni pencereler görünür yüksekliğe (dvh) oturur; önizlemede web-telefon görünümüne Safari çubukları eklendi (görünür alan 393×659).
2. Sıra: Ad, Soyad, Telefon → onay kutuları → "Temsilcimiz size gelsin" düğmesi (konum simgesi + yazı) → Gönder. Altta açılan uzun alanlar kaldırıldı.
3. Düğme → takvim penceresi (gün + saat) → Onayla → harita penceresi (haritadan yer, İş yeri/Ev) → Onayla → düğmede kısa özet, × ile kaldırma.
4. E-posta alanı kaldırıldı; teşekkür ve önizleme "mesaj" diliyle.
5. Demo: her açılışta ve "Yeni başvuru"da örnek bilgilerle dolu.
- Doğrulama: 393×659 telefon ve 1440×900 bilgisayarda tam akış (takvim, harita sürükleme + adres, gönderim, mesaj önizleme, yeni başvuru); sayfa hatası yok, yatay taşma yok.
- Bekleyen: `taslak/web-akisi.html` eski akışı (anahtar + alanlar + e-posta) gösteriyor; güncellenmesi gerekiyor.

### 2026-10-21 - Finansman planı web'de, site görünümü uygulamaya

1. Web: sitedeki Konut / Araç / İşyeri kutuları (bilgisayarda üst menü; telefonda Çözümlerimiz kartları ve menü) "Ödeme planınızı oluşturun" penceresini açar: tür, aylık ödeme (koyu yeşil kart), tutar (+hazır tutarlar), peşinat, vade, Bireysel/Çekilişli. Hesap uygulamadakiyle aynı; "Örnek hesaplamadır" notu. "Bu planla başvur" → plan forma tek satır eklenir, form açılır.
2. Web teşekkür: temsilci hemen gösterilmez ("Görüşme saatinden önce bilgilendirileceksiniz"); uygulama indirme yazısı; haritadaki İş yeri/Ev kaldırıldı.
3. Web pencereleri (takvim, saat, harita, plan) sitenin renk/köşe/gri kutu değerleriyle.
4. Uygulama: tüm ekranlar site görünümüne çevrildi (renk, turuncu ana düğme, gri hap kutular, yeşil çerçeveli ikincil düğmeler, yazı tipi). Yeni müşteri akışı: yer türü ve e-posta kaldırıldı, temsilci hemen gösterilmez. Finansman sonuç kartı web'deki gibi; tür seçilince tutar örnekle dolu.
- Doğrulama: web 393×659 ve 1440×900 (kart → plan → form → takvim → harita → teşekkür, plan satırından yeniden açma); uygulamada giriş, KVKK, müşteri, finansman 3 adım, ayarlar, yeni müşteri 3 adım, personel ekranları; sayfa hatası yok.

### 2026-10-21 - Ürün kuralları yazıldı (konuşarak ilerleme)

- CLAUDE.md başına "Ürün kuralları" bölümü: uygulama kapsamlı / web hızlı aksiyon, marka birliği, web formunda radio + konum izni + küçük harita (yeşil hizmet bölgeleri: Ümraniye, Ataşehir, Üsküdar) + elle konum, Başarılı ekranı, web→uygulama geçişi (telefonla kayıtlı, finansmansız), 3 sayfalık Hoş geldiniz, Kayıtlı Müşteri demo senaryosu, uygulamada Temsilci iste.
- Kod henüz değişmedi; açık sorular kullanıcıyla adım adım netleşecek.

### 2026-10-21 - Adım 1: web formunda temsilci seçimi + küçük harita

- Onay kutularından sonra iki seçenek (radio). "Temsilci çağırmak istiyorum" → form içinde küçük harita, konum izni, yeşil hizmet bölgeleri (Ümraniye, Ataşehir, Üsküdar), dokunarak/sürükleyerek seçim, adres/mekân arama, "Konumumu kullan".
- Bölge dışı: "Bu bölgede henüz temsilci hizmetimiz yok… sizi telefonla arayalım" → telefonla başvuru.
- Haritadan sonra gün/saat satırı → takvim penceresi. Eski "Temsilcimiz size gelsin" düğmesi ve büyük harita penceresi kaldırıldı.
- Finansman penceresi yedekte; sitedeki kutularla bağlantısı kesildi.
- Doğrulama: izinli (Ümraniye), izinsiz (örnek Ataşehir), bölge dışı arama (Moda/Kadıköy), bilgisayar paneli; sayfa hatası yok.

### 2026-10-21 - Adım 2: Başarılı ekranı, ödeme cümleleri kaldırıldı

- Web: "Başarılı!" ekranı (kurumsal-samimi metin, özet, temsilci bilgisi uygulamadan, uygulama kartı + "Uygulamayı aç"; link ad/tel/gün/saat/yer taşır). Telefonla ve bölge dışı durumları için kısa metin.
- Kural: ödeme/ücret güvencesi cümleleri hiçbir yerde yok — web, uygulama ve taslaklardan kaldırıldı.

### 2026-10-21 - Temsilci seçimi pencereye taşındı

- Formda yalnız "Temsilci çağırmak istiyorum" kaydırmalı düğmesi. Açılınca pencere: harita (üstte arama, sağ altta "Hizmet bölgesini göster" / "Konumuma dön") → gün ve saat → Onayla. Formda tek satır özet.
- Bölge dışı: "Telefonla görüşmeyle devam et" → formda not, başvuru telefonla.
- Doğrulama: telefon (izinli Ümraniye, bölge düğmesi iki yönlü, takvim, özet, gönderim; onaysız kapatma; Kadıköy bölge dışı) ve bilgisayar; sayfa hatası yok.

### 2026-10-21 - Uygulama senaryoları kurallara uyduruldu

- Giriş/kayıt telefonla; "Yeni Müşteri" artık telefonla kayıt (eski üyeliksiz temsilci akışı girişten kalktı).
- Web "Uygulamayı aç" → uygulama telefonla kayıtlı müşteri olarak açılır (finansman yok, talep + atanan temsilci + sohbet).
- Yeni sekmeler: Başvurum, Sohbet, Finansman, Ayarlar. 3 sayfalık Hoş geldiniz. Kayıtlı Müşteri: randevusu netleşmiş, temsilcisini bekliyor.
- Uygulamadan "Temsilci iste" (hizmet bölgesi kontrolü). Temsilci akışı ekranları giriş ekranının dışına taşındı (uygulama içinden açılmıyordu).
- Doğrulama: web→uygulama uçtan uca, web telefonla, kayıtlı müşteri (telefonla giriş, sohbet, görüşme günü), yeni kayıt → Temsilci iste (Kadıköy reddi, Ataşehir kabul → atandı); sayfa hatası yok.

### 2026-10-21 - Telefonda alt çubuk, uygulamada web gibi temsilci isteme

- Önizleme (`linkler.html`) telefonda görünür yüksekliğe oturur (dvh + visualViewport): Safari'nin alt çubuğu uygulamanın alt sekmelerini / formun Gönder'ini kapatmıyordu.
- Uygulama "Temsilci iste": web penceresiyle aynı — 1/2 harita (`konum-sec.html`: arama, yeşil hizmet bölgeleri, Konumuma dön) → 2/2 gün ve saat (10:00–20:00) → "Talebiniz alındı" → Başvurumu gör. Bölge dışı → telefonla talep.
- Finansman sekmesinde temsilci bulma/iletişim düğmesi yok; kaydedince Finansman'da kalır. Eski "Temsilci Bul" eşleştirme ekranı kaldırıldı.
- Doğrulama: yeni kayıt → Başvurum boş → harita (Üsküdar) → gün/saat → başarılı → temsilci atandı; Finansman'da temsilci düğmesi yok; sayfa hatası yok.

### 2026-10-21 (gece) - Randevum, saat onayı, temsilci bilgileri, resimli Hoş geldiniz

- Başvurum → **Randevum**; tekrarlayan yazılar kaldırıldı; temsilci "Bilgiler" tuşuyla (Randevum + Sohbet) alt pencerede.
- Sohbet: temsilci saati önerir, "Saati onayla" düğmesi. Finansman: "+ Yeni", "Değiştir".
- Kayıtlı Müşteri: KVKK sorulmuyor, görüşme günü senaryosu (temsilci yolda, "Temsilcinizi takip edin").
- Hoş geldiniz: 3 sayfa, basit resimler. Web Başarılı (bilgisayar): mağaza simgeleri. Önizlemede bilgisayarda Safari çubukları yok.
- Doğrulama: kayıtlı müşteri, yeni kayıt → harita → onay → sohbette saat onayı, web bilgisayar başarılı ekranı; sayfa hatası yok.

### 2026-10-21 (gece 2) - Değiştir/iptal, gecikme, görüşme özeti, puan, temsilci profili

- A/B/C: finansman kaydı sohbete düşer; Finansman ilk adım yazısı temsilcisi olmayana söz vermez; bölge dışı müşteride "Başka adres için temsilci iste".
- Randevum: Gün/saati değiştir (temsilci onayıyla), İptal et, gecikme uyarısı, görüşme özeti (doğru / sorun var), puan, yeni randevu.
- Temsilci bilgileri: puan, deneyim, görüşme sayısı.
- Doğrulama: kayıtlı müşteri (gecikme → bitti → puan → özet → sorun), yeni kayıt (talep → değiştir → netleşti → finansman sohbete → iptal), web'den bölge dışı; sayfa hatası yok.

### 2026-10-21 (gece 3) - Kapıda QR doğrulama, personel ekranları marka birliği

- Müşteri: görüşme günü "Kapıda kimliğini doğrula" → QR + 4 haneli kod; personel okutunca ekran yeşil ("Temsilciniz yanınızda").
- Personel (SPY): "Bugünkü randevu" kartı + QR okutma ekranı (kod ile yedek, yanlış kodda uyarı).
- Personel ekranları sitenin renk/kutu/yazı tipine çevrildi. Düzeltilen eski hatalar: personel çıkışı müşteri kaydını eziyordu; bildirim başlığı her zaman "Yeni Başvuru" yazıyordu.
- Doğrulama: müşteri QR → personel yanlış/doğru kod → müşteri yeşil → görüşme bitti → puan; önceki tüm akışlar; sayfa hatası yok.

### 2026-10-22 - Senaryo sekmesi (müşteri + personel tableti, adım adım)

- linkler.html'e üçüncü üst sekme "Senaryo"; `senaryo.html`: solda müşteri (telefon ya da bilgisayar), sağda personel tableti (yatay), 12 adımlık Senaryo 1, İleri/Geri, otomatik oynat, adım linkleri.
- Bilgisayardaki müşteri için uygulamasız takip sayfası tasarlandı; kapıda SMS linkiyle telefon.
- Doğrulama: bilgisayar (1440) ve telefon (390) genişliği, iki müşteri cihazı, sekmeler arası geçiş; sayfa hatası yok.

### 2026-10-22 - Personel tablet düzeni, Görüşmeler, Saha Canlı, bugünkü rota

- Personel girişi yatay tablet düzeninde (önizleme çerçevesi kendiliğinden tablete döner). SPY ve Takım Lideri: Görüşmeler (Bekleyen / Şu an görüşülüyor / Gerçekleşti, tarih sırası), Performans; TL/SGL/ASK: Saha Canlı (3 sayı + personel listesi).
- Eski mantıklar kaldırıldı: geri arama sayacı, eski harita düğmeleri, Geçmiş sekmesi, uydurma bildirimler; müsaitlik görüşmede otomatik.
- Müşteri ↔ personel bağlantısı: QR → "Şu an görüşülüyor"; "Görüşmeyi bitir" → müşteride özet + puan; puan personelde görünür; uygulamadan talep → "Yeni talep".
- Fotoğraf: sentetik portre komutu `assets/temsilci/OKUBENI.md`, dosyalar bekleniyor.
- Doğrulama: SPY (kabul, rota, QR, bitir), müşteri (özet, puan), TL (Görüşmeler, Saha Canlı), ASK (Saha Canlı, Performans), önizleme tablet/telefon geçişi, telefon genişliği, önceki müşteri akışları; sayfa hatası yok.

### 2026-10-22 - Yerinde hizmet modelleri ve tasarım araştırması

- `rapor/tasarruf-yanimda-karsilastirma-2026-10-22.md`: Türkiye ve dünya örnekleri, resmî kaynaklar, başvuru/randevu/takip/doğrulama karşılaştırması ve Tasarruf Yanımda için öneriler.
- Enpara, Akbank, Memorial, Kolay Gelsin, tasarruf finansmanı uygulamaları; ANZ, PSB Alliance, Urban Company, Uber ve Bank of America incelendi. Yeni müşterinin hem webden hem uygulama kaydından başvurması esas alındı.
- PSB ekran kılavuzu, ANZ hazırlık listesi ve Urban Company güvenlik şeması render edilerek incelendi; beş görsel `rapor/arastirma-gorselleri/` altında saklandı. Canlı tarayıcı erişimi olmadığı ve tarihli ekranların güncel arayüz kanıtı sayılmadığı raporda belirtildi.
- Düzeltme: Birevim uygulamadan yeni başvuru sunuyor; rakiplerin yalnız sözleşme sonrasında başladığı genellemesi kullanılmamalı. Bulunamayan özellikler yokluk kanıtı olarak sunulmadı.
- Doğrulama: raporun beş yerel görsel bağlantısı kontrol edildi. Uygulama kodu değiştirilmedi; yayın/commit/push yapılmadı.

### 2026-10-22 - Randevu, takip ve görüşme sonrası döngüsü

- Randevum durum odaklı düzenlendi; doğrudan saat onayı, temsilci erişimi, değişiklik/iptal ve destek. Bekleyen yeni öneri eski randevuyu değiştirmiyor; personel onaylıyor.
- Web başvurusu kimlik, tarih ve koordinatlarla uygulamaya aktarılıyor. Çalışma durumu/yaş aralığı başvuru sonrasında atlanabilir; müşteri uygulamasında düzenleniyor, personel ayrıntısında görünüyor.
- Personelin hareketi, gecikmesi, QR doğrulaması ve özeti aynı randevuya bağlandı. Sabit kod yerine randevu/temsilci/revizyona bağlı, süreli ve tek kullanımlık demo kodu. Gerçek kamera/sunucu doğrulaması ve canlı GPS/ETA henüz yok.
- Görüşme özeti, personel notu ve sonraki adım müşteriye ulaşıyor. Açıklamalı düzeltme/destek talebi ve ASK panelinden inceleme/yanıt; müşteri durum takibi. Puan isteğe bağlı; yeni randevuyu engellemiyor.
- İptaller ve geçmiş görüşmeler korunuyor; sekme içi sessionStorage ile yenilemede geri geliyor. Gerçek cihazlar arası eşitleme henüz yok.
- Native paketleme ve PWA listesine yeni randevu modülü, konum/rota sayfaları ve QR kitaplığı eklendi. Web önizlemesi yeniden üretildi.
- Web üreticisinde satır sonları kararlı LF çıktısına çevrildi; canlı siteden gelen Citrix performans ölçümü de ayıklanıyor. Bu nedenle üretilmiş index.html farkı kaynak formundan daha büyük; satır sonu temizliği içeriyor.
- Doğrulama: organizasyon ve randevu regresyonları; Chrome'da 320/393 px müşteri, 1180 px personel; 393/1440 px web başvurusu ve uygulamaya veri aktarımı. Görsel inceleme yapıldı. Senaryo sayfası değiştirilmedi.

### 2026-10-22 - Telefon sekmelerinde yerleşim düzeltmesi

- Finansman/Ayarlar ekranlarında alt menünün yukarı çıkması ve Sohbet altındaki boşluk düzeltildi. Yükseklik kuralları animasyon adlarından bağımsız `app-stage`, `customer-shell` ve `customer-panel` sınıflarına bağlandı.
- Başlık/alt menü sabit alanı ve orta kaydırma alanı ayrıldı; finansman eylemleri, kısa ekran pencereleri ve görünür ekran yüksekliği düzenlendi.
- 400 px altındaki personel sayaçlarında kelime bölünmesi giderildi; performans göstergeleri iki sütuna alındı.
- Doğrulama: `tests/phone-layout.py` ile 320×568, 393×852, 390×659, 430×932; kısa görünür alan, QR penceresi, müşteri/personel sekmeleri ve linkler.html telefon çerçevesi. Chrome görselleri incelendi; `tests/browser-flows.py` geçti. Yerel web paketi yenilendi; yayın/push yapılmadı.

### 2026-10-22 - Hazırlık bilgileri saat onayından sonra

- Sayfadaki hazırlık kartı ve gömülü form kaldırıldı; Randevum veya Sohbet üzerinden saati onaylayınca isteğe bağlı alt pencere açılıyor. Önceden bilgi paylaşılmışsa tekrar otomatik sorulmuyor.
- Şimdi değil veya dış alana dokunma pencereyi kapatır; randevu onayı korunur. Onay sonrası Randevum üzerinden bilgi ekleme/düzenleme erişimi sürer.
- Doğrulama: 320×568 ve 393×852 ekranlarda onay öncesi gizlilik, her iki sekmeden açılma, atlama, kaydetme, yeniden giriş ve görsel kontrol (`tests/preparation-popup.py`); tam müşteri/personel akışı geçti. Yerel paket yenilendi.

### 2026-10-22 - Hazırlık penceresinden finansman tercihleri

- Hazırlık bilgileri penceresine görüşmeyi beklerken finansman seçeneklerini inceleme açıklaması ve Ön tercihlerimi oluştur düğmesi eklendi. Pencere kapanıp Finansman sekmesi açılır; mevcut tercihler ve randevu korunur.
- 320/393 px görsel kontrol ve hazırlık penceresi testinde yönlendirme doğrulandı.

### 2026-10-22 - Randevularım listesi ve iPhone güvenli alanları

- Randevularım sekmesi temsilci ve tarih sütunlarıyla açılır. Aktif randevu önce, geçmiş kayıtlar yakın tarihten geriye sıralanır. Yeni/henüz açılmamış aktif kayıtta ünlem vardır; okunma bilgisi randevu kimliği/revizyonuyla sekme içinde saklanır.
- Satırdan ayrıntıya geçilir; üstte geri/ileri ve tüm randevular bağlantısı vardır. Geçmiş kayıtlar kendi temsilci/tarih/özetini gösterir; aktif randevu eylemleri geçmiş kayda uygulanmaz.
- Müşteri başlığındaki Giriş kaldırıldı; Ayarlar çıkışı sürer. Finansman ön tercih yönlendirmesi hazırlık penceresinden aktif randevu ayrıntısına taşındı.
- Masaüstü iPhone 15 önizlemesinde 59 px üst durum alanı, ölçeklenen 126×37 kamera adası ve 34 px alt güvenli alan/ana ekran göstergesi. Gerçek cihazda kamera çizilmez; sistem safe-area değerleri kullanılır. Alt pencereler üst/alt güvenli alanı gözetir.
- Doğrulama: organizasyon/randevu regresyonları; müşteri–personel–QR–özet–destek, hazırlık penceresi, 320–430 px telefon yerleşimi ve yeni liste/okunma/gezinme testleri geçti. iPhone çerçevesi ve 320 px görüntüleri incelendi. Gerçek iPhone cihaz testi yapılmadı. Yerel paket yenilendi, yayın/push yok.

### 2026-10-22 - Sade randevu ayrıntısı ve Konuşmalar listesi

- Ayrıntı içindeki Tüm randevular/açıklama ve ileri/geri çubuğu kaldırıldı. Üst başlıkta logo yerine Geri görünür; randevu veya konuşma listesine döner.
- Kesinleşen randevunun yola çıkış açıklaması kaldırıldı; tarih/adres altına Temsilciniz: ad soyad eklendi. Ayrı temsilci kartı ve Temsilciye yaz düğmesi kaldırıldı.
- Sohbetler sekmesi Konuşmalar listesi açar; mevcut temsilcinin adından konuşma açılır. Doğrudan takip ekranındaki Mesaj gönder konuşmayı açmaya devam eder.
- Liste kartlarında randevu durumu belirgin etiket; henüz kesinleşmeyen bekleyen kayıtta, okunmuş olsa bile ünlem kalır. Kesinleşmiş kayıt için mevcut okunma davranışı korunur.
- Telefon modu URL algısındaki kontrol karakteri düzeltildi; native=1 önizlemesi yanlışlıkla servis çalışanı kurup girişten sonra yenilenmez.
- Doğrulama: liste/geçmiş/Geri/konuşma açma ve mesaj gönderme, okunmuş bekleyen kayıtta ünlem; tam müşteri-personel akışı; hazırlık ve 320–430 px yerleşim testleri. Görseller incelendi; yerel paket güncellendi.

### 2026-10-22 - Lacivert üst şeritlerin kaldırılması

- Giriş ve KVKK ekranlarındaki dekoratif 30 px lacivert şeritler kaldırıldı. Eski panel durum çubuğunun varsayılan rengi başlık yeşiline bağlandı.
- 393×852 Chrome görüntülerinde giriş/onay ekranları incelendi; lacivert üst şerit olmadığı doğrulandı. Yerel paket güncellendi.

### 2026-10-22 - Tek yerde Geri ve sade müşteri başlığı

- Müşteri başlığındaki Eminevim logosu ve sağdaki fotoğraf/baş harf simgesi kaldırıldı. Başlık ortada hizalanır; dönüş gereken ekranda sol üstte yalnız Geri metni görünür.
- Finansman formunun altındaki Geri ve takip/başvuru kartlarındaki dönüş düğmeleri kaldırıldı; finansman adımlarında ve ekran başlıklarında Geri kullanılır. Girişte form içindeki geri de sol üste taşındı. Harita başlıkları yalnız Geri metni kullanır.
- Doğrulama: 320–430 px telefon sekmeleri ve finansman adımlarında üst Geri ile adım/liste dönüşleri; randevu ve konuşma liste/detay akışları geçti. iPhone önizleme görseli incelendi, yerel paket yenilendi.

### 2026-10-22 - Codex değişikliklerinin incelenmesi ve yayını

- Codex'in randevu modeli, Randevularım/Konuşmalar, hazırlık penceresi, destek, iPhone güvenli alanı ve web üreticisi değişiklikleri incelendi; 5 tarayıcı testi geçti (Node bu sunucuda yok, birim testleri çalıştırılamadı).
- Düzeltmeler: başka kurumlardan alınmış 5 araştırma görseli herkese açık depodan çıkarıldı (.gitignore; raporda kaynak linkleri); Ayşe Kaya kaynağı "Uygulama · kayıtlı müşteri"; randevu ayrıntısında "Temsilcinizi takip edin" ikincil düğme (ana eylem kapıda doğrulama); CLAUDE.md'de sona eklenmiş notlar "Müşteri uygulaması yerleşimi ve gezinme" bölümüne taşındı.

### 2026-10-22 - SMS giriş kodu ve parola oluşturma

- Web: temsilci çağrıldıysa başarı ekranında SMS önizlemesi (6 haneli kod, 24 saat; uygulama hizmetleri cümlesi; link).
- Uygulama: web linki kod ekranını açar → kod → parola oluştur → randevu. Yeni müşteri: telefon → kod → ad soyad + parola → KVKK → Hoş geldiniz. Kayıtlı müşteri: "Parolamı unuttum · SMS koduyla gir".
- tests/web-flows.py SMS kodu + parola adımlarıyla güncellendi; yanlış kod ve uyuşmayan parola uyarıları denendi. Tüm tarayıcı testleri geçti.

### 2026-10-22 - Senaryo: uygulamadan başlayan akış

- Senaryo 1 artık uygulamadan başlıyor (18 adım): SMS koduyla kayıt, parola, Hoş geldiniz, Randevularım'dan temsilci isteme, saat onayı Randevularım'da, hazırlık penceresi, kapıda QR, özet. Web'den başlayan akış Senaryo 2 olarak duruyor.
- Ekranlar uygulamanın güncel görünümüne uyduruldu (logo yok, Geri, yeni sekme adları, puan isteğe bağlı). Bilgilendirme formu adımı "öneri" olarak işaretli.

### 2026-10-23 - Tanıtım videosu (içeride izlenecek)

- `video/tasarruf-yanimda-tanitim.mp4`: 16:9, sessiz, ekran yazılı, yaklaşık 2 dk 14 sn. Bölümler: Neden? (temas tek yönlü) · Nasıl çalışır? (Senaryo 1 ekranları, müşteri telefonu + SPY tableti) · Nasıl ilerleyeceğiz? (aktif SPY'ler, dört aşama, "ölçerek göstereceğiz").
- Kaynak `video/tanitim.html` (tarayıcıda oynar; metinler `B` dizisinde), üretim `python video/kaydet.py` (imageio-ffmpeg gerekir). Ekranlar `video/kareler/` (senaryo.html'den). Bilgilendirme formu (öneri) videoda gösterilmez; tablet hazırlık kartı gizlendi.
- senaryo.html: Senaryo 1 adım 9 "Yeni talep" ekranında müşteri kartı yerine kod görünüyordu, düzeltildi.
- linkler.html alt satırına "Tanıtım videosu" eklendi.

### 2026-10-23 - Tanıtım videosu v2

- Kullanıcı geri bildirimiyle yeniden kurgulandı: daha hızlı (~1 dk 44 sn), proje tanıtımı havası (açık zemin, bölüm etiketleri), satış cümleleri ve "vaat etmiyoruz" sahnesi çıktı, "SPY'ler".
- Yeni açılış: İstanbul haritası, hizmet bölgeleri ve ilçe balonları, Ataşehir'e yakınlaşma, SPY'nin işyeri kapılarını tek tek ziyaret ettiği sokak çizimi. Cumartesi takvimi, Finansman Aracı (uygulama ekranları) ve tablette ön bilgi eklendi; yol haritası şeması + genişleyen hizmet alanı; kapanışta çift yönlü temas ve SPY kaynağının önceliklendirilmesi.
- senaryo.html Senaryo 1'e "SPY ön bilgiyi görür" adımı eklendi (telefonda Finansmanlarım, tablette ÖN BİLGİ kartı); 19 adım.

### 2026-10-24 - Tanıtım videosu v8

- Sorun ve Çözüm girişi düz ikon yerine aynı izometrik mahallede kamera hareketli anlar; yeni karakter Müşteri (lacivert). Mahallede ağaç sallanması, bulut gölgesi; açılışta arkada soluk mahalle.
- Telefon + tablet: kamera etkin cihazın vurgulu yerine yakınlaşır (yazılar okunur), ekranlar kayarak değişir, talep telefondan tablete bildirim kartı olarak uçar, cihaz etiketleri alt bantta.
- Yol haritası: harita baştan, simgeli "İzlenecek" kartları, ilçeler dalga gibi; Sultanbeyli/Pendik etiket çakışması giderildi. Öncelik sahnesinde kişiler başlıkların üstünden geçmiyor. Kapanış kartları birleşip logoya dönüyor.
- Bölüm kartlarında ve köşe etiketlerinde numara yok (kullanıcı isteği). 50 kare/sn, kayıpsız kare; seslendirme ve altyazı değişmedi. Önce/sonra sayfası: `video/v8-karsilastirma/`.

### 2026-10-24 - Tanıtım videosu v9

- Kapı kapı ziyaretlerde olumsuz sonuçlar da var (kırmızı çarpı); çağrıya giden SPY'nin ziyaretleri hep olumlu. Yayalar SPY/müşteriyle aynı boy.
- İşleyiş yavaşladı (bölüm sonlarında bekleme, Talep 4 ekran, yavaş kaydırma/kamera); finansman bütçe ekranı canlı (peşinat ve vade değişir, aylık ödeme sayar).
- Seslendirme: "Yani", "Peki" çıktı; "talep" yerine "çağrı"; son cümle "Önceliği bizi çağırana vermek, saha gücümüzü doğru yere yönlendirmeyi kolaylaştırır."
- Son bölüm şemaları: ok etiketleri, Yan kazanç hapları, öncelikte dağılımın değişmesi (3/5 → 4/4), kapanış kartlarında ikinci satır. Süre ~2 dk.

## 2026-10-26 · Tanıtım videosu v10 + pilot bölgesiz yan video
- Seslendirme ve altyazıda SPY yerine "Saha Portföy Yöneticileri"; "kanal ise yok" → "kanal yok"; "İlk adımı müşteri de atabilse?" → "Bu kez ilk adımı müşteri atıyor."
- İşleyiş bölümünde ekranlara yakınlaşma azaltıldı.
- Yan video: yol haritası (pilot bölge) bölümü yok; `python video/kaydet.py --yan`.

## 2026-10-30 · Tanıtım videosu v11: animasyon kalitesi (motion-design skill denetimi)
- Yürüyüş: ayak kayması giderildi (adım yola bağlı), dizli bacak, iki kol, kalkış/duruşta yumuşak adım.
- Sahne geçişleri boş zemine düşmüyor (çapraz geçiş; bölüm kartı sahnenin üstüne kayıyor).
- Kamera yakınlaşması oranla, eşit hızda.
- Kayıt: BT.709 renk etiketi (telefonda marka renkleri doğru), CRF 18, müzik konuşmada kısılıyor, ses -16 LUFS.
- Seslendirme metni ve ses aynı. Gemini TTS (ücretsiz) araştırıldı, ertelendi.
