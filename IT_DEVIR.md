# Tasarruf Yanımda — IT devir rehberi

Bu prototip, şirket sistemlerine **bağlanmadan** çalışacak biçimde yazıldı: her dış kaynak (personel, satış, randevu, konum, bildirim,
SMS, müşteri hesabı, harita) **tek bir dosyanın arkasında** durur. Bu dosyalara "kapı" diyoruz. Bugün kapıların arkasında örnek veri ya da
basit bir dosya var; şirket sistemi bağlanırken **yalnız kapı dosyası değişir**, ekranlar ve geri kalan kod değişmez.

Depo herkese açıktır (GitHub Pages gösterisi). Gerçek kişi, hedef, satış verisi ve gizli anahtarlar depoya konmaz.

## 1. Genel yapı
```
eminevim-saas/
├── Eminevim Saha Paneli.dc.html   ekranlar (müşteri, SPY, yönetici) — tek sayfa, şablon + Component sınıfı
├── uygulama/                      uygulama modülleri (sırası sayfanın <head> bölümünde)
│   ├── servisler.js   DIŞ SERVİSLER  harita altlığı, rota, adres arama adresleri
│   ├── ayarlar.js     uygulama ayarları (hizmet ilçeleri, canlı yoklama aralığı ...)
│   ├── bicim.js       biçim/renk/hesap yardımcıları (iş kuralı yok)
│   ├── finansman.js   FİNANSMAN KAPISI  plan türleri, örnek hesap (senaryoHesapla)
│   ├── personel.js    PERSONEL KAPISI   SPY ayrıntıları (veri/spyler.js'ten), atama mesajı
│   ├── hesap.js       MÜŞTERİ HESABI KAPISI (gösteri modunda yerel; merkezde api/musteri)
│   ├── ornek-veri.js  gösteri verisi (Pages kopyası için)
│   ├── canli.js       merkez bağlantısı (yalnız merkezden açılınca devrede)
│   ├── appointment.js, assignment.js   randevu ve atama yardımcıları (Node testleri var)
│   └── support.js     şablon çalışma zamanı (değiştirilmez)
├── harita/            map.html (Saha Canlı), rota.html, konum-sec.html — Leaflet; adresler uygulama/servisler.js'ten
├── veri/              SPY listesi ve ham şirket verisi (veri/OKUBENI.md)
├── araclar/           veri_hazirla.py (ham veri → SPY listesi), ornek_veri_uret.py (uydurma ham veri)
├── merkez/            canlı test sunucusu (Python, yalnız standart kütüphane + pywebpush)
│   ├── sunucu.py      giriş (çalıştır / --durdur)
│   └── ty/            parçalar — aşağıda
├── web-basvuru/       web formu (form_bolumu.html → python olustur.py → index.html)
└── ios/, codemagic.yaml, scripts/   iPhone paketi (Capacitor)
```

## 2. Kapılar — neyi bağlamak gerekiyor

### 2.1 Personel ve H/G (otomatik SPY listesi)
- **Bugün:** `veri/kaynak/*.csv` (şirket dışa aktarımıyla aynı sütun adları, uydurma değerler) → `python araclar/veri_hazirla.py` → `veri/spyler.js`.
- **Bağlantı:** iki yol var:
  1. En kolayı: şirket sistemi aynı CSV'leri (aynı sütun adlarıyla) her gece `veri/kaynak/`a bırakır, betik çalışır, merkez yeniden başlar.
  2. Doğrudan: `araclar/veri_hazirla.py` içindeki `personel_oku`, `sube_oku`, `hedef_oku`, `satis_oku`, `randevu_oku` fonksiyonları
     veritabanından okuyacak şekilde değiştirilir; dönüş biçimleri aynı kalır.
- Kurallar kodda değil `veri/ayarlar.json`'da (dönem, eşik, günlük randevu hedefi, sayılan durumlar, sütun adları).
- Listedeki alanlar: `id, sicil, ad, cinsiyet, gorev, ilce, mahalle, sube, bolge, klasman, lat, lng, foto, deneyim, puan, gorusme, randevuHG, ciroHG`.
  `id` uygulama içi kimliktir (`spy_ek.csv` → Uygulama Id); şirket kimliği `sicil`.

### 2.2 Canlı konum (saha takip)
- **Bugün:** SPY'nin konumu = son 10 dk içinde gelen canlı konum, yoksa bugünkü son randevusunun yeri, yoksa kayıtlı sabit konum.
- **Giriş:** `POST /<yol>/api/konum` gövde `{"id": "s1", "lat": 41.0, "lng": 29.1}`. Şirketin saha takip sistemi ya da uygulama bu adrese yazar.
  Kod: `merkez/ty/konum.py` (`konum_yaz`, `anlik_konum`). Süre `merkez/ty/ayarlar.py → CANLI_KONUM_DK`.
- Atama (yakınlık puanı) ve Saha Canlı haritası bu konumu kendiliğinden kullanır; `api/durum` yanıtında SPY başına `konumAn` ve `canliKonum`.

### 2.3 Şirkete aktarım (randevu ve aday müşteri kaydı)
- **Bugün:** `merkez/ty/aktarim.py` her yeni çağrıda `merkez/aktarim/musteri_karti.jsonl`, SPY kabul ettikten sonra her durum değişikliğinde
  `merkez/aktarim/randevu.jsonl` dosyasına bir satır yazar (aynı `Id`'nin son satırı geçerli).
- Alan adları şirketin randevu listesi ve müşteri kartı sütun adlarıyla aynıdır (`Şube, Planl. Tarih, Randevu Durumu, Sorumlu Personel, Id ...`).
  Ek öneri alanları: `Sorumlu Personel Sicil`, `Kaynak`. `Kart No` boştur, şirket sistemi verir.
- **Bağlantı:** `aktarim.yaz()` şirketin randevu / müşteri servisine gönderecek şekilde değiştirilir. Hata çağrı akışını durdurmaz.

### 2.4 Satış (ileride saha ekibinden güncelleme)
- Satışlar bugün yalnız H/G hesabına girer (`satis_kaydi.csv`). Uygulamadan satış girişi istenirse: görüşme sonucu (`sonrakiAdim`) zaten
  randevu aktarımında `Randevu Sonucu` olarak gidiyor; satış kaydı şirket sisteminde açılır, ertesi günkü H/G hesabına kendiliğinden girer.

### 2.5 Müşteri hesabı ve SMS
- **Bugün:** hesaplar merkezde (`veri.json → musteriler`: adi, soyadi, aydinlatmaTarih, kampanya + tarihi; oturum jetonu). **Parola yok:**
  telefon + SMS kodu; oturum "Çıkış yap"a kadar telefonda kalır. SMS gönderilmez; kod ekranda gösterilir (test).
- **Tek hesap:** ayrı "Tasarruf Yanımda üyeliği" açılmaz. Gerçek yayında Eminevim'in var olan üye/müşteri hesabı kullanılır: gerçek Eminevim
  üyeleri aynı hesapla (aynı telefon) girer, yeni müşteri o sistemde aday olarak açılır.
- **Bağlantı:** `merkez/ty/musteri.py → kod_gonder()` SMS servisine bağlanır ve kod yanıtta **dönmez**; `musteri_islem()` hesap okuma/açmayı
  Eminevim üye sistemine yönlendirir (islem: kod, dogrula, kayit, web, oturum, cikis).
- **KVKK:** aydınlatma metni gösterilir, müşteri "okudum, bilgilendirildim" kutusunu işaretler (merkez `aydinlatmaOnay` + `aydinlatmaTarih` = onay anı); açık rıza yalnız isteğe bağlı ticari elektronik ileti için (ayrı kutu, `kampanya`).
  Uygulamadaki ve web formundaki metinler örnektir: yayından önce Eminevim uyum/hukuk onayı gerekir. Hukuki sebep, saklama süresi ve
  İYS (ileti izin sistemi) kaydı şirket sürecine göre netleşir. Metin tek dosyada: `uygulama/aydinlatma.js` (saklama süreleri
  örnek: 2 yıl / 10 yıl / izin için 3 yıl). İzin değişikliği `musteri_islem(islem="izin")` → İYS'ye bu noktadan bildirilir.
  Uygulama tarafı: `uygulama/hesap.js` (yalnız gösteri modunda kullanılır).

### 2.6 Bildirim
- **Bugün:** Web Push (`merkez/ty/bildirim.py`, pywebpush; anahtar `merkez/vapid.pem` yalnız sunucuda).
- **Bağlantı:** `bildir()` (SPY'ye) ve `bildir_musteri()` iPhone bildirimine (APNs) ve/veya SMS'e bağlanır; çağıran kod değişmez.
  iPhone uygulaması kapalıyken bildirim için APNs anahtarı + Capacitor bildirim eklentisi gerekir (yapılmadı).

### 2.7 Depo (veritabanı)
- **Bugün:** tek JSON dosyası (`merkez/veri.json`), her istek kilit altında oku → değiştir → yaz (`merkez/ty/depo.py`).
- Yapı: `{surum, sifirlama, spyler{id: {...liste alanları, durum, sonGorulme}}, kayitlar{id: çağrı}, musteriler{tel: hesap}, olaylar[]}`.
- **Bağlantı:** `depo.oku()` / `depo.yaz()` veritabanına bağlanır; çok sunuculu yapıda kilit yerine satır kilidi / işlem (transaction).

### 2.8 Atama kuralı
- `merkez/ty/atama.py` (eleme + puan; varsayılan seçenekler `merkez/ty/ayarlar.py → ATAMA_VARSAYILAN`, canlı testte değiştirilen `veri["atamaAyar"]`). Yol km/süresi `merkez/ty/yol.py` (YOL KAPISI, şu an OSRM genel sunucusu), tipik trafik çarpanı `merkez/ty/trafik.py` (TRAFİK KAPISI, İBB açık verisinden `veri/trafik-carpan.json`, üretici `araclar/trafik_hazirla.py`). Kural belgesi: `rapor/tasarruf-yanimda-proje-calismasi/10-atama-ve-rota.md`.

### 2.9 Harita, rota, adres arama
- `uygulama/servisler.js` (`window.TY_SERVISLER`): bugün OpenStreetMap altlığı, OSRM rota, Nominatim adres arama (ücretsiz, deneme amaçlı).
  Şirket kendi servisini kullanacaksa yalnız bu dosyadaki adresler değişir (ya da sayfadan önce `window.TY_SERVISLER` tanımlanır).
- **KVKK notu (yurt dışı aktarım):** bu ücretsiz servisler yurt dışındaki sunuculardır; adres arama ve rota isteğinde müşterinin seçtiği
  konum/adres onlara gider. Gerçek yayında yurt içi ya da sözleşmeli bir harita servisi kullanılmalı veya yurt dışı aktarım KVKK m.9'a göre
  ele alınmalı (aydınlatma metninde de yazılmalı). Web Push bildirim servisleri (Apple/Google) için de aynı değerlendirme yapılır.

### 2.10 Finansman hesabı
- `uygulama/finansman.js → senaryoHesapla`: **örnek** formül. Gerçek yayında şirketin onaylı hesabı + uyum/hukuk onayı şart.

## 3. Merkez parçaları (`merkez/ty/`)
| Dosya | Ne |
|---|---|
| `ayarlar.py` | yollar, port, atama sabitleri, sunulan dosyalar |
| `yardim.py` | zaman, metin, uzaklık, olay kaydı |
| `personel.py` | SPY listesini `veri/spyler.js`'ten okur |
| `depo.py`, `konum.py`, `atama.py`, `yol.py`, `trafik.py`, `bildirim.py`, `musteri.py`, `dogrulama.py`, `aktarim.py` | kapılar (yukarıda; `dogrulama.py` kapıda QR/kod: gerçek sistemde SPY kimliği personel girişinden) |
| `islemler.py` | istek kuralları: `api/cagri, kayit, mesaj, spy, aktar, konum, kod, musteri, dogrulama, sifirla` |
| `api.py` | HTTP sunucusu: adresler, dosya sunma, `api/durum`, başlat/durdur |

## 4. Çalıştırma ve test
- Merkez: `python merkez/sunucu.py` (127.0.0.1:8794/<gizli yol>/), durdurma `python merkez/sunucu.py --durdur`.
  Deneme kopyası: `TY_PORT=8795 TY_YOL=deneme TY_VERI=<geçici dosya> TY_AKTARIM=<geçici klasör>`.
- Testler: `npm test` (Node), `tests/merkez-akis.py` (deneme merkezi 8795 açıkken), `tests/*.py` Playwright (yerel `python -m http.server 8799`).
- iPhone paketi: `npm run web:sync` → `www/` (Capacitor), derleme Codemagic (`IOS_TESTFLIGHT.md`).
