# SPY fotoğrafları (sentetik)

Kural: gerçek kişi fotoğrafı kullanılmaz. Buradaki 30 portre yapay olarak üretilmiş, var olmayan kişilerdir
(thispersondoesnotexist.com, 512×512 JPG). Kişi bilgileri `spyler.js`'te (uygulama `TEMSILCI_DETAY` ve merkez `merkez/sunucu.py` aynı dosyayı okur).
Klasör adı (`temsilci/`) kod yolu olduğu için değişmedi. Pilot bölge: Üsküdar, Ümraniye, Ataşehir. H/G değerleri uydurmadır (son 3 ay).
Onur Kaya, Derya Aksoy, Berk Cengiz, Selin Arslan (s1-s4) tanıtım videosu ve senaryodaki kişilerdir.
**2026-11-11:** uygulamada **7 SPY** var ("Kullanılıyor" = evet; hepsinin iki H/G'si ≥ %100). Diğer 23 portre klasörde duruyor, gerekirse yeniden eklenir.

| Dosya | Kişi | Sabit test konumu | Randevu / ciro H/G | Kullanılıyor |
|---|---|---|---|---|
| onur-kaya.jpg | Onur Kaya | Atatürk Mah., Ataşehir | %115 / %129 | evet |
| derya-aksoy.jpg | Derya Aksoy | Mimar Sinan Mah., Üsküdar | %126 / %130 | evet |
| berk-cengiz.jpg | Berk Cengiz | Namık Kemal Mah., Ümraniye | %105 / %105 | evet |
| selin-arslan.jpg | Selin Arslan | Bulgurlu Mah., Üsküdar | %120 / %100 | evet |
| emre-dogan.jpg | Emre Doğan | Altunizade Mah., Üsküdar | %108 / %101 | hayır |
| elif-sen.jpg | Elif Şen | Kısıklı Mah., Üsküdar | %117 / %114 | hayır |
| murat-sahin.jpg | Murat Şahin | Valide-i Atik Mah., Üsküdar | %94 / %103 | hayır |
| zeynep-guler.jpg | Zeynep Güler | Ünalan Mah., Üsküdar | %125 / %114 | hayır |
| burak-yildiz.jpg | Burak Yıldız | Beylerbeyi Mah., Üsküdar | %113 / %106 | hayır |
| merve-tunc.jpg | Merve Tunç | Çengelköy Mah., Üsküdar | %101 / %91 | hayır |
| kerem-aydin.jpg | Kerem Aydın | Kuzguncuk Mah., Üsküdar | %103 / %112 | hayır |
| busra-kilic.jpg | Büşra Kılıç | Ferah Mah., Üsküdar | %101 / %126 | hayır |
| gizem-ates.jpg | Gizem Ateş | Atakent Mah., Ümraniye | %102 / %129 | hayır |
| serkan-ozturk.jpg | Serkan Öztürk | Tantavi Mah., Ümraniye | %104 / %92 | hayır |
| ece-yalcin.jpg | Ece Yalçın | Çakmak Mah., Ümraniye | %114 / %113 | evet |
| mert-demir.jpg | Mert Demir | Esenşehir Mah., Ümraniye | %106 / %125 | hayır |
| pinar-cakir.jpg | Pınar Çakır | İnkılap Mah., Ümraniye | %88 / %95 | hayır |
| cem-koc.jpg | Cem Koç | Yukarı Dudullu Mah., Ümraniye | %103 / %104 | hayır |
| seda-kara.jpg | Seda Kara | Site Mah., Ümraniye | %101 / %123 | hayır |
| tolga-kurt.jpg | Tolga Kurt | Ihlamurkuyu Mah., Ümraniye | %96 / %110 | hayır |
| burcu-avci.jpg | Burcu Avcı | Madenler Mah., Ümraniye | %127 / %115 | evet |
| tugba-ozkan.jpg | Tuğba Özkan | Barbaros Mah., Ataşehir | %116 / %105 | hayır |
| baris-celik.jpg | Barış Çelik | İçerenköy Mah., Ataşehir | %117 / %116 | evet |
| neslihan-ucar.jpg | Neslihan Uçar | Kayışdağı Mah., Ataşehir | %102 / %97 | hayır |
| volkan-aksu.jpg | Volkan Aksu | Küçükbakkalköy Mah., Ataşehir | %121 / %104 | hayır |
| damla-bulut.jpg | Damla Bulut | Yenişehir Mah., Ataşehir | %109 / %126 | hayır |
| can-erdem.jpg | Can Erdem | Ferhatpaşa Mah., Ataşehir | %90 / %104 | hayır |
| irem-tas.jpg | İrem Taş | Esatpaşa Mah., Ataşehir | %105 / %128 | hayır |
| okan-polat.jpg | Okan Polat | Örnek Mah., Ataşehir | %99 / %99 | hayır |
| ugur-keskin.jpg | Uğur Keskin | İnönü Mah., Ataşehir | %116 / %104 | hayır |

Yeni kişi eklenirse aynı stilde yapay portre kullanın; kurumsal görünüm istenirse bir görsel üretme aracına:

```
Photorealistic corporate headshot of a fictional Turkish sales representative, [man/woman, age, hair].
Friendly natural smile, looking at camera, head and shoulders, centered. Dark green (#00724C) blazer over
a white shirt. Plain light grey (#F2F2F2) background, soft daylight. Square 1:1. No logos, no text.
The person must not resemble any real or famous person.
```
