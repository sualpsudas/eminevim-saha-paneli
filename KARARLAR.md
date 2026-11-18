# Tasarruf Yanımda — kararlar ve tarihçe

Yalnız gerektiğinde okunur (amaç/ilke, plan, belge işi, "bu neden böyle" sorusu). Geçerli kurallar `CLAUDE.md` ve `URUN_KURALLARI.md`'de.

## Amaç ve ilke (2026-10-22, kullanıcı onaylı)
- Eski tanım "cumartesi yığılmasını hafta içine yaymak" idi; yerine geçen ilke (kaynak yönetimi): "Saha gücümüzün bir bölümü bizi çağıran
  müşteriye ayrılır; diğerleri sahada çalışır; dağılım talebe göre ayarlanır." Cumartesi yoğunluğu ana amaç değil.
- "Talebe ulaşan saha gücümüzü, talebin bize ulaştığı bir kanalla tamamlıyoruz." Müşteri kimin geleceğini önceden görür, görüşme günü takip eder.
- Varsayım: var olan talebe yetişmek talep yaratmaktan verimli. Ana ölçü: temsilci saati başına görüşme/satış.
- **SPY (2026-10-23):** saha personeli = Saha Portföy Yöneticisi, "SPY'ler" diye yazılır; ayrı ekip adı YOK, talepleri "Tasarruf Yanımda'da
  aktif SPY'ler" karşılar. İlk aşamada en başarılı SPY'ler, "teşvik" olarak (ödül değil); sonra kimlerin aktif olacağı belirsiz.
  Atamada ilk ölçüt başarı, yöntem sonra (anlık hizmet/çağrı uygulamaları referans). Taşmada takım lideri atar.
- Finansman Aracı + isteğe bağlı bilgiler (meslek) = SPY için görüşme öncesi ön bilgi; aynı gün talepleri de kapsanır (prototipte var, 2026-11-11).
- Uygulama ve web formu bu fikrin ilk aşamalarıdır; aynı marka görünümü, senaryoları birebir aynı olmak zorunda değil.
- **Proje çerçevesi belgesi:** düzenleme claude.ai belgesinde (https://claude.ai/artifact/WBKdRt8hzNXjTymiJzqG9p, oturum ister);
  paylaşım için sitede `rapor/proje-cercevesi.html` (linkler.html alt satırı); md kopyası
  `rapor/tasarruf-yanimda-proje-calismasi/00-proje-cercevesi.md`. Belge değişince site sayfası ve md kopyası da güncellenir.
  Ayrıntı ve araştırma: `rapor/tasarruf-yanimda-proje-calismasi/`.

## Proje planı (2026-11-03 yeni yön, 2026-11-04 onaylı durum)
- Aşamalar: **1 Proje Çerçevesi · 2 Araştırma · 3 Yöntem ve Tasarım · (Sunum, olacaksa, 3'ten sonra) · 4 Teslim.**
  Alt başlıkların (1.1–4.3) ve görev tanımlarının tek kaynağı OneDrive
  `Eminevim\AlternatifSatisKanali\Belgeler\Tasarruf Yanimda Gorev Dagilimi\kaynak\gorev-tanimlari.md`.
- Asıl iş projenin **mühendisliği: yöntem ve tasarım.** Çerçeve (ana fikir, hedef kitle, temel işleyiş) netleşmeden tasarıma geçilmez;
  sonra araştırmalarla geliştirme, sonra tasarım adım adım (uygulama–web–kanal→SPY işleyişi ve iletişim), oluşturma, sunum, teslim.
  3.1 Uçtan uca işleyiş ÖNCE biter, diğerleri ona dayanır. Ayrı "altyapı kaynakları" aşaması yok (ön araştırma 2.6, BT ile netleştirme 4.1).
- Tasarım kararı verilmedi: prototipe ekleme/çıkarma olabilir, yöntemler (kimlik doğrulama, giriş, kapıda doğrulama) değişebilir.
- Proje çerçevesi, uygulama, senaryo, videolar ve tüm belgeler aynı standartta, çelişkisiz olacak; bu iş Claude ile birlikte yapılır.
- 4 kişi: Pazarlama (müşteri), Fizibilite 1 (personel), Fizibilite 2 (araştırma, altyapı, BT), Alternatif Satış Kanalı (veri, raporlama,
  prototip değişiklikleri; belgelerde "Sen" değil bu ad). 43 iş (yük: Pazarlama 22, Fizibilite 1 21, Fizibilite 2 22, Alternatif Satış Kanalı 24).
- `kaynak\uret.py` (conda scrapling) genel plan + 4 kişi PDF'ini ve `gorev-takip\baslangic.json`'ı üretir. Taslak 1 `kaynak\eski-taslak1\`.
  Plana giren iki öneri: 3.9a ekran notları geldikçe parça parça; 3.8'e 3.9a sonrası son kontrol. Video güncellemesi plana eklenmedi
  (kullanıcı istemedi). Takip sayfası yayını ayrıca onay ister (`gorev-takip\CLAUDE.md`).

## Ortak dil uygulaması
- Karar 2026-11-03: talep → çağrı, temsilci → SPY, talep ekibi → aktif SPY'ler, ödül → teşvik, pilot → pilot bölge denemesi.
  2026-11-11 kesin kural: müşteriye "temsilci", içeride "SPY", ikisinde "çağrı" (eski açık soru kapandı).
- **Belgelerde uygulandı (2026-11-05):** 00 (Docs, md, site, PDF, Taslak 0.7), 01, 02, 05, 06, 07, 08, README, benzer-uygulamalar
  (yalnız bize dönük ders ve fikirler). Bilerek değişmedi: 03 (dış araştırma metni), 04 ve kaynaklar (kayıt), 09, PROJE_ILERLEME (tarihçe),
  08'de seçilmeyen modeller.
- **Uygulamada ve HTML'lerde (2026-11-11):** uygulama, web formu (`olustur.py` ile üretildi), `senaryo.html`, `rota.html`, `konum-sec.html`,
  taslaklar, `URUN_KURALLARI.md` (ASK → Alternatif Satış Kanalı Müdürü); müşteri ekranları "temsilci", personel/yönetici "SPY".
  "Talep" yalnız müşteri çağrısı anlamında "çağrı" oldu; destek/düzeltme/randevu değişikliği talebi aynı.
  Bilerek değişmedi: `video/` (tanıtım sayfası, 4 video, altyazılar; ses de "temsilci" diyor, kullanıcı videoyu değiştirmiyor).

## Modüler yapı ve IT'ye devir (2026-11-18, kullanıcı kararı)
- Uygulama IT'ye devredilecek: iPhone'da yenilemeden önce son büyük yapı değişikliği (kozmetik dışı). Her dış kaynak (personel, H/G, satış,
  randevu, canlı konum, bildirim, SMS, müşteri hesabı, harita) tek "kapı" dosyasının arkasında; şirket sistemi bağlanırken yalnız kapı değişir.
  Rehber `IT_DEVIR.md`.
- SPY listesi elle yazılmaz, H/G'ye göre **otomatik** oluşur (şirket dosyalarıyla aynı sütun adları; depoda uydurma değerler).
- H/G kuralları (kullanıcı, `tf_orn.xlsx` örneği üzerinden): klasman **şubenin** klasmanı, personel şubesinden alır;
  "Saha Portföy Yöneticisi (1)" = SPY1 ("(2)" = SPY2 varsayıldı, doğrulanacak); satış dosyasındaki bütün kayıt türleri sayılır;
  ciro ayı **Kayıt Tarihi**; randevu hedefi günlük 10 (genel); H/G **son 3 ay** ortalaması; randevu dosyasında kişi ad soyadla yazılı.
- Açık: gerçek şube–klasman tablosu; yeni personelde ciro hedefinde kıst (orantılama) yok; ad soyad eşleşmesi kırılgan (sicil sütunu önerilir).

## Tarihçe
- 2026-10-20/21: proje adı Tasarruf Yanımda; müşteriye uygulama indirtilmez, önce web. Web formunda e-posta istenmez (10-21 akşam).
  Bütçe hesabı kullanıcı kararıyla web sitesine de eklendi. Görünüm kaynağı eminevim.com oldu.
- 2026-10-21 akşamı uygulama kullanıcı isteğiyle değişti: tüm ekranlar site görünümüne çevrildi, yeni müşteri akışı web kararlarına
  uyduruldu (yer türü ve e-posta yok, temsilci hemen gösterilmez), finansman sonuç kartı web'deki gibi.
- 2026-10-21: `rapor/benzer-uygulamalar.html` taslağı (Türkiye + dünya benzer uygulamalar, yenilik fikirleri, uyarılar); kullanıcıyla
  konuşulup ortak rapora dönüşecek.
- 2026-11-04: linkler.html'deki Yapılacaklar paneli kaldırıldı (görev takibi `gorev-takip`te).
- 2026-11-05: ürün kuralları CLAUDE.md'den `URUN_KURALLARI.md`'ye taşındı.
- 2026-11-10/11: canlı test merkezi, 7 SPY, puanlı atama, Saha Canlı, Web Push bildirimi, müşteri hesabı. `AGENTS.md` (Codex rehberi) yazıldı.
- 2026-11-17: CLAUDE.md sadeleştirildi; teknik ayrıntı `TEKNIK.md`'ye, gerekçe/plan/tarihçe bu dosyaya taşındı (eski hâl git geçmişinde).
