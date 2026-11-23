# Çok kişili test: kimlik havuzu, telefon biçimi, sıfırlama, test paneli

Karar tarihi: 2026-11-23 (kullanıcı onayladı). **Adım 1-7 aynı gün kodlandı** (durum için aşağıdaki "Yapılanlar").
Her adımdan sonra: bilgisayarda Playwright kontrolü, `tests/merkez-akis.py`, commit + push. Merkezde kod
değişince merkez düzgünce yeniden başlatılır (`python sunucu.py --durdur`, sonra başlat; taskkill değil).

## Amaç
Başkalarının iPhone'una (TestFlight) kurulacak. Herkes müşteri olarak girip devam edecek; yönetici panelinden
hepsi izlenip "onaylandı" vb. geri dönüş bildirimi verilebilecek. Aynı kimliği iki kişi kullanmasın.

## Kullanıcı kararları
- Kimlik seçimi serbest: kişi kendi kimliğini de başka bir kimliği de seçebilir (test aşaması).
- **Çıkış yapınca kimlik o kişinin olmaktan çıkar** (serbest kalır); başkası alabilir. "Aynı kişi geri döner" özel durumu yok.
- Telefon: **+90 sabit ön ek**, kişi 5 ile başlayan 10 haneyi yazar. Biçim `+90 (5__) ___ __ __`, adım adım dolar, yalnız rakam.
- Telefon girilen **her yerde** zorunlu biçim (giriş, yeni üyelik, temsilci isteği, yönetici/personel formları…).
- "Test verisini sıfırla": tüm hesaplardan çıkış yaptırır, "kullanımda" işaretleri silinir, veri ilk haline döner.

## Adımlar (bu sırayla)
1. **Telefon biçimi.** Tek bir ortak giriş (maske) kuralı: yalnız rakam, +90 (5__) ___ __ __. Tüm `type=tel` /
   `inputmode="tel"` alanlarında kullan (dc.html: kodTel, yaTel, yeni üyelik, personel/yönetici formları; grep ile bul).
   Eksik/geçersiz numarada düğme pasif. Kayıtta hep 10 hane (5XXXXXXXXX) saklanır; gösterim biçimi ayrı.
2. **"Kullanımda" kaydı (merkez).** `merkez/ty`: bir örnek müşteri/yeni kimlik giriş yapınca cihaza bağlı olarak
   işaretlenir (cihaz kimliği = mevcut abonelik/oturum anahtarı); çıkışta (çıkış isteği) serbest. Başka cihaz seçemez,
   o numarayla giriş yapamaz. Yeni API: boş kimlikleri listele, al, bırak. Sıfırlama hepsini temizler.
3. **Giriş listesi (uygulama).** "Örnek müşteri seçin" listesi merkezden gelir, yalnız boşları gösterir
   (`uygulama/ornek-veri.js` ORNEK_MUSTERILER + `merkez/ty/musteri.py` ile aynı kaynak; ikisi tutarlı kalsın).
   Hepsi doluysa "Hepsi kullanımda" mesajı. Seçilmiş numara elle de girilemez.
4. **Yeni üyelik.** Ad, soyad ve numara "seçilmemiş" havuzdan önerilir; aynı numarayla ikinci kayıt reddedilir.
5. **Personel listesi.** Aynı mantık: seçilen personel başkasına görünmez, çıkışta serbest kalır.
6. **Sıfırlama tamamlama.** `merkez/ty/islemler.py` `sifirla()` zaten veriyi yedekleyip boşaltır, müşteri abonelerini
   siler, `sifirlama` sürümünü artırır (cihazlar eski kayıtları bırakır). Eksik: "kullanımda" işaretlerini silmek ve
   personel oturumlarını da kapatmak. Telefonlar bir sonraki açılışta/foreground'da haberleşir.
7. **Test paneli (yönetici içinde, en son).** Katılımcı listesi (ad, son görülme, bildirim açık mı, adım, zaman çizelgesi),
   hızlı yanıt düğmeleri (Onayla, Temsilci ata, Randevu kabul/iptal, test bildirimi, serbest mesaj; tek kişiye ya da hepsine),
   bildirim günlüğü (kime, ne zaman, Apple yanıtı), "bu kimliği serbest bırak" düğmesi. Test kayıtları "TEST" etiketli;
   sıfırlama yalnız onları siler. Yalnızca yönetici görür. İlk sürüm: liste + yanıt düğmeleri + günlük; senaryo otomasyonu sonra.

## Dikkat
- Merkez canlı servis: kod değişince yeniden başlatma gerekir (kısa kesinti).
- `tests/merkez-akis.py` örnek müşteriyi seçerek ilerliyor; yeni kurala göre güncellenmeli (şu an 8795 deneme merkezi ile koşar).
- Çok cihazlı senaryo yalnız iki gerçek telefonla doğrulanabilir; kullanıcıdan birlikte deneme iste.
- Apple tarafı kullanıcıya ait: iç test (en çok 100 App Store Connect kullanıcısı, incelemesiz) ya da dış test grubu
  (link, ilk sürümde kısa beta incelemesi). Gerekirse adım adım yaz. Kaç kişi/kimler henüz belli değil.
- Aynı oturumda UI sorunları (klavye, düğme) için bkz. CLAUDE.md "iPhone" notları; Codemagic derleme 15 son derleme.

## Yapılanlar (2026-11-23)
1. Telefon maskesi: `bicim.js` (`telMaske`, `telGecerli`), uygulamada giriş + temsilci isteği + web formu; geçersizde düğme pasif (web formunda hata satırı).
2. "Kullanımda" kaydı: `merkez/ty/musteri.py` (`kimlik_*`), cihaz kimliği `ty-cihaz`.
3. Giriş listesi merkezden (`islem: bos`), hepsi doluysa "Kayıtlı kimliklerin hepsi kullanımda".
4. Yeni üyelik önerisi merkezden (`islem: oner`); aynı numarayla ikinci kayıt zaten reddedilir.
5. Personel: `api/kimlik` (al/bırak/boş), liste başkasının aldığını göstermez, çıkışta serbest.
6. Sıfırlama: kimlikler silinir, personel girişe döner (müşteri zaten dönüyordu).
7. Test paneli: `merkez/takip.html` + `ty/testpanel.py` (katılımcılar, hızlı yanıtlar, bildirim günlüğü, serbest bırak).
Sınanan: deneme merkezinde (8795) iki ayrı tarayıcıyla kimlik alma/bırakma/başkasının göremeyişi, personel, sıfırlama, test paneli. Sınanmadı: gerçek iPhone ve gerçek bildirim.
Açık: personel "serbest bırak" yalnız listeyi açar (cihaz bir sonraki açılışta kimliği yeniden alır); `tests/merkez-akis.py` Ayarlar'daki kaldırılmış düğmede takılıyor.
