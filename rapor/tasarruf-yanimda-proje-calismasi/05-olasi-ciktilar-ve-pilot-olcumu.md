# Olası proje çıktıları ve pilot ölçümü

Tarih: 22 Ekim 2026. Durum: geliştirilmek üzere hazırlanmış öneriler. Kullanıcı çıktıların ayrıca geliştirileceğini belirtmiştir; aşağıdakiler kesin kapsam veya onaylı hedef değildir.

## Somut çıktı adayları ve beklenen sonuçlar

| Somut çıktı adayı | Beklenen iş sonucu / sınanacak varsayım |
|---|---|
| Saha hizmetini anlatan, müşterinin temsilci isteyebildiği giriş noktası | Hizmeti bilmeyen veya ekiple karşılaşmayan müşteri de ulaşabilir |
| Konum ve zaman tercihi içeren talep kaydı | Talepler uygulanabilir görüşmelere dönüştürülebilir |
| Bölge ve kapasiteye göre yönlendirme, sorumlu temsilci kaydı | Talep sahipsiz kalmaz; yönlendirme gecikmeleri görülebilir |
| Randevu onayı, değişiklik ve iptal imkânı | Müşteriyle ekibin planı netleşir; gerçekleşmeyen ziyaretler azaltılabilir |
| Temsilci bilgisi ve iletişim alanı | Müşteri kiminle görüşeceğini bilir ve muhatabına ulaşabilir |
| İsteğe bağlı ihtiyaç/ön tercih paylaşımı | Temsilci hazırlanabilir; bunun talep tamamlamayı zorlaştırıp zorlaştırmadığı ölçülebilir |
| Görüşme sonucu, sonraki adım ve geçmiş kaydı | İlk görüşmeden sonraki fırsatlar takip edilebilir |
| Talep, görüşme, satış ve maliyet raporu | Kanalın toplam katkısı ile mevcut satışların kanal değiştirmesi ayrıştırılabilir |

Canlı konum, QR doğrulama veya otomatik atama gibi özellikler bu tabloyla zorunlu kapsam hâline gelmez. Her biri ihtiyaca, maliyete ve pilotta öğrenilecek soruya göre ayrıca önceliklendirilmelidir.

## Pilotun cevaplayacağı sorular

1. Görüşmek isteyen kişiler bu hizmeti keşfedip talep oluşturuyor mu?
2. Talepler mevcut saha ilişkilerinden mi geliyor, yeni kişilere erişim sağlıyor mu?
3. Kapasite içinde ne kadar hızlı karşılanıyor ve gerçekleşen görüşmeye dönüşüyor?
4. Tamamlanmış izleme dönemi sonunda ilave satış ve maliyet açısından katkı var mı?
5. Müşteri deneyimi, temsilci zamanı ve seyahat yükü nasıl etkileniyor?
6. Talep, görüşme ve satışın gün/saat dağılımı nasıl değişiyor?

## Önerilen ölçüm tanımları

| Metrik | Tanım / dikkat noktası |
|---|---|
| Geçerli talep | Test, spam ve tekrarlar çıkarılmış benzersiz talep; tekrar kuralları önceden belirlenmeli |
| Yeni erişilen müşteri oranı | Tanımlı geçmiş dönemde aktif kayıt/temas bulunmayan müşteriler / geçerli talep veren müşteriler; tek başına ilave satış kanıtı değil |
| İlk insan temas süresi | Talep ile ilk insan teması arasındaki süre; otomatik mesaj ayrı, temas girişimi ve başarılı temas ayrı kaydedilmeli; medyan ve geciken talepler izlenmeli |
| Talep → onaylı randevu | Onaylı randevuya dönüşen geçerli talepler / geçerli talepler; aynı izleme süresine sahip gruplar kullanılmalı |
| Randevu → görüşme | Gerçekleşen görüşmeler / tarihi gelmiş onaylı randevular; ileri tarihli randevular paydaya alınmamalı |
| Görüşme → satış | Belirli takip süresinde satışa dönüşen müşteriler / görüşme yapılan benzersiz müşteriler; tekrar görüşmeler ayrı sayılmalı |
| Katılmama ve iptal | Müşteri katılmaması, personel kaynaklı aksama ve önceden iptal ayrı nedenlerle kaydedilmeli |
| Talep / görüşme / satış maliyeti | Reklam, operasyon, personel ve seyahat maliyetleri açık kapsamla hesaplanmalı; kurulum ve işletme maliyeti ayrılmalı |
| Satış hacmi ve katkı | Satış adedi, finansman/sözleşme tutarı ve gelir farklı ölçülerdir; kurum tanımları ve iptal durumu belirtilmeli |
| Toplam bölge sonucu | Yalnız Tasarruf Yanımda etiketli satış değil, ilgili kanalların toplamı ve olası şube/saha kaymaları izlenmeli |
| Gün/saat dağılımı | Talep zamanı, görüşme zamanı ve satış zamanı ayrı alanlarda tutulmalı |
| Deneyim ve kapasite | Müşteri geri bildirimi, şikâyet, temsilci başına gerçekleşen görüşme ve seyahat süresi birlikte değerlendirilmeli |

## İlave katkı nasıl araştırılır?

Mümkünse benzer bölgelerde veya uygun birimler arasında kontrollü/kademeli açılış tasarlanır. Mevcut saha faaliyetleri sürdürülür; reklam, ekip sayısı, kampanya ve kapasite farkları kaydedilir. Bölgeler arasında talep geçişi ve aynı müşterinin birden çok kanalda görünmesi izlenir.

Basit karşılaştırma fikri: **(Pilotun son dönem sonucu − pilotun başlangıç sonucu) − (kontrolün son dönem sonucu − kontrolün başlangıç sonucu).** Bu hesap tek başına nedensel kanıt değildir; karşılaştırılabilir geçmiş eğilimler, benzer koşullar ve yeterli veri gerekir.

Yeni kanalda satış oluşurken toplam sonuç artmıyorsa kanal taşıması ihtimali incelenir. Bunun kesin hüküm olması için yeterli izleme süresi, müşteri geçmişi ve belirsizlikler değerlendirilmelidir. Kanal taşıması olsa bile maliyet veya deneyim kazanımı ayrıca ölçülebilir; ilave satışla karıştırılmamalıdır.

## Henüz belirlenmeyen pilot kararları

- Bölge ve ekipler; önceki prototip bölgeleri otomatik olarak pilot kararı sayılmaz.
- Öğrenme dönemi, değerlendirme dönemi ve satışların olgunlaşması için takip süresi.
- Örneklem büyüklüğü, ana başarı metriği ve anlamlı kabul edilecek katkı.
- Kabul edilebilir maliyet, kapasite ve müşteri deneyimi sınırları.
- Reklamın kapsamı ve mevcut müşteri/talep eşleştirme yöntemi.

Perplexity'nin 8–12 hafta, %50, %70 ve %80 önerileri için bu bağlamda dayanak yoktur; hedef olarak benimsenmemiştir. Cumartesi satış payının düşmesi başarı koşulu değildir.
