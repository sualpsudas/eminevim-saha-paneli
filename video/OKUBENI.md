# Tanıtım videosu

`CLAUDE.md`'den 2026-11-05'te aynen taşındı.

- `video/` — **tanıtım videosu** (2026-10-26 **v10**, linkler.html'de `?v=10`; içeride izlenecek KURUMSAL PROJE TANITIMI; 16:9, ~2 dk, 50 kare/sn,
  seslendirme + kodla üretilen sakin müzik (sessiz kapanışta yükselir) + açılıp kapanabilen Türkçe altyazı izi ve `.srt`).
  v8 (kullanıcı "en iyi iyileştirmeler"): Sorun ve Çözüm girişi düz ikon değil, AYNI izometrik mahallede kamera hareketli anlar; yeni karakter
  MÜŞTERİ (lacivert ceket, telefonlu, "Müşteri" etiketli; 05'teki diyagramda da müşteri lacivert). Mahallede ağaç sallanması + bulut gölgesi
  (kuş denendi, hata gibi göründü → kaldırıldı; sokak lambası tabelaya bindi → kaldırıldı). Altyazı/seslendirme DEĞİŞMEDİ.
  v9 (2026-10-24, üretildi): kapı kapı ziyaretlerde sonuç karışık: yeşil tik + KIRMIZI çarpı (`OLUMLU` izo.js;
  bugün 1,0,0,1,0,1 · sorunda ECZANE çarpı · çözümde turuncu SPY KUAFÖR çarpı, çağrıya giden yeşil SPY hep tik); yayalar SPY/müşteriyle AYNI boy (izometride
  uzaklık küçültmez); işleyiş yavaşladı: her bölüm seslendirmeden sonra +1,6 sn bekler, Talep 4 ekran (tel02 → tel07 → tel08 → tel09), ekran kaydırma 0,6 sn,
  kamera 1,2 sn → video ~2 dk 0 sn.
  v10 (2026-10-26, kullanıcı): konuşma/altyazıda SPY yerine "Saha Portföy Yöneticileri / Yöneticisinin" (ekrandaki kısa SPY etiketleri
  kaldı); "kanal ise yok" → "kanal yok"; çözüm girişi "Bu kez ilk adımı müşteri atıyor."; işleyişte yakınlaşma azaldı (telefon ×1,3,
  tablet ×1,15, ön bilgi ×1,2). YAN VİDEO: `kaydet.py --yan` (sayfa `?yan=1`) yol haritası kartı ve bölümü olmadan → pilot bölgeden
  söz edilmez; `tasarruf-yanimda-tanitim-kisa.mp4` (~1 dk 47 sn), linkler.html'de "Tanıtım videosu (pilot bölgesiz)" `?v=N`.
  v11 (2026-10-30, motion-design skill denetimi; metin/ses DEĞİŞMEDİ): yürüyüş `kisi().ciz` adım evresi YOLA bağlı (ayak kaymaz), dizli bacak,
  iki kol + dosya sallanır, öne eğilme; `adimGenlik(p)` kalkış/duruşta adımı küçültür (yeni yürüyüşte de kullan). Sahne geçişi boş zemine
  düşmez: çapraz geçiş `GECIS` .5 sn + hafif ölçek; kart önceki sahnenin son karesine kayar, çıkarken sonrakinin ilk karesini açar
  (`KART_GIR` .55 / `KART_CIK` .45, kartlar z-index 20). Kamera yakınlaşması oranla (`kamAra`, izo `kamera`). kaydet.py: BT.709 renk
  dönüşümü + etiketi (eskiden etiketsiz → telefonda renk kayması), CRF 18 + tune animation, müzik konuşmada kısılır (sidechain),
  loudnorm -16 LUFS, AAC 192k. **v11 ses düzeltmesi (2026-10-31):** sidechaincompress yan girdi (konuşma) bitince duruyordu → sessiz kapanışta
  (son ~7 sn) hiç ses yoktu; artık yan girdi `apad` ile uzar. Yalnız ses değişince `kaydet.py --ses [--yan]` (görüntü aynen, birkaç dk); `?v=12` / kısa `?v=3`. Hareket bulanıklığı yapılmadı (üretimi 2-3 kat uzatır; istenirse). Ses için ücretsiz Gemini 3.8 Flash TTS
  (Türkçe, tarifle ton) araştırıldı, kullanıcı şimdilik erteledi; kelime zamanı vermez → Whisper ile hizalama gerekir.
  Dolgu kelime YOK (kullanıcı 2026-10-24): "Yani" ve "Peki" metinden çıktı (sorun/çözüm sesleri yeniden üretildi). Tek parça yenilemek:
  `python video/ses_uret.py sorun cozum` (diğer parçalar plan.js’ten aynen kalır).
  Son cümle (kullanıcı: -ceğiz ve talep olmasın): "Önceliği bizi çağırana vermek, saha gücümüzü doğru yere yönlendirmeyi kolaylaştırır."; ekranda "Dağılım,
  gelen çağrılara göre ayarlanır"; "doğru yere"de bir kişi saha kutusundan çağrı kutusuna geçer (3/5 → 4/4). Çift yönlü şemada ok etiketleri (Uygulamadan
  çağrı / Saha ziyareti), tek haleli saha ekibi, "Yan kazanç: Ön bilgi → Ek veri" hapları. Kapanış kartlarında ikinci satır. Finansman fin2 ekranı CANLI
  (`finansmanCanli`, `#finCanli` kaydırma katmanında): %20 → %10 dokunuş, vade 48 → 72 sürükleme, aylık 58.333 → 65.625 → 43.750 ₺ (= ön bilgi).
  Seslendirmede ve video yazılarında "talep" YOK, yerine "çağrı" (kullanıcı 2026-10-24; işleyiş bant adı "Çağrı", yol haritasında "Çağrı sayısı").
  Uygulama ekran görüntülerindeki "Yeni talep" / "Talebiniz alındı" ve bildirim kartı uygulamayla aynı kaldı (uygulama değişirse birlikte değişir).
  Sıra: Açılış (arkada soluk mahalle, kamera kayar; logo süpürme, "Tasarruf Yanımda" kelime kelime) → bölüm geçiş kartı (yeşil, yalnız başlık; NUMARA YOK, köşe etiketlerinde de yok: kullanıcı 2026-10-24) → 01 Bugün sahada
  (İZOMETRİK mahalle `izo.js` mod "bugun": SPY kapı kapı, kamera SPY'ye yakından başlar açılır) → 02 Sorun (`izo.js` mod "sorun", bant yazısı üç kez değişir:
  tek yönlü temas = SPY'den kapıya kavisli ok · çağrı kanalı yok = müşteri telefonuna bakar, balonda telefon+? → "yok"ta turuncu çarpı ·
  cumartesi = üstte gün şeridi, hafta içi gri geçer + BÜRO'da çanta balonu, Cmt turuncu: SPY ile müşteri buluşur, iki kişi balonu) →
  03 Çözüm (mod "cozum": "Dilediği yer, dilediği zaman" = müşteri telefona dokunur, BÜRO üstünde çağrı simgesi; sonra geniş açı: turuncu SPY kapı kapı
  + çağrıya giden yeşil SPY (ikisi de yalnız "SPY"; "aktif" kelimesi
  görüntüde ve konuşmada YOK, ayrım renkle), gün şeridinde vurgu haftanın günleri üzerinde sırayla ilerler (belirli gün öne
  çıkmaz, "her gün" de yazılmaz) → işleyiş
  telefon+tablet 4 bölüm: Talep · Eşleşme (telefondan tablete uçan "Yeni talep" bildirim kartı) · Hazırlık·ön bilgi (Finansman ekranları, tablette
  ön bilgiye yakınlaşma) · Güven. KAMERA (`kamHedef`): yalnız telefon etkinse ×1,6 vurgulu yere, yalnız tablet ×1,32 (ön bilgi ×1,5), ikisi birden geniş;
  ekranlar çerçeve içinde sağdan KAYARAK değişir (`.kay` katmanı, kopyalar ekran alanına kırpılı); parmak izi + dokunuş dalgası; cihaz etiketleri alt bantta
  (etkin turuncu), "Prototip ekranları" notu yalnız geniş açıda) → 04 Yol haritası (4 aşama; harita pilot bölgeyle erken gelir, sağda simgeli
  "İzlenecek" kartları: talep sayısı/yanıt süresi/gerçekleşen görüşme; genişlemede harita uzaklaşır, Anadolu yakası ilçeler dalga gibi;
  Sultanbeyli/Pendik etiket yeri elle)
  → 05 Hedeflenen düzen (çift yönlü temas + "yan kazanç: ön bilgi = ek veri" · "Öncelik bizi çağırana" rozetli kutular; kişiler iki kutunun
  arasından yatay dağılır, başlıkların üstünden geçmez) → sessiz kapanış (3 simgeli özet kartı ortada birleşip kaybolur → logo). SES EFEKTİ YOK.
  Seslendirme kuralları (kullanıcı): SPY "Seğpeğyeğ" yazımıyla okutulur (telaffuz denemesinde E seçildi, `ses-deneme/`); açılışta konuşma 2,8 sn sonra başlar; bölüm kartları 2 sn; "Tasarruf Yanımda" ve kısa cümleler tek başına okutulmaz (çok dilli
  ses yabancı dil sanıyor) → uzun parçalar, ekran geçişleri edge-tts KELİME ZAMANLARINA bağlı (`W()`); zaman kipi karışık,
  çözüm gelecek zaman; kelime tekrarı yok; satış vaadi ve "Amacımız" yok; ilçe adı söylenmez ("belirlenecek bir pilot bölge",
  "uygun görülen ilçelere genişletmek mümkün"); konuşmada "işyeri" değil "müşteri". Metin ChatGPT dış gözüyle birleştirildi.
  Üretim: `python video/ses_uret.py` (METIN + kelime zamanları → ses/plan.js) → `python video/kaydet.py` (sahne süreleri sesten;
  SES_PLAN, ALTYAZI cümle cümle, KAPANIS_T). Ses edge-tts `fr-FR-RemyMultilingualNeural` +8% (kullanıcının seçtiği "Ses 4";
  ücretsiz Türkçe Ahmet sesi servis tarafında çalışmadı). Tam doğal Türkçe için seçenek: ElevenLabs (ücretli).
  `kareler/vurgu.js` = ekranlardaki turuncu vurgulu düğmenin yeri (otomatik tespit; dokunuş dalgası ve yakınlaşma için).
  `kareler/`: senaryo görüntüleri, `fin1-3` uygulamanın Finansman ekranları, `harita_z11` OpenStreetMap gri (atıf zorunlu);
  ilçe sınırları Nominatim. Gerekenler conda `video` ortamında (playwright, imageio-ffmpeg, edge-tts, numpy, pillow; 2026-10-24 kuruldu):
  `%LOCALAPPDATA%\miniconda3\envs\video\python.exe video/kaydet.py` (50 kare/sn PNG → ~45-60 dk sürer; `--kare 12 40.5` hızlı önizleme). Videoyu her güncellemede
  linkler.html'deki `?v=N`'i artır (telefon eski kopyayı gösteriyordu). Müşteriye yönelik reklam videosu kapsam dışı.
