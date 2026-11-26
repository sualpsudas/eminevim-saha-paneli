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
- **Çağrı iletimi:** çağrı önce "alındı" kalır, 4 sn sonra (`atama.py` ILETIM_BEKLEME_SN, bekçi 1 sn) SPY'ye iletilir. **Sunum görünümü (2026-11-23):** `merkez/takip.html` — solda canlı saha haritası (açık çağrıdaki müşteriler lacivert nokta), sağda "Bildirimler"
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

- **Atama seçenekleri, yol ve trafik (2026-11-25):** `atama.ayar(veri)` = `ayarlar.ATAMA_VARSAYILAN` + `veri["atamaAyar"]` (sıfırlamada korunur).
  `api/atama-ayar` {islem: oku | kaydet (ayar) | varsayilan | dene (id)}; `dene` çağrıyı değiştirmeden şimdiki seçeneklerle sıralar.
  Her teklif/yeniden değerlendirmede çağrıya `siralama` {t, uzaklik, agirlik, hemen, adaylar[{id, ad, puan, parca{yakinlik,yuk,ciro,randevu}, km, dk, carpan, kaynak, cagri}], elenen[{id, ad, neden}]} ve `varisDk` yazılır.
  `yol.olc(noktalar, hedef)`: OSRM `table` (sources=adaylar, destinations=müşteri) tek istek, 3 sn zaman aşımı, bellekte önbellek (~10 m), hata olursa 60 sn kuş uçuşu.
  `trafik.carpan(a, b, gun, saat)`: düz hat üstündeki 5 noktanın geohash-6 karelerinin ortalaması (`veri/trafik-carpan.json`; yeniden üretmek için
  İBB aylık CSV'leri indirilip `python araclar/trafik_hazirla.py <csv...>`; CSV'ler depoya girmez). `sureleri_denetle` sık yoklamada `adaylar(..., olc=False)` kullanır (yol servisine istek gitmez).
  Arayüz `merkez/takip.html` → "Atama seçenekleri" (sağdan panel; gösteri sürümünde yok).
- **Şube konumu, öncelik basamakları, hemen 60 dk (2026-11-26):** şube konumları `veri/kaynak/sube_konum.csv` → `veri_hazirla.py` → `veri/spyler.js`
  içinde `window.TY_SUBELER` [{ad ("Ataşehir Şubesi", SPY kaydındaki `sube` ile aynı), gorunen, adres, lat, lng}]; merkez `personel.SUBELER`
  (`_dizi` ile okur; `spyler.js`'i okuyan her yer ilk `];`'ye kadar almalı). Haritalar (`merkez/takip.html`, `harita/map.html`) küçük yeşil nokta (`.sube-ik`).
  `atama.kalan_dk(k)` ≥ `subeSaat`×60 ise başlangıç noktası `sube_yeri(s)`, değilse `anlik_konum`. Sıralama anahtarı
  (`not ayniIlce`, `not oncelik`, `-puan`): `ayniIlce` = `sube_ilce(s)` (şube konumundan `ilce_bul`) müşterinin ilçesi ve `ilceOnceligi` açık;
  `oncelik` = yol km < `oncelikKm`. Ayrıntıya `nereden`, `subeIlce`, `ayniIlce`, `oncelik`; `siralama`'ya `oncelikKm`, `subeden`, `subeSaat` eklendi
  (`atama.siralama_ozet`, `dene` de bunu kullanır). `ilceSarti` (eleme) kaldırıldı → `ilceOnceligi`. `HEMEN_DK` 120 → 60.
  Takip haritası: trafik katmanı (sol alt; yalnız o anki İBB canlı trafiği, geçmiş/saat seçimi yok — 2026-11-26 kararı; `GET api/trafik-yol` ← `trafik.canli_yollar()`: harita.istanbul'un kendi adresleri — önce `sehirharitasigateway.ibb.gov.tr/auth/anonim` yanıtındaki `ABC-3903258-571632` anonim anahtarı, sonra aynı adlı başlıkla `.../TrafikSegment/MapServer/0/query` (pilot kutusu, tek istek ~3.000 segment, alanlar color/speed/tip); pilot ilçe sınırına kırpılır, 3 dk bellekte, 401'de anahtar yenilenir. Çizim İBB'deki gibi: renkler 1-2 #80CF63/#54AC35 akıcı, 3 #FF9C07 yoğun, 4 #F42A2A, 5 #9B0808, 0 çizilmez; tip 2 ara yollar yalnız yakınlık 14+ ince/soluk. Resmi hizmet değil, gerçek yayında İBB izni gerekir; atamada `canliSaat` (2) saatten yakın randevuda `yol.rotalar()` (OSRM route alternatives=3, parça başına mesafe/süre) → `atama.en_hizli_rota()` anlık süresi en kısa olanı seçer + `trafik.canli_rota_dk()` (parça orta noktası ≤20 m İBB segmentiyle eşleşirse o hız; ~50 m ızgara dizini), en yakın noktaya tek rota/SPY; sunumda `atama.varis_dk()` → `varisZamani`, `yolDk`, yürüyüş `yolSure` = dk×3 sn (10-90)); ilçe adı etiketleri kaldırıldı;
  Atama seçenekleri paneli kısa etiketlerle sadeleşti (açıklama metinleri yok).
- **İlçe kuralı, randevu önerisi, hareketli SPY (2026-11-25):** ~~`atama.adaylar` yalnız müşterinin ilçesindeki SPY'leri aday yapar~~ → 2026-11-26 öncelik oldu (aşağıda Şube konumu). İlçede o an uygun SPY yoksa `atama.oneri_bul` 30 dk adımlarla (10:00–20:00, 7 gün) ilçedeki bir SPY'nin ileri-saat kurallarına uyan ilk saati bulur; çağrıda `oneri` {tarih,saat,gunYazi,repId,repAd} durur, müşteriye bildirim gider, uygulamada "Bu saati kabul et / Başka saat seç" kartı çıkar (`api/oneri` {id, karar: kabul|red}; kabul → o saate teklif, red → `oneriYok`, çağrı kimse almadı olarak bekler, müşteri `mDegistir` ile saat seçer). Uygun SPY çıkarsa öneri kalkar, çağrı doğrudan teklif edilir. 5 hareketli örnek SPY (`personel.SIM_SPYLER`, id h1–h5, `sim: true`): ilçelerinde sin dalgasıyla dolaşır (`konum.gezi_konum`, takip aynı formülü `animKonum`'da çalıştırır), atamaya gerçek SPY gibi girer, teklifi 4 sn sonra kendiliğinden kabul eder (`sunum.sim_kabul`, bekçi 1 sn). Uygulama `veri/spyler.js` yanıtına `window.TY_SPYLER_SIM` eklenir (müşteri tarafı bilgi kartı; SPY girişinde görünmez). Konum önceliği `konum.konum_ve_kaynak`.
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
- **Hareketli SPY yolu (2026-11-25):** `veri/sim-yollar.js` (`window.TY_SIM_YOL={id:[[lat,lng],…]}`, `python araclar/sim_yol_uret.py` ile OSRM'den üretilir, `STATIK_KOK`'ta) her örnek SPY için ilçesinde kapalı tur; konum = (t·hiz + faz·uzunluk) mod uzunluk, merkez `konum.gezi_konum` ve takip `geziKonum` aynı formül. Çağrı `yolda` olunca 2 sn içinde ilerletilmezse `sunum.yurume_baslat` yürümeyi başlatır (`yolaCikis`, `YOLA_CIKIS_BEKLEME_SN=2`).
- **Çağrı ekle → hesap (2026-11-25):** `cagri_ekle` ad+telefonla `musteri.hesap_ac(..., "yonetici")` açar (aydınlatma tarihi dolu); `bos_kimlikler` listesinde görünür. Çağrı `kaynak: yonetici` ise `sunum.sim_kabul` atlanır.
- **Otomatik ilerlet ve randevu bekleyen çağrı (2026-11-25):** `sunum.ilerlet` önce `oneriKabul` olmayan açık çağrıları ilerletir; yalnız onlar bitince (tamamlandı) `oneriKabul` çağrıları ilerler.
