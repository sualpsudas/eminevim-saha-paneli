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
