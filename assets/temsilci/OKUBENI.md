# Temsilci fotoğrafları (sentetik)

Kural: gerçek kişi fotoğrafı kullanılmaz. Portreler bir görsel üretme aracıyla (ChatGPT, Gemini vb.) üretilir.
Dosyaları bu klasöre aşağıdaki adlarla koyun (kare, en az 512×512, JPG). Sonra uygulamada
`TEMSILCI_DETAY` içindeki `foto` alanları doldurulur (ör. `foto: "assets/temsilci/onur-kaya.jpg"`).

| Dosya | Kişi | Rol | Tarif |
|---|---|---|---|
| onur-kaya.jpg | Onur Kaya | Temsilci, Ataşehir | erkek, 30–35 yaş, kısa koyu saç, temiz traşlı |
| derya-aksoy.jpg | Derya Aksoy | Temsilci, Üsküdar | kadın, 28–33 yaş, omuz hizasında koyu kumral saç |
| berk-cengiz.jpg | Berk Cengiz | Temsilci, Ümraniye | erkek, 38–45 yaş, kısa saç, kısa bakımlı sakal |
| ahmet-yilmaz.jpg | Ahmet Yılmaz | Takım Lideri | erkek, 42–48 yaş, kır düşmüş kısa saç |
| selin-arslan.jpg | Selin Arslan | Temsilci (yedek) | kadın, 35–40 yaş, toplu saç |
| emre-dogan.jpg | Emre Doğan | Temsilci (yedek) | erkek, 26–30 yaş, kısa saç |

## Görsel aracına yapıştırılacak metin

Her kişi için ayrı ayrı, `[TARİF]` yerine tablodaki tarifi yazarak (İngilizce daha tutarlı sonuç verir):

```
Photorealistic corporate headshot of a fictional Turkish sales representative, [TARİF, İngilizce:
ör. "man, 32 years old, short dark hair, clean-shaven"]. Friendly natural smile, looking at camera,
head and shoulders, centered. Wearing a dark green (#00724C) blazer over a white shirt, small plain
white name badge with no text. Plain light grey (#F2F2F2) studio background, soft even daylight,
sharp focus. Square 1:1, 1024x1024. No logos, no text, no watermark. The person must not resemble
any real or famous person.
```

Aynı stilde olsun diye altısını aynı sohbette, ilkine benzetmesini isteyerek üretin
("Same lighting, background, framing and clothing as the previous image").
