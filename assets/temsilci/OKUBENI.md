# SPY fotoğrafları (sentetik)

Kural: gerçek kişi fotoğrafı kullanılmaz. Buradaki dört portre yapay olarak üretilmiş, var olmayan kişilerdir
(thispersondoesnotexist.com, 512×512 JPG). Uygulamada `TEMSILCI_DETAY` → `foto`, merkezde `merkez/sunucu.py` → `SPYLER` kullanır.
Klasör adı (`temsilci/`) kod yolu olduğu için değişmedi.

| Dosya | Kişi | Rol | Şube / sabit test konumu |
|---|---|---|---|
| onur-kaya.jpg | Onur Kaya | SPY | Ataşehir Şubesi · Atatürk Mah., Ataşehir |
| derya-aksoy.jpg | Derya Aksoy | SPY | Üsküdar Şubesi · Mimar Sinan Mah., Üsküdar |
| berk-cengiz.jpg | Berk Cengiz | SPY | Ümraniye Şubesi · Namık Kemal Mah., Ümraniye |
| selin-arslan.jpg | Selin Arslan | SPY | Üsküdar Şubesi · Bulgurlu Mah., Üsküdar |

Yeni kişi eklenirse aynı stilde yapay portre kullanın; kurumsal görünüm istenirse bir görsel üretme aracına:

```
Photorealistic corporate headshot of a fictional Turkish sales representative, [man/woman, age, hair].
Friendly natural smile, looking at camera, head and shoulders, centered. Dark green (#00724C) blazer over
a white shirt. Plain light grey (#F2F2F2) background, soft daylight. Square 1:1. No logos, no text.
The person must not resemble any real or famous person.
```
