# Tasarruf Yanımda — Kaynak yönetimi

Tarih: 22 Ekim 2026, güncelleme 23 Ekim 2026. Durum: kullanıcının yönlendirmesiyle (“sahada çok çalışan var, herkes çağrıya gitmeyebilir”; “ekibin ayrılmış kısmı bunlarla ilgilenebilir”) hazırlanmış çerçeve. Yön: çağrıları aktif SPY'ler karşılar. Ayrıntılı kurallar henüz karar değildir. Proje çerçevesi: [00](00-proje-cercevesi.md).

## Çerçeve

Sahada çok sayıda çalışanımız var. Gelen çağrıları karşılamak için herkesin çalışma düzenini değiştirmek gerekmez. Proje bir **kaynak yönetimi** sorusudur:

> **Saha gücümüzün ne kadarını, hangi kurallarla gelen çağrılara ayıracağız; geri kalanını nasıl sahada tutacağız?**

İlke buna göre şöyle güncellenir:

**Saha gücümüzün bir bölümü bizi çağıran müşteriye ayrılır; diğer çalışanlarımız sahadaki çalışmalarını sürdürür. Bu dağılım gelen çağrılara göre ayarlanır.**

## Zamanlama: aynı gün çağrıları de var

Çağrılar yalnızca ileri tarihli olmayabilir; müşteri **aynı gün** için de SPY çağırabilir (kullanıcı düzeltmesi, 23 Ekim 2026). Bu nedenle çağrılar iki türdür:

- **İleri tarihli çağrılar:** Önceden bilinir, günün planına yerleşir.
- **Aynı gün çağrıları:** Gün içinde hızlı yönlendirme gerektirir.

Aynı gün çağrısı için SPY'nin elindeki işi bırakması verimli değildir. Bu çağrıları, gün içinde yönlendirilebilir olan **aktif SPY'ler** karşılar.

> Uygulama notu: Prototipte takvim bugün “yarından itibaren 3 hafta” açılıyor; aynı gün seçeneği yok. Bu karar kabul edilirse takvim güncellenmelidir.

## Kaynak ayırma modelleri

| Model | Nasıl işler? | Güçlü yanı | Zayıf yanı |
|---|---|---|---|
| **1. Ayrılmış ekip** | Belirli SPY'ler yalnız gelen çağrıları karşılar | Basit; sorumluluk net; karşılaştırma kolay | Çağrı azsa bu kişiler boş kalır; “kolay müşteri onlara gidiyor” algısı oluşabilir |
| **2. Nöbet / dönüşümlü görev** | Her gün bölge başına belirli SPY'ler “çağrı sorumlusu” olur. Randevu yokken sahada çalışır, randevu varsa ona gider | Boşa zaman yok; fırsat herkese dönüşümlü düşer | Gün planı randevulara göre değişir; nöbet çizelgesi gerekir |
| **3. Uygun olana atama** | Çağrı, o saatte boş ve en yakın SPY'ye atanır | Kaynak en verimli kullanılır | Karmaşık; stant gibi sabit işleri bozabilir; anlık konum ve takvim verisi gerekir |
| **4. Karma** | Bölge başına nöbetçi; nöbetçi doluysa takım lideri uygun bir başkasına atar | Esnek ve kontrollü | Kuralların açıkça yazılması gerekir |

## Seçilen yön

**Model 1: çağrıları ayrılmış bir grup SPY (aktif SPY'ler) karşılar; taşan çağrıyı takım lideri atar (Model 4'ten).** Kullanıcı yönlendirmesi, 23 Ekim 2026.

Gerekçe:
1. Aynı gün çağrıları hızlı yönlendirme ister; bunu diğer SPY'lerin işini bölmeden aktif SPY'ler karşılar.
2. Sorumluluk nettir: çağrı sahipsiz kalmaz.
3. Aktif SPY'lerin sonuçları, benzer başarıdaki meslektaşlarıyla karşılaştırılabilir.

Bu yönün iki zayıf yanı için önlemler:
- **Çağrı azsa boş zaman:** Aktif SPY sayısı küçük başlar, gelen çağrılara göre artırılır. Aktif SPY'ler boş zamanlarında kendi bölgelerinde saha çalışması yapabilir.
- **“Kolay müşteri onlara gidiyor” algısı ve ölçüm sapması:** Karar (23 Ekim 2026): Sistem ilk aşamada **başarılı SPY'lerin** kullanımına açılır. Ölçüm sapmasını önlemek için aktif SPY'ler, benzer başarıdaki meslektaşlarıyla karşılaştırılır; seçim ölçütleri açıkça paylaşılır. Tasarruf Yanımda'da aktif olmak başarılı SPY'ler için bir teşvik olarak konumlanır (müşteriyi kolay bulan, satışa yakın görüşmeler). Sistemin sonra kimlere açılacağı henüz belirlenmedi; pilot bölge denemesinin sonuçlarıyla değerlendirilecek.

## Kim çağrıya gider? Kim sahada kalır?

| Kriter | Açıklama |
|---|---|
| **Bölge** | SPY, çağrının geldiği hizmet bölgesinden olmalı. Yol süresi verimliliği belirler. |
| **Takvim** | O saatte randevusu veya stant görevi olmamalı. |
| **Görev türü** | Stant gibi sabit noktada yapılan işten çekilmez. Kapı kapı gibi esnek işlerden çekilebilir. |
| **Atama** | İlk ölçüt başarıdır; yöntemin geri kalanı (yakınlık, uygunluk, sıra, performans puanı) sonra belirlenecek. |
| **Taşma** | Aktif SPY'ler doluysa takım lideri başka bir SPY'ye atar. Kimse uygun değilse müşteriye telefonla görüşme veya başka bir saat önerilir. |

## Kapasiteyi çağrıya göre ayarlamak

Ayrılan kaynak sabit değildir; iki sinyale göre büyür ya da küçülür:

| Sinyal | Anlamı | Yapılacak |
|---|---|---|
| Karşılanamayan veya ertelenen çağrı artıyor | Ayrılan kaynak yetmiyor | Aktif SPY sayısı veya saatleri artırılır |
| Aktif SPY'lerin randevusuz saatleri çok | Çağrı beklenenden az | Aktif SPY sayısı azaltılır; bulunabilirlik çalışmaları gözden geçirilir |

Bu ayar haftalık yapılabilir. Takım lideri ve satış yönetimi aynı göstergeleri görür.

## Rollerin sorumlulukları (öneri)

| Rol | Sorumluluk |
|---|---|
| **Aktif SPY** | Çağrıları kabul eder, randevuya gider; randevu olmayan saatlerde saha çalışmasını sürdürür |
| **Diğer SPY'ler** | Sahadaki çalışmalarını sürdürür |
| **Takım lideri** | Aktif SPY'lerin programını izler, taşan çağrıyı atar, geciken çağrıyı izler |
| **Saha grup lideri / yönetim** | Bölgeler arası dengeyi ve haftalık kapasite ayarını yapar |

Bu tablo öneridir; rollerin gerçek yetki ve sorumlulukları kurumla birlikte netleştirilmelidir.

## Ölçüm

Kaynak yönetimi bakışıyla ana ölçü aynı kalır, ama karşılaştırma netleşir:

- **SPY saati başına görüşme ve satış:** Çağrıya ayrılan saatler ile saha çalışmasına ayrılan saatler karşılaştırılır.
- **Ayrılan kaynağın doluluk oranı:** Aktif SPY'lerin çağrıya ayrılan saatlerinin ne kadarı randevuyla doldu?
- **Karşılanamayan çağrı oranı**
- **Çağrıya ilk dönüş süresi**

Aktif SPY'ler başarılı SPY'lerden seçildiği için sonuçlar tüm SPY'lerle karşılaştırılmaz; aksi hâlde farkın kanaldan mı kişiden mi geldiği anlaşılmaz. Karşılaştırma, benzer başarıdaki meslektaşlarıyla yapılır.

## Açık sorular

1. Bir bölgede kaç saha çalışanı var ve takımlar nasıl kurulu?
2. Stant ve kapı kapı çalışmalarının günlük planı kim tarafından, nasıl yapılıyor?
3. Prim veya hedef sistemi gelen çağrılardan yapılan satışları nasıl sayacak?
4. Aktif olma günlük mü, dönemlik mi olmalı?
