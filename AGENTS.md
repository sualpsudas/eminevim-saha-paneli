# Codex çalışma rehberi — Tasarruf Yanımda

Bu depo uzun süredir emek verilerek geliştirilen çalışan bir prototiptir. **Önce oku, sonra küçük ve geri alınabilir adımlarla değiştir,
test et, kanıt göster.** Emin olmadığın her şeyde dur ve kullanıcıya sor. Kullanıcı teknik değil: Türkçe, sade, numaralı adımlarla yaz.

## 1. Başlamadan önce (her seferinde)
1. `git pull origin master` ve `git status`. Çalışma alanında senin olmayan değişiklik varsa **dokunma**, kullanıcıya söyle.
2. Şu dosyaları oku: `CLAUDE.md` (proje kararları), `URUN_KURALLARI.md` (ekran, akış, metin kuralları — çelişkide bu geçerli),
   işin ilgilendirdiği bölümde `rapor/tasarruf-yanimda-proje-calismasi/10-atama-ve-rota.md` (atama kuralları).
3. Değiştireceğin kodu oku; aynı işi yapan başka yer var mı ara (`grep`). Tahminle değiştirme.
4. Kullanıcıya 3-5 maddelik plan yaz: **ne değişecek, hangi dosyalar, ekranda/akışta kullanıcı neyi farklı görecek, ne değişmeyecek.**
   Onay gelmeden başlama.

## 2. Dosya haritası
| Dosya / klasör | Ne | Dikkat |
|---|---|---|
| `Eminevim Saha Paneli.dc.html` | Uygulamanın tamamı (müşteri, SPY, yönetici) | Şablon dili: `{{ }}`, `<sc-if>`, `<sc-for>`; durum `state`, görüntü değerleri `renderVals()`. Çalışma zamanı `support.js` (değiştirme). |
| `canli.js` | Uygulamanın merkeze bağlantısı | `window.TY_CANLI` yalnız merkezden açılınca var; GitHub Pages'te gösteri modu sürmeli. |
| `spyler.js` | 7 SPY listesi (uygulama + merkez ortak) | Değerler uydurmadır; kimlikler (`s1`…) testlerde ve merkez verisinde kullanılıyor. |
| `assignment.js`, `appointment.js`, `org-data.js` | Atama / randevu / örgüt yardımcıları | Node testleri var. |
| `merkez/sunucu.py` | Canlı test merkezi (Python stdlib HTTP, 8794) | Atama, 2 dk kabul, devret, bildirim (Web Push). |
| `merkez/takip.html` | Yönetici "Saha Canlı" sayfası | |
| `merkez/canli-sw.js` | Merkezdeki bildirim servis çalışanı (`sw.js` adıyla sunulur) | Kökteki `sw.js` (Pages) ayrı dosyadır. |
| `web-basvuru/form_bolumu.html` + `olustur.py` | Web formu kaynağı + üretici | `index.html` **üretilir, elle düzenlenmez**: `python olustur.py`. |
| `senaryo.html`, `rota.html`, `konum-sec.html`, `taslak/`, `linkler.html` | Yardımcı sayfalar | |
| `capacitor.config.json`, `codemagic.yaml`, `scripts/`, `ios/` | iPhone (TestFlight) paketi | İmza/sertifika ayarlarına dokunma. |
| `tests/` | Testler (aşağıda) | |
| `video/`, `backup/`, `rapor/` | Tanıtım videosu, eski sürüm yedeği, proje belgeleri | `video/` ve `backup/` **değişmez**. |
| `CODEX_PROMPT_hiyerarsi_paneli.md` | Eski (tarihi) görev metni | Uygulama; geçerli kurallar bu dosyada ve `URUN_KURALLARI.md`'de. |

## 3. Değişiklik kuralları
- **Ortak dil:** müşterinin gördüğü her yerde "temsilci"; personel, yönetici, takip ve iç belgelerde "SPY"; ikisinde "çağrı".
  "ASK" kısaltması yazılmaz: "Alternatif Satış Kanalı". Kod adları (`temsilci`, `TEMSILCI_DETAY`, `assets/temsilci/`) **değiştirilmez**.
- Görünüm eminevim.com değerleriyle: yeşil `#00724c`, turuncu `#ea803f`, kutu `#EEE` (köşe 22px), kart köşesi 14px, yazı `#666`,
  yazı tipi Century Gothic. Yeni bileşen bu değerlerle yapılır.
- Web formunda e-posta istenmez; sayfadaki tüm linkler etkisizdir (`data-ty-dis` hariç) — bu kural korunur.
- Gerçek kişi fotoğrafı kullanılmaz (yalnız sentetik görseller).
- KVKK: kayıtlı olmayan numara KVKK onayı vermeden müşteri hesabına giremez. Web'den gelen müşteride onay web formunda alınır.
- İstenen işin dışına taşan "iyileştirme", yeniden adlandırma, biçim düzeltme, bağımlılık güncellemesi **yapma**. Gördüğün sorunu
  rapor et, kendiliğinden düzeltme.
- Silmek yerine kapatmayı tercih et; büyük bir şeyi kaldırman gerekiyorsa önce sor.

## 4. Test (değişiklikten sonra hepsi geçmeli)
Bilgisayara göre Python yolu değişir; Playwright `channel="chrome"` ile (Chromium indirme yok).
1. Yerel sayfa sunucusu: depo kökünde `python -m http.server 8799`.
2. Deneme merkezi (asıl merkeze dokunmadan), `merkez/` içinde:
   `TY_PORT=8795 TY_YOL=deneme TY_VERI=<geçici klasör>/deneme.json python sunucu.py` — kapatma: `TY_PORT=8795 python sunucu.py --durdur`.
3. `python tests/merkez-akis.py`, `browser-flows.py`, `preparation-popup.py`, `web-flows.py`, `phone-layout.py`, `appointment-list.py`
4. `npm test` (Node testleri).
Bir test bozulursa testi gevşetme/silme; nedenini bul. Test yeni davranışa göre değişecekse bunu planda açıkça yaz.

## 5. Yayınlama
- **GitHub Pages:** `master`'a push = yayın (~1 dk): https://sualpsudas.github.io/eminevim-saha-paneli/ — **depo herkese açık.**
  Push öncesi `git diff --cached` ile gizli bilgi olmadığını kontrol et. Commit'ler küçük ve açıklamalı (Türkçe).
- Git kimliği depoda yerel ayarlı (`sualpsudas <sualpsudas@users.noreply.github.com>`); değiştirme.
- **Merkez (yalnız sunucu bilgisayarı DESKTOP-06OAID8):** sayfa dosyaları (`.html`, `.js`) diskten anında sunulur, yeniden başlatma
  gerekmez. `merkez/sunucu.py` değiştiyse **tek seferde** yeniden başlat: `python sunucu.py --durdur`, sonra Başlangıç kısayolu
  "Tasarruf Yanimda Merkezi" ile (conda base `pythonw.exe sunucu.py`, çalışma klasörü `merkez/`). Laptopta değişiklik yaptıysan
  sunucuda `git pull` gerekir.
- Merkez test verisini sıfırlamak (`api/sifirla`) ve dışarıya açma (Tailscale Funnel) **yalnız kullanıcı isteyince**.
- **iPhone (TestFlight):** derlemeyi Codemagic'te kullanıcı başlatır. Sen derleme başlatma, imza dosyası/anahtar isteme.

## 6. YAPMA listesi (uzun emekle yapılan işler bozulmasın)
1. **Gizli bilgiler depoya girmez, ekrana/belgeye yazılmaz:** `merkez/gizli_yol.txt` (merkezin gizli adresi), `merkez/vapid.pem`
   (bildirim anahtarı — silinirse tüm telefonların bildirim kaydı geçersiz olur), `merkez/veri.json`, `*_abonelik.json`, `yedek/`,
   `.p8/.p12/.mobileprovision`. `.gitignore` kurallarını gevşetme. Kullanıcının kişisel e-postasını hiçbir dış servise gönderme.
2. `git push --force`, geçmişi yeniden yazma, dal/etiket silme (`eski-uygulama-2026-10-21` etiketi kalır), `git reset --hard`,
   `git clean` — **yok**.
3. `output/`, `tests/__pycache__/`, `rapor/Tasarruf_Yanimda_Arastirma_Raporu.pdf` commit'lenmez.
4. Servisler `taskkill` ile **kapatılmaz**; yalnız `--durdur`. Bu bilgisayardaki **diğer projelere/servislere** (İlan/Ürün/Tatil
   Gözetmen, WhatsApp İletici, Ev Alışverişi, Dosya Köprüsü, Görev Takip) dokunma.
5. `video/` (tanıtım sayfası, videolar, altyazılar), `backup/` değiştirilmez.
6. `web-basvuru/index.html` elle düzenlenmez (kaynağı `form_bolumu.html`).
7. Merkez verisi sıfırlanmaz, Funnel/Tailscale ayarı değiştirilmez, Codemagic derlemesi başlatılmaz — kullanıcı açıkça istemedikçe.
8. Depo adı, Pages adresi, klasör adları değiştirilmez (paylaşılmış linkler bozulur).
9. Belgelere/commit'lere yapay zeka model adı yazılmaz.
10. İki denemede çözülemeyen sorunda dur: kök nedeni ve yeni yolu kullanıcıya yaz.

## 7. Bekleyen işler — yapılırsa ne değişir
Her biri ayrı onay ister. Planı yazarken aşağıdaki etkileri kullanıcıya hatırlat.

**A. Web formunda açık rıza (konum) onayı**
- Bugün: web formunda yalnız "Aydınlatma Yazısını okudum" kutusu; uygulamadaki KVKK ekranı ise kişisel veri + **konum** için açık rıza ister.
  Web'den gelen müşteriye uygulamada KVKK sorulmaz.
- Yapılırsa: `web-basvuru/form_bolumu.html`'de "Temsilci çağırmak istiyorum" seçilince ek onay kutusu (uygulamadaki rıza cümlesi), zorunlu;
  `python olustur.py` ile `index.html` yeniden üretilir; merkeze giden çağrıya onay bilgisi (tarih) eklenebilir (`merkez/sunucu.py` `api/cagri`).
  Değişen testler: `web-flows.py`, `merkez-akis.py` (form doldurma adımı). Uygulama tarafı değişmez. Kesin metin Eminevim uyum/hukuk onayına bağlı.

**B. Giriş Yap / Kayıt Ol / Parolamı unuttum sadeleştirme**
- Bugün: "Kayıt Ol" ve "Parolamı unuttum" aynı SMS kodu akışını açar; kayıtlı numara Kayıt Ol'da sessizce parola yenilemeye düşer;
  Giriş Yap'ta kayıtsız numara Kayıt Ol akışına yönlenir (KVKK).
- Yapılırsa: tek giriş "Telefon numaranızla devam edin" → SMS kodu → sistem karar verir (kayıtlı: parola; yeni: ad soyad + parola + KVKK;
  web'den gelen: parola + çağrı açılır). Değişen: uygulamada giriş ekranı ve `kodIleri`/`submitGiris`/`kodAdGerekli`; `URUN_KURALLARI.md`
  giriş bölümü; testler `web-flows.py`, `browser-flows.py`, `phone-layout.py`, `merkez-akis.py` (giriş adımları); `senaryo.html` ve
  taslaklardaki giriş ekranı metinleri kontrol edilir. `video/` değişmez (videodaki eski ekran bilerek kalır).

**C. Müşterinin "kayıtlı" bilgisini merkezde tutmak — YAPILDI (2026-11-11)**
- `merkez/sunucu.py` `api/musteri` (islem: sorgu, kod, kodkontrol, kayit, giris, yenile, web); `veri.json` → `musteriler`.
  Uygulamada `musteriMerkez`, `musteriOturumu`. Parola özeti (`tuz`, `ozet`) hiçbir yanıtta dışarı çıkmamalı.

**D. TestFlight uygulamasına kapalıyken bildirim (APNs)**
- Bugün: tarayıcı/ana ekran sürümünde Web Push çalışıyor; TestFlight uygulamasında (WKWebView) Web Push yok.
- Yapılırsa: Capacitor bildirim eklentisi (`package.json`), `canli.js`'de yerel uygulama için kayıt, merkezde APNs ile gönderim
  (Apple .p8 anahtarı, Key ID, Team ID — kullanıcı sağlar, depoya girmez), Codemagic'te yeni derleme (kullanıcı başlatır).
  Web Push yolu bozulmamalı: `merkez-akis.py` bildirim adımları geçmeye devam etmeli.

**E. SPY Performans'taki "Çağrı size nasıl gelir?" kartını kaldırmak — YAPILDI (2026-11-12)**
- Bugün: SPY Performans sekmesinde, ekip sıralamasının altında "Çağrı size nasıl gelir?" kartı + `pfKural` metni (atama kuralı özeti).
- Yapılırsa: o kart ve `pfKural` değeri kaldırılır; `URUN_KURALLARI.md` SPY ekranı maddesindeki "kural özeti" çıkarılır.
  Değişen testler: bu metni bekleyen test varsa (`merkez-akis.py`, `phone-layout.py` personel sekmeleri) güncellenir.

**F. SPY Görüşmeler: kart dokununca ayrı pencere (kullanıcı istedi, 2026-11-12; sonra yapılacak)**
- Bugün: Görüşmeler sekmesinde solda liste, sağda seçili görüşmenin ayrıntısı aynı sayfada (telefonda alt alta).
- Yapılırsa: görüşme kartına dokununca **yeni bir pencere gibi** açılır (telefonda tam ekran, bilgisayarda ortada pencere):
  müşteri bilgileri, o duruma uygun seçenekler (Kabul et / Devret, Yola çık, gecikme, QR okut, mesajlar, kapanış/özet)
  ve **kapat düğmesi** (sağ üst ✕ + boşluğa dokununca/Geri ile kapanma). Liste ekranı yalnız kartlardan oluşur.
  Yeni çağrı bildirimine dokununca da bu pencere açılır. Değişen: `Eminevim Saha Paneli.dc.html` SPY Görüşmeler bölümü (`tpD*` değerleri),
  testler `merkez-akis.py` (kabul/mesaj/yola çıkış/QR adımları pencereden yapılır), `browser-flows.py`, `phone-layout.py` personel sekmeleri;
  `senaryo.html` SPY ekranları ve `URUN_KURALLARI.md` SPY ekranı maddesi güncellenir.

**G. Personel paneli kozmetik iyileştirmeleri — YAPILDI (2026-11-12; ayrıntı `PROJE_ILERLEME.md`, kural `URUN_KURALLARI.md` → Personel)**
- Kaynak: `design-plans/personel-panel-inceleme-2026-11-12.md` (dış inceleme metni). Yalnız **kozmetik** (boyut, ağırlık, renk tonu,
  hiza, boşluk, seçili görünüm, kontrast); akış, veri, düğme sayısı ve ekran yapısı değişmez.
- Filtre (incelemedeki öneri bu kurallarla çelişirse kural kazanır):
  - Görünüm kaynağı eminevim.com: yeşil #00724c, turuncu ana düğme #ea803f, kart köşesi 14px, hap 22px, yazı tipi GOTHIC/Century Gothic.
    **Inter'e geçilmez, yeni renk paleti toplu getirilmez** (yalnız gerekli tek tük nötr/kehribar ton).
  - Personel kartları düz (beyaz, #DDD çizgi, degrade/cam gölge yok). Mobil yerleşim kuralları (`URUN_KURALLARI.md` "Müşteri uygulaması
    yerleşimi") bozulmaz; masaüstü telefon çerçevesi `linkler.html` önizlemesi için kalır (yalnız sadeleştirilebilir).
  - Yapılmaz: E (Çağrı size nasıl gelir kartı — ayrı karar), F (görüşme penceresi), harita altlığı/doygunluk değişimi, saydırma/zıplama animasyonu.
- Uygun görülenler (sıra): SPY Performans H/G yüzdeleri büyük + %100 hedef çizgisi + sıra/çağrı rakamları nötr; personel alt menü
  etiket kontrastı + aktif sekme vurgusu; Yönetici Performans tablo hizası/başlık kırılması/yüzde tonu/Ekip ortalaması satırı;
  Saha Canlı sayaçlar nötr, örnek zaman etiketi, ortak seçili filtre stili, harita yüksekliği (kişi kartları ilk ekranda);
  Görüşmeler filtre/sayaç/rota düğmesi seçili görünümü; Profil Müsait/Molada seçili görünümü, Çıkış yap nötr.
- Testler: tüm `tests/*.py` + node testleri; önce/sonra ekran görüntüsü (masaüstü 1363×936, telefon 390). Bitince `URUN_KURALLARI.md`
  personel maddesi + `PROJE_ILERLEME.md`; commit + push; merkez tek seferde yeniden başlatılır ve canlıda doğrulanır.

## 8. Bitirirken
1. Tüm testler geçti (çıktının son satırlarını göster).
2. `PROJE_ILERLEME.md`'ye tarihli kısa not; kural değiştiyse `URUN_KURALLARI.md` / `CLAUDE.md` güncel.
3. Commit + push; Pages'te `curl -s "<adres>?t=$RANDOM"` ile yayını doğrula. Merkez değiştiyse yeniden başlat ve yanıt verdiğini göster.
4. Kullanıcıya: ne değişti, ekranda nasıl görünür, neyi kontrol etmeli — kısa, numaralı.
