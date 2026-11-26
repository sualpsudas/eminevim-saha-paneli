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


## 2026-10-31 · Tanıtım videosu ses düzeltmesi
- v11'de sessiz kapanışta (son ~7 sn) ses yoktu: müziği konuşmada kısan sidechain, konuşma bitince müziği de kesiyordu. Düzeltildi (apad); iki videonun yalnız sesi yeniden kuruldu (`kaydet.py --ses`). linkler.html `?v=12` / kısa `?v=3`.

## 2026-11-04 · İş planı ve görev dağılımı yenilendi
- Kullanıcı onayladı: 4 aşama + isteğe bağlı Sunum, 43 iş. Genel plan ve 4 kişi için görev PDF'leri OneDrive'da; görev takip listesi güncel.
- Takip sayfası yayına alındı; bağlantı ekibe WhatsApp'tan verilir.

## 2026-11-05
- Tanıtım videosunun ElevenLabs sesli iki sürümü yayında: kadın (Nazlı Yeni) ve erkek (Ahmet). Eski video ve pilot bölgesiz sürüm değişmedi. Ayrıntı `video/OKUBENI.md`.
- Belgelerde ortak dil uygulandı: çağrı, SPY, aktif SPY'ler, teşvik, pilot bölge denemesi. 08'de seçilen yönle çelişen nöbet düzeni ve sıralı dağıtım çıkarıldı. Proje Çerçevesi Taslak 0.7. Uygulama, web formu, senaryo ve video sonraya bırakıldı (`CLAUDE.md` → Açık işler).

## 2026-11-10 / 11 · Test sürümü: canlı merkez, 4 SPY, ortak dil
- **Merkez sunucusu** (`merkez/sunucu.py`, sunucuda 8794, Başlangıç kısayolu "Tasarruf Yanimda Merkezi"): müşteri çağrısı, SPY kayıtları ve
  mesajlar tek yerde; cihazlar 2,5 sn'de bir yalnız değişenleri alır. Merkezden açılan uygulama "canlı", GitHub Pages kopyası gösteri olarak kalır.
- **4 SPY** (sentetik fotoğraflı, sabit test konumlu): Onur Kaya (Ataşehir), Derya Aksoy (Üsküdar), Berk Cengiz (Ümraniye), Selin Arslan (Üsküdar).
  Personel girişinde isimle seçilir; telefon ve tablet düzeni ikisi de çalışır.
- **Geçici atama:** haritada seçilen konuma en yakın, molada olmayan SPY (eşitlikte açık çağrısı az olan). Bildirim uygulama açıkken sesli +
  titreşimli + ekranda; kapalıyken bildirim (push) sonraki adım. Takip sayfasından elle aktarılabilir. Rota/atama yöntemi sonra konuşulacak.
- **Canlı takip sayfası** (`<merkez>/takip`): SPY kartları, harita, çağrı tablosu (aktar), mesajlar, son olaylar, test verisini sıfırla.
- **Ortak dil uygulamada ve HTML'lerde:** temsilci → SPY, talep → çağrı (müşteri çağrısı anlamında; destek/düzeltme/randevu talebi aynı kaldı),
  ASK → Alternatif Satış Kanalı Müdürü. Uygulama, senaryo, web formu, rota/konum/harita, taslaklar, URUN_KURALLARI. Video ve altyazılar değişmedi.
- **Aynı gün çağrısı:** uygulama ve web formu takvimi bugünü de gösterir (saat 19'dan önce; geçmiş ve bir saat içindeki saatler kapalı).
- iPhone: `scripts/merkez-adresi.mjs` Codemagic'teki `TY_MERKEZ_URL` değişkeniyle uygulamayı merkez sayfasına bağlar (adres depoya yazılmaz).
- Testler: `tests/merkez-akis.py` (yeni, deneme merkezi 8795) + eski Playwright testleri ve node testleri geçti.

## 2026-11-11 · 30 SPY, atama kuralları, ortak dil düzeltmesi, yönetici ve web formu merkeze bağlı
- **30 SPY** (`spyler.js`; uygulama ve merkez ortak): pilot bölge Üsküdar / Ümraniye / Ataşehir, her biri farklı mahallede, sentetik fotoğraflı;
  uydurma son 3 ay randevu ve ciro H/G → 22 aktif (ikisi de ≥ %100). s1-s4 video kişileri, bilgileri aynı.
- **Atama** (rapor 10): eleme (aktif, molada değil, günlük 4, aynı gün uygulaması açık / ileri tarih ±90 dk boş) + puan (aynı gün yakınlık
  ağırlıklı, ileri tarih H/G ağırlıklı); teklif 2 dk, süre dolunca ya da Devret'te sıradaki; 3 ret → yöneticiye düşer; yönetici atar.
- **Ortak dil düzeltmesi (kullanıcı):** müşteri ekranları, web formu, SMS, senaryo ve taslaklardaki müşteri ekranları yeniden **"temsilci"**;
  personel/yönetici/takip ve iç belgeler "SPY"; her yerde "çağrı".
- **Giriş:** müşteri girişi aynı; Personel Girişi'nde SPY açılır listeden (fotoğraflı önizleme) + tek **Yönetici** (hepsini görür).
  TL / SGL / Alternatif Satış Kanalı Müdürü ayrı girişleri kalktı.
- **SPY ekranı:** kabul için kalan süre, "Neden size geldi"; Performans son 3 ay randevu + ciro H/G, aktiflik, sıra, bugünkü çağrı, kabul.
- **Yönetici:** Saha Canlı = takip sayfası (uygulama içinde); Performans 30 SPY H/G sıralaması + süzgeç. Eski OrgData aylık ciro ekranları kapalı.
- **Takip sayfası** yeniden: yöneticiye düşenler (SPY seç + Ata), kalan süre, puan, gerekçe, 30 SPY süzgeç/arama, telefona uyumlu.
- **Web formu** merkezden açılınca çağrıyı merkeze gönderir; giriş kodunu merkez verir; uygulamada kodla aynı çağrı açılır.
- Düzeltmeler: yöneticiye düşen çağrıyı atarken sunucu hatası; web formu kopyasındaki `<base>` etiketi yüzünden merkez adresi yanlış çözülüyordu.
- Testler: `tests/merkez-akis.py` yeniden yazıldı (30 SPY, aynı gün, geri sayım, molada, ileri tarih, 3 ret, yönetici, web kodu) — tüm testler geçti.
- Ek (aynı gün): yönetici destek talepleri ayrı **Destek** sekmesine taşındı (her sekmenin üstünde duruyordu); SPY çağrı kartında kaynak
  doğru yazıyor (uygulamadan gelen çağrı "Uygulama", web formu "Web formu"); kapalı eski performans şablonu silindi; `sw.js` önbelleğine `spyler.js`.

## 2026-11-11 (2) · 7 SPY, yeni atama puanı, Saha Canlı haritası, kompakt performans, destek kalktı, hazırlık uygulamada, web sonuç ekranı
Kullanıcıyla konuşulup onaylanan plan ("onaylandı").
- **7 SPY** (Onur Kaya, Derya Aksoy, Berk Cengiz, Selin Arslan, Ece Yalçın, Burcu Avcı, Barış Çelik); "aktif değil" kavramı yok — uygulamada
  yalnız iki H/G'si ≥ %100 olanlar. Kullanılmayan 23 sentetik fotoğraf `assets/temsilci`'de duruyor.
- **Atama:** hemen çağrı (bugün, en geç 2 saat sonrası) → elenir: molada, uygulaması kapalı, yolda/görüşmede, günlük 4 dolu; puan yakınlık 50,
  H/G 30, bugünkü çağrı 20. İleri saat/gün → elenir: ±90 dk çakışma, gün dolu; puan H/G 50, yakınlık 30, o günkü çağrı 20. 2 dk kabul
  edilmezse ya da Devret'te sıradakine; kimse kalmazsa "kimse almadı" (haritada kırmızı), uygun SPY çıkınca kendiliğinden teklif.
  Yöneticiye düşme, Ata ve Aktar kalktı.
- **Saha Canlı** (uygulama + bilgisayar takip sayfası aynı): bugün Gelen Çağrı / Görüşme Sayısı, süzgeç Tümü/Boşta/Randevuda/Molada,
  pilot ilçe + mahalle sınırları ve adları (`assets/pilot-sinirlar.js`, OpenStreetMap), küçük renkli simgeler, kırmızı sahipsiz çağrı.
  Altlık CARTO → OpenStreetMap (CARTO anahtar istiyordu, "API KEY REQUIRED" yazıyordu). Pages gösterisi örnek veriyle (`takip.html?demo=1`).
- **Performans (yönetici):** kompakt liste — sıra, ad, ort. randevu H/G, ort. ciro H/G; iki oranın ortalamasına göre.
- **Destek** yönetici, müşteri ve testlerden kaldırıldı.
- **Görüşmeye hazırlık** yalnız uygulamada: çalışma durumu, yaş aralığı, "Ne için düşünüyorsunuz?", kısa not; web'den gelen müşterinin ilk
  girişinde (tanıtım bitince) ve saat onayında; "Şimdi değil" → Randevum'da kart. SPY çağrı ayrıntısında görür.
- **Web sonuç ekranı:** "Sayın Ad Soyad, temsilci çağrınız alındı!", özet, SMS satırı + Kapat'a kadar duran SMS penceresi, kısa uygulama
  kartı; bölge dışı "Sayın Ad Soyad, çağrınız alındı!" + turuncu not. "Başarılı!", uzun cümleler, hazırlık bölümü, "Yeni başvuru" kalktı.
  Senaryo (yalnız destek ve hazırlık) ve web akışı taslağı da güncellendi; video değişmedi.
- **Düzeltmeler:** merkezin atama puanı müşteri yıldız puanıyla aynı alandaydı (`puan`) → web'den gelen müşteride uygulama hata veriyordu ve
  müşteri puanı merkeze kaydedilmiyordu; alan `atamaPuan` oldu. Tanıtım penceresi ile hazırlık penceresi üst üste açılıyordu → hazırlık tanıtımdan sonra.
- Testler: `merkez-akis.py` yeni kurallara göre yeniden yazıldı (7 SPY, hemen/ileri, devret → kimse almadı, harita + süzgeç, kompakt performans,
  SMS penceresi, hazırlık); `web-flows`, `browser-flows`, `preparation-popup`, `appointment.test.js` güncellendi. Tümü geçti.


## 2026-11-11 (3) · Uygulama kapalıyken bildirim (Web Push)
Kullanıcı onaylı plan: hemen çağrıda uygulamanın açık olması şartı kalktı; yeni çağrı bildirim olarak gider.
- Bir telefon tek SPY'ye bağlı (başka SPY seçilince bağ geçer, Çıkış yapınca kalkar); aynı SPY birden çok telefonda seçilebilir, bildirim hepsine gider.
- Merkez: `api/anahtar`, `api/abone`, `api/abone-sil`; Google/Apple servisi "artık yok" (404/410) derse abonelik silinir. Bağımlılık `pywebpush` (conda base).
  Anahtar `merkez/vapid.pem` ve abonelikler yalnız sunucuda. Servis çalışanı `merkez/canli-sw.js`.
- Uygulama: girişte izin (dokununca), Profil'de "Bildirimler" kartı ve "Bildirimleri aç". Takip sayfasında SPY başına bildirimi açık telefon sayısı.
- iPhone: Safari'de Ana Ekrana Ekle ile çalışır; TestFlight uygulaması (Build 1, 2026-10-05 var) için APNs ayrı adım.
- Doğrulama: gerçek Chrome + Google bildirim servisiyle abonelik → çağrı → bildirim gösterildi (gönderim "ok"). Bu deneme Google'ın yanıt süresine
  bağlı ve kararsız olduğundan kalıcı teste konmadı (personel girişi ileride yalnız telefondan olacak — kullanıcı). `merkez-akis.py` sahte bildirim
  sunucusuyla: iki telefona gönderim, telefon değişimi, 410 temizliği, imza/şifreleme başlıkları. Tüm testler geçti.
- Funnel açıldı (kullanıcı isteğiyle). Telefonda sayfa yarım yükleniyordu (aynı anda ~20 dosya, merkezin bekleme sırası 5 → Funnel 502); sıra 128 yapıldı.

## 2026-11-11 (4) · Paket 2: uygulama ekranlarında ortak görünüm
- Müşteri ve personel ekranlarında düğme ölçüleri, başlık hiyerarşisi ve ilgili kartların iç boşlukları eşitlendi. Yönetici ad ve rolü aynıysa üst çubukta tek satır gösteriliyor.
- Renkler, web formu ve senaryo değişmedi.

## 2026-11-11 (5) · Web konum onayı ve tek müşteri girişi
- Web temsilci çağrısında uygulamayla aynı açık rıza cümlesi ayrı bir kutuda gösteriliyor; merkez onay tarihini kaydediyor.
- Telefon numarasından sonra kayıtlı müşteriye parola, yeni müşteriye test kodu ve KVKK adımları açılıyor. Parola yenileme ve web çağrısına kodla geçiş korundu.
- Senaryo ve uygulama taslağında yalnız giriş ekranı güncellendi. “Temsilciniz yolda” üst başlığı metin göründüğü sürece Randevularım’a dönüyor.
- Web konum onayı cümlesi amacı kendi içinde söylüyor ("yukarıda belirtilen" web'de boşta kalıyordu). Merkez: Windows'ta dosya o an açıkken kaydetme "erişim engellendi" verebiliyordu (testte görüldü) → kısa aralıklarla yeniden dener.

## 2026-11-11 (6) · Müşteri hesabı merkezde
- Merkez müşteri hesaplarını tutuyor (telefon, ad soyad, KVKK onay tarihi, web'den geldiyse konum onay tarihi; parola yalnız özet olarak).
  Aynı numara + parola her telefonda çalışıyor; başka telefonda girişte çağrılar Randevularım'a geliyor. 5 yanlış parola → 5 dk kilit.
- SMS test kodunu artık merkez üretiyor ve doğruluyor (ekranda gösterilmesi aynı). Pages gösterisi eski davranışla kaldı.
- `merkez-akis.py`: A telefonunda kayıt → B telefonunda parolayla giriş, yanlış parola, kilit, kayıtsız numara, web müşterisinin başka telefonda girişi.

## 2026-11-11 (7) · Müşteriye bildirim
- Uygulama kapalıyken müşteriye: temsilci belli oldu (ad · saat), temsilci yola çıktı (tahmini varış), temsilcinin mesajı. Dokununca o randevu açılır.
- Girişten sonra Randevularım'da "Bildirimleri açın" kartı, Ayarlar'da Bildirimler kartı. Abonelik girişte merkezin verdiği jetonla (başkası adına abone olunamaz).
- Kabul ve yola çıkışta giden hazır temsilci mesajı ikinci bir bildirim üretmiyor. Test: `merkez-akis.py` (sahte bildirim sunucusu).

## 2026-11-11 (8) · Sıfırlama telefona yansır, oturum kalıcı, sade yazılar
- Test verisini sıfırlama artık telefondaki uygulamayı da sıfırlıyor (o sırada kapalı olsa bile açılınca); müşteri giriş ekranına döner.
- Yeni sürüm yüklenince "Yeni sürüm hazır · Yenile" şeridi; ana ekran uygulamasında aşağı çekip yenileme.
- Müşteri oturumu "Çıkış yap"a kadar açık kalıyor (telefonda parola değil, merkezin oturum anahtarı).
- Kaldırılan yazılar: "Emin olmak, güven demek", "Neden size geldi", SPY çağrısındaki açıklama notları (yalnız "Kabul için kalan süre" kaldı),
  "Şirket ortalamasına göre", performans ve harita açıklamaları, Randevularım / Randevu al / kapanış alt açıklamaları.
- Test: `merkez-akis.py` (sıfırlama, sürüm şeridi, yeniden açınca girişli kalma, çıkış sonrası eski oturum reddi) + diğer 7 test.

## 2026-11-12 · Finansman seçimi, demo/koyu mod kalktı, telefonda dokunma hissi
- Finansman kendiliğinden seçilmiyor: tutar/plan/peşinat/vade boş başlar, kaydedilen ✓ almaz; müşteri dokunarak seçer.
- Demo modu (otomatik kabul) ve koyu tema kaldırıldı. Temsilci iste penceresindeki lacivert üst şerit telefonda yok.
- `improve-ui` incelemesi: Randevularım tablosu köşesi 14px'e çekildi (kart kuralı). Eklenenler: basma hissi, liste ↔ ayrıntı kayması,
  hafif kart gölgesi, eşit genişlikte rakamlar.
- Test: `phone-layout.py` (finansman seçimsiz başlar + kayıt ✓ almaz, demo/koyu düğmesi yok, şerit gizli) + diğer 7 test.

## 2026-11-12 · Personel paneli kozmetik düzen (AGENTS.md G)
- Kaynak: `design-plans/personel-panel-inceleme-2026-11-12.md`; yalnız boyut, ton, hiza, seçili görünüm (akış/veri aynı).
- SPY Performans: H/G yüzdeleri büyük (28/24 px), çubukta %100 hedef çizgisi + "%100 hedef" etiketi, sıra/çağrı rakamları koyu nötr (payda soluk).
  İçerik başlıkla aynı hizada (iç içe boşluk kalktı), en fazla 880 px.
- Yönetici Performans: sütunlar geniş, başlık kırılmıyor, yüzde 15 px; %100'ün üstü yeşil, tam %100 koyu nötr; Ekip ortalaması satırı belirgin.
- Personel alt menü: etiketler daha koyu (#767676, 12 px), seçili sekmede üstte yeşil çizgi.
- Saha Canlı (`merkez/takip.html` + başlık): sayaçlar koyu, "Mesai dışında: örnek olarak … durumu" açık kehribar etiket,
  seçili süzgeç açık yeşil + yeşil çerçeve, uygulama içinde harita kısa (masaüstü ≤460 px, telefon 300 px) → kişi kartları ilk ekranda.
- Görüşmeler/Profil: süzgeç ve Müsait/Molada seçili görünümü ortak (açık yeşil + yeşil çerçeve; Müsaitlik'te ✓), telefonda 44 px;
  sayaçlar nötr; "Rotayı kapat" açıkken açık yeşil; Çıkış yap gri çerçeve, koyu yazı.
- Yapılmadı: E/F (onay bekliyor), harita altlığı, Inter/yeni palet, Personel Girişi çerçevesi (linkler önizlemesi), animasyon.
- Test: 6 tarayıcı testi (`merkez-akis.py` 8795 deneme sunucusunda) + 2 node testi geçti.
- Ek (aynı gün, kullanıcı): "Çağrı size nasıl gelir?" kartı kaldırıldı (AGENTS E). Sekme başlıkları dar tek satır, alt yazılar
  ("Tüm SPY'ler · pilot bölge", bölge, tarih) kalktı; Saha Canlı'da mesai dışında yalnız "Örnek: 11 Kasım 15:30" etiketi. Testler yine geçti.

## 2026-11-12 · Saha Canlı telefonda Harita | Liste
- Telefonda sayfa artık kaymıyor (iç içe kaydırma kalktı): süzgeçlerin altında Harita | Liste seçimi; harita kalan ekranı doldurur,
  liste yalnız kendi içinde kayar. Simgeler 32 px; dokununca alttan kişi kartı (✕). Listeden kişi → haritada açılır.
- Liste sırası: kimse almayan çağrılar (kırmızı, Tümü'nde) → Randevuda → Molada → Boşta. Süzgeçler telefonda tek satır.
- Uygulamadaki Saha Canlı çerçevesi her ekranda tam oturuyor (bilgisayarda da dış kaydırma kalktı).
- Kalabalık ekip için yapılacaklar AGENTS.md H'ye yazıldı (simge toplama, arama, takım kapsamı, performans süzgeci, yöneticiye bildirim).
- Test: `phone-layout.py`'ye Saha Canlı telefon kontrolü eklendi; tüm testler geçti.

## 2026-11-12 — Tema standardı (müşteri = personel düzeni)
- Müşteri üst bandı personelinki gibi: düz yeşil bant, solda logo (Geri varsa önünde), sağda durum yazısı + baş harf düğmesi (Ayarlar'a gider). Eski yuvarlak köşeli "Tasarruf Yanımda" başlığı kalktı.
- Müşteri alt menüsü: 52 px, 12 px etiket, #767676 pasif, seçili sekmede üstte 2 px yeşil çizgi (`aria-current`).
- Kök sekmelerde (Randevularım, Sohbetler, Finansmanlarım, Ayarlar) personeldeki gibi beyaz sayfa başlığı bandı (`.tp-bas`); gövdedeki eski başlıklar kaldırıldı. Ayrıntı ekranlarında bant yok.
- Yönetici/SPY zaten personel düzeninde. Sırada: örnek müşteriler, Görüşmeler sayfa akışı + bildirim, tablo/harita/rota.
- Bilinen: Finansman kök listesinde "Geri" görünüyor (eski davranış, değişmedi).
- Test: phone-layout.py ve browser-flows.py geçti.

## 2026-11-12 — Örnek müşteriler, rastgele yeni üye, Finansman'da Geri
- 5 örnek müşteri kayıtlı (Ayşe Kaya, Zeynep Arslan, Can Öztürk, Elif Yıldız, Burak Şahin); parola `test123`; hiçbirinde finansman yok (Ayşe'nin eski Konut Finansmanı kaydı ve metinleri silindi). Ayşe'nin "yolda" randevusu duruyor, diğerleri boş başlar.
- Giriş ekranında "Örnek müşteriler" düğmeleri ve "Yeni üye: örnek numara getir". Yeni üye adımında ad ve parola rastgele dolu gelir (parola ekranda gösterilir); SMS kodu zaten otomatik.
- Finansman kök listesinde ve 1. adımda Geri yok; yalnız adım içinde/düzenlemede.
- URUN_KURALLARI'ndaki eski "müşteri başlığında logo yok, simetrik" kuralı güncellendi. `senaryo.html` müşteri ekranını taklit ediyor, henüz güncellenmedi (açık iş).
- Testler: appointment-list, phone-layout (liste için kayıt ekler), browser-flows, web-flows, preparation-popup geçti.

## 2026-11-12 (akşam) — Örnek müşteri açılır kutusu, personel girişinde Müşteri Girişi
- Giriş ekranında örnek müşteriler çip yerine açılır kutu (Ayşe, Zeynep, Can, Elif, Burak + "Yeni üye (örnek bilgilerle)"). Tek seçim: örnek müşteri seçiliyken parola ekranına gider, kayıt ekranına değil; "Yeni üye" seçilince rastgele kayıtsız numara gelir. Telefon elle değişirse seçim ona göre güncellenir.
- Personel Girişi ekranında sağ üstte "Müşteri Girişi" (sol üstte Geri); ikisi telefon çerçevesinin içinde.

## 2026-11-12 (gece) — "Hesabınızı oluşturun" sorunu (canlı merkez)
- Neden: merkez sürümünde (CANLI) hesaplar merkezde tutulur; yalnız Ayşe merkezde kayıtlıydı, diğer örnek müşteriler "kayıtlı değil" sayılıp kayıt ekranına düşüyordu.
- Çözüm: `merkez/sunucu.py` açılışta/okumada 5 örnek müşteriyi (parola test123) ekler (`ORNEK_MUSTERILER`); uygulamadaki liste ile aynı olmalı. Servis yeniden başlatıldı.
- Burak Şahin'in numarası 0543 650 78 90 oldu (önceki numara merkezde gerçek bir test hesabına — Emre Güneş — aitti).

## 2026-11-12 (gece) — Görüşmeler: sayfa akışı ve bildirimden görüşmeye gitme
- Dar ekranda (<900 px) Görüşmeler iki sayfa gibi: liste → bir görüşmeye dokununca yalnız ayrıntı açılır, başlıkta "Geri" listeye döner. Tablet/geniş ekranda liste solda, ayrıntı sağda aynen kaldı (Geri görünmez).
- Yeni çağrı gelince ayrıntı kendiliğinden açılmaz (liste "Yeni çağrılar" grubunda, tarih sırasıyla görünür).
- SPY bildirimi (uygulama içi, yeni çağrı ve yeni mesaj) dokununca o görüşmenin sayfasını açar. Tarayıcı/telefon bildirimi de: `merkez/sunucu.py` SPY bildirimine `rid` ekledi; uygulama kapalıysa `?ac=<id>` ile açılır, açıksa servis işçisi mesajla görüşmeyi seçer; SPY girişi yoksa girişten sonra açılır.

## 2026-11-12 (gece) — Personel girişi, yönetici Performans tablosu, sade Saha Canlı
- Personel girişinde "Hesabınızı seçerek giriş yapın" satırı kalktı; seçilen SPY büyük fotoğraflı (132 px) ortalı kartla görünür.
- Yönetici Performans: sabit başlık (İsim, Şube, Rand H/G, Ciro H/G), ince satırlı tablo, yalnız satırlar kayar, altta Ekip ortalaması.
- Saha Canlı: liste ve Harita/Liste düğmesi kalktı; sayı kartları küçüldü; SPY ve "kimse almadı" işaretleri insan simgesiz küçük nokta; altlık OpenStreetMap, gri tonlu (CARTO anahtar istediği için başka sade altlık eklenmedi).
- Testler: `phone-layout` (liste yerine nokta kontrolü), `merkez-akis` (bildirime dokunarak görüşme açma, yeni tablo) güncellendi.

## 2026-11-12 (gece) — Geri konumu, giriş ekranları standardı, yönetici test sıfırlama
- Müşteri sayfalarında Geri üst yeşil banttan başlık bandına (personeldeki gibi) taşındı; Geri çıkınca/gelince EMİNEVİM logosu kaymaz. Bant, Geri olan sayfalarda da görünür (başlıklar: Randevu, Sohbet, Finansman).
- Müşteri ve personel girişinde sol üst Geri kalktı. Müşteri girişinde adımlar arası dönüş formun altında "Geri dön" bağlantısı; personelde sağ üstte "Müşteri Girişi".
- İki giriş ekranı aynı ölçüde: logo 150 px, başlık 18 px, yan boşluk 30 px, sağ üst bağlantı aynı yükseklik (personel ekranı müşteri girişinin çerçeve kurallarına bağlandı).
- Yönetici Profil sayfasına "Test verisini sıfırla" (canlıda merkeze api/sifirla, gösteride yerel temizlik; onay sorar).

## 2026-11-12 (gece) — Personel girişi yeniden düzenlendi
- Sıra: EMİNEVİM, Personel Girişi, fotoğraf (kartsız, 132 px), açılır kutu, Giriş yap. "SPY" ve "YÖNETİCİ" etiketleri ve Yönetici düğmesi kalktı; Yönetici açılır kutunun son seçeneği (seçilince kutu soft sarı, fotoğraf yerinde "Y" dairesi).
- Müşteri ve personel giriş ekranlarında içerik üstten sabit (logo/başlık aynı yükseklikte).

## 2026-11-12 (gece) — Yola çık: gerçek yol rotası
- `rota.html` `yol=1` ile OSRM genel sunucusundan gerçek yol rotasını çizer (yeşil, kalın) ve altta "N dk · X km" rozeti gösterir; alınamazsa eski kesikli düz çizgi kalır. `e=` ile etiket (müşteride "Temsilciniz", SPY'de "Siz").
- SPY "Yola çık" deyince görüşme sayfasında rota kartı açılır. Müşterinin "Temsilcinizi takip edin" haritası aynı rotayı gösterir.
- Tahmini varış gerçek yol süresiyle güncellenir (`yolSuresiGuncelle`; müşteri ekranındaki "Tahmini varış" da buna uyar).
- Sınır (prototip): OSRM genel sunucusu ticari kullanıma uygun değil, kullanım sınırı var; gerçek yayında ücretli/kendi yönlendirme servisi gerekir. SPY'nin canlı GPS'i yok: rota SPY'nin kayıtlı konumundan çizilir, hareket etmez.

## 2026-11-13 — Yönetici oturumu cihazda kalır
- Merkez (canlı) sürümde yönetici girişi de SPY ve müşteri gibi cihazda kalır (`ty-yonetici`); Çıkış yap'a kadar uygulama yeniden açılınca giriş sorulmaz. GitHub Pages gösterisi (merkezsiz) oturum tutmaz.

## 2026-11-18 — Modüler yapı (IT'ye devir öncesi)
- Uygulama yardımcıları `Eminevim Saha Paneli.dc.html`'den `uygulama/` modüllerine çıkarıldı (servisler, ayarlar, bicim, finansman, personel, hesap, ornek-veri); `support.js`, `canli.js`, `appointment.js`, `assignment.js` da `uygulama/`ya; harita sayfaları `harita/`ya; `org-data.js` ve `spyler.js` `veri/`ye.
- SPY listesi artık üretiliyor: `veri/kaynak/*.csv` (şirket sütun adları, uydurma değerler) + `veri/ayarlar.json` → `araclar/veri_hazirla.py` → `veri/spyler.js` + `hg_ozet.json`. Eski 7 SPY aynen çıktı, 6 kişi H/G < %100 nedeniyle dışarıda.
- Merkez `merkez/ty/` paketine bölündü (ayarlar, yardim, personel, depo, konum, atama, bildirim, musteri, aktarim, islemler, api); `sunucu.py` ince giriş, komutlar aynı. Yeni: `api/konum` (canlı konum girişi), şirkete aktarım `merkez/aktarim/*.jsonl` (randevu + aday müşteri kartı, şirket sütun adlarıyla).
- Belgeler: `IT_DEVIR.md` (yeni), `veri/OKUBENI.md` (yeni), CLAUDE.md, AGENTS.md, TEKNIK.md, KARARLAR.md, assets/temsilci/OKUBENI.md.
- Testler: `npm test` OK; `tests/merkez-akis.py` (deneme merkezi 8795) OK; Playwright browser-flows, phone-layout, web-flows, appointment-list, preparation-popup OK; `npm run web:sync` → `www/` hatasız açılıyor.

## 2026-11-18 (2) — Parolasız giriş ve KVKK düzeni
- Kullanıcı onayı: "önerilerinle ilerle, parola kalkabilir, ad soyad ayrı kutu olabilir".
- Uygulama: telefon → SMS kodu → kayıtlıysa içeri; yeni müşteri Ad + Soyad (ayrı kutu), aydınlatma bilgisi + "Aydınlatma Metni" penceresi,
  isteğe bağlı işaretsiz ticari ileti kutusu. Parola, "Parolamı unuttum", ayrı KVKK ekranı ve eski "Kayıt Ol" penceresi kalktı.
- Merkez `ty/musteri.py`: islem kod/dogrula/kayit/web/oturum/cikis; hesapta adi, soyadi, aydinlatmaTarih, kampanya. Aktarım müşteri kartı
  Adı/Soyadı'nı hesaptan alır, "Ticari İleti İzni" alanı eklendi.
- Web formu: kabul kutusu ve konum rıza kutusu kalktı; bilgi satırı + Aydınlatma Metni penceresi; çağrıya aydinlatma/kampanya, bağlantıya
  adi/soyad/kampanya. `olustur.py` ile yeniden üretildi.
- Belgeler: URUN_KURALLARI, TEKNIK, IT_DEVIR (tek hesap, KVKK, yurt dışı harita servisleri), KARARLAR, AGENTS. sw CACHE v20.
- Testler (hepsi OK): browser-flows, web-flows, appointment-list, phone-layout, preparation-popup, merkez-akis (deneme merkez 8795), npm test.

## 2026-11-18 (3) — Panel (panel.html)
- Kullanıcı isteği: ana sayfada kutular (Proje Çerçevesi, Tanıtım Videosu, Senaryo 1, Senaryo 2); tıklayınca solda dar dikey menü,
  sıra Proje Çerçevesi → Tanıtım Videosu → Senaryo 1 (web formundan) → Senaryo 2 (uygulamadan). Web formu/uygulama panelden açılmaz.
- Senaryolar yeni (parolasız) girişe göre yazıldı. linkler.html'e "Panel" bağlantısı. Telefon (390) ve bilgisayar (1366) ekran denemesi OK.

## 2026-11-18 (4) — Panel senaryoları gerçek ekranlarla, kadın sesli video
- Neden: eski senaryo (`senaryo.html`) elle çizilmiş sabit ekranlardı, uygulama değiştikçe güncellenmemişti (parola, KVKK ekranı vb.).
- Yeni `araclar/senaryo_goruntu.py`: gerçek web formu + uygulama (gösteri) adım adım yürütülür, müşteri (393x852) ve SPY (1180x820)
  görüntüleri `senaryo/goruntu/` + `senaryo/adimlar.js`. Senaryo 1 web 15 adım, Senaryo 2 uygulama 16 adım.
- panel.html: Senaryo 1/2 iki bölmeli (solda müşteri, sağda SPY tablet), Geri/İleri, noktalar, ok tuşları; dar ekranda tek taraf +
  Müşteri/SPY düğmesi, dokununca tam boyut. Tanıtım Videosu'na "Kadın sesli" seçimi (`tasarruf-yanimda-tanitim-kadin.mp4?v=1`).
- linkler.html: "Senaryo" sekmesi kaldırıldı, eski `#senaryo-…` panele yönlenir. senaryo.html silinmedi (güncellenmez).
- Testler: yeni `tests/panel-senaryo.py` (1440 ve 393 genişlik) OK; appointment-list, phone-layout OK. Uygulama kodu değişmedi.


## 2026-11-18 (5) — Panel düzeltmeleri (kullanıcı geri bildirimi)
- Tanıtım Videosu: yalnız kadın sesli sürüm, sürüm seçimi ve "Sesi açarak izleyin" kalktı; başlık sadece "Tanıtım Videosu".
- Senaryo altındaki bilgi yazıları kaldırıldı.
- Telefon gerçekçi iPhone kasası: durum çubuğu (9:41, ada, sinyal/wifi/pil) ve ev çizgisi; renkleri görüntünün üst/alt satırından
  (`adimlar.js` ust/alt). Tablet koyu kasa. Cihaz boyu sahneye JS ile sığdırılır (ResizeObserver) → Geri/İleri bandı ekranı örtmez.
- KVKK adımları eklendi: Senaryo 1'de web formunun Aydınlatma Metni penceresi, Senaryo 2'de uygulamanınki (onay kutusu yok,
  ticari ileti izni isteğe bağlı/işaretsiz; betik bunu da denetler). Senaryo 1: 16, Senaryo 2: 17 adım.
- Test `tests/panel-senaryo.py`: 1440x900, 1280x640, 393x852, 390x664'te her adımda taşma denetimi OK.

### 2026-11-18 (6) Görüşmeye hazırlık: finansman türü kalktı, Finansman Aracı düğmesi geldi
- Kullanıcı isteği: kozmetik öneriler (taslak/kozmetik/*.jpg) uygulanmadı; yalnız bu değişiklik.
- Hazırlık penceresinden "Ne için düşünüyorsunuz?" (Konut/Araç/İşyeri/Henüz karar vermedim) kalktı; yerine "Finansman Aracı" düğmesi:
  girilenleri kaydeder, Finansman sekmesini açar (tür/tutar/vade orada; SPY'ye ön bilgi olarak gider). SPY detayında "Ne için" satırı da kalktı.
- Testler: preparation-popup (düğme → kaydet + Finansman), merkez-akis (çalışma durumu ile), browser-flows, appointment-list, phone-layout,
  web-flows, panel-senaryo OK. Senaryo görüntüleri yeniden üretildi.

### 2026-11-18 (7) KVKK Aydınlatma Metni yenilendi, izin geri alma, 18 yaş altı kalktı
- Eminevim'in kendi KVKK metni (eminevim.com/kvkk) ve Aydınlatma Yükümlülüğü Tebliği m.5 ile karşılaştırıldı. Eski örnek metinde eksik:
  Mersis/KEP/adres, veri kategorileri, amaç ↔ hukuki sebep eşleşmesi, toplama yöntemi, yurt dışı aktarım, Holding şirketlerine (ticari ileti)
  aktarım, saklama süresi, m.11'in tam listesi, başvuru yolları. Eminevim'in sitedeki metninden alınmayanlar: "izin vermeniz hâlinde
  paylaşırız" (hizmet sağlayıcı aktarımı rızaya bağlanmaz) ve "üçüncü kişinin ihlallerinden sorumlu değiliz" beyanı.
- Tek kaynak `uygulama/aydinlatma.js`; uygulama (giriş, Ayarlar → Kişisel verileriniz, hazırlık penceresi) ve web formu aynı metni gösterir.
  Web formunda `<base>` canlı siteyi gösterdiği için `olustur.py` dosyayı sayfaya gömer.
- Ayarlar: Aydınlatma Metni düğmesi + ticari ileti izni aç/kapat; merkezde `musteri_islem(izin)` (jetonla, tarihiyle, olay kaydı).
- Hazırlık penceresinde "18 yaş altı" seçeneği kalktı; altına aydınlatma bağlantısı eklendi.
- Testler: browser-flows, web-flows (Tebliğ başlıkları), preparation-popup, appointment-list, phone-layout, merkez-akis (izin geri alma,
  diğer telefonda da kapalı), panel-senaryo OK. Senaryo görüntüleri yeniden üretildi. Merkez yeniden başlatıldı.
- Açık (hukuk/uyum): saklama süreleri örnek; yurt dışı aktarım için standart sözleşme; İYS bağlantısı; "Hesabımı sil" kararı.

### 2026-11-18 (8) KVKK: müşteri tıklayarak onay veriyor
- Kullanıcı kararı: "amacımız onay alabiliyor olmak". Web formu ve uygulamada yeni hesap ekranında zorunlu kutu:
  "Aydınlatma Metni'ni okudum; kişisel verilerimin bu metinde anlatıldığı şekilde işleneceği konusunda bilgilendirildim." (açık rıza değil)
- İşaretlenmezse "Devam etmek için Aydınlatma Metni'ni okuduğunuzu onaylayın."; metin bağlantısı kutuyu işaretlemez. Merkez `aydinlatmaOnay`
  olmadan web çağrısı / yeni hesap kabul etmez; `aydinlatmaTarih` onay anı. Kampanya izni ayrı, isteğe bağlı, işaretsiz.
- Testler: browser-flows, web-flows, preparation-popup, appointment-list, phone-layout, merkez-akis, panel-senaryo OK. Senaryo görüntüleri yenilendi.

### 2026-11-19 Kapıda QR gerçek: kod merkezde, SPY kamerayla okur + hizalama kontrolü
- Kullanıcı: "iPhone'a geçmeden QR ve gerçek kod gerçekten çalışsın, navbar/hizalar kontrol edilsin" (SMS gerçek değil: a seçeneği, kod ekranda kalır).
- Yeni `merkez/ty/dogrulama.py` + `api/dogrulama`: müşteriye randevuya özel 4 haneli kod (10 dk, yalnız bellekte; SPY cihazına/veri dosyasına
  gitmez), SPY QR ya da kodla doğrular → merkez randevu/SPY/sürüm/süre kontrolü, 5 hatada iptal, `gorusmede`. `api/kayit` artık
  "gorusmede" yazamaz, eski kopya görüşmeyi geri alamaz. Uygulama: SPY tarayıcı ekranında gerçek arka kamera (BarcodeDetector / `vendor/jsQR.js`),
  izin yoksa "kodu elle girin"; başarı ekranında gerçek müşteri adı (eskiden sabit "Ayşe Kaya"). Örnek düğmeleri yalnız gösteride.
  iPhone Info.plist kamera izni metni; `sw.js` v22 (+jsQR).
- Hizalama: 320/393/430 telefon, iPad dikey/yatay, SPY/TL/yönetici. Düzeltilen: telefonda süzgeç çipleri tek satır (yana kayar, Saha Canlı ile aynı),
  iPad dikeyde üst çubukta ad/durum görünür (eskiden ≤899 px gizliydi), yönetici performans tablosunda ad/şube kesilmez.
  Sorun olmayan: sohbet ekranındaki soluk yazı yalnız geçiş animasyonu anında alınan görüntü.
- Testler: merkez-akis (sahte kamerayla gerçek QR okuma, kodun SPY'ye gitmemesi, ret durumları), browser-flows, appointment-list, phone-layout,
  preparation-popup, web-flows, panel-senaryo, node birim testleri: OK.

### 2026-11-19 Yeni Tasarruf Yanımda logosu: simge, açılış, giriş ekranı
- Kullanıcı logoyu ChatGPT ile Eminevim renklerine yaklaştırdı; ana yeşil elle #00724C'ye düzeltildi (kaynak: OneDrive Belgeler
  `Tasarruf Yanımda_ Ev ve Araba3_renk.png`). Kullanıcı: "simge olduğu gibi olmalı" → simgede logonun tamamı (ev + araba + yazı + telefon).
- Ana ekran simgesi: beyaz zemin, opak (`assets/icon-180/192/512.png`, iOS `AppIcon-512@2x.png` 1024). iPhone açılış: beyaz zeminde ortada
  logo (`Splash.imageset` 3×2732, logo 900 px: aspectFill kırpmasına sığar). Giriş ekranı: "Tasarruf Yanımda" yazısı yerine şeffaf
  `assets/tasarruf-yanimda-logo.png`, üstte küçük EMİNEVİM logosu. Üst yeşil çubuk ve web formu değişmedi. `sw.js` v23.
- iPhone simgesi/açılışı bir sonraki Codemagic derlemesiyle gelir. Testler: phone-layout, browser-flows, appointment-list, web-flows: OK.
- 2026-11-19: iPhone uygulama hissi (giriş ekranı EMINEVIM+işaret, native CSS, scrollEnabled=false, viewport kilidi), merkez gzip+ETag. Codemagic yeni derleme gerekir. Sırada: alt menü/kart örnek ekran, bildirim (APNs).

## 2026-11-19 — resimli üst bölüm
Müşteri ekranları: koyu yeşil gradyan + sekme resmi (assets/ty/hero-*.webp), banda binen yuvarlak sayfa, yüzen alt menü; finansman taşıt simgesi yan görünüm. Finansman/Profil başlığı hâlâ sayfa içinde.

## 2026-11-19 — tasarım karşılaştırması
Revize mockup ile birebir: sistem fontu, koyu yeşil yazı, durum hapı (yeşil nokta), lime çizgi, sol vurgulu sohbet kartı, mint ikon kutuları, yeşil gradyan düğmeler, yüzen menü (yeni ikonlar), giriş ekranı yeşil bölüm + beyaz sayfa. Finansman/Profil başlığı yeşil bölümde.

## 2026-11-19 — 3D varlık kütüphanesi
OneDrive Belgeler/eminevim-saas "Yeşil 3D Uygulama Varlık Kütüphanesi.png" (şeffaf) kesildi: assets/ty/hero-finans|ayar|profil.webp, kart-konut|tasit|isyeri.webp. Randevu/sohbet resimleri hâlâ mockup kırpması.

## 2026-11-19 — yeni şeffaf 3D resimler
OneDrive gorsel\ klasöründeki 10 görsel kesildi: assets/ty/hero-*.webp (sohbet, randevu, finans, ayar, profil, ev), kart-*.webp, giris-sahne.webp (giriş ekranı ev+araba). Finansmandaki 1/3 sayacı gizlendi (resimle çakışıyordu).

- 2026-11-19: Giriş ekranı: üstte "Tasarruf Yanımda", altta ortada küçük EMİNEVİM logosu.

- 2026-11-19: Başlık + yeşil çizgi tüm sayfalarda aynı hizada (üst yeşil bant içinde, sol kenar 18px); finansman kartları nane dolgu + beyaz çerçeve; alt menü yazıları küçüldü.

- 2026-11-19: SPY (personel) ekranları müşteri uygulamasıyla aynı dile geçti (yeşil bant, yumuşak kartlar, yüzen alt menü); Görüşmeler/Performans/Profil. Yeni görünüm yalnız ?native=1 ile (iPhone uygulamasında otomatik).

- 2026-11-19: Hero görseli genişliğe oranlı (başlıkla çakışmaz); finansman seçili kart boyutu düzeldi, açıklama cümlesi gizli; ayarlarda Çıkış yap + marka satırı altta sabit; finans/profil sayfa zemini diğerleriyle aynı yükseklik.

- 2026-11-19: Dalga beyaz alanın ortasına; Geri düğmesi beyaz sayfada (müşteri sohbeti + SPY ayrıntı); gönderilen sohbet balonu okunur; kozmetik (iç ışık, başlık gölgesi, basış geri bildirimi).

- 2026-11-19: Finansman 2. adım ve sonrası düzeltildi (1. adım hileleri sızıyordu): normal beyaz sayfa, Geri düğmesi, görünür başlık, radyo kartları, beyaz alanlar.

- 2026-11-19: Finansman kartları (Konut/Taşıt/İşyeri) 320-520 px genişlikte taşmaz (3 eşit sütun, minmax(0,1fr)); 388 px altında sağa taşıp seçince kayıyordu.

- 2026-11-19: SMS kod ekranı: "Kodu tekrar gönder" nane hap düğme, "Geri dön" sade ‹ bağlantı, kod kutusu ortalı.

- 2026-11-19: Bilgisayarda alt menü tarayıcı genişliğine yayılıyordu (position:fixed) -> ekran çerçevesine göre absolute; sayfa esnemesi kapatıldı (html fixed + overscroll none); kod ekranı: Kodu tekrar gönder düz yazı, Geri sol üstte küçük.

- 2026-11-19: Giris "Geri don" okunu kaldirdik; giris/kod ekrani kisa telefonda (667px) tum sayfa kaymaz (b33). Diger ekranlarda tum sayfa kaymasi yok; yalniz profil/ayarlar panel ici kayar.

- 2026-11-19: Randevularim: tarih blogu + saat + durum rozeti (Bekliyor sari, Onaylandi yesil, Yolda mavi, Tamamlandi yesil, Iptal kirmizi) ve filtre cipleri; bos ekranda 3 guven yazisi. sw v31. Yonetici ekrani ve "Ornek" dugmelerini ayirma sirada.

- 2026-11-19: Geri dugmesi ust banda tasindi (Tasarruf Yanimda yazisi kalkti); finansman adim 1-3 beyaz sayfa ayni hizada, Devam/Kaydet 24px asagi (nav ustu); b36 olcekli olculer (clamp, 320-430 px denendi, genis ekranda max 480). sw v32.

- 2026-11-19: Beyaz sayfa ustu tum musteri ekranlarinda ayni (143px, 320/393/430 genislikte olculdu: randevu, sohbet, ayarlar, profil, finansman 1-2, detay); baslik h1 sabit yukseklik; gorsel genisligi clamp(104,30vw,200) ve finansman cubugu gorselle cakismaz (b37-b40). sw v33.

- 2026-11-19: Tum sayfa basliklari ayni boy (32px, dar telefonda 27px) ve ayni hizada (cap ust 81px @393/430; Randevu, Sohbet, Finansman 1-3, Ayarlar, Profil). Kod ekraninda "Kodu tekrar gonder" ve Test notu kartsiz duz yazi (class kod-tekrar/kod-demo, b41). sw v34.

- 2026-11-19: Musteri Randevularim filtre cipleri kaldirildi (istek). sw v35.

- 2026-11-19: Basliklar 16px yukari (header margin-bottom -16px, hero-yuk 156, gorsel top 132, profil basligi top 56); beyaz sayfa ustu hepsinde 128px; Geri/durum cipi ile cakisma yok. sw v36. Codemagic build 9 (f31b4ea) sirada bekliyordu; bu degisiklik canli merkezden gelir, derleme gerekmez.

- 2026-11-19: Gorseller buyudu (clamp 110-210px/38vw); ortak dugme temasi (birincil koyu yesil, ikincil acik yesil #D4EEE2, 52px, tam yuvarlak; Cikis yap/Aydinlatma/Devam ayni); panel alt boslugu guvenli alani sayar (110+safe, finans 92+safe) -> Devam navbara binmez (47/34 simule edildi). Codemagic build 9 (f31b4ea) basarili, TestFlight isleme. sw v37.

- 2026-11-19: Temsilci iste akisi (ya-akis) native modda alttan acilan sayfa: ustte ekran gorunur, yesil ust bant + Geri pill, ortak yesil duygme temasi, guvenli alan (CSS b47, sw v38). 393x852, 375x667, 320x568 dogrulandi.

- 2026-11-19: Temsilci iste onay adimi: koyu yesil baslik, acik yesil ozet karti, uygulamada "Randevularima don" dugmesi (CSS b48-b49, sw v39).

- 2026-11-19: Randevu ayrintisi alttan acilan pencere (m-sheet): asagi surukle=kapat, yukari cek=tam sayfa (Geri ile pencereye doner), perdeye dokun=kapat. Liste arkada hep gorunur; Geri ust bandi kalkti. Pull-to-refresh pencere icinde kapali. CSS b50, sw v40. Dokunmatik surukleme CDP ile dogrulandi.

- 2026-11-20: Giris kod ekrani: "Geri" (sol ok + Geri yazisi), "Kodu tekrar gonder" duz yazi; secici siniflara tasindi (Safari stil yazimi farki). CSS b51, sw v41.

- 2026-11-20: Baslik hizasi olculdu (7 sayfa x 320/393/430: cap-top ayni, en fazla 1px harf farki). Alt cubuk secili sekme sade: arka plan yok, simge ici yesil dolu, yazi yesil (CSS b52, sw v42; simgelerde .i ic cizgi sinifi).

- 2026-11-20: Randevu penceresi: Tarihi degistir (acik gri-yesil) / Iptal et (acik kirmizi) yan yana. Pencere ustu pencereler (QR, iptal, puan, ek bilgi, temsilci bilgi, takip, temsilci iste) pencerenin onune alindi (m-modal, z120); sayfa degistiren eylemler (on tercihler, takip, degistir, temsilci iste) pencereyi once kapatir; pencere yalniz Randevu sekmesinde gorunur. CSS b53, sw v43.

- 2026-11-20: Randevu penceresi akici: yukseklik parmakla birlikte akar (sabit alt kenar), ust yesil bant yumusak belirir; Geri = pencere asagi kayarak tamamen kapanir; Bilgi ekle karti yesil kartin icine alindi; pencere yuksekligi icerige gore olculur. CSS b54, sw v44. Dokunmatik: yukari, asagi, kapat, perdeye dokun CDP ile dogrulandi.

- 2026-11-20: Finansman ilerleme cubuklari diger sayfalarin yesil cizgisiyle ayni hizaya (105-109px; once 12px asagidaydi; baslik cap-top zaten ayni). Acilis ekrani (EMINEVIM buyuk, Tasarruf Yanimda, slogan "Dilediginiz yerde temsilcimizle gorusme planlayin!", ev-araba sahnesi; yalniz uygulama gorunumu, oturumda bir kez ~2.5 sn): acilisEkrani() + CSS b55-b56, sw v46. iOS yerel acilis (LaunchScreen) ayri: yeni derleme ister.

- 2026-11-20: Randevu bolumu kompakt: uzun aciklamalar kalkti (Gorusmeye hazirlik yalniz baslik+Bilgi ekle, on tercih satiri kisaldi, bos durumdaki cumle kalkti), pencere ici bosluk/yazi/dugme kucultuldu, liste satiri dar. Pencere ~495px -> ~300px. CSS b57-b58, sw v47.

- 2026-11-20: Finansman baslik hizasi (ilk harf olcumu): fin1 1px asagida, fin2/3 1px yukaridaydi -> hepsi diger sayfalarla ayni satir (393 ve 320, guvenli alan simule edilerek de tutarli). CSS b59, sw v48.

- 2026-11-20: Randevu penceresi: Finansman on tercihleri + Gorusmeye hazirlik tek satirda iki kompakt dugme; "Kapida kimligini dogrula" yesil kartin icine alindi (ayri kart kalkti); kartin disinda yalniz Tarihi degistir / Iptal et. CSS b60, sw v49.

- 2026-11-20: Finansman tum hizalar test edildi (baslik ilk harf, alt cizgi, beyaz panel ust kenari, gorsel kutusu; 7 ekran, 393 ve 320): fin2/3 cizgisi 1px asagi, fin1 cubugu 1px kalin duzeltildi (b61). Randevu penceresi tam hali artik Randevularim sayfasinin beyaz paneli gibi (ust baslik gorunur, yesil bant/Geri yok, perde seffaf); popup en fazla %70 (b62, sw v51). Tam halden asagi cek: kucult, cok asagi cek: kapat.

- 2026-11-20: Logo: 4 ozgun isaret onerisi taslak/logo-onerileri.png (A konum catisi, B e+cati, C ev-tekerlek, D birlikte); tik begenilmedi. Karar bekliyor.

- 2026-11-20: Yeni logo: catı + iki nokta (beyaz/yesil) + firca gulumseme (ucları ince, saga yukselen, beyazdan yesile). Kaynak taslak/ikon.svg. Uygulama ikonu (ios AppIcon 1024, assets/icon-180/192/512), acilis ekranina ikon (assets/ty/ikon.png), sw v52. iOS ikonu ve yerel acilis ekrani yeni Codemagic derlemesi ister; web/Pages hemen gecer. Turk Patent marka sorgusu yapilmadi.

- 2026-11-20: Ikon eski duz hale dondu (catı + iki nokta + simetrik beyazdan yesile gulumseme, firca dudak kaldirildi). Dosyalar ayni (ios AppIcon, assets/icon-*, assets/ty/ikon.png), sw v53.

- 2026-11-20: Acilis ekrani artik gercek fotograf (assets/ty/acilis-foto.webp, Nano Banana ciktisinin ust sag kare kirpimi, 378x681 dusuk cozunurluk): ev + el sikisan iki kisi, yazi ustte. sw v54. Yuksek cozunurluklu tek gorsel gelince degistirilecek. iOS yerel acilis ekrani ayri (Codemagic).

- 2026-11-20: Acilis fotografi GPT ciktisiyla degisti (941x1672, 124 KB): gun batimi, ev ve el sikisan iki kisi, ust yesil gecis yazi icin. 393 ve 320 test edildi. sw v55.

- 2026-11-20: Acilis ekrani logosuz, sure 2.6 -> 4.3 sn (sw v56).

- 2026-11-20: Acilis fotografi el sikismaya yakinlastirildi (scale 1.55, yavas zoom animasyonu, ustte yesil gecis katmani). sw v57. Giris ekrani gercek gorsel istegi: kullanici farkli bir sey istiyor, konusulacak.

- 2026-11-20: Acilis ekraninda EMINEVIM yazisi yerine logo (assets/logo-white.png), sw v58. Giris ekrani icin GPT ev+araba fotografi geldi (images/30.webp), kullanima karar bekliyor.

- 2026-11-20: Giriş ekranı sade yapıldı (A): ev+araba çizimi kalktı; uygulama ikonu + "Tasarruf Yanımda" (soldan sağa yeşilden beyaza) + slogan; gülümseme çizilme animasyonu. 320 px ekranda ikon küçülme hatası giderildi. sw v60.
- 2026-11-20: Açılış fotoğrafı yakın başlar, zoom animasyonu yok. Giriş animasyonları açılış bitince başlar (ikon belirir, gülümseme çizilir, başlık soldan sağa açılır ~1,5 sn, slogan sonra). sw v61.
- 2026-11-20: Giris ekraninda beyaz bolum (telefon formu) ust kisimdan sonra alttan kayarak gelir (ty-giris-anim sinifi, ilk 9,5 sn). sw v62.
- 2026-11-20: Beyaz form bolumu slogan bitince (≈1 sn sonra) alttan yavasca (1,7 sn) yukari cikar. sw v63.
- 2026-11-20: Randevu penceresi: tam hal Randevularim paneline yerlesir (ayni baslik/gorsel/hiza), tutamac yok, asagi cekilmez, yalniz "Randevulara don" dugmesi; yukselme/inme gecisleri daha akici. sw v64.
- 2026-11-20: Giris animasyonu sirasi: cati soldan saga, sol nokta, sag nokta, agiz, sonra baslik+slogan ayni anda soldan saga, en son beyaz bolum (toplam ~7 sn, acilistan sonra). Nokta gecikme hatasi duzeltildi. sw v65.
- 2026-11-20: Beyaz bolum, baslik+slogan ile ayni anda baslar (T+3.5s). sw v66.
- 2026-11-20: iOS yerel acilis ekrani (Splash) web acilisiyle ayni gorsel (1290x2796); web acilista foto yumusak belirme kaldirildi (kesintisiz gecis). sw v67. Codemagic derlemesi kullanici baslatir.
- 2026-11-20: Cikis yapinca giris ekrani animasyonsuz gelir (animasyon yalniz uygulama acilisinda, ty-giris-anim sinifi varken). sw v68.
- 2026-11-20: Personel Girisi dugmesi durum cubugunun (saat/sarj/sebeke) altina indirildi (safe-area-inset-top + 14px). sw v69.
- 2026-11-20: Giris logo animasyonu hizlandirildi (cati .2s, noktalar .8/1.1s, agiz 1.4s, yazilar+beyaz bolum 2.1s; toplam ~4 sn). sw v70.
- 2026-11-20: Personel (SPY) ekrani: .tp native-app ici position:relative oldugu icin sayfa uzuyor, alt menu ekran disinda kaliyordu -> fixed inset 0; Performans/Profil yuvarlak ustlu panel + baslik gorselleri (hero-finans/hero-profil). sw v71.
- 2026-11-20: Personel Girisi ekrani musteri girisiyle ayni duzen (yesil ust, beyaz yuvarlak ustlu panel, logo beyaz). sw v72.
- 2026-11-20: Yonetici ekrani: fotografsiz avatar (Y) duzeltildi (ustte beyaz daire/yesil harf; profilde yesil), Saha Canli ust bosluk. sw v73.
- 2026-11-20: Giris ekrani: logo kare zemini kalkti (yalniz cati+noktalar+agiz), 2,5 kat buyudu; ust bolum ve beyaz panel asagi kaydirildi; kisa ekranlarda kucultme. sw v74.

- 2026-11-20: Personel girişi: "Eminevim" logosu altına gradyanlı "Tasarruf Yanımda" eklendi, "Personel Girişi" küçük alt başlık oldu (animasyonsuz). sw v75.

- 2026-11-20: Yeni üye adımı: üst bölüm küçüldü, form tek ekranda, Geri düğmesi kartın sağ üstünde. Personel girişi yerleşimi müşteri girişiyle aynı (foto=ikon, Tasarruf Yanımda=başlık, Personel Girişi=slogan, Eminevim altta). Açılış animasyonu denemesi: logo ortada büyük çizilir, küçülür, arka plan flu->net; yazı/kart animasyonsuz; animasyonlar ~
- 2026-11-20: Yeni üye adımı: üst bölüm küçüldü, form tek ekranda, Geri düğmesi kartın sağ üstünde. Personel girişi yerleşimi müşteri girişiyle aynı (foto=ikon, Tasarruf Yanımda=başlık, Personel Girişi=slogan, Eminevim altta). Açılış animasyonu denemesi: logo ortada büyük çizilir, küçülür, arka plan flu->net; yazı/kart animasyonsuz; animasyonlar ~18 yüzde hızlandı. sw v76.

- 2026-11-20: Yeni üye adımı: slogan geri geldi, Hesabımı oluştur düğmesi ekranın altına sabit, üst bölüm orantılı. sw v77.

- 2026-11-20: Açılış: el sıkışma fotoğrafı (assets/ty/acilis-el-sikisma.webp) ellerin üstüne zoom yapar, yeşile dönüşür, logo çizilir, giriş ekranına bağlanır. Eski acilis-foto.webp kullanılmıyor. sw v78.

- 2026-11-20: Açılış dönüşümü: fotoğraftaki çatı/başlar/kollar SVG ile giriş logosunun çatı/nokta/ağzına dönüşür (acilisDonusum), giriş logosu açılış varken çizilmez, büyük bekleyip küçülür. Kullanıcı gerçek geçiş için video önerdi (ilk/son kare ile video üretimi). sw v79.

- 2026-11-20: Açılış videosu (assets/ty/acilis.mp4, Kling, 3 MB): oturumda bir kez, sessiz tam ekran; 4,3. sn'de giriş ekranına yumuşak geçer, giriş logosu videonun son karesindeki logoyla aynı yerden küçülür (giKuculV). Kling işareti video 1.04 büyütülüp altı kırpılarak gizlendi. Video 2,5 sn içinde başlamazsa fotoğraf+çizim dönüşümü yedeği. sw v80.

- 2026-11-20: Açılış videosu: logo oluşurken üstte Eminevim logosu + Tasarruf Yanımda belirir, sonra flu geçişle giriş ekranına (arada/girişte başka animasyon yok). Giriş logosu 130x137 -> 160x169 (başlık/kart konumu aynı kaldı). sw v81.

- 2026-11-20: Video telefonda oynamıyordu: önbellek (sw.js) mp4 için tam dosya (200) döndürüyordu, iPhone 'Range' (206) ister. sw.js videoYanit eklendi (v82); video bekleme süresi 2,5 -> 5 sn. SUNUCU (merkez) tarafı: .mp4 uzantısı ve Range desteği yok -> merkez/ty/ayarlar.py + api.py (onayla, servis yeniden başlat).

- 2026-11-20: Giriş logosu 160 -> 200 px (başlık/kart konumu aynı), açılışta son kare 1 sn daha uzun (5. sn'de flu geçiş). sw v83.

- 2026-11-20: Açılış videosu uygulamada başlamazsa yedek (fotoğraf+çizim dönüşümü) 5 sn yerine 2,5 sn sonra devreye girer; video özniteliği (muted/autoplay) src'den önce verilir; loadeddata'da yeniden play. sw v84. Animasyonlu WebP yedeği üretilemedi (Playwright seek askıda), SVG yedek yeterli.

- 2026-11-20: Giriş logosu web boyutuna (300x317) büyüdü, animasyon ölçüleri uyarlandı. Açılış: video yüklenene kadar yeşil ekran, video oynayınca 1,1 sn yumuşak belirir; tüm zamanlama 'playing' anından sayılır (yedek 12 sn). sw v85.

- 2026-11-20: Giriş logosu telefon görünümündeki link boyutuna (191x202) döndü (300 çok büyüktü). sw v86.

- 2026-11-20: Açılış videosu tamamen indirilene kadar (blob) yeşil bekler, sonra oynar; yazı video saatine (2,3 sn), flu geçiş video bitince +1 sn; takılırsa süre+3 sn; inmezse 25 sn sonra yedek. sw v87.

- 2026-11-20: Giriş logosu telefonda Safari'de linkin gösterdiği boyuta (157x166, link logosu ekran yüksekliğine göre küçülüyor) eşitlendi. sw v88.

- 2026-11-20: Açılış animasyonu cihazda (localStorage ty_acilis) bir kez; yalnız 'Çıkış yap' sonrası açılışta yeniden. Giriş logosu 140x148. sw v89.

- 2026-11-20: Video 5 sn içinde inmezse ilk kare (fotoğraf) görünür, 1,6 sn sonra flu geçişle giriş sayfası (SVG dönüşüm yedeği kalktı). sw v90.

- 2026-11-20: Ana ekrana eklenen web kısayolu (standalone) uygulama görünümünü (native-app sınıfı) alır; düz gri giriş sayfası sorunu. sw v91.

- 2026-11-20: Açılışta ilk kare (fotoğraf) yüklenir yüklenmez görünür, video üstüne biner; video 7 sn'de inmezse ilk kare en az 1,8 sn kalıp flu geçiş. sw v92.

- 2026-11-20: Telefon tarayıcısında (dokunmatik + dar ekran) da native-app görünümü; ana ekran kısayolu düz gri sayfa açıyordu. Masaüstü değişmedi. sw v93.

- 2026-11-20: Videosuz açılışta Eminevim+Tasarruf Yanımda yazıları animasyonsuz hemen, bekleme 5,5 sn, ilk kare 1,2 sn + kısa flu geçiş; animasyon işareti artık GİRİŞ yapınca konur (girişsiz her açılışta oynar), çıkışta silinir. sw v96.

- 2026-11-20: Açılış animasyonu kuralı sadeleşti: kayıtlı oturum (müşteri/SPY/yönetici) yoksa her açılışta gösterilir; eski ty_acilis işareti yüzünden gösterilmeme hatası giderildi. sw v97.

- 2026-11-20: Giriş/yeni üye/personel: beyaz kart içerik kadar (Devam et'in biraz altında biter), Eminevim logosu kartın altında beyaz; Geri düğmesi sola; açılışta Eminevim+Tasarruf Yanımda yazıları fotoğrafla birlikte (animasyonsuz). Kurallar telefon tarayıcısındaki link için de geçerli. sw v99.

- 2026-11-20: Açılışta Eminevim logosu yeşil, Tasarruf Yanımda koyu yeşil (gökyüzü üstünde okunaklı, hafif beyaz parıltı). sw v100.

- 2026-11-20: Açılış: ilk kare artık yalnız video gelmezse görünür (normalde yeşil bekleme → video yumuşak); yazılar yeşil, video yeşil zemine geçince beyaza döner, parıltı yok. Giriş/personel: Eminevim logosu kart altı ile ekran dibi arasında dikey ortalı. sw v101.

- 2026-11-20: Eminevim logosu kural: kart altı ile ekran dibi arası dikey ortalı; giriş, kod, yeni üye (780px üstü ekranda; kısa ekranda gizli) ve personel girişinde ölçüldü. sw v102.

- 2026-11-20: Video gelmezse ilk kare + yazılar 3 sn ekranda kalır, sonra flu geçiş. sw v103.

- 2026-11-20: Açılış görsel (ilk kare) yedeği kapatıldı: video inene kadar yeşil ekranda beklenir (güvenlik: 90 sn veya hata → sessizce giriş sayfası). sw v104.

- 2026-11-20: Uygulamada video 3-5 sn içinde girişe atlıyordu. Yedekler: indirme olmazsa videoyu doğrudan adresten akıt; oynatma reddedilirse 0,6 sn sonra tekrar; hepsi olmazsa nedeni yeşil ekranda 4,5 sn yazıp (v105 etiketli) girişe geç. Neden: bilinmiyor, kullanıcıdan ekrandaki yazı istenecek. sw v105.

- 2026-11-20: iPhone uygulamasında video play() NotAllowedError veriyordu (otomatik oynatma engeli, büyük ihtimalle Düşük Güç Modu). Çözüm: aynı animasyon assets/ty/acilis.webp (hareketli WebP, 396 KB, ffmpeg imageio-ffmpeg ile üretildi) olarak oynatılır; zamanlama aynı (yazı 2,3 sn, geçiş ~6 sn). Video oynarsa video kullanılır. sw v106.

- 2026-11-20: Otomatik oynatma kapalıysa (Düşük Güç Modu) hareketli WebP yerine ilk kare fotoğraf + yazılar 3 sn, sonra flu geçişle giriş (webp dosyası kullanılmıyor, assets'te duruyor). sw v107.

- 2026-11-20: Eminevim logosu ekranın altında SABİT (alttan 30px + güvenli alan; giriş, yeni üye, personel hepsinde aynı yerde). Yeni üye adımı 800px altı ekranda kart yukarı: üst padding/ikon/başlık küçülür, slogan gizlenir. 667-852 yükseklikte ölçüldü. sw v108.

- 2026-11-20 (sw v109, b80): giriş modern görünüm — koyu yeşil ışıklı zemin + dalga, ikonlu/ayraçlı alanlar (telefon, ad), odakta yeşil halka, derin yeşil düğme (basınca küçülür), SMS kodu geniş aralıklı. Müşteri, yeni üye, personel ve web aynı. 6 ayrı SMS kutusu yapılmadı (tek alan).

- 2026-11-20 (sw v110, b81): ortak standart — birincil düğme tek değişkenden (--ty-btn, derin yeşil gradyan; turuncu birincil artık yeşil), ikincil düğme beyaz+ince kenar, tüm giriş alanları/seçiciler/metin kutuları beyaz+kenar+yeşil odak halkası, basınca küçülme. Personel girişi zemini müşteri girişiyle aynı (ışık+dalga). Web formu (form_bolumu) eminevim.com site tasarımında bırakıldı. Müşteri/SPY ekranları zaten ortak temada.

- 2026-11-20 (sw v111, b82): giriş ekranında logo, "Tasarruf Yanımda", slogan ve Eminevim yazısı çevresinde yumuşak yeşilimsi ışık hâlesi (B şiddeti; alt logoda daha güçlü). Personel girişindeki Eminevim logosunda da var.

- 2026-11-20 (sw v112): giriş ışık hâlesi azaltıldı (icon/yazı 16px .38, alt logo 12px .7).

- 2026-11-20 (sw v113): giriş hâlesi bir kademe daha azaltıldı; uygulama ikonuna (iOS 1024 + assets/icon-180/192/512) logo çevresinde çok hafif ışık eklendi, logo aynı. iOS ikonu yeni Codemagic derlemesi ister.

- 2026-11-20 (sw v114): giriş hâlesi bir kademe daha azaltıldı.

- 2026-11-20 (sw v115): giriş hâlesi yalnız ev logosunda ve Eminevim logosunda; başlık/slogandan kaldırıldı, bir kademe daha azaltıldı.

- 2026-11-20 (sw v116): açılış ekranına (yeşil/video/yedek fotoğraf) iki kez dokunulursa doğrudan giriş ekranına kestirme. Tek dokunuş etkisiz. Giriş ekranına ek içerik (10 taslak) şimdilik eklenmedi, karar: kalsın.

- 2026-11-20 (sw v117, b83): giriş alanına dokununca klavye açılınca görünür alan kısalır: alt Eminevim logosu Devam et düğmesinin üstüne biniyor ve kart taşıyordu. Düzeltme: <=600px yükseklikte alt logo gizlenir, ikon/başlık küçülür, slogan gizlenir, giriş ekranı kayar; odaklanan alan görünür alana kaydırılır (focusin). Chrome ile 516/420 px yüksekliğinde denendi; gerçek iPhone klavyesinde denenmedi.

- 2026-11-20 (v118): giriş kartı başlığı tek satıra sabitlendi (b84, yazı tipi yüklenince alt satıra inmesin); açılış ekranında çift dokunuş kestirmesi artık dokunuşu yutuyor, alttaki "Personel Girişi" vb. tetiklenmiyor (perde 800 ms sonra kalkar). 393/375/360 genişlikte Playwright ile doğrulandı.


## 2026-11-23
- Klavye/giriş: sabit düzen (resize none, build 15), düğmeler tek biçim (soft yeşil, 54px), Ayarlar: Yenile + Çıkış yap, çekip yenileme kaldırıldı, Bildirimler ve Aydınlatma Ayarlar'dan çıktı.
- Çok kişili test kararı verildi: `PLAN-test-kimlik.md` (kimlik havuzu, telefon maskesi, sıfırlama, test paneli). Henüz kodlanmadı.
- Çok kişili test işi yapıldı (PLAN-test-kimlik.md adım 1-7): +90 (5__) ___ __ __ telefon maskesi (uygulama + web formu), kimlik tek cihazda ("kullanımda", çıkışta serbest), boş kimlik listesi, personel kimliği, sıfırlamada personel çıkışı, sunum görünümü. sw v119. Deneme merkezinde (8795) iki tarayıcıyla doğrulandı; canlı merkez (8794) yeniden başlatılınca devreye girer; gerçek iPhone ve gerçek bildirimle denenmedi.
- Test paneli kaldırıldı, yerine sunum görünümü: takip sayfasında harita + bildirim akışı + tek "Otomatik ilerlet" düğmesi (açık çağrıların hepsini bir aşama taşır, müşteriye bildirim). `ty/sunum.py`. Deneme merkezinde (8795) masaüstü ve telefon genişliğinde sınandı.
- Sunum haritası sadeleştirildi: mahalle çizgileri kalktı, altlık soluk; çağrılar aşamaya göre renk/animasyon, yoldaki SPY için rota çizgisi, aşama göstergesi, bilgisayarda tarayıcı bildirimi. Deneme merkezinde sınandı (rota + renk sınıfları, sayfa hatası yok). sw v124.
- Harita altlığı adsız açık gri (Esri World Light Gray Base): mahalle/cadde adları kalktı, yalnız ilçe adları ve noktalar. sw v125.
- Harita altlığı OpenFreeMap vektör (maplibre): caddeler/sokaklar açık gri çizgi, mahalle/cadde adı yok (yazı katmanları gizli); WebGL yoksa Esri. sw v126.
- Harita: yollar sınıfına göre (otoyol koyu, ana cadde orta, sokak açık), yalnız ana cadde adları; rota inceltildi; test verisi sıfırlanınca SPY konumları da sıfırlanır (ty/konum.py konum_sifirla). Deneme merkezinde sınandı. sw v127.
- Harita dengelendi: ana yollar belirgin, iç sokaklar ince/açık, seyrek yer adları (semt, ana cadde, su), yakınlaşınca mahalleler. sw v128.
- Çağrı geldikten 10 sn sonra SPY'ye iletilir (teklifZamani, bekçi 2 sn); takip sayfasında Personel ve Müşteri çip grupları (müşteri aşamasına göre süzme); müşteri yanındaki SPY ikonu yana kayar; sahipsiz ikon da 16px. Deneme merkezinde sınandı. sw v130. tests/merkez-akis.py çağrı anında atama varsayıyor (bayat).
- Takip sayfası üst düğmeleri tek açılır "Göster" menüsüne toplandı: Personel ve Müşteri aç/kapa + durum işaretleri (kutucuk). sw v131.

## 2026-11-24 — Takip haritası renkleri, örnek müşteri konumu
- `merkez/takip.html`: SPY = beyaz daire + koyu yeşil çerçeve (boşta beyaz, molada gri, çağrıyla eşleşince dolu yeşil); müşteri = turuncu çerçeve (yeni çağrı beyaz + yanıp söner, temsilci belli olunca dolu turuncu); SPY→müşteri rotası turuncu (atandıda ince kuş uçuşu, yolda gerçek yol).
- `uygulama/ornek-veri.js`: 5 örnek müşteriye pilot bölge içinde farklı kayıtlı konum (Ataşehir ×2, Üsküdar ×2, Ümraniye); Zeynep ve Elif'in adresi pilot bölgeye taşındı. Uygulamada "temsilci iste" bu konumla doğrudan gün-saat adımına açılır; yeni üyede harita adımı kalır (`ornekKonum`, `mTemsilciIste`).
- Not: TEKNIK.md'deki "atandı mavi, yolda mor" ifadesi eskidi.
- (aynı gün) `merkez/ty/atama.py`: hemen atamada "meşgul" SPY elenir (`mesgul_mu`): teklif beklenen, atandı, yolda ya da görüşmede çağrısı olan SPY'ye ikinci çağrı gitmez; sıradaki uygun SPY'ye geçer, kimse kalmazsa "kimse almadı". Önceden yalnız yolda/görüşmede elenirdi, atandı aşamasındaki SPY'ye ikinci çağrı da gidebiliyordu. Merkezin yeniden başlatılması gerekir.
- (aynı gün) `merkez/ty/sunum.py`: Otomatik ilerlet'te SPY yola çıkınca artık yarı yola kaymaz (rota çizgisi çizilir); görüşmede müşterinin yerine gelir. Merkez yeniden başlatıldı.
- (aynı gün) Müşteri çıkışında bildirim aboneliği sunucuda da silinir (`abone_jeton_sil`, abonelik artık jeton özeti taşır); giriş listesi artık tüm kayıtlı müşterileri (yeni üyeler dahil, sıfırlanana kadar) gösterir, açık çağrısı olanlar hafif sarı; çıkışta giriş telefonu/yeni üye önerisi sıfırlanır. Merkez yeniden başlatıldı.
- (aynı gün) Giriş ekranı örnek müşteri listesi özel açılır liste oldu (iPhone seçici renk göstermez); randevuda olan satır sarı. Merkez yeniden başlatıldı.
- (aynı gün) Yeni müşteri kaydında yöneticiye/akışa "Yeni müşteri hesabı" olayı düşmez (hesap_ac); müşteriye giden bildirimler değişmedi.
- (aynı gün) Takip haritası altlığı standart sokak (OpenStreetMap) oldu; eski sade gri OpenFreeMap vektör altlığı git geçmişinde.

- 2026-11-25 Takip haritasında müşteri ve SPY işaretleri sürüklenebilir (müşteri kabul edilene kadar, SPY kabul ettiği çağrı yokken); konum değişince çağrı yeniden değerlendirilir, daha uygun SPY varsa teklif ona geçer. Haritada "+ Çağrı ekle" ile gerçek örnek çağrı eklenir (sıfırlanana kadar kalır). Kod: `merkez/ty/islemler.py` (konum_tasi, cagri_ekle), `atama.py` (yeniden_ata), `konum.py` (elleKonum), `takip.html`. Deneme merkezinde (8795) API ve arayüz sınandı. Ayrıca harita OpenFreeMap vektör altlık (Google benzeri renk, az etiket, renkli yol rozetleri) oldu.
- (aynı gün) Pilot bölge denetimi: müşteri bölge dışına sürüklenince çağrı telefonla görüşmeye döner (bolgeDisi), SPY taşınamaz, bölge dışına çağrı eklenemez. Merkez yeniden başlatıldı.
- (aynı gün) Çağrı ekle: form kalktı, düğmeye basıp haritaya dokunmak çağrıyı rastgele ad/telefonla hemen ekler.
- (aynı gün) Otomatik ilerlet: SPY artık yolda aşamasında müşteriye ışınlanmaz (konum.py, yolda iken eski yerinde kalır, rota çizilir; varışta elle konum bırakılır). Konum sürüklemeleri bildirim akışına olay yazmaz. Merkez yeniden başlatıldı.
- (aynı gün) Otomatik ilerlet: yolda aşamasından sonraki basışta SPY rota boyunca müşteriye sürekli yürür (15 sn; merkez başlangıç+süreyi tutar yolBasladi/yolSure/yolBaslangic, konum.py zamana göre hesaplar, takip.html animKonum ile akıcı çizer); bir sonraki basışta görüşmede. Merkez yeniden başlatıldı.
- (aynı gün) Otomatik ilerlet: yürüme 30 sn, rota SPY ilerledikçe kısalır, varışta kendiliğinden görüşmeye geçer (sunum.varis_denetle, api.py bekçisi 2 sn). SPY açılır kutusunda Ciro %/Rnd % gösterilir; Bugün N çağrı ve Bildirim satırları kalktı. Merkez yeniden başlatıldı.
- (aynı gün) Çağrı iletimi 10 sn yerine 4 sn sonra (ILETIM_BEKLEME_SN=4, bekçi 1 sn). Merkez yeniden başlatıldı.
- (aynı gün) Çağrı ekle: rastgele ad sistemde (kapalı çağrılar dahil) zaten varsa yeniden seçilir.
- 2026-11-25 İlçe kuralı (çağrı yalnız kendi ilçesindeki SPY'ye), ilçede uygun SPY yoksa randevu önerisi (merkez + takip + uygulamada kabul/başka saat kartı), 5 hareketli örnek SPY (h1–h5, atamaya katılır, teklifi 4 sn sonra kabul eder), `api/oneri`, sw.js v134. Merkez yeniden başlatıldı. Müşteri uygulamasındaki öneri kartı ekran görüntüsüyle doğrulanmadı (yalnız kod ve API denendi).
- (aynı gün) Takip sayfası tarayıcı bildirimi (Notification) kaldırıldı; sağdaki Bildirimler listesi aynen duruyor.
- (aynı gün) Hareketli SPY'ler artık rastgele dolaşmıyor: yol üstünde kapalı tur (OSRM, `veri/sim-yollar.js`, `araclar/sim_yol_uret.py` üretir; ~8 m/sn, SPY başına faz; formül `konum.gezi_konum` + takip.html `geziKonum`), takip haritasında ince yeşil hare (`.spy-ik.hare`). "Yola çıktı" yazılıp 2 sn ilerletilmezse SPY kendiliğinden yürümeye başlar (`sunum.yurume_baslat`, `yolaCikis`). Deneme merkezinde doğrulandı; canlı merkez yeniden başlatıldı.
- (aynı gün) Hareketli SPY de atanınca durur (`kayit["don"]`, konum kaynağı "dondu"): sabit SPY ile aynı aşamalar; rota hep aynı yerden çizilir, yürüyüş o noktadan başlar. Önceden hareketli SPY'nin başlangıcı her yoklamada kaydığı için ön rota hiç görünmüyordu.
- (aynı gün) Takip sayfasından eklenen çağrılarda hareketli SPY teklifi artık kendiliğinden kabul etmez: sabit SPY ile aynı aşamalar ("Otomatik ilerlet" ile kabul); uygulamadan gelen çağrılarda 4 sn sonra kabul sürer. "+ Çağrı ekle" müşterisi KVKK/Aydınlatma adımı geçmiş yeni üye olarak açılır (`hesap_ac`, kaynak yonetici), uygulama giriş listesinde görünür (sıfırlanana kadar), randevu oradan yanıtlanabilir.
- (aynı gün) Atama puanı sırası: yakınlık 50, ciro H/G 25, randevu H/G 15, çağrı yükü 10 (hemen ve ileri çağrıda aynı; `ayarlar.AGIRLIK`, URUN_KURALLARI.md ve 10-atama-ve-rota.md güncellendi). Merkez yeniden başlatıldı.
- (aynı gün) Temsilci belli olunca hareketli SPY artık durmaz (atandı aşamasında yolda dolaşmaya devam eder); "yola çıktı" aşamasında durur, rota o noktadan çizilir ve yürüyüş buradan başlar (`kayit["don"]` artık yola çıkışta konur).
- (aynı gün) Bir SPY bir saatte en fazla bir randevu: `ARALIK_DK` 90→60, kural hemen çağrıda da geçerli (`atama.adaylar`). Randevu önerisi (`oneri_bul`) 30 dk adımla her saatte uygun SPY arar; başka müşteriye önerilmiş saat de dolu sayılır (sonuç: 4 SPY'ye 13:00, sonra 14:00 önerildi). Merkez yeniden başlatıldı.
- (aynı gün) Müşteri önerilen randevuyu kabul edince takip haritasında işareti beyaz zemin + eğik turuncu çizgi, üstünde "Randevu 13:00" etiketi (`kayit.oneriKabul`, takip.html `randevuIkon`); SPY yola çıkınca normal işarete döner. Ekran görüntüsüyle doğrulandı.
- (aynı gün) Önerilen ileri randevuyu kabul eden çağrı (`oneriKabul`) "Otomatik ilerlet"te sıra bekler: öteki açık çağrılar bitene kadar ilerlemez, bitince bir sonraki basışta ilerler (`sunum.ilerlet`; yanıtta `bekleyen`). SPY'si olmayan (kimse almadı) çağrılar engel olmaz. Deneme merkezinde 4 çağrı tamamlandıktan sonraki basışta randevu çağrısı atandı→yolda→görüşmede ilerledi.
- (aynı gün) Takip haritasında ilçe adları (Üsküdar, Ümraniye, Ataşehir) işaretlerin ve rotaların arkasına alındı (ayrı harita katmanı `ilceAd`, z 420) ve soluklaştırıldı (opaklık .45). Yalnız takip.html; merkez yeniden başlatması gerekmedi.
- (aynı gün) Takip haritasında pilot bölge sınırı belirginleştirildi (çizgi 1,5→2,8 px, opaklık .6→.95, dolgu .03→.09 yeşil). Yalnız takip.html.
- (aynı gün) Takip haritası: yakınlaşınca (zoom 14+) personel adları işaretin üstünde görünür; ilçe sınırı çizgisi inceltildi (2,8→1,8 px). Genel müdürlük işareti bekliyor: adres/konum kullanıcıdan istenecek (internette bulunamadı, tahmin edilmedi).
- (aynı gün) Takip haritası: personel adları artık zoom 13'ten itibaren (bir tık uzakta) görünür. Genel Müdürlük: küçük turuncu nokta + etiket, Yamanevler Ahmet Tevfik İleri Cd. No:20 A Ümraniye; konum yalnız cadde düzeyinde bulundu (41.02873, 29.11376; bina numarası OSM'de yok, ~±200 m sapabilir) — kullanıcıdan Google Haritalar koordinatı alınırsa takip.html'deki GM işaretinde düzeltilir.
- (aynı gün) Genel müdürlük noktasının üstündeki yazı kaldırıldı (yalnız turuncu nokta; dokununca adres kutusu).
- (aynı gün) İlçe kuralı sıkılaştı: hemen çağrı yalnız o an müşterinin ilçesinde bulunan SPY'ye gider (SPY'nin anlık konumunun ilçesi; yol turu başka ilçeye taşan ya da haritada başka ilçeye taşınan SPY'ye gitmez, taşındığı ilçedeki çağrıyı alır). İleri saatli çağrıda SPY'nin kayıtlı ilçesi geçerli. 288 rastgele noktada yanlış ilçe 0.
- 2026-11-25 (akşam) Atama: yeni puan sırası **yakınlık 40, çağrı sayısı 30, ciro H/G 20, randevu H/G 10** (kullanıcı kararı); yakınlık **trafikli varış süresi**
  (OSRM yol süresi × İBB saatlik trafik yoğunluğu verisinden tipik trafik çarpanı, 30 dk'da sıfır). Yeni kapılar `merkez/ty/yol.py`, `merkez/ty/trafik.py`,
  veri `veri/trafik-carpan.json` (`araclar/trafik_hazirla.py`, İBB 2024-10/11 + 2025-01). Takip sayfasına **Atama seçenekleri** paneli (ağırlık, uzaklık türü,
  sınırlar, ilçe şartı; çağrı başına aday puan dökümü ve elenenler, "şimdiki seçeneklerle yeniden hesapla"). Belgeler: 10-atama-ve-rota.md, URUN_KURALLARI, TEKNIK, IT_DEVIR.
- 2026-11-25: Personel girişinde yalnız giriş yapabilen SPY'ler listeleniyor. Müşteri giriş düğmesinin erişilebilir adı adımın metnine bağlandı. Chrome'da müşteri girişi ve randevu listesi, deneme merkezinde personel seçimi doğrulandı. Genel tarayıcı testlerinde yerel bağlantı ve bekleme hataları sürüyor. Merkez akışı testi Ayarlar ekranından kaldırılmış Aydınlatma Metni düğmesini bekliyor.
- 2026-11-25: Atama seçenekleri uygulama içindeki Saha Canlı sekmesinden de açılıyor. Yeniden hesaplama sonucunda birinci aday “ilk sırada” etiketiyle gösteriliyor. Deneme merkezinde dört uzaklık türü, puan toplamı, ilçe şartı, ayarın sonraki çağrıya uygulanması, eski teklifin korunması, sıfır ağırlığın reddi ve varsayılana dönüş doğrulandı. Telefon ölçüsünde panel ve harita filtreleri çalıştı. Genel müşteri akışı ve yerleşim testleri geçmediği için yayın bekliyor.

- 2026-11-25 (devam): Codex işi denetlendi (personel giriş listesi `TY_SPYLER`, telefon düzeni kararı, testler). `tests/merkez-akis.py` tek-cihaz kimlik kuralına uyarlandı: A telefonu ve web müşterisinin uygulaması başka telefonda girmeden önce çıkış yapar. Tüm testler geçti.

- 2026-11-26: Atama: şube konumları (eminevim.com: Ümraniye, Ümraniye Çarşı, Ataşehir, Örnek Mah., Üsküdar) haritalarda yeşil nokta; randevuya 4 saat+ varsa yakınlık SPY şubesinden; hemen çağrı 60 dk; sıra önceliği: aynı ilçedeki şube → 2 km altı → puan (ilçe artık eleme değil). Seçenekler panelinde ayarlanabilir. Tüm testler geçti.
- 2026-11-26 (devam): Takip haritasına trafik katmanı (gün + saat −/+), ilçe adları kaldırıldı, Atama seçenekleri açıklamaları sadeleşti.

- 2026-11-26: Takip haritası trafik katmanı kareler yerine yollar: İBB canlı trafik vektör karoları (anahtarsız) merkezde çözülüp pilot ilçe sınırına kırpılıyor (`api/trafik-yol`, `ty/trafik.py`); "Şimdi" canlı, diğer saatler tipik çarpan. İBB Şehir Haritası API'si (2016, iframe + anahtar) incelendi, kullanılmadı.
- 2026-11-26 (2): Trafik katmanı yalnız canlı (gün/saat −/+ kalktı, kullanıcı: "hep şimdiye göre"); kaynak İBB TrafikSegment sorgusu (anonim anahtar, hız dahil), İBB çizim kuralları (ana yol her zaman, ara yol 14+). Sıradaki: canlı hızı rotaya/atamaya eklemek.
- 2026-11-26 (3): Atamada 2 saate kadar anlık trafik (rota + İBB segment hızı), sonrası tipik çarpan; Atama seçeneklerine "Anlık trafik (saat)". Sunumda varış her SPY'nin kendi rotasından (önceden herkes 10 dk / 30 sn). Yakın görünümdeki çizgi kayması ölçüldü: ortanca 1,8 m, rotayı etkilemiyor.
- 2026-11-26 (4): Rota aşama 1: yol servisinin 1-3 alternatif rotasından anlık trafikle en kısa süreli olan seçiliyor (atama + sunum varışı). Sıradaki aşama (konuşulacak): seçilen rotanın kaydı, SPY'nin yoldaki hıza göre hareketi, haritada aynı rotanın çizimi.
- 2026-11-26 (5): Rota aşama 2: sunumda seçilen en hızlı rota zamanlı kaydediliyor (yolRota), harita aynı rotayı çiziyor, SPY her yolun anlık hızına göre ilerliyor; merkez ve harita aynı konumu hesaplıyor. Yolda yeniden hesaplama yok (karar). Açık: gerçek SPY'de tahmini varış güncellemesi (kullanıcı sonra bakacak).


- **2026-11-26:** Atama seçeneklerinde adaylar ad, süre ve puanla tek satırda gösterilir; açılan ayrıntıda ölçütlerin gerçek değerleri ve puan katkıları görünür. Puan hesabı değişmedi.
- **2026-11-26:** Çağrı sıralaması ayrıntısında şube adı ismin altında gösterilir; yakınlık yalnız km ve dakika olarak sadeleştirildi.
- 2026-11-26 (6): Codex'in kompakt sıralaması incelendi: km ile ölçülürken satır özeti "—" kalıyordu (km gösterilir), ayrıntıdan düşen anlık trafik/rota/nereden bilgisi Yakınlık satırına geri eklendi. Takip haritasına "Pilot bölge" aç/kapa düğmesi.
