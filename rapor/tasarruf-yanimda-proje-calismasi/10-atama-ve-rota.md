# Tasarruf Yanımda — Atama ve rota (başlangıç kuralları)

Tarih: 11 Kasım 2026. Durum: kullanıcıyla konuşularak kararlaştırıldı; test sürümünde uygulanacak, pilot bölge denemesi verisiyle gözden geçirilecek.
Dayanak: [08 Kaynak yönetimi](08-kaynak-yonetimi.md) ("atamada ilk ölçüt başarı"), benzer sistemler araştırması (aşağıda).

## 1. Kim aktif SPY olabilir?

Son 3 ayın ortalamasında **hem randevu H/G hem ciro H/G %100 veya üstü** olan SPY'ler. İkisinden biri %100'ün altındaysa
o SPY'ye Tasarruf Yanımda çağrısı gitmez (sahadaki çalışmasına devam eder). Liste her ay yenilenir.

## 2. Eleme (önce uymayanlar çıkar)

| Kural | Aynı gün çağrısı | İleri tarihli çağrı |
|---|---|---|
| Aktif SPY (madde 1) | ✓ | ✓ |
| Müsaitlik | Şu an müsait, uygulaması açık, yolda ya da görüşmede değil | O gün, istenen saatin 1,5 saat öncesi ve sonrasında başka randevusu yok |
| Günlük üst sınır | O gün en fazla **4** çağrı | Aynı |
| Uzaklık | Müşteriye makul mesafede (İstanbul içi, aynı yaka öncelikli) | Aynı |

## 3. Puan (100 üzerinden)

Randevu H/G ile ciro H/G **eşit ağırlıkta**. Değer %100–120 arasında puanlanır (%120 ve üstü tam puan), çünkü %100 altı zaten elenmiştir.

| Ölçüt | Aynı gün | İleri tarih |
|---|---|---|
| Randevu H/G (son 3 ay) | 15 | 25 |
| Ciro H/G (son 3 ay) | 15 | 25 |
| **Yakınlık** — aynı gün: şu anki yerden; ileri tarih: o günkü önceki/sonraki randevudan, yoksa şubeden | **50** | 20 |
| Yük dengesi (bugün / bu hafta az çağrı alan artı) | 10 | 20 |
| Hız ve güvenilirlik (kabul süresi, kabul oranı, iptal, gecikme) | 10 | 10 |

- **Aynı gün:** müşteri bekliyor; en yakın olanın puanı belirgin biçimde yüksek olur.
- **İleri tarih:** zaman var; başarı ve yük dengesi öne çıkar, yakınlık o günün rotasına göre hesaplanır.
- Hiç verisi olmayan yeni SPY ekip ortalamasıyla başlar. Tasarruf Yanımda'ya özel dönüşüm oranı (çağrıdan satışa) veri biriktikçe eklenir.

## 4. Teklif ve kabul

1. Çağrı en yüksek puanlı SPY'ye gider; telefonunda sesli uyarı.
2. **2 dakika** içinde kabul etmezse sıradaki SPY'ye geçer (aynı gün ve ileri tarih için aynı süre).
3. Üç SPY üst üste kabul etmezse çağrı **yöneticiye** düşer; yönetici elle atar (çerçevedeki "taşmada takım lideri atar" kararı).
4. Yönetici her çağrıyı başka SPY'ye aktarabilir. SPY çağrıyı neden aldığını görür (ör. "En yakın · H/G yüksek").

## 5. Rota (başlangıç)

- İki randevu arasında görüşme süresi (yaklaşık 60 dk) + yol süresi kadar boşluk olmalı.
- İleri tarihli çağrı, SPY'nin o günkü programına "araya eklenince ne kadar ek yol getirir" diye bakılarak yerleştirilir.
- Yönetici her SPY'nin günlük sıralı rotasını haritada görür.

## 6. Test sürümü

- 30 SPY, İstanbul'un farklı ilçelerinde (Anadolu ve Avrupa yakası); H/G değerleri **uydurmadır**, bir kısmı %100 altında (elenme görülsün diye).
- Konumlar sabit (şube/ilçe merkezi); canlı konum sonraki adım.
- Rol ayrımı: yalnız **Personel** (SPY) ve **Yönetici**. Takım liderinin ekibini izleme ekranı şimdilik yok.

## Araştırmadan alınanlar

- Saha servis sistemleri önce kesin kurallarla eler, kalanları ağırlıklı puanla seçer (Salesforce Field Service).
- Satış ekiplerinde performansa göre ağırlıklı dağıtım; son 3 ay, ayda bir güncelleme; hedefin altında kalanın payı azalır (lead routing kaynakları).
- Emlak örneği: müşteri, satışa çevirme olasılığı en yüksek danışmana; iyi sonuç verenin payı zamanla büyür (Zillow).
- Hız: geç dönülen müşteri soğur; kabul süresi dolunca sıradakine geçilir (sigorta ve taksi uygulamaları).
- Uyarı: az veriyle performans puanı yanıltır; aşırı yüklenmeyi günlük üst sınır ve yük dengesi önler.
