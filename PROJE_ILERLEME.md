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
