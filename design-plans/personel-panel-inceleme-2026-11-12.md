# Personel paneli görsel tasarım incelemesi (kullanıcının getirdiği metin, 2026-11-12)

Kullanıcı kararı: **radikal değil, kozmetik** değişiklikler; uygun görülenler sorulmadan yapılır.
Uygulama kuralları ve kapsam: `AGENTS.md` → "G. Personel paneli kozmetik iyileştirmeleri".

---

EMİNEVİM SAHA PANELİ — GÖRSEL TASARIM İNCELEMESİ

## 1. GENEL DEĞERLENDİRME

İlk değişikliği SPY’nin Performans ekranında yapardım. Randevu H/G ve Ciro H/G, çağrı uygunluğunu belirliyor. Buna rağmen göz önce büyük yeşil 4 / 7 ve 0 / 4 değerlerine gidiyor. Yönetici Performans ekranında sıralama kolay taranıyor, ancak tablo geniş ekranda sol tarafa sıkışıyor. Saha Canlı’da harita işlevine uygun biçimde öne çıkıyor, fakat kişi kartlarını ilk ekranın dışına itiyor.

Korunacak detaylar
- Yeşil üst şeritteki beyaz Eminevim logosu.
- Yönetici sıralamasında adın altında bölge bilgisi, sağa hizalı yüzdeler ve ayrı Ekip ortalaması satırı.
- Saha Canlı filtrelerinde durum adı, sayaç ve renkli noktanın birlikte gösterilmesi.
- Görüşmeler ekranındaki masaüstü liste ve ayrıntı ayrımı.

En belirgin üç sorun
1. Ana metrikler yeterince baskın değil. SPY Performans’ta H/G yüzdeleri küçük. Yönetici Performans’ta %100 ile %130 aynı görsel tonda.
2. Masaüstü hizaları tutarsız. Başlık yaklaşık 22 px, Performans içeriği 44 px, Saha Canlı içeriği 10 px içeriden başlıyor. Yaklaşık 716 px genişliğindeki Performans içeriğinin sağında büyük boşluk kalıyor.
3. Seçili olmayan alt menü etiketleri 11 px ve #AAAAAA. Beyaz üzerindeki yaklaşık 2,3:1 kontrast, kullanılabilir sekmeleri devre dışı gibi gösteriyor.

İnceleme kapsamı
1363 × 936 masaüstü görünümünde Tasarruf Yanımda, Personel Girişi, Yönetici için Saha Canlı, Performans ve Profil, SPY için Görüşmeler, Performans ve Profil ekranlarını gezdim. Rota açılışını, harita filtrelerini, bir kişi kartı seçimini, boş filtre sonuçlarını ve bildirim izni mesajını gördüm. Dolu görüşme ayrıntısı ve telefon girişinden sonraki müşteri ekranları doğrulanamadı. Mobil öneriler mevcut CSS kurallarına dayanıyor ve telefon ekranında görsel doğrulama gerektiriyor. Hover ve klavye odağı bütün kontrollerde ölçülmedi. Kod değişikliği uygulanmadı.

## 2. SAYFA VE SEKME BAZINDA ÖNERİLER

### TASARRUF YANIMDA VE PERSONEL GİRİŞİ

İyi çalışan detay: Logo, başlık ve giriş işlemi sade bir akış oluşturuyor.
En belirgin sorun: Masaüstündeki kalın lacivert telefon çerçevesi, büyük gölge ve geniş boşluk, formun önüne geçiyor.

| Konum | Mevcut görünüm ve sorun | Önerilen değişiklik | Neden | Öncelik |
|---|---|---|---|---|
| Giriş yüzeyi | Kalın çerçeve ve ağır gölge | Masaüstünde en fazla 400 px genişlik, 28 px iç boşluk, 12 px köşe ve 1 px sınırla beyaz form yüzeyi. Mobilde 16 px yan boşluk | Logo ve işlem öne çıkar | Yüksek |
| Personel Girişi ve Geri | Personel bağlantısı küçük. Geri formdan uzakta | 14 px/600 ve en az 44 px dokunma alanı. Geri’yi formun sol kenarıyla hizala | İkincil işlemler daha kolay bulunur | Orta |
| SPY seçin ve seçili kişi | Portre, yeşil sınır ve turuncu Giriş yap aynı satırda yarışıyor | Açılır liste 44 px, portre 36 px, ad 14 px, bölge 12 px. Seçili satır açık yeşil, Giriş yap marka yeşili. Mevcut siyah odak çerçevesini ortak odak halkasına taşı | Seçim ve giriş işlemi ayrışır | Orta |

### SAHA CANLI · YÖNETİCİ

İyi çalışan detay: Bölge sınırları, kişi işaretçileri ve durum filtreleri birlikte çalışıyor.
En belirgin sorun: Yaklaşık 570 px yüksekliğindeki harita, ilk ekranda kişi kartlarının üst kısmından fazlasını göstermiyor.

| Konum | Mevcut görünüm ve sorun | Önerilen değişiklik | Neden | Öncelik |
|---|---|---|---|---|
| Başlık altı | Şirket Geneli ve mesai dışı örnek zaman aynı gri satırda | Kapsamı 13 px nötr metin, örnek zaman bilgisini 12 px/600 ve açık kehribar yüzeyle göster. Mobilde ikinci satıra doğal kırılsın | Görülen verinin bağlamı hızlı anlaşılır | Yüksek |
| Gelen Çağrı · bugün ve Görüşme Sayısı · bugün | Her iki sayı da yeşil, sıfır dahil | Sayıları 28 px/700 koyu metin, etiketleri 13 px yap | Yeşil, durum ve seçimler için ayırt edici kalır | Orta |
| Tümü / Boşta / Randevuda / Molada | Seçili filtre kalın koyu çerçeveli. Görüşmeler ekranında seçim farklı gösteriliyor | Seçili filtreye #E7F3EE dolgu, #00724C sınır ve 600 ağırlık. Noktaları ve sayaçları koru. Mobilde 44 px yükseklik ve iki satıra kırılma | Seçim tutarlı olur. Molada (0) kullanılabilir görünür | Yüksek |
| Harita ve kişi kartları | Harita altlığı yoğun. İlk kişi sırası kesiliyor | 936 px ekran yüksekliğinde haritayı 450–470 px, mobilde 280–320 px yap. Mümkünse altlığın doygunluğunu azalt. Bölge çizgisi 2 px, kişi işaretçisi 26 px ve beyaz konturlu olsun. Seçili kartta dolgu ve sınır kullan | Harita ile kişi durumu aynı bakışta okunur | Yüksek |
| Bu durumda SPY yok. | Boş filtre sonucu haritanın altında | Mevcut mesajı liste alanında 14 px ve 16 px iç boşlukla göster | Boş sonucun nedeni anlaşılır | Orta |
| İlk yüklenme | Harita gelmeden önce büyük gri alan görünüyor | Harita alanını baştan ayır. Beklerken aynı boyutta açık gri yüzey ve Harita yükleniyor etiketi göster | Bekleme anlaşılır, kartlar yer değiştirmez | Orta |

### PERFORMANS · YÖNETİCİ

İyi çalışan detay: Ad ve bölge iki satırda. Sıra numaraları ve yüzdeler kolay taranıyor.
En belirgin sorun: SPY sütunundaki boşluğa rağmen ORT. RANDEVU H/G başlığı kırılıyor. Hedefteki ve hedef üzerindeki değerler aynı yeşilde.

| Konum | Mevcut görünüm ve sorun | Önerilen değişiklik | Neden | Öncelik |
|---|---|---|---|---|
| Tablo yerleşimi | Başlık ve tablo farklı sol çizgilerde. Tablo yaklaşık 716 px | İkisini aynı 24 px çizgisine al. En fazla 880 px tablo genişliği. Sütunlar yaklaşık 48 px / esnek / 152 px / 136 px | İsim alanı ve metrik sütunları dengelenir | Yüksek |
| Sütun başlıkları ve yüzdeler | Küçük başlıklar farklı biçimde kırılıyor. Yüzdeler aynı yeşilde | Başlık 12 px/700. Yüzde 15 px/650, eşit genişlikli rakamlar ve sağ hizalama. Mevcut %100 referansında eşik üstü yeşil, eşikte koyu nötr | Karşılaştırma hızlanır | Yüksek |
| Satırlar ve Ekip ortalaması | Ortalama satırı ayrılıyor, etiketi zayıf | Satırlar 50–52 px, ayırıcı 1 px. Ad 14 px/650, bölge 12 px/400. Uzun ad iki satıra açılabilir. Ortalama satırı #F1F4F2, etiket 14 px/700 ve üst ayırıcı | Özet ve sıralama daha hızlı taranır | Orta |
| Mobil sıralama | Mevcut CSS 480 px altında satırları karta dönüştürüyor | Mevcut düzeni koru. Üstte sıra, ad ve bölge. Altta iki eşit alanda H/G etiketleri ve 15 px değerler. Kart içi 12 px, kart arası 8 px | İki oran dar ekranda okunabilir kalır | Yüksek |

### GÖRÜŞMELER · SPY

İyi çalışan detay: Bugünkü rota görünür. Liste solda, ayrıntı veya harita sağda.
En belirgin sorun: Boş listede iki ayrı kutu benzer ağırlıkta görünüyor. Sağdaki mesaj, o anda seçilemeyen bir görüşmeye yönlendiriyor.

| Konum | Mevcut görünüm ve sorun | Önerilen değişiklik | Neden | Öncelik |
|---|---|---|---|---|
| Tümü / Bekleyen / Şu an / Gerçekleşti | Seçim, Saha Canlı’dan farklı biçimde gösteriliyor | Ortak açık yeşil seçili stil. Köşe 8 px, aralık 8 px, etiket 13 px/600. Mobil hedef 44 px, gerekirse iki satır | Aktif ve seçili olmayan filtreler kolay ayırt edilir | Yüksek |
| Boş liste ve ayrıntı | İki beyaz kutu eşit ağırlıkta | Bu süzgeçte görüşme yok. mesajı 14 px ve 16 px iç boşlukla kalsın. Sağ yardımcı metin 13 px, gölgesiz, nötr yüzeyde olsun. Mobilde kısa metni tek sütunla doğrula | Önce boş sonucun nedeni okunur | Orta |
| Bugünkü görüşme / Bekleyen / Gerçekleşti | Sıfır değerler de durum renkleriyle gösteriliyor | Sayılar 26 px/700 koyu metin, etiketler 13 px. Renk gerekirse etikete yakın küçük işarette. Mevcut mobil CSS bu sayaç grubunu gizliyor | Sıfır bekleyen, uyarı görünümü almaz | Orta |
| Bugünkü rota / Rotayı kapat | Açık ve kapalı durumda aynı yeşil çerçeve | Açık durumda açık yeşil dolgu ve seçili sınır. İşaretçide beyaz kontur. Mobilde 44 px kontrol ve yaklaşık 300 px harita | Rota modu iki görsel ipucuyla anlaşılır | Orta |
| Bildirimler kapalı | İri, gölgeli kutu üst şeridin önüne geçiyor | Köşe 12 px, hafif gölge, başlık 14 px/650, açıklama 13 px. Kapatma alanı 44 px, mobil yan boşluk 16 px | Uyarı görünür kalırken üst alan sadeleşir | Orta |

### PERFORMANS · SPY

İyi çalışan detay: Son 3 ay ortalaması kartındaki iki oran aynı ölçekte.
En belirgin sorun: %100 eşiği yalnızca açıklamada. Küçük H/G yüzdelerini iri yeşil sıra ve çağrı değerleri gölgeliyor.

| Konum | Mevcut görünüm ve sorun | Önerilen değişiklik | Neden | Öncelik |
|---|---|---|---|---|
| Randevu H/G ve Ciro H/G | Yüzdeler küçük. Çubuklar sayıdan baskın | Etiket 14 px/600. Yüzde masaüstü 28 px/700, mobil 24 px/700. Etiket solda, yüzde sağda, 8 px ray altta | Önce asıl değer okunur | Yüksek |
| Hedef işareti | %100 eşiği ray üzerinde görünmüyor | Mevcut %150 ölçeğinde her iki rayın üçte iki noktasına 2 px koyu işaret. Üst raya %100 hedef etiketi | Hedefle gerçekleşen oran tek bakışta karşılaştırılır | Yüksek |
| Ekipte H/G sıranız ve Bugünkü çağrı (en fazla 4) | 4 / 7 ve 0 / 4 iri ve yeşil | 22 px/650 koyu nötr rakam. Pay koyu, payda ikincil metin tonunda. Kart içi 16 px, kart arası 12 px | Destek metrikleri kolay okunur, H/G öne çıkar | Yüksek |
| Çağrı size nasıl gelir? | Uzun paragraf ana kartlarla aynı yüzey ağırlığında | Başlık 14 px/650, metin 13 px ve 20 px satır yüksekliği. Açık nötr yüzey, 16 px iç boşluk ve yaklaşık 75 karakterlik satır | Açıklama daha rahat okunur | Orta |

### PROFİL · YÖNETİCİ VE SPY

İyi çalışan detay: Kimlik bilgisi ve Çıkış yap aynı kartta kolay bulunuyor.
En belirgin sorun: SPY’de Müsait ve Molada 36 px. Bildirim izni uyarısı sıradan yardımcı metin gibi görünüyor.

| Konum | Mevcut görünüm ve sorun | Önerilen değişiklik | Neden | Öncelik |
|---|---|---|---|---|
| Kimlik kartı | Yönetici adı ve rolü aynı sözcüğü tekrar ediyor | Avatar 48 px, ad 18 px/700, rol 13 px/500. Yönetici rol satırını daha düşük ağırlıkta göster | Kimlik hiyerarşisi tutarlı olur | Düşük |
| Müsait / Molada ve BİLDİRİMLER | Seçim çoğunlukla renkle anlaşılıyor. İzin mesajı zayıf | Seçimde dolgu, sınır ve küçük onay işareti. Mobilde 44 px. Mevcut izin mesajı 13 px ve açık kehribar yüzey | Seçim ve dikkat durumu ayrışır | Orta |
| Çıkış yap | Tam genişlikte yeşil çerçeve güçlü vurgu alıyor | 44 px yükseklik, nötr sınır ve koyu metin | SPY’de müsaitlik kontrolü daha belirgin kalır | Düşük |

## 3. PANEL GENELİNDE ORTAK TASARIM KARARLARI

Panelde ölçülen marka yeşili #00724C. Diğer HEX değerleri tasarım önerisi. Resmî marka paleti doğrulanmadı. Mevcut font zinciri GOTHIC → Century Gothic → Segoe UI → Arial. Etkin font dosyası doğrulanamadı.

| Karar | Öneri |
|---|---|
| Marka ve yüzey | Marka #00724C, hover #005C3D, sayfa #F5F7F6, kart #FFFFFF, ayırıcı #DCE3DF, kontrol sınırı #87958E |
| Metin | Ana #192C25, ikincil #52635B. Küçük metinlerde en az 4,5:1 kontrast hedefi |
| Durumlar | Olumlu #00724C / #E7F3EE, dikkat #8A4B12 / #FFF1DD, olumsuz #A12E35 / #FDECEE, nötr #52635B / #EDF1EF. Rengin yanında etiket, ikon veya şekil kullan |
| Tipografi | Inter. Türkçe karakterleri ve uzun adları doğrula. Başlık masaüstü 24/30 px, mobil 22/28 px, 700. Bölüm 16/22 px, 650–700. Gövde 14/20 px, yardımcı 13/18 px, tablo başlığı 12/16 px, 700. Yüzde ve sıralamada eşit genişlikli rakamlar |
| Yerleşim | Masaüstü yan boşluk 24 px, mobil 16 px. Kart içi 16 px, ana KPI kartı masaüstünde 20 px. Kart arası 12 px, bölüm arası 24 px, köşe 10–12 px |
| Üst alan ve sekmeler | Logo yaklaşık 20 px, profil kontrolü 44 px. Alt menü ikonu 20 px, etiket 12 px/600, hedef 52 px. Aktif sekmede 2 px üst çizgi ve koyu yeşil metin |
| Buton ve filtreler | Masaüstü 40 px, mobil 44 px. Seçimde dolgu, sınır ve ağırlık birlikte değişsin. Hover’da hafif yüzey değişimi. Klavye odağında 2 px #195F9F halka ve 2 px dış boşluk. Devre dışı görünüm yalnızca gerçekten kullanılamayan kontrollerde |
| Grafik ve rakamlar | H/G gerçekleşeni dolu çubuk, hedefi koyu çizgi ve metinle göster. İncelenen ekranlarda ayrı zaman serisi grafiği veya TL tutarı görülmedi |
| Hareket | Sekme ve filtre 100–120 ms renk geçişi. Rota açılışı 140 ms opaklık, kaydırma konumu sabit. Harita işaretçisi seçimi 120 ms kontur geçişi. KPI ve tablolarda saydırma veya zıplama kullanma. Azaltılmış hareket tercihinde değişiklikler anında görünsün |
| Görseller | Saha Canlı ve Bugünkü rota için harita, Profil ve Personel Girişi için mevcut portre yeterli. İncelenen ekranlara dekoratif fotoğraf, illüstrasyon veya video eklemeyi önermiyorum. Kontrol ikonları 18 px, menü ikonları 20 px, çizgi 1,75–2 px |

## 4. UYGULAMA SIRASI

1. Performans · SPY — İki H/G değerini büyüt, %100 işaretini ekle, sıra ve çağrı değerlerini nötrleştir. Etki çok yüksek, efor düşük–orta.
2. Personel sekmeleri — Etiket kontrastını yükselt, aktif sekmeye üst çizgi ve kontrollerin tamamına görünür klavye odağı ekle. Etki yüksek, efor düşük.
3. Performans · Yönetici — Tablo hizasını, sütun genişliklerini, yüzde stilini ve Ekip ortalaması satırını düzenle. Mobil kartları 360 ve 390 px’de doğrula. Etki yüksek, efor orta.
4. Saha Canlı — Harita yüksekliğini ayarla, örnek zamanı belirginleştir, kişi kartlarını ilk ekranda görünür kıl. Etki yüksek, efor orta.
5. Saha Canlı, Görüşmeler ve Profil — Ortak seçim stillerine geç. Personel Girişi çerçevesini ve gölgesini sadeleştir. Etki orta–yüksek, efor orta.

Harita altlığı ve geçişleri son aşamaya bırak. Önce sabit ekranda başlık, veri ve durumların okunma sırasını kontrol et.

## 5. ÖNCE VE SONRA TASVİRİ

### PERFORMANS · SPY

Önce: Başlık solda, içerik daha içeriden başlıyor. Ana kartta iki uzun yeşil çubuk var, yüzdeler sağ uçta küçük. Alt sıradaki 4 / 7 ve 0 / 4 daha önce görülüyor.

Sonra — masaüstü: Başlık ve kartlar aynı 24 px çizgiden başlar. İçerik en fazla 880 px genişler. Ana kartta 20 px iç boşluk, üstte Son 3 ay ortalaması. Her H/G satırında solda etiket, sağda 28 px yüzde, altta 8 px çubuk. %100 işaretleri aynı düşey çizgide. İki destek kartı 12 px arayla eşit genişlikte ve 22 px koyu rakamlı. Açıklama en altta açık nötr yüzeyde. Alt menüde Performans üst çizgiyle seçili.

Sonra — mobil: 16 px yan boşluk, tek sütunda ana kart, 24 px yüzdeler. Destek kartları 360 px’de rahat sığıyorsa yan yana, etiketler sıkışıyorsa alt alta. %100 etiketi üst çubukta bir kez görünür.

### SAHA CANLI · YÖNETİCİ

Önce: Başlık, iki sayaç ve dört filtre görünür. Harita kalan yüksekliğin çoğunu kaplar. Kişi kartları alt menünün hemen üzerinde kesilir. Mesai dışı örnek zaman küçük gri metinde kalır.

Sonra — masaüstü: Başlık, sayaçlar, filtreler ve harita aynı 24 px çizgiye hizalanır. Başlığın altında Şirket Geneli ve mevcut örnek zaman farklı ağırlıkta görünür. İki sayaç tek sırada ve 28 px koyu rakamlarla gösterilir. Seçili filtre açık yeşil. Randevuda turuncu işaretini ve metnini korur. Harita yaklaşık 460 px. Alt menünün üzerinde ilk kişi kartı sırası ve durumları okunur. Seçilen kişi kartı sınır ve dolguyla ayrılır.

Sonra — mobil: Sayaçlar iki eşit sütunda. Filtreler 44 px hedeflerle gerektiğinde iki satıra kırılır. Harita yaklaşık 300 px, kişi kartları hemen altında tam genişlikte sıralanır. Alt menü için güvenli alan ayrılır ve harita kaynak bilgisi görünür kalır.
