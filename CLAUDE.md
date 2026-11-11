# Tasarruf Yanımda

Tek proje: **Tasarruf Yanımda** (klasör adı `eminevim-saas`, depo `sualpsudas/eminevim-saha-paneli` eski adlardır).
**Amaç (2026-10-22, kullanıcı onaylı; eski "cumartesi yığılmasını hafta içine yaymak" tanımının yerine):** İlke (kaynak yönetimi) "Saha gücümüzün bir bölümü bizi çağıran müşteriye ayrılır; diğerleri sahada çalışır; dağılım talebe göre ayarlanır" (2026-10-23: saha personeli = **SPY** (Saha Portföy Yöneticisi), "SPY'ler" diye yazılır; ayrı ekip adı YOK, talepleri "Tasarruf Yanımda'da aktif SPY'ler" karşılar; ilk aşamada en başarılı SPY'ler, "teşvik" olarak (ödül değil); sonra kimlerin aktif olacağı belirsiz; atamada ilk ölçüt başarı, yöntem sonra (anlık hizmet/çağrı uygulamaları referans, marka adı yazma); "pilot" değil "pilot bölge denemesi"; "ayağına gitmek" yerine "dilediği yerde ve saatte ulaşmak"; Finansman Aracı + isteğe bağlı bilgiler (meslek) = SPY için görüşme öncesi ön bilgi; aynı gün talepleri de; taşmada takım lideri atar. Düzenleme claude.ai belgesinde (https://claude.ai/artifact/WBKdRt8hzNXjTymiJzqG9p, oturum ister); paylaşım için sitede rapor/proje-cercevesi.html (linkler.html alt satırı) — belge değişince bu sayfa ve md kopyası da güncellenir; md kopyası rapor/tasarruf-yanimda-proje-calismasi/00-proje-cercevesi.md; aynı gün çağrısı prototipte de var (2026-11-11)) (var olan talebe yetişmek talep yaratmaktan verimli — varsayım; ana ölçü temsilci saati başına görüşme/satış). Yani mevcut saha
satış gücüne **müşteriden doğrudan gelen talep kanalı** eklemek — ekip müşteriyi bulmaya devam eder, görüşmek isteyen müşteri
de temsilci (SPY) çağırabilir; temsilci uygun yer/saatte gider, müşteri kimin geleceğini önceden görür, görüşme günü takip eder.
"Talebe ulaşan saha gücümüzü, talebin bize ulaştığı bir kanalla tamamlıyoruz." Cumartesi yoğunluğu ana amaç değil; satış
artışı kanıtlanmış değil, pilotta ölçülecek. Ayrıntı ve araştırma: `rapor/tasarruf-yanimda-proje-calismasi/`.
Uygulama ve web formu bu fikrin ilk aşamalarıdır. İkisi **aynı marka görünümünü** kullanır (`URUN_KURALLARI.md`);
senaryoları birebir aynı olmak zorunda değil.

## Nereye bakılır
- **Ekran, akış, metin, personel, senaryo veya taslak işine başlamadan önce `URUN_KURALLARI.md` dosyasını oku.** Ürün kuralları orada;
  bu dosyadaki Kararlar ile çelişirse orası geçerlidir.
- Tanıtım videosu işi: `video/OKUBENI.md`.

## Klasörler
- `index.html`, `assignment.js`, `org-data.js`, `map.html`, `sw.js` — uygulama (web/PWA). Aynı kod Capacitor ile iPhone'a
  paketlenir (`scripts/prepare-web.mjs`, `IOS_TESTFLIGHT.md`, Codemagic).
- `web-basvuru/` — eminevim.com ana sayfa kopyasında yeni Hızlı Başvuru formu (`form_bolumu.html` düzenlenir,
  `python olustur.py` → `index.html`). Sayfadaki tüm linkler etkisizdir; bu kural korunmalı.
- `taslak/` — sunuma eklenebilir ekran taslakları (`URUN_KURALLARI.md` → Taslak isteği).
- Personel tablet düzeni ve `senaryo.html` (Senaryo sekmesi): `URUN_KURALLARI.md`.
- `video/` — tanıtım videosu: `video/OKUBENI.md`.
- `rapor/benzer-uygulamalar.html` — Türkiye + dünya benzer uygulamalar, yenilik fikirleri, uyarılar (2026-10-21 taslak; kullanıcıyla
  konuşulup ortak rapora dönüşecek). linkler.html'de "Araştırma raporu".
- `backup/2026-10-21-eski-uygulama/` — sade akıştan önceki uygulama (açılır hâlde; git etiketi `eski-uygulama-2026-10-21`).
  Geri dönmek gerekirse: `git checkout eski-uygulama-2026-10-21 -- "Eminevim Saha Paneli.dc.html"`.
- `PROJE_ILERLEME.md` — her çalışmadan sonra tarihli kısa not eklenir.

Yayın: GitHub Pages `master` dalından → https://sualpsudas.github.io/eminevim-saha-paneli/ (depo public; kullanıcı izinli).
Paylaşım için tek sayfa: `linkler.html` → https://sualpsudas.github.io/eminevim-saha-paneli/linkler.html — yeni sayfa eklenince güncelle.
**Çalışma sayfası** (ekibin kullandığı ad): https://sualpsudas.github.io/eminevim-saha-paneli/linkler.html#web-bilgisayar; görev takip sayfasından da bağlantı verilir.
- Telefonda: yalnız sol üstte küçük "Uyg / Web" tuşları, sayfa gerçek boyutunda tam ekran.
- Bilgisayarda: iPhone 15 çerçevesi (393×852); uygulamanın bilgisayar görünümü YOK, Telefon/Bilgisayar seçimi yalnız Web'de.
  Yapılacaklar paneli 2026-11-04 kaldırıldı (görev takibi `gorev-takip`te). Adreslenebilir: `#uygulama-telefon`, `#web-telefon`, `#web-bilgisayar`.

## Kararlar (2026-10-20 / 21)
- Proje adı Tasarruf Yanımda; amaç 2026-10-22'de değişti (yukarıdaki "Amaç"; eskiden cumartesi yığılmasını yaymak). Müşteriye uygulama indirtilmez, önce **web**.
- Uygulama ve web formu ilk aşamalar; aynı marka görünümü (akış birebir aynı olmak zorunda değil, bkz. `URUN_KURALLARI.md`). Yeni müşteri üyeliksiz; finansman/bütçe yalnız üyelere ("Finansmanlarım").
- Web formunda **e-posta istenmez** (2026-10-21 akşam); temsilci bilgisi ve takip linki telefona mesajla gider (önizleme "Gelecek mesajı önizle").
  Web formu **gerçek site formu gibi**, temsilci çağırma **isteğe bağlı** seçenek.
- Web formu demo: her açılışta ve "Yeni başvuru"da örnek bilgilerle dolu gelir (Mehmet Demir, 532 123 45 67; takvimde ilk hafta içi günü + 18:00, haritada Caferağa/Kadıköy, Ev).
- Bütçe hesabı (kaba formül): 2026-10-21 kullanıcı kararıyla web sitesinde de var — sitedeki Konut / Araç / İşyeri kutuları
  (üst menü, Çözümlerimiz kartları, mobil menü) "Ödeme planınızı oluşturun" penceresini açar; hesap uygulamadakiyle aynı
  (`senaryoHesapla`), "Örnek hesaplamadır" notuyla. Gerçek yayında şirketin onaylı hesabı + uyum/hukuk onayı yine şart.
- **Görünüm kaynağı eminevim.com** (2026-10-21): renk/köşe/kutu/yazı tipi sitenin :root değerleri — yeşil #00724c,
  ana düğme turuncu #ea803f, gri hap kutu #EEE (köşe 22px), kart köşesi 14px, yazı #666, çizgi #DDD, açık yeşil #e9f0ed,
  yazı tipi GOTHIC → "Century Gothic" (site dosyası başka adrese izin vermiyor). Uygulama da bu değerlere çevrildi
  (tema değişkeninde `--kutu`); yeni ekran/bileşen bu değerlerle yapılır, web ve uygulama birbirine uyumlu tutulur.
- Temsilci başvurudan hemen sonra gösterilmez: "Görüşme saatinden önce temsilciniz hakkında bilgilendirileceksiniz".
  Yer türü (İş yeri / Ev) yok. Teşekkürde: "Görüşme öncesinde Çözümlerimize, Kampanyalarımıza ve Finansman aracına göz
  atmak isterseniz Eminevim uygulamasını indirebilirsiniz." (uygulamada aynı dil "üye olun" ile).
- Uygulama dosyası 2026-10-21 akşamı kullanıcı isteğiyle değişti: tüm ekranlar site görünümüne çevrildi, yeni müşteri
  akışı web kararlarına uyduruldu (yer türü ve e-posta yok, temsilci hemen gösterilmez), finansman sonuç kartı web'deki gibi.

## Açık işler
- **İş planı ve görev dağılımı (2026-11-03):** 4 kişi: Pazarlama (müşteri), Fizibilite 1 (personel), Fizibilite 2
  (araştırma, altyapı, BT), Alternatif Satış Kanalı (veri, raporlama, prototip değişiklikleri; belgelerde "Sen" değil bu ad).
  Belgeler OneDrive
  `Eminevim\AlternatifSatisKanali\Belgeler\Tasarruf Yanimda Gorev Dagilimi\`; görev takip sayfası `..\gorev-takip`
  (yayında; ayrıntı o klasörün CLAUDE.md'si). Aşağıdaki yeni yöne göre yeniden yazıldı (2026-11-04).
- **Yeni yön (kullanıcı, 2026-11-03) — bundan sonraki planın dayanağı:**
  - Aşamalar: **1 Proje Çerçevesi · 2 Araştırma · 3 Yöntem ve Tasarım · (Sunum, olacaksa, 3'ten sonra) · 4 Teslim.**
  - Asıl iş bu projenin **mühendisliği: yöntem ve tasarım.** Görev tanımları buna göre ve daha kolay anlaşılır yazılır.
  - İlk adım çerçeve: ana fikir, hedef kitle, temel işleyiş gibi ana konular netleşmeden tasarıma geçilmez. Sonra
    araştırmalarla birlikte geliştirme; sonra tasarım adım adım: uygulama nasıl çalışacak, uygulama–web–kanal→saha
    personeli işleyişi ve aralarındaki iletişim; oluşturma; sunuma hazırlama; sonrası teslim.
  - **Tasarım kararı henüz verilmedi.** Mevcut prototip kesin değil: ekleme/çıkarma olabilir, yöntemler (ör. kimlik
    doğrulama, giriş, kapıda doğrulama) değişebilir. Mevcut ekranları "karar" sayma.
  - Proje çerçevesi, uygulama, senaryo, videolar ve tüm belgeler **aynı standartta, çelişkisiz** olacak; bu iş Claude ile birlikte yapılır.
  - "Yapay zekayla yapılabilir" etiketi KULLANILMAZ (kullanıcı vazgeçti).
  - **Onaylı alt başlıklar (2026-11-03):**
    1 Proje Çerçevesi: 1.1 Ana fikir ve amaç · 1.2 Hedef kitle (kim çağırır, hizmeti nerede görür) · 1.3 Temel işleyiş
    (çağrıdan görüşme sonrasına tek sayfalık akış) · 1.4 Kapsam ve sınırlar · 1.5 Varsayımlar ve başarı ölçüsü · 1.6 Ortak dil (sözlük).
    2 Araştırma: 2.1 Bugünkü durum (saha verisi) · 2.2 Benzer uygulamalar (müşteri ve personel) · 2.3 Saha ve atama yöntemleri ·
    2.4 Kimlik doğrulama ve güven yöntemleri · 2.5 Hukuk ve uyum · 2.6 Altyapı ön araştırması (SMS, harita, mevcut sistemler) ·
    2.7 Uyarlama kararları.
    3 Yöntem ve Tasarım: 3.1 Uçtan uca işleyiş (müşteri–web–uygulama–kanal–SPY–yönetici; kim, ne zaman, kime, ne bildirir —
    ÖNCE bu biter, diğerleri buna dayanır) · 3.2 Kurallar (atama, taşma, dönüş süresi, satış sahipliği) · 3.3 Kimlik doğrulama
    ve güven · 3.4 Bildirim ve iletişim (SMS, bildirim, sohbet) · 3.5 Müşteri ekranları (uygulama + web) · 3.6 Personel ekranları
    (telefon + tablet) · 3.7 Yönetici ekranları ve ölçüm · 3.8 Standart birliği (belge, senaryo, video çelişki kontrolü) ·
    3.9 Çalışan prototip.
    Sunum (isteğe bağlı, 3'ten sonra).
    4 Teslim: 4.1 Altyapı ihtiyaçları ve BT görüşmesi · 4.2 Devir paketi · 4.3 Devir toplantısı.
    Ayrı "altyapı kaynakları" aşaması yok (ön araştırma 2.6, BT ile netleştirme 4.1).
  - Görevler, kişi dağılımı ve görev tanımları bu başlıklara göre çıkarıldı.
  - **Durum (2026-11-04, kullanıcı onayladı):** 43 iş (yük: Pazarlama 22, Fizibilite 1 21, Fizibilite 2 22, Alternatif Satış Kanalı 24).
    Tek kaynak OneDrive `...Gorev Dagilimi\kaynak\gorev-tanimlari.md`; `kaynak\uret.py` (conda scrapling) genel plan + 4 kişi PDF'ini ve
    `gorev-takip\baslangic.json`'ı üretir. Taslak 1 `kaynak\eski-taslak1\`. Plana giren iki öneri: 3.9a ekran notları geldikçe parça parça;
    3.8'e 3.9a sonrası son kontrol. Video güncellemesi plana eklenmedi (kullanıcı istemedi). Belgelerde "ASK" kısaltması yok, tam ad yazılır.
    Takip sayfası yayını ayrıca onay ister (`gorev-takip\CLAUDE.md`).
- **Ortak dil (kullanıcı kararı 2026-11-03):** talep → çağrı, temsilci → SPY, talep ekibi → aktif SPY'ler, ödül → teşvik, pilot → pilot bölge denemesi.
  **Belgelerde uygulandı (2026-11-05):** 00 (Docs, md, site, PDF, Taslak 0.7), 01, 02, 05, 06, 07, 08, README, benzer-uygulamalar (yalnız bize dönük ders ve fikirler).
  Bilerek değişmedi: 03 (dış araştırma metni), 04 ve kaynaklar (kayıt), 09, PROJE_ILERLEME (tarihçe), 08'de seçilmeyen modeller.
  **Uygulamada ve HTML'lerde (2026-11-11, aşağıdaki kurala göre):** uygulama, web formu (`olustur.py` ile üretildi), `senaryo.html`, `rota.html`,
  `konum-sec.html`, taslaklar, `URUN_KURALLARI.md` (ASK → Alternatif Satış Kanalı Müdürü); müşteri ekranları "temsilci", personel/yönetici "SPY".
  "Talep" yalnız müşteri çağrısı anlamında "çağrı" oldu; destek/düzeltme/randevu değişikliği talebi aynı. Kod adları (`temsilci`, `TEMSILCI_DETAY`, `assets/temsilci/`) değişmedi.
  **Bilerek değişmedi:** `video/` (tanıtım sayfası, 4 video, altyazılar; ses de "temsilci" diyor — kullanıcı videoyu değiştirmiyor).
  **Kural (kullanıcı, 2026-11-11):** müşterinin gördüğü her yerde (müşteri ekranları, web formu, SMS) **"temsilci"**; personel, yönetici,
  takip sayfası ve iç belgelerde **"SPY"**; ikisinde de **"çağrı"**. Ayrıntı `URUN_KURALLARI.md` → Ortak dil. (Eski açık soru kapandı.)
- **Canlı test sürümü (2026-11-10; 2026-11-11: 7 SPY `spyler.js` (yalnız iki H/G'si ≥ %100 olanlar, "aktif değil" yok), hemen/ileri puanlı
  atama, 2 dk kabul, Devret → sıradaki, kimse kalmazsa "kimse almadı" (haritada kırmızı; yönetici ataması yok), Saha Canlı haritası,
  kompakt performans, Destek bölümü yok, görüşmeye hazırlık yalnız uygulamada, girişte yalnız SPY + Yönetici, web formu merkeze bağlı):** `merkez/` — `sunucu.py` (8794, Başlangıç kısayolu "Tasarruf Yanimda Merkezi", conda base pythonw;
  durdurma `python sunucu.py --durdur`; deneme kopyası `TY_PORT=8795 TY_YOL=deneme TY_VERI=<geçici>`), `takip.html` (bilgisayar takip sayfası),
  kök `canli.js`. Gizli yol `merkez/gizli_yol.txt` (depoda yok, belgeye yazılmaz). Dışarıya Tailscale Funnel ayrı yolla:
  `/<gizli_yol>` → `http://127.0.0.1:8794/<gizli_yol>`. Kurallar `URUN_KURALLARI.md` → "Canlı test sürümü". Test `tests/merkez-akis.py`.
  Aynı porta ikinci kopya bağlanmaz (Windows'ta adres yeniden kullanımı kapatıldı).
- iPhone (TestFlight): `scripts/merkez-adresi.mjs` Codemagic'te `TY_MERKEZ_URL` (merkezin tam https adresi + gizli yol) varsa uygulamayı
  merkez sayfasına bağlar → uygulama değişikliği yeni derleme istemeden telefona gelir. Değişken yoksa paketteki gösteri sürümü açılır.
  Derleme henüz yapılmadı (`IOS_TESTFLIGHT.md`). Kapalı uygulamaya bildirim (push) için APNs anahtarı + eklenti gerekir (yapılmadı).
- Finansmanlarım rakamları için Eminevim uyum/hukuk onayı.
- Klasör/depo adı eski (eminevim-saas / eminevim-saha-paneli) — yeniden adlandırma kararı verilmedi (Pages adresi değişir).
- Öneri olarak bekliyor: cumartesi yığılmasını rakamla gösteren analiz (SPY raporları), yönetime kısa sunum.

## Teknik notlar
- Uygulama: tek dosya `Eminevim Saha Paneli.dc.html` (şablon `{{ }}`, `<sc-if>`, `<sc-for>`; durum `state`, görüntü değerleri
  `renderVals()`), `support.js` çalışma zamanı. `?native=1` telefon düzeni ve service worker kapalı.
- Web formu: `web-basvuru/form_bolumu.html` (TY_CSS / TY_FORM / TY_TAKIP / TY_JS blokları) → `python olustur.py` canlı
  eminevim.com'u indirir, formu masaüstü paneline ve mobil pencereye koyar (mobilde `tk-input*Mobil*` sınıfları), izleme
  kodlarını çıkarır, tüm `<a>`'ları etkisizleştirir (`data-ty-dis` hariç). Değişiklikten sonra mutlaka yeniden üret.
- Test: conda `scrapling` Python + Playwright `channel="chrome"` (sunucuda Chromium indirme yok); yerel sunucu
  `python -m http.server 8799`. Pages yayını ~1 dk; `curl ...?t=$RANDOM` ile kontrol.
- Bu depoda git kimliği yerel ayarlı: `sualpsudas <sualpsudas@users.noreply.github.com>`.

