# veri/ — SPY listesi nereden geliyor

Uygulamadaki ve merkezdeki SPY listesi (`spyler.js`) **elle yazılmaz**: şirket dosyalarından üretilir.

```
veri/kaynak/*.csv  +  veri/ayarlar.json   →   python araclar/veri_hazirla.py   →   veri/spyler.js  (+ veri/hg_ozet.json)
```

## Dosyalar
| Dosya | Ne | Kim değiştirir |
|---|---|---|
| `kaynak/personel.csv` | Personel listesi (Sicil Numarası, Görev, Şube, Prim İşe Giriş Tarihi ...) | Şirket dışa aktarımı |
| `kaynak/sube_bolge_saha.csv` | Şube → Bölge, Saha, **Klasman** (personelin klasmanı şubesinden gelir) | Şirket dışa aktarımı |
| `kaynak/spy_hedef.csv` | Görev × Klasman ciro hedefi; kıdem kuralı (SPY1: 1-3 ay YSPY1, 4-6 YSPY2, 7-9 YSPY3) | Şirket dışa aktarımı |
| `kaynak/satis_kaydi.csv` | Satış kayıtları (ciro: `Org Tutar`, ay: `Kayıt Tarihi`, kişi: `UyeSatisTemsilciSicilNo`) | Şirket dışa aktarımı |
| `kaynak/randevu.csv` | Randevular (kişi: `Sorumlu Personel` ad soyad, ay: `Planl. Tarih`, sayılan: `Randevu Gerçekleşti`) | Şirket dışa aktarımı |
| `kaynak/sube_konum.csv` | Şube konumları (ad, adres, enlem, boylam; eminevim.com/subeler'den). Haritada yeşil nokta; 4 saatten ileri çağrıda yakınlık SPY'nin şubesinden | Proje ekibi |
| `kaynak/spy_ek.csv` | Şirket dosyalarında olmayan, yalnız bu uygulamanın istediği alanlar (sabit konum, fotoğraf, cinsiyet, müşteri puanı) | Proje ekibi |
| `ayarlar.json` | İş kuralları: H/G dönemi (3 ay), liste eşiği (%100), günlük randevu hedefi (10), iş günleri, sütun adları | Proje ekibi |
| `spyler.js` | **ÜRETİLEN** liste (`window.TY_SPYLER` + şubeler `window.TY_SUBELER`) | Elle düzenleme |
| `hg_ozet.json` | Her personelin ay ay hesabı ve listede olup olmadığının nedeni (kontrol için) | Üretilir |
| `org-data.js` | Örgüt yapısı (saha / bölge / şube / TL), gösteri verisi | |

## Kurallar (ayarlar.json'dan)
- **H/G** = gerçekleşen / hedef × 100. Son 3 **tamamlanmış** ayın ortalaması (içinde bulunulan ay sayılmaz; işe girişten önceki aylar atlanır).
- **Randevu hedefi** = günlük 10 × o aydaki iş günü (Pzt-Cmt; işe giriş ayında girişten sonraki günler).
- **Ciro hedefi** = `spy_hedef.csv`'den görev (kıdeme göre) × şubenin klasmanı.
- **Liste:** yalnız randevu H/G **ve** ciro H/G ikisi de %100 ve üzeri olan SPY uygulamada görünür.
- Departman `Alternatif Satış Ekibi`; görev adları `gorev_eslesme` ile SPY1/SPY2'ye çevrilir.

## Önemli
- Bu depo **herkese açık** (GitHub Pages). `kaynak/` altındaki dosyalar şirket sütun adlarıyla ama **uydurma değerlerle** üretilmiştir
  (`python araclar/ornek_veri_uret.py`). Gerçek kişi, hedef ve satış verisi buraya konmaz; gerçek sistemde bu klasör şirketin iç sunucusunda olur.
- Liste değişince merkez yeniden başlatılır (`merkez/sunucu.py --durdur`, sonra Başlangıç kısayolu).
- Bilinen zayıf nokta: randevu dosyasında kişi **ad soyadla** yazıyor; eşleşme adla yapılıyor (aynı adda iki kişi ya da yazım farkı sorun çıkarır).
  Şirket dosyasına sicil no sütunu eklenirse `randevu.kisi_sutunu` o sütunun adına çevrilir (kod hem adı hem sicili tanır).
