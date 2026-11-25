# Tasarruf Yanımda — Atama ve rota (başlangıç kuralları)

Tarih: 11 Kasım 2026 (aynı gün ikinci güncelleme: hemen/ileri puanı, ret sınırı ve yöneticiye düşme kalktı); 25 Kasım 2026: yeni puan sırası, yol mesafesi, İBB trafik çarpanı, atama seçenekleri. Durum: kullanıcıyla konuşularak
kararlaştırıldı; test sürümünde uygulandı, pilot bölge denemesi verisiyle gözden geçirilecek.
Dayanak: [08 Kaynak yönetimi](08-kaynak-yonetimi.md) ("atamada ilk ölçüt başarı"), benzer sistemler araştırması (aşağıda).

## 1. Kim aktif SPY olabilir?

Son 3 ayın ortalamasında **hem randevu H/G hem ciro H/G %100 veya üstü** olan SPY'ler. İkisinden biri %100'ün altındaysa
o SPY Tasarruf Yanımda'da yer almaz (sahadaki çalışmasına devam eder). Liste her ay yenilenir. Uygulamada "aktif değil" diye bir
durum yoktur: listede yalnız şarta uyanlar bulunur. "Molada" ayrı bir durumdur.

## 2. Hemen mi, ileri mi?

- **Hemen çağrı:** bugün ve saati en geç 2 saat sonra (uygulama 1 saatten yakın saati seçtirmez; test sürümünde eşik 2 saat).
- **İleri saat/gün:** daha sonraki saat ya da gün.

## 3. Eleme (önce uymayanlar çıkar)

| Kural | Hemen çağrı | İleri saat/gün |
|---|---|---|
| Müşteriyle aynı ilçede (seçenek, varsayılan açık) | ✓ şu anki yeri | ✓ kayıtlı ilçesi |
| Molada değil | ✓ | — |
| Başka müşteriye bağlı değil (teklif, atandı, yolda, görüşmede) | ✓ | — |
| Randevu arası | İstenen saatin **60 dk** öncesi ve sonrasında başka randevusu yok (bir SPY bir saatte en fazla bir randevu) | aynı |
| Günlük üst sınır | Bugün en fazla **4** çağrı | O gün en fazla **4** çağrı |

## 4. Puan (100 üzerinden)

Öncelik sırası (2026-11-25, ikinci karar): **yakınlık, çağrı sayısı, ciro H/G, randevu H/G**; hemen ve ileri çağrıda aynı.

| Ölçüt | Ağırlık | Nasıl |
|---|---|---|
| **Yakınlık** | **40** | Trafikli varış süresi: 0 dk tam puan, **30 dk** ve üstü sıfır. Hemen: SPY'nin şu anki yeri; ileri: kendi yeri ya da o günkü randevularından müşteriye en yakını |
| Çağrı sayısı (o gün az çağrısı olan önde) | 30 | 0 çağrı tam puan, günlük sınırda sıfır |
| Ciro H/G (son 3 ay) | 20 | %100 sıfır, %130 ve üstü tam puan (%100 altı zaten listede yok) |
| Randevu H/G (son 3 ay) | 10 | aynı |

- Hiç verisi olmayan yeni SPY ekip ortalamasıyla başlar. Tasarruf Yanımda'ya özel dönüşüm oranı (çağrıdan satışa) veri biriktikçe eklenir.

## 5. Teklif ve kabul

1. Çağrı en yüksek puanlı SPY'ye gider; telefonunda sesli uyarı. SPY ekranında kabul için kalan süre görünür.
2. **2 dakika** içinde kabul etmezse ya da **Devret** derse sıradaki SPY'ye geçer. Deneme sayısı sınırı yoktur.
3. İlçede uygun SPY kalmazsa müşteriye **randevu önerilir**: 7 gün içinde, 10:00–20:00 arası, 30 dk adımlarla ilk uygun saat
   (müşteri uygulamadan kabul eder ya da başka saat seçer).
4. Önerilecek saat de yoksa çağrı **"kimse almadı"** olur, yöneticinin Saha Canlı haritasında **kırmızı** görünür; uygun bir SPY çıkınca
   (moladan döndü, görüşmesi bitti) kendiliğinden ona teklif edilir.
5. **Yöneticiye düşme, yöneticinin elle ataması (Ata) ve aktarması yoktur** (kullanıcı kararı, 2026-11-11).

## 6. Rota ve varış süresi (2026-11-25)

- **Uzaklık yol üzerinden ölçülür:** araçla yol km'si ve trafiksiz süre ücretsiz genel yol servisinden (OSRM) gelir; tüm adaylar tek istekte.
  Servis yanıt vermezse kuş uçuşuna düşülür (km × 1,3, 25 km/sa) ve sıralamada "kuş uçuşu" diye görünür.
- **Trafik:** trafiksiz süre, İBB Açık Veri "Saatlik Trafik Yoğunluk Veri Seti"nden çıkarılan **tipik trafik çarpanı** ile çarpılır.
  Çarpan = o karede gece serbest akış hızı / o gün tipi (hafta içi, cumartesi, pazar) ve saatteki tipik hız; pilot bölgede 448 kare,
  dönem 2024-10, 2024-11, 2025-01 (İBB'nin yayımladığı son aylar). Örnek: pilot bölge geneli hafta içi 18:00 ×1,56, pazar 09:00 ×1,07.
  **Anlık trafik değildir** (kaza, kapanma görünmez); anlık veri için ücretli yönlendirme servisi ya da İBB'nin lisanslı verisi gerekir.
- İleri tarihli çağrıda yakınlık, SPY'nin o günkü randevu yerleri de hesaba katılarak ölçülür. "Araya eklenince ne kadar ek yol getirir"
  ve iki randevu arasında yol süresi kadar boşluk kuralları henüz yok (şimdilik sabit 60 dk); pilot bölge denemesinden sonra.
- Yönetici her SPY'nin günlük sıralı rotasını haritada görür.

## 7. Atama seçenekleri (canlı test)

Takip sayfasında (Saha Canlı) üstteki **Atama seçenekleri** düğmesi:

- Dört ağırlık, yakınlığın nasıl ölçüleceği (trafikli varış süresi / trafiksiz yol süresi / yol km / kuş uçuşu km) ve sıfır eşiği,
  günlük en fazla çağrı, randevu arası, ilçe şartı değiştirilebilir. Kaydedince sonraki çağrılarda geçerli; test verisi sıfırlansa da korunur;
  "Varsayılana dön" yukarıdaki kurallara döndürür.
- **Çağrı sıralaması:** seçilen çağrıda her adayın puanı ölçüt ölçüt (çubuk + rakam), km, varış süresi, trafik çarpanı ve elenenler gerekçesiyle.
  "Şimdiki seçeneklerle yeniden hesapla" aynı çağrıyı yeni seçeneklerle sıralar; çağrıyı değiştirmez.

## 8. Test sürümü

- **7 SPY** + 5 hareketli örnek SPY, pilot bölgede (**Üsküdar, Ümraniye, Ataşehir**), her biri farklı mahallede; hepsinin iki H/G'si
  ≥ %100 (değerler **uydurmadır**). Liste: `veri/spyler.js`.
- Konum: elle taşınan > telefondan gelen canlı konum (10 dk taze) > bugünkü son randevu yeri > kayıtlı mahalle noktası. Uygulamanın açık olması
  gerekmez: yeni çağrı, o SPY'yi seçmiş tüm telefonlara bildirim olarak gider (bir telefon tek SPY'ye bağlı; aynı SPY birden çok telefonda seçilebilir).
- Rol ayrımı: girişte yalnız **SPY** ve **Yönetici** (her yönetici hepsini görür). Yönetici: Saha Canlı haritası (boşta yeşil, randevuda
  turuncu, molada gri; kimse almadı kırmızı) ve kompakt performans listesi.
- Kabul süresi, Devret ve "kimse almadı" test sürümünde çalışır. "Hız ve güvenilirlik" ölçütü test sürümünde kullanılmıyor.

## Araştırmadan alınanlar

- Saha servis sistemleri önce kesin kurallarla eler, kalanları ağırlıklı puanla seçer (Salesforce Field Service).
- Satış ekiplerinde performansa göre ağırlıklı dağıtım; son 3 ay, ayda bir güncelleme; hedefin altında kalanın payı azalır (lead routing kaynakları).
- Emlak örneği: müşteri, satışa çevirme olasılığı en yüksek danışmana; iyi sonuç verenin payı zamanla büyür (Zillow).
- Hız: geç dönülen müşteri soğur; kabul süresi dolunca sıradakine geçilir (sigorta ve taksi uygulamaları).
- Uyarı: az veriyle performans puanı yanıltır; aşırı yüklenmeyi günlük üst sınır ve yük dengesi önler.
