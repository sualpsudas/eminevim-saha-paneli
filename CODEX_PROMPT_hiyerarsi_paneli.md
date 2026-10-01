# Codex Prompt — Hiyerarşik Performans Panelleri + iPhone Test Sürümü

> Aşağıdaki metnin tamamını Codex'e ver.

---

## Bağlam

Proje: **Eminevim Saha Paneli / Tasarruf Yanımda** (`sualpsudas/eminevim-saha-paneli`, dal `master`, GitHub Pages: https://sualpsudas.github.io/eminevim-saha-paneli/).

Mimari (mutlaka koru):
- Tüm uygulama tek dosyada: `Eminevim Saha Paneli.dc.html` (dc-runtime şablonu: `<sc-if>`, `<sc-for>`, `{{ binding }}`, `class Component extends DCLogic` + `state` + render'da hesaplanan alanlar).
- `support.js` **üretilmiş dosya, elle düzenleme.**
- `assignment.js` (SPY atama), `map.html` (Leaflet/OSM harita, iframe + postMessage), `sw.js` (PWA cache, şu an `eminevim-v4`), `manifest.json`, `index.html` (yönlendirme).
- Renk token'ları `--bg --card --ink --dim --line --tintGreen --tintRed --tintGold`, ana yeşil `#276F4E`, fontlar Manrope/Inter. Koyu tema destekli; yeni ekranlar da token kullanmalı.
- Giriş ekranında sağ üstte **"Personel Girişi"** butonu var → `personelLoginOpen` modalı → `submitPersonelGiris` ile SPY paneline giriyor.
- `PROJE_ILERLEME.md` ilerleme kaydı; iş bitince tarihli not ekle.

Mevcut müşteri akışı, SPY (Tasarruf Yanımda saha) akışı, Admin paneli ve harita **bozulmamalı.**

---

## Adım 0 — Yedekleme (her şeyden önce)

1. Çalışma ağacının temiz olduğunu doğrula.
2. Mevcut durumu etiketle ve dal olarak sakla:
   - `git tag yedek/hiyerarsi-oncesi-2026-10-01`
   - `git branch yedek/hiyerarsi-oncesi`
3. Ek olarak dosya yedeği: `backup/2026-10-01/` klasörüne `Eminevim Saha Paneli.dc.html`, `sw.js`, `manifest.json`, `assignment.js`, `map.html` kopyala. `backup/` klasörünü `sw.js` ASSETS listesine ekleme.
4. Yeni geliştirmeyi `feature/hiyerarsi-panelleri` dalında yap. `master`'a merge ve push etmeden önce bana sor.

---

## Adım 1 — Organizasyon hiyerarşisi (demo veri modeli)

Raporlama zinciri:
**Personel (SPY) → Takım Lideri (TL) → Saha Grup Lideri (SGL) → Alternatif Satış Kanalı Müdürü (ASK Müdürü)**

Coğrafya: **4 Saha → 22 Bölge → 220 Şube**, toplam **250 personel**.
- Her saha bir SGL'ye ait. Bölgeler ve şubeler sahalara **dengesiz** dağılmalı (ör. saha başına 3–9 bölge, bölge başına 4–18 şube, şube başına 0–3 personel; bazı şubeler personelsiz).
- Takım liderleri şehirlerde aktif; her TL **1 veya birden fazla şubeden** sorumlu (ör. ~45 TL; bazı TL'lerde 2 personel, bazılarında 12). Bir TL'nin şubeleri aynı saha içinde olmalı.
- Tüm SGL'ler ASK Müdürü'ne bağlı.

Uygulama:
- Ayrı bir `org-data.js` dosyası oluştur: **seed'li (deterministik) üretici** — her yüklemede aynı veri. Gerçek Türk şehir/ilçe adları kullan (İstanbul, Ankara, İzmir, Bursa, Antalya, Konya, Adana, Kayseri, Gaziantep, Samsun, Trabzon, Eskişehir vb.); şube adı "Kadıköy Şubesi" formatında.
- Veri yapısı: `sahalar[]`, `bolgeler[]`, `subeler[]`, `takimLiderleri[]`, `personeller[]` — her kayıtta `id`, `ad`, üst kırılımın id'si (`sahaId`, `bolgeId`, `subeId`, `tlId`, `sglId`).
- Mevcut `spylerList` içindeki SPY'ler (Onur K., Derya A., Berk C.) bu 250 personelin içinde yer almalı ve canlı SPY akışıyla bağlantılı kalmalı.
- İleride gerçek backend'e geçiş için tek bir veri erişim katmanı yaz (`OrgData.getPeriod(scope, id, periodKey)` gibi); UI doğrudan diziye değil bu katmana bağlansın. `window.EMINEVIM_CONFIG.orgEndpoint` tanımlıysa oradan çekmeye hazır yer tutucu bırak.

---

## Adım 2 — Metrikler

Her personel için **günlük** demo metrik üret (son 400 gün, seed'li, hafta sonu düşük, ay sonu hafif artış, kişiden kişiye gerçekçi performans farkı):

| Öncelik | Metrik | Tanım |
|---|---|---|
| 1 | **H/G** | Hedef / Gerçekleşme oranı = Gerçekleşen ciro ÷ ciro hedefi (%). Renk: ≥%100 yeşil, %80–99 sarı/altın, <%80 kırmızı (token'larla). |
| 2 | **Ciro** | ₺ (kompakt gösterim: 1,2 Mn ₺ / 845 B ₺) |
| 3 | **Randevu** | adet |
| 4 | **Açılan Kart** | adet |
| 5 | **Kayıt** | adet |
| 6 | **Dönüşüm** | Randevu → Kart %, Kart → Kayıt %, Randevu → Kayıt % (huni) |

- Hedefler personel bazında aylık tanımlansın; üst kırılımların hedefi = altındakilerin toplamı. Gün/hafta hedefi aylık hedeften iş günü oranıyla türetilsin.
- Tüm toplamalar hiyerarşi boyunca yukarı doğru **toplam** (ciro, adet) ve **oran** (H/G, dönüşüm → toplamlardan yeniden hesapla, ortalama alma).
- Dönemler: **Gün, Hafta, Ay, Yıl**. Her biri önceki eşdeğer döneme göre değişim (▲/▼ %) göstersin.

> Not: "H/G" kısaltmasını Hedef/Gerçekleşme olarak varsaydım. Kodda tek bir sabitte (`METRIK_TANIMLARI`) tanımla ki etiketi/formülü kolayca değiştirebileyim.

---

## Adım 3 — Personel Girişi'nin genişletilmesi

Personel Girişi modalında, mevcut "Giriş Yap" (Personel/SPY) butonunun **altına** 3 rol butonu ekle:
- **Takım Lideri**
- **Saha Grup Lideri**
- **Alternatif Satış Kanalı Müdürü**

Her biri demo kullanıcıyla giriş yapar (ör. TL için 2+ şubeli bir TL, SGL için orta büyüklükte bir saha). Giriş sonrası `panel` state'i role göre değişir: `spy | tl | sgl | ask`. Panelden çıkış (Ayarlar → Çıkış) giriş ekranına döner.

---

## Adım 4 — Rol panelleri (ortak iskelet, kapsama göre filtre)

Tüm yönetici panelleri **aynı bileşen yapısını** kullansın, sadece kapsam (scope) değişsin. Alt navigasyon 4 sekme:

### 4.1 Performans (ana sekme)
- Üstte **dönem anahtarı** iki varyasyonlu segment: **Kısa dönem (Gün | Hafta)** ve **Uzun dönem (Ay | Yıl)**. Varsayılan: Gün.
- **Hedef kartı (hero):** Kapsamın H/G yüzdesi büyük rakam + ilerleme halkası/çubuğu, altında "Ciro 4,2 Mn / Hedef 5,0 Mn". Önceki döneme göre ▲/▼.
- Altında **kompakt 2x2 KPI ızgarası:** Ciro · Randevu · Açılan Kart · Kayıt (her biri değer + hedefe göre mini çubuk + değişim oku).
- **Dönüşüm hunisi:** Randevu → Kart → Kayıt tek satırlık yatay huni, oranlar yüzde.
- **Mini trend:** seçili dönemin kırılımı (Gün=saatlik veya son 7 gün, Hafta=günler, Ay=haftalar, Yıl=aylar) sparkline/mini sütun; sadece ciro ve H/G.

### 4.2 Ekibim (kendi ilgi alanı)
- Doğrudan altındaki birimlerin **sıralı listesi**: TL → personeller; SGL → TL'ler (+ bölge/şube kırılımına geçiş); ASK Müdürü → 4 saha / SGL'ler.
- Her satır tek satır yüksekliğinde: ad · H/G rozeti · ciro · R/K/K (randevu/kart/kayıt) küçük sayılar.
- Sıralama çipi: H/G, Ciro, Randevu, Kart (varsayılan H/G, azalan). "Dikkat" filtresi: H/G < %80 olanlar.
- Satıra dokununca **drill-down**: o birimin Performans görünümü (aynı bileşen), üstte breadcrumb (ASK › Marmara Saha › Ankara Bölge › Çankaya Şubesi › Onur K.). Geri ile yukarı çık. En alt seviye personel kartı.

### 4.3 Saha Canlı (Tasarruf Yanımda — şu an ne oluyor)
- Kapsamdaki **canlı** durum: aktif SPY sayısı (Müsait / Molada / Görüşmede), bekleyen talep, yolda, görüşmede, bugün tamamlanan, bugün alınan randevu.
- **Son 24 saat / son 7 gün** akış listesi (kısa): "14:32 · Derya A. · Üsküdar · Görüşme tamamlandı · Sözleşme imzalandı".
- Mevcut SPY/Admin canlı state'inden (`spylerList`, `basvurular`, `spyDurum`, `tamamlanan`, randevular) beslensin; kapsam dışındaki veriler gizlensin.
- İsteğe bağlı: mevcut `map.html` iframe'ini kapsamla filtreli küçük harita olarak yeniden kullan (Admin harita mantığını tekrar kullan, kopyalama).

### 4.4 Genel (büyük resim)
- Kullanıcının **üst hiyerarşisinin** rakamlarını salt okunur göster: TL kendi şubeleri + bağlı olduğu saha + şirket geneli; SGL kendi sahası + şirket geneli; ASK Müdürü şirket geneli + 4 sahanın karşılaştırması.
- Her seviye tek kompakt satır: H/G · Ciro · Randevu · Kart · Kayıt.
- **Sıralama bilgisi:** "Takımınız sahada 3./11", "Sahanız 2./4" gibi.
- Kardeş birimlerin detayına erişim yok (sadece sıra ve toplam); detay sadece kendi alt ağacı için.

### Yetki kuralı
- Personel: sadece kendisi + (Genel sekmesinde) takımının/sahasının toplamları.
- TL: kendi şubeleri ve personelleri.
- SGL: kendi sahası (bölgeler, şubeler, TL'ler, personeller).
- ASK Müdürü: hepsi.
Bunu tek bir `kapsamFiltrele(kullanici, veri)` fonksiyonunda topla.

---

## Adım 5 — Personel (SPY) arayüzünün güncellenmesi

Mevcut SPY paneline (liste/harita/profil akışını bozmadan) **"Performansım"** sekmesi ekle (veya Profil'in en üstüne kart olarak koy — alt nav 4 sekmeyi geçmesin):
- Aynı Performans bileşeni, kapsam = tek personel.
- Kısa (Gün/Hafta) ve Uzun (Ay/Yıl) dönem anahtarı.
- Hedef kartı (H/G), 2x2 KPI, dönüşüm hunisi.
- Altında "Takımımda sıram: 4/9" ve takım ortalamasına göre fark.

---

## Adım 6 — Mobil / kompaktlık kuralları

- Hedef cihaz iPhone (375–430 px genişlik). Her panelin **ilk ekranı kaydırmadan** H/G + 4 KPI + dönüşümü göstermeli.
- Rakamlar büyük ve kalın (Manrope 800), etiketler 10–11 px, satır yüksekliği ≤ 48 px, dokunma hedefi ≥ 44 px.
- Kompakt sayı biçimi (`Intl.NumberFormat('tr-TR', { notation: 'compact' })`), ₺ ve % Türkçe biçimde.
- Renk anlamı sadece H/G ve değişim oklarında; geri kalan nötr. Koyu temada token'lar.
- Dönem değişince iskelet yükleme (mevcut yükleme stilini kullan), boş durum ekranları.
- `safe-area-inset` (iPhone çentiği/home bar) için padding.

---

## Adım 7 — iPhone'a indirilebilir test sürümü

**7a. PWA (zorunlu, ilk teslim):**
- Mevcut GitHub Pages yayını üzerinden "Ana Ekrana Ekle" ile tam ekran çalışmalı.
- `manifest.json`: `display: standalone`, uygun `name`, `start_url`; HTML `<head>`'e `apple-mobile-web-app-capable`, `apple-mobile-web-app-status-bar-style`, `apple-touch-icon` (180px) etiketleri.
- `sw.js`: cache adını `eminevim-v5` yap, `org-data.js`'i ASSETS'e ekle, offline açılış çalışsın.
- `?rol=tl|sgl|ask|spy` URL parametresiyle doğrudan ilgili panele demo girişi (test kolaylığı).
- README'ye/`PROJE_ILERLEME.md`'ye "iPhone'a kurulum" adımlarını yaz (Safari → Paylaş → Ana Ekrana Ekle) ve QR kod (`eminevim-qr.png`) güncel URL'yi gösteriyor mu kontrol et.

**7b. Native sarmalayıcı (hazırlık — çalıştırmadan önce bana sor):**
- Capacitor ile iOS projesi iskeleti (`capacitor.config.json`, `www/` kopyalama script'i). Ben Windows kullanıyorum, Mac yok: bulut derleme için **Codemagic** (`codemagic.yaml`) ile TestFlight'a gönderim yapılandırması hazırla.
- Apple Developer hesabı, bundle id, sertifika/imza gibi sırları dosyaya yazma; `codemagic.yaml`'da ortam değişkeni adlarıyla bırak ve gereken adımları `IOS_TESTFLIGHT.md` dosyasında listele.

---

## Adım 8 — Doğrulama ve teslim

- Tarayıcıda 390x844 viewport'ta her rol için uçtan uca test: giriş → Performans (4 dönem) → Ekibim drill-down → Saha Canlı → Genel → çıkış.
- Hiyerarşi tutarlılık testi (konsolda veya küçük `tests/org-data.test.js`): 4 saha, 22 bölge, 220 şube, 250 personel; her seviyede alt toplamların toplamı = üst toplam; H/G toplamlardan hesaplanmış.
- Mevcut müşteri + SPY + Admin akışlarının regresyon kontrolü (konu seç → çağır → konum → yolda → ulaştı → tamamla → puanla).
- Koyu tema kontrolü.
- `PROJE_ILERLEME.md`'ye tarihli not ekle.
- Commit'leri `feature/hiyerarsi-panelleri` dalına küçük ve anlamlı parçalar halinde at. Commit mesajlarına **Co-Authored-By satırı ekleme.** `master`'a merge ve push için onay iste.

---

## Belirsizlikler (karar verirken bana sor, tahminle ilerleme)

- H/G'nin tanımı farklıysa (ör. Hafta/Gün değil, Hedef/Gerçekleşme dışında bir oran).
- Ciro hedeflerinin kaynağı ve büyüklüğü (demo için personel başı aylık 1,5–4 Mn ₺ varsayılabilir).
- Native iOS (7b) adımına geçilip geçilmeyeceği.
