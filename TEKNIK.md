# Tasarruf Yanımda — teknik ayrıntılar

Kod ve altyapı işinde ilgili başlığı oku. Kurallar `CLAUDE.md`'de, ürün/ekran davranışı `URUN_KURALLARI.md`'de.

## Uygulama
- Tek dosya `Eminevim Saha Paneli.dc.html`: şablon `{{ }}`, `<sc-if>`, `<sc-for>`; durum `state`, görüntü değerleri `renderVals()`;
  çalışma zamanı `uygulama/support.js`. `?native=1` telefon düzeni ve service worker kapalı.
- **Modüller** (`IT_DEVIR.md`): sayfa yalnız ekranları ve `Component` sınıfını tutar; yardımcılar `uygulama/*.js` klasik betikler
  (üst düzey `const`/`function` global olur, sınıf içinden doğrudan kullanılır). Sıra `<head>`'de: veri → servisler → ayarlar → bicim →
  finansman → personel → hesap → ornek-veri → support. Yeni modül eklenince: `<head>`, `sw.js` listesi + CACHE sürümü,
  `merkez/ty/ayarlar.py → SURUM_DOSYALARI`, `tests/appointment.test.js` modül listesi.
- `index.html`, `harita/`, `veri/`, `sw.js` — uygulama (web/PWA). Aynı kod Capacitor ile iPhone'a paketlenir
  (`scripts/prepare-web.mjs` → `www/`: `uygulama/`, `harita/`, `assets/`, `vendor/`, `veri/*.js`; `IOS_TESTFLIGHT.md`, Codemagic).
- Eski uygulama (sade akıştan önceki): `backup/2026-10-21-eski-uygulama/` (açılır hâlde), git etiketi `eski-uygulama-2026-10-21`.
  Geri dönmek gerekirse: `git checkout eski-uygulama-2026-10-21 -- "Eminevim Saha Paneli.dc.html"`.
- Bu depoda git kimliği yerel ayarlı: `sualpsudas <sualpsudas@users.noreply.github.com>`.

## Görünüm (eminevim.com :root değerleri, 2026-10-21)
Yeşil #00724c, ana düğme turuncu #ea803f, gri hap kutu #EEE (köşe 22px), kart köşesi 14px, yazı #666, çizgi #DDD, açık yeşil #e9f0ed,
yazı tipi GOTHIC → "Century Gothic" (site dosyası başka adrese izin vermiyor). Uygulamada tema değişkeni `--kutu`; yeni ekran/bileşen bu değerlerle yapılır.

## Web formu (`web-basvuru/`)
- eminevim.com ana sayfa kopyasında yeni Hızlı Başvuru formu. `form_bolumu.html` (TY_CSS / TY_FORM / TY_TAKIP / TY_JS blokları) düzenlenir →
  `python olustur.py` canlı eminevim.com'u indirir, formu masaüstü paneline ve mobil pencereye koyar (mobilde `tk-input*Mobil*` sınıfları),
  izleme kodlarını çıkarır, tüm `<a>`'ları etkisizleştirir (`data-ty-dis` hariç) → `index.html`. Değişiklikten sonra mutlaka yeniden üret.
- Form **gerçek site formu gibi**; temsilci çağırma isteğe bağlı seçenek. Temsilci bilgisi ve takip linki telefona mesajla gider
  (önizleme "Gelecek mesajı önizle").
- Demo: her açılışta ve "Yeni başvuru"da örnek bilgilerle dolu gelir (Mehmet Demir, 532 123 45 67; takvimde ilk hafta içi günü + 18:00,
  haritada Caferağa/Kadıköy, Ev).
- Temsilci hemen gösterilmez: "Görüşme saatinden önce temsilciniz hakkında bilgilendirileceksiniz". Yer türü (İş yeri / Ev) yok.
  Teşekkür metni: "Görüşme öncesinde Çözümlerimize, Kampanyalarımıza ve Finansman aracına göz atmak isterseniz Eminevim uygulamasını
  indirebilirsiniz." (uygulamada aynı dil "üye olun" ile).
- Bütçe hesabı (kaba formül): sitedeki Konut / Araç / İşyeri kutuları (üst menü, Çözümlerimiz kartları, mobil menü) "Ödeme planınızı
  oluşturun" penceresini açar; hesap uygulamadakiyle aynı (`senaryoHesapla`), "Örnek hesaplamadır" notuyla.

## Canlı test merkezi (`merkez/`)
- Ürün davranışı (7 SPY, atama, 2 dk kabul, Devret, "kimse almadı", Saha Canlı, giriş): `URUN_KURALLARI.md` → "Canlı test sürümü".
- `sunucu.py` (8794; yalnız giriş, kod `merkez/ty/` — parça listesi `ty/__init__.py`), `takip.html` (bilgisayar takip sayfası), `uygulama/canli.js`.
  Canlı konum girişi `api/konum` (`ty/konum.py`), şirkete aktarım `merkez/aktarim/*.jsonl` (`ty/aktarim.py`, depoda yok). Gizli yol `merkez/gizli_yol.txt` (depoda yok, belgeye yazılmaz).
  Tailscale Funnel: `/<gizli_yol>` → `http://127.0.0.1:8794/<gizli_yol>`. Windows'ta adres yeniden kullanımı kapatıldı (ikinci kopya bağlanamaz).
- **Bildirim (Web Push):** merkez, hemen çağrıyı o SPY'yi seçmiş tüm telefonlara gönderir (bir telefon = bir kişi; aynı SPY birden çok telefonda).
  API: `api/anahtar`, `api/abone`, `api/abone-sil`; servis çalışanı `merkez/canli-sw.js` (merkezde `sw.js` adıyla; kökteki `sw.js` Pages için ayrı).
  Bağımlılık: conda base'de `pywebpush`. `merkez/vapid.pem` ve `*_abonelik.json` yalnız sunucuda. iPhone Safari'de yalnız Ana Ekrana Ekle ile.
  Bilgisayar Chrome'unda bildirim denemesi Google'a bağlı ve kararsız, kalıcı teste konmadı; merkez mantığı `tests/merkez-akis.py`
  sahte bildirim sunucusuyla sınanır. Kullanıcı notu: personel girişi ileride yalnız telefondan (ya da yerel uygulamadan) olacak.
- **Müşteri hesabı:** merkezde (`api/musteri` islem: kod, dogrula, kayit, web, oturum, cikis; `veri.json` → `musteriler`: adi, soyadi,
  aydinlatmaTarih, kampanya). Parola yok (2026-11-18): telefon + SMS kodu. Girişte merkez bir jeton verir; müşteri
  aboneliği (`api/abone` + `musteri`, `jeton`) yalnız onunla. Bildirimler: SPY kabul ("Temsilciniz belli oldu"), yola çıkış (tahmini varış),
  SPY mesajı (kabul/yola çıkış hazır mesajları `oto` ile ayrı bildirim üretmez). Dokununca o randevu açılır (`?ac=` / servis çalışanı mesajı).
  Bir telefon tek kişiye bağlı (SPY ya da müşteri; sonuncusu geçerli).
- **Test kimliği (2026-11-23, `PLAN-test-kimlik.md`):** çok kişili test için bir kimlik aynı anda tek cihazda. Cihaz kimliği telefonda
  `ty-cihaz` (uygulama/hesap.js `cihazKimligi`); merkezde `veri.json → kimlikler`: müşteri `<tel>`, personel `spy:<id>` → {cihaz, tarih}.
  Müşteri: `api/musteri` islem `bos` (boş örnek kimlikler), `oner` (yeni üyelik için kayıtsız ad/soyad/telefon); `kod/dogrula/kayit/web`
  başka cihazdaysa "kullanımda" hatası verir; giriş alır, `cikis` bırakır. Personel: `api/kimlik` (`bos | al | birak`, `ty/islemler.py`).
  Telefon her yerde `+90 (5__) ___ __ __` (`uygulama/bicim.js` `telMaske/telGecerli/telAnahtar`; web formu aynı kuralı kendi içinde taşır);
  saklanan değer 10 hane. `api/sifirla` kimlikleri siler, personeli de girişe döndürür (`yerelSifirla`).
  Not: bu kural test aşaması içindir; gerçek yayında bir müşteri birden çok cihazdan girebilmeli (`ty/musteri.py` `kimlik_*` işlevleri kaldırılır).
- **Çağrı iletimi:** çağrı önce "alındı" kalır, 10 sn sonra (`atama.py` ILETIM_BEKLEME_SN, bekçi 2 sn) SPY'ye iletilir. **Sunum görünümü (2026-11-23):** `merkez/takip.html` — solda canlı saha haritası (açık çağrıdaki müşteriler lacivert nokta), sağda "Bildirimler"
  akışı (`api/durum` → son olaylar: "Çağrı geldi · Ayşe Kaya, Üsküdar") ve tek düğme "Otomatik ilerlet" (`POST api/ilerlet`, `ty/sunum.py`):
  açık çağrıların hepsi bir aşama ilerler (yeni → SPY atandı → yola çıktı [SPY yerinde kalır, rota çizgisi çizilir] → görüşmede [SPY müşterinin yerine gelir] → tamamlandı), her aşamada
  müşteriye bildirim. Seçim yok. Harita sade (mahalle yok, adsız açık gri OpenFreeMap vektör altlık: caddeler çizili, tüm yazılar gizli; WebGL yoksa Esri adsız gri); çağrılar aşamaya göre renkli nokta (yeni çağrı turuncu yanıp söner, atandı mavi, yolda mor halkalı, görüşmede yeşil), yoldaki SPY→müşteri rotası OSRM ile çizilir; bilgisayarda yeni olay için tarayıcı bildirimi (ilk tıklamada izin istenir). Yönetici girişi sınırsız (`?rol=ask`), telefon ve bilgisayardan açılır.
- **Kapıda doğrulama (2026-11-19):** `api/dogrulama` (`ty/dogrulama.py`). `islem:kod` (müşteri tel + jeton) → 4 haneli kod, yalnız bellekte
  (`KAPI_KODLARI`, merkez yeniden başlarsa müşteri "Kodu yenile"). QR içeriği `{randevu, revision, kod}`. `islem:dogrula` (id, spy, kod, revision)
  → randevu + SPY + sürüm + süre kontrolü, `gorusmede` + `dogrulandi {zaman, yol: qr|kod}`, müşteriye bildirim. Kamera: `getUserMedia` (https
  gerekir; Funnel https), çözme BarcodeDetector ya da `vendor/jsQR.js` (Apache-2.0, ekran açılınca yüklenir). iPhone: Info.plist
  `NSCameraUsageDescription`. Test: `merkez-akis.py` sahte kamerayla (Chrome `--use-file-for-fake-video-capture`, müşterinin QR'ı .y4m).

- **Takipte sürükleme ve çağrı ekleme (2026-11-25):** `api/konum-tasi` {tur: musteri|spy, id, lat, lng}: müşteri yalnız `alindi` durumunda (teklif bekleyen dahil), SPY yalnız kabul ettiği (atandi/netlesti/yolda/gorusme/gorusmede) çağrısı yokken taşınır; SPY konumu `veri["elleKonum"]`da durur (test sıfırlanınca ya da gerçek canlı konum gelince silinir, `konum.py`). Sonra `atama.yeniden_ata`: daha uygun SPY çıktıysa teklif ona geçer (eski SPY reddetmediği için elenmiş sayılmaz; gönderilmiş bildirim geri alınamaz), değilse uzaklık/puan güncellenir. `api/cagri-ekle` {ad, tel, yer, lat, lng}: gerçek kayıt (`y-…`, kaynak yonetici); sıfırlanana kadar kalır, uygulama akışı aynı. Arayüz yalnız `merkez/takip.html` (düğme haritanın sağ üstünde, dokunulan noktaya form sormadan rastgele ad/telefonla eklenir; panelin Saha Canlı sekmesi onu gömer; gösteri/GitHub Pages sürümünde yok).

- **Pilot bölge denetimi (2026-11-25, `merkez/ty/bolge.py`, sınırlar `assets/pilot-sinirlar.js`):** müşteri bölge dışına sürüklenirse çağrı `bolgeDisi` olur (temsilci gönderilmez, telefonla görüşülür; takipte "Pilot bölge dışı"), bölgeye geri taşınınca baştan teklif edilir. SPY bölge dışına taşınamaz, bölge dışına çağrı eklenemez (400 hata).

## iPhone (TestFlight)
- TestFlight'ta derleme var (Build 1, 2026-10-05; `IOS_TESTFLIGHT.md`).
- `scripts/merkez-adresi.mjs`: Codemagic'te `TY_MERKEZ_URL` (merkezin tam https adresi + gizli yol) varsa uygulamayı merkez sayfasına bağlar →
  uygulama değişikliği yeni derleme istemeden telefona gelir. Değişken yoksa paketteki gösteri sürümü açılır.
- Uygulama kapalıyken bildirim (APNs, 2026-11-22): iPhone uygulaması `@capacitor/push-notifications` ile Apple cihaz kodunu alır, `api/abone` ile merkeze verir
  (kayıt anahtarı `apns:<token>`, Web Push ile aynı `*_abonelik.json`). Merkez `ty/apns.py` ile Apple'a gönderir (önce üretim, `BadDeviceToken` olursa sandbox).
  `ios/App/App/App.entitlements` (`aps-environment`) + `AppDelegate.swift` köprüsü. Bildirime dokununca `tyRandevuAc` ilgili randevuyu açar.
- Uygulama yalnız iPhone (`TARGETED_DEVICE_FAMILY = 1`): iPad'de büyütülmüş iPhone penceresinde açılır, SPY tablet düzeni görünmez.
  SPY'ler iPad'de merkez linkini (Safari / Ana Ekrana Ekle) kullanır; iPad desteği ayrı karar (2026-11-19).

## linkler.html ve çalışma sayfası
- Telefonda: yalnız sol üstte küçük "Uyg / Web" tuşları, sayfa gerçek boyutunda tam ekran.
- Bilgisayarda: iPhone 15 çerçevesi (393×852); uygulamanın bilgisayar görünümü YOK, Telefon/Bilgisayar seçimi yalnız Web'de.
  Adreslenebilir: `#uygulama-telefon`, `#web-telefon`, `#web-bilgisayar`. Yapılacaklar paneli 2026-11-04 kaldırıldı (görev takibi `gorev-takip`te).
- Görev takip sayfasından da Çalışma sayfasına bağlantı verilir. `rapor/benzer-uygulamalar.html` linkler.html'de "Araştırma raporu".
