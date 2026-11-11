# Tasarruf Yanımda — Atama ve rota (başlangıç kuralları)

Tarih: 11 Kasım 2026 (aynı gün ikinci güncelleme: hemen/ileri puanı, ret sınırı ve yöneticiye düşme kalktı). Durum: kullanıcıyla konuşularak
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
| Molada değil | ✓ | — |
| Uygulaması açık | ✓ | — |
| Yolda ya da görüşmede değil | ✓ | — |
| Saat çakışması | — | O gün, istenen saatin 1,5 saat öncesi ve sonrasında başka randevusu yok |
| Günlük üst sınır | Bugün en fazla **4** çağrı | O gün en fazla **4** çağrı |

## 4. Puan (100 üzerinden)

Randevu H/G ile ciro H/G **eşit ağırlıkta**. Değer %100–130 arasında puanlanır (%130 ve üstü tam puan), çünkü %100 altı zaten listede yoktur.

| Ölçüt | Hemen | İleri |
|---|---|---|
| **Yakınlık** — hemen: o anki yer (bugünkü son randevusu, yoksa kendi mahallesi); ileri: kendi bölgesi ya da o günkü randevuları | **50** | 30 |
| H/G (randevu + ciro, son 3 ay) | 30 (15 + 15) | **50** (25 + 25) |
| Çağrı yükü (bugün / o gün az çağrı alan önde) | 20 | 20 |

- **Hemen:** müşteri bekliyor; yakın olan öne geçer.
- **İleri:** zaman var; başarı öne çıkar, yakınlık o günün programına göre hesaplanır.
- Hiç verisi olmayan yeni SPY ekip ortalamasıyla başlar. Tasarruf Yanımda'ya özel dönüşüm oranı (çağrıdan satışa) veri biriktikçe eklenir.

## 5. Teklif ve kabul

1. Çağrı en yüksek puanlı SPY'ye gider; telefonunda sesli uyarı. SPY çağrıyı neden aldığını görür (uzaklık, H/G, o günkü çağrı sayısı).
2. **2 dakika** içinde kabul etmezse ya da **Devret** derse sıradaki SPY'ye geçer. Deneme sayısı sınırı yoktur.
3. Uygun SPY kalmazsa çağrı **"kimse almadı"** olur, yöneticinin Saha Canlı haritasında **kırmızı** görünür; uygun bir SPY çıkınca
   (moladan döndü, uygulamayı açtı) kendiliğinden ona teklif edilir.
4. **Yöneticiye düşme, yöneticinin elle ataması (Ata) ve aktarması yoktur** (kullanıcı kararı, 2026-11-11).

## 6. Rota (başlangıç)

- İki randevu arasında görüşme süresi (yaklaşık 60 dk) + yol süresi kadar boşluk olmalı.
- İleri tarihli çağrı, SPY'nin o günkü programına "araya eklenince ne kadar ek yol getirir" diye bakılarak yerleştirilir.
- Yönetici her SPY'nin günlük sıralı rotasını haritada görür.

## 7. Test sürümü

- **7 SPY**, pilot bölgede (tanıtım videosundaki gibi **Üsküdar, Ümraniye, Ataşehir**), her biri farklı mahallede; hepsinin iki H/G'si
  ≥ %100 (değerler **uydurmadır**). Liste: `spyler.js`.
- Konumlar sabit (mahalle noktası); canlı konum sonraki adım. "Uygulaması açık" = son 30 saniyede merkeze bağlanmış.
- Rol ayrımı: girişte yalnız **SPY** ve **Yönetici** (her yönetici hepsini görür). Yönetici: Saha Canlı haritası (boşta yeşil, randevuda
  turuncu, molada gri; kimse almadı kırmızı) ve kompakt performans listesi.
- Kabul süresi, Devret ve "kimse almadı" test sürümünde çalışır. "Hız ve güvenilirlik" ölçütü test sürümünde kullanılmıyor.

## Araştırmadan alınanlar

- Saha servis sistemleri önce kesin kurallarla eler, kalanları ağırlıklı puanla seçer (Salesforce Field Service).
- Satış ekiplerinde performansa göre ağırlıklı dağıtım; son 3 ay, ayda bir güncelleme; hedefin altında kalanın payı azalır (lead routing kaynakları).
- Emlak örneği: müşteri, satışa çevirme olasılığı en yüksek danışmana; iyi sonuç verenin payı zamanla büyür (Zillow).
- Hız: geç dönülen müşteri soğur; kabul süresi dolunca sıradakine geçilir (sigorta ve taksi uygulamaları).
- Uyarı: az veriyle performans puanı yanıltır; aşırı yüklenmeyi günlük üst sınır ve yük dengesi önler.
