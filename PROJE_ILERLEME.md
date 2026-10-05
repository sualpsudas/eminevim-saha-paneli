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
