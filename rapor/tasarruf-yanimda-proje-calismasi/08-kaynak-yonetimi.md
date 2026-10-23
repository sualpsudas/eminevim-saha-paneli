# Tasarruf Yanımda — Kaynak yönetimi

Tarih: 22 Ekim 2026, güncelleme 23 Ekim 2026. Durum: kullanıcının yönlendirmesiyle (“sahada çok çalışan var, herkes talebe gitmeyebilir”; “ekibin ayrılmış kısmı bunlarla ilgilenebilir”) hazırlanmış çerçeve. Yön: ayrılmış talep ekibi. Ayrıntılı kurallar henüz karar değildir. Proje tüzüğü: [00](00-proje-tuzugu.md).

## Çerçeve

Sahada çok sayıda çalışanımız var. Gelen talepleri karşılamak için herkesin çalışma düzenini değiştirmek gerekmez. Proje bir **kaynak yönetimi** sorusudur:

> **Saha gücümüzün ne kadarını, hangi kurallarla gelen taleplere ayıracağız; geri kalanını nasıl sahada tutacağız?**

İlke buna göre şöyle güncellenir:

**Saha gücümüzün bir bölümü bizi çağıran müşteriye ayrılır; diğer çalışanlarımız sahadaki çalışmalarını sürdürür. Bu dağılım gelen talebe göre ayarlanır.**

## Zamanlama: aynı gün talepleri de var

Talepler yalnızca ileri tarihli olmayabilir; müşteri **aynı gün** için de temsilci isteyebilir (kullanıcı düzeltmesi, 23 Ekim 2026). Bu nedenle talepler iki türdür:

- **İleri tarihli talepler:** Önceden bilinir, günün planına yerleşir.
- **Aynı gün talepleri:** Gün içinde hızlı yönlendirme gerektirir.

Aynı gün talebi için saha çalışanının elindeki işi bırakması verimli değildir. Bu talepleri, gün içinde yönlendirilebilir olan **ayrılmış talep ekibi** karşılar.

> Uygulama notu: Prototipte takvim bugün “yarından itibaren 3 hafta” açılıyor; aynı gün seçeneği yok. Bu karar kabul edilirse takvim güncellenmelidir.

## Kaynak ayırma modelleri

| Model | Nasıl işler? | Güçlü yanı | Zayıf yanı |
|---|---|---|---|
| **1. Ayrılmış ekip** | Belirli temsilciler yalnız gelen talepleri karşılar | Basit; sorumluluk net; karşılaştırma kolay | Talep azsa bu kişiler boş kalır; “kolay müşteri onlara gidiyor” algısı oluşabilir |
| **2. Nöbet / dönüşümlü görev** | Her gün bölge başına belirli temsilciler “talep sorumlusu” olur. Randevu yokken sahada çalışır, randevu varsa ona gider | Boşa zaman yok; fırsat herkese dönüşümlü düşer | Gün planı randevulara göre değişir; nöbet çizelgesi gerekir |
| **3. Uygun olana atama** | Talep, o saatte boş ve en yakın temsilciye atanır | Kaynak en verimli kullanılır | Karmaşık; stant gibi sabit işleri bozabilir; anlık konum ve takvim verisi gerekir |
| **4. Karma** | Bölge başına nöbetçi; nöbetçi doluysa takım lideri uygun bir başkasına atar | Esnek ve kontrollü | Kuralların açıkça yazılması gerekir |

## Seçilen yön

**Model 1: ayrılmış talep ekibi; taşan talep için takım lideri ataması (Model 4'ten).** Kullanıcı yönlendirmesi, 23 Ekim 2026.

Gerekçe:
1. Aynı gün talepleri hızlı yönlendirme ister; bunu saha çalışanının işini bölmeden ayrılmış ekip karşılar.
2. Sorumluluk nettir: talep sahipsiz kalmaz.
3. Talep ekibi ile saha ekibinin sonuçları doğrudan karşılaştırılabilir.

Bu yönün iki zayıf yanı için önlemler:
- **Talep azsa boş zaman:** Talep ekibi küçük başlar ve talebe göre büyütülür. Boş zamanında kendi bölgesinde saha çalışması yapabilir.
- **“Kolay müşteri onlara gidiyor” algısı ve ölçüm sapması:** Talep ekibine yalnız en başarılı temsilciler seçilmez; ekip üyeliği dönemsel olarak değişebilir. (Önceki taslakta önerilen nöbet modeli bu önlemin bir biçimi olarak kalabilir.)

## Kim talebe gider? Kim sahada kalır?

| Kriter | Açıklama |
|---|---|
| **Bölge** | Temsilci, talebin geldiği hizmet bölgesinden olmalı. Yol süresi verimliliği belirler. |
| **Takvim** | O saatte randevusu veya stant görevi olmamalı. |
| **Görev türü** | Stant gibi sabit noktada yapılan işten çekilmez. Kapı kapı gibi esnek işlerden çekilebilir. |
| **Dönüşüm sırası** | Fırsatlar nöbetçiler arasında sırayla ve görünür şekilde dağıtılır. |
| **Taşma** | Nöbetçi doluysa takım lideri başka bir temsilciye atar. Kimse uygun değilse müşteriye telefonla görüşme veya başka bir saat önerilir. |

## Kapasiteyi talebe göre ayarlamak

Ayrılan kaynak sabit değildir; iki sinyale göre büyür ya da küçülür:

| Sinyal | Anlamı | Yapılacak |
|---|---|---|
| Karşılanamayan veya ertelenen talep artıyor | Ayrılan kaynak yetmiyor | Nöbetçi sayısı veya saatleri artırılır |
| Nöbetçilerin randevusuz saatleri çok | Talep beklenenden az | Nöbetçi sayısı azaltılır; bulunabilirlik çalışmaları gözden geçirilir |

Bu ayar haftalık yapılabilir. Takım lideri ve satış yönetimi aynı göstergeleri görür.

## Rollerin sorumlulukları (öneri)

| Rol | Sorumluluk |
|---|---|
| **Saha personeli (SPY)** | Nöbet günü talepleri kabul eder, randevuya gider; diğer saatlerde saha çalışmasını sürdürür |
| **Takım lideri** | Nöbet çizelgesini yapar, taşan talebi atar, geciken talebi izler |
| **Saha grup lideri / yönetim** | Bölgeler arası dengeyi ve haftalık kapasite ayarını yapar |

Bu tablo öneridir; rollerin gerçek yetki ve sorumlulukları kurumla birlikte netleştirilmelidir.

## Ölçüm

Kaynak yönetimi bakışıyla ana ölçü aynı kalır, ama karşılaştırma netleşir:

- **Temsilci saati başına görüşme ve satış:** Talebe ayrılan saatler ile saha çalışmasına ayrılan saatler karşılaştırılır.
- **Ayrılan kaynağın doluluk oranı:** Nöbet saatlerinin ne kadarı randevuyla doldu?
- **Karşılanamayan talep oranı**
- **Talebe ilk dönüş süresi**

Dikkat edilmesi gereken bir nokta var. Talebe en başarılı temsilciler ayrılırsa sonuçlar şişer: farkın kanaldan mı, yoksa kişiden mi geldiği anlaşılmaz. Dönüşümlü nöbet bu sorunu da azaltır.

## Açık sorular

1. Bir bölgede kaç saha çalışanı var ve takımlar nasıl kurulu?
2. Stant ve kapı kapı çalışmalarının günlük planı kim tarafından, nasıl yapılıyor?
3. Prim veya hedef sistemi gelen taleplerden yapılan satışları nasıl sayacak?
4. Nöbet günlük mü, yarım günlük mü olmalı?
