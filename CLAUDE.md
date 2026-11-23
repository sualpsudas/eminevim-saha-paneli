# Tasarruf Yanımda

Mevcut saha satış gücüne **müşteriden doğrudan gelen talep kanalı** eklemek: ekip müşteri bulmaya devam eder, görüşmek isteyen
müşteri web formundan veya uygulamadan temsilci (SPY) çağırır; aktif SPY'ler uygun yer ve saatte gider. Satış artışı kanıtlanmış değil,
pilot bölge denemesinde ölçülecek. Klasör `eminevim-saas`, depo `sualpsudas/eminevim-saha-paneli` (eski adlar; değiştirme kararı yok,
Pages adresi değişir). **Tasarım kararı henüz verilmedi:** mevcut prototip kesin değil, ekranları "karar" sayma.

## Ne zaman hangi dosya
| İş | Önce oku |
|---|---|
| Ekran, akış, metin, personel, senaryo, taslak, canlı test davranışı | `URUN_KURALLARI.md` (çelişkide o geçerli) |
| Kod, merkez, bildirim, müşteri hesabı, web formu üretimi, iPhone, linkler.html görünümü | `TEKNIK.md` (ilgili başlık) |
| Proje amacı/ilkesi, plan ve aşamalar, belge işi, "bu neden böyle" sorusu | `KARARLAR.md` (ilgili başlık) |
| Atama kuralları | `rapor/tasarruf-yanimda-proje-calismasi/10-atama-ve-rota.md` |
| Tanıtım videosu | `video/OKUBENI.md` |
- `PROJE_ILERLEME.md` çok büyük: tamamını okuma; her çalışmadan sonra sonuna tarihli kısa not ekle, gerekirse yalnız son kayıtlara bak.
- `AGENTS.md` Codex rehberidir; buradaki bir kural değişince onu da güncelle.
- Yeni karar nereye: kalıcı kural → buraya (ürün/ekran kuralıysa `URUN_KURALLARI.md`), teknik ayrıntı → `TEKNIK.md`, gerekçe/tarihçe → `KARARLAR.md`.

## Kurallar
- **Ortak dil:** müşterinin gördüğü her yerde (ekran, web formu, SMS) "temsilci"; personel, yönetici, takip sayfası ve iç belgelerde "SPY";
  ikisinde de "çağrı". Kod adları (`temsilci`, `TEMSILCI_DETAY`, `assets/temsilci/`) değişmez. Ayrıntı `URUN_KURALLARI.md` → Ortak dil.
- "ASK" yazılmaz: "Alternatif Satış Kanalı". "Pilot" değil "pilot bölge denemesi". "Ayağına gitmek" değil "dilediği yerde ve saatte ulaşmak".
  "Ödül" değil "teşvik". Belgelerde rakip/benzer uygulamaların marka adı yazılmaz. "Yapay zekayla yapılabilir" etiketi kullanılmaz.
- Müşteriye uygulama indirtilmez, önce **web**. Yeni müşteri üyeliksiz; finansman/bütçe yalnız üyelere ("Finansmanlarım").
- Web formunda **e-posta istenmez**; temsilci çağırma isteğe bağlı. Temsilci başvurudan hemen sonra gösterilmez.
- Bütçe hesabı her yerde "Örnek hesaplamadır" notuyla; gerçek yayında şirketin onaylı hesabı + uyum/hukuk onayı şart.
- Görünüm eminevim.com'dan: yeşil #00724c, turuncu düğme #ea803f, Century Gothic (tam liste `TEKNIK.md` → Görünüm). Web ve uygulama uyumlu.
- Web formunun sayfasındaki tüm linkler etkisiz kalır (`data-ty-dis` hariç); `index.html` elle düzenlenmez.
- GitHub Pages kopyası (sunucusuz gösteri) bozulmamalı. `video/` ve `backup/` değişmez.
- Gizli dosyalar depoya ve belgelere girmez: `merkez/gizli_yol.txt`, `merkez/vapid.pem` (silinirse tüm bildirim abonelikleri gider), `*_abonelik.json`.

## Dosyalar
- **Modüler yapı ve IT'ye devir: `IT_DEVIR.md`** (her dış kaynak tek "kapı" dosyasının arkasında; yeni kod bu düzene uyar).
- Uygulama: `Eminevim Saha Paneli.dc.html` (ekranlar) + `uygulama/` (modüller, `support.js`, `canli.js`), `harita/` (map, rota, konum-sec), `index.html`, `sw.js`.
- SPY listesi `veri/spyler.js` **üretilir**: `veri/kaynak/*.csv` + `veri/ayarlar.json` → `python araclar/veri_hazirla.py` (`veri/OKUBENI.md`).
- Web formu: `web-basvuru/form_bolumu.html` düzenlenir → `python olustur.py` ile **mutlaka yeniden üret**.
- Canlı test merkezi: `merkez/` (`sunucu.py` giriş, kod `merkez/ty/` parçaları, `takip.html`, `canli-sw.js`), bağlantı `uygulama/canli.js`.
- iPhone: Capacitor + Codemagic (`IOS_TESTFLIGHT.md`). Taslaklar `taslak/`, proje belgeleri `rapor/`. `senaryo.html` eski çizim tahtası (güncellenmez).
- **Panel `panel.html`** (2026-11-18): ana sayfa kutuları → solda dar dikey menü: Proje Çerçevesi, Tanıtım Videosu, Senaryo 1 (web formundan),
  Senaryo 2 (uygulamadan). Web formu ve uygulama panelden açılmaz (ayrı linkler). Video: yalnız kadın sesli sürüm (başlık sadece "Tanıtım Videosu").
  Senaryolar iki bölmeli (müşteri telefon | SPY tablet) ve **gerçek ekran görüntüleri**: `python araclar/senaryo_goruntu.py`
  (yerel 8799 açıkken) üretir → `senaryo/`. **Uygulama veya web formu ekranı/akışı değişince yeniden çalıştır.** Test `tests/panel-senaryo.py`.

## Çalıştırma ve yayın
- **Merkez (7/24, port 8794):** durdurmak için `python sunucu.py --durdur` (taskkill değil); başlatma Başlangıç kısayolu
  "Tasarruf Yanimda Merkezi" (conda base pythonw). Aynı porta ikinci kopya bağlanmaz; deneme kopyası `TY_PORT=8795 TY_YOL=deneme TY_VERI=<geçici>`.
  `veri/spyler.js` değişince merkez yeniden başlatılır. Dışarıya Tailscale Funnel ayrı yolla.
- **Yayın:** `master` → GitHub Pages https://sualpsudas.github.io/eminevim-saha-paneli/ (~1 dk; `curl ...?t=$RANDOM` ile kontrol).
  Tek paylaşım sayfası `linkler.html`: yeni sayfa eklenince güncelle. Ekibin "Çalışma sayfası": https://sualpsudas.github.io/eminevim-saha-paneli/linkler.html#web-bilgisayar
- **Test:** conda `scrapling` Python + Playwright `channel="chrome"`; yerel `python -m http.server 8799`; merkez akışı `tests/merkez-akis.py`.

## Açık işler
- Plan: 1 Proje Çerçevesi · 2 Araştırma · 3 Yöntem ve Tasarım · (Sunum) · 4 Teslim; 43 iş, 4 kişi. Tek kaynak OneDrive
  `Eminevim\AlternatifSatisKanali\Belgeler\Tasarruf Yanimda Gorev Dagilimi\kaynak\gorev-tanimlari.md`; görev takip `..\gorev-takip`. Ayrıntı `KARARLAR.md`.
- iPhone uygulama kapalıyken bildirim (APNs): YAPILDI, telefonda doğrulandı (2026-11-22). Anahtar yalnız sunucuda: `merkez/apns.p8` + `merkez/apns.json`
  ({key_id, team_id, topic}; ikisi de gitignore). Kod `merkez/ty/apns.py`; conda base'de `pyjwt` + `httpx[http2]` (h2) gerekir.
- **Çok kişili test (2026-11-23 YAPILDI, canlı merkezde yeniden başlatma bekliyor):** `PLAN-test-kimlik.md` — telefon maskesi, kimlik "kullanımda" kaydı, boş kimlik listesi, sıfırlama, yönetici Test paneli (takip sayfasında). Ayrıntı `TEKNIK.md` → Test kimliği. Kalan: iki gerçek telefonla deneme, `tests/merkez-akis.py` güncelleme (Ayarlar'daki Aydınlatma düğmesi kalktı).
- Finansmanlarım rakamları için Eminevim uyum/hukuk onayı.
- Öneri olarak bekliyor: cumartesi yığılmasını rakamla gösteren analiz (SPY raporları), yönetime kısa sunum.
