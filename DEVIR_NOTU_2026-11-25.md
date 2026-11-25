# 25 Kasım 2026 çalışma ve devir notu

## Devralınan yerel çalışma

Bu çalışmaya başlanırken son kayıt `ccfe141` idi. Hemen çağrıların aynı ilçede bulunan SPY'lere gitmesi bu kayıtta zaten vardı. Aşağıdaki değişiklikler çalışma klasöründe hazırdı ve henüz Git'e kaydedilmemişti.

- `merkez/ty/atama.py` ve `ayarlar.py` içinde varsayılan puanlar yakınlık 40, günün çağrı sayısı 30, ciro hedef gerçekleşmesi 20, randevu hedef gerçekleşmesi 10 olarak düzenlenmişti.
- `merkez/ty/yol.py` ve `trafik.py`, yol mesafesi ve tahmini varış süresi hesabını sağlıyordu. `araclar/trafik_hazirla.py` ve `veri/trafik-carpan.json`, İBB'nin geçmiş verilerinden tipik trafik çarpanlarını hazırlamak için eklenmişti.
- `merkez/ty/islemler.py` ve `merkez/takip.html` içinde atama seçeneklerini okuma, kaydetme, varsayılana dönme, çağrı başına sıralama ve deneme hesabı eklenmişti.
- Belgeler de güncellenmişti. İlgili dosyalar `IT_DEVIR.md`, `TEKNIK.md`, `URUN_KURALLARI.md`, `PROJE_ILERLEME.md` ve `rapor/tasarruf-yanimda-proje-calismasi/10-atama-ve-rota.md`.

## Sonradan yapılan değişiklikler

1. `Eminevim Saha Paneli.dc.html` içinde personel giriş seçimi gerçek giriş listesine bağlandı. Beş hareketli örnek SPY giriş listesinden çıkarıldı. Müşteri giriş düğmesinin erişilebilir adı ekrandaki metne bağlandı. Chrome dekoratif oku “Devam et” ve “Doğrula” düğmelerinin adına ekliyordu.
2. `merkez/takip.html` içinde uygulamaya gömülü canlı Saha Canlı ekranında Atama seçenekleri düğmesi görünür yapıldı. Yeniden hesaplama sonucunun birincisi “ilk sırada”, gerçek teklifin birincisi “teklif edilen” olarak gösteriliyor.
3. `tests/merkez-akis.py` içinde Aydınlatma Metni'ni açma, saklama süresini okuma ve kapatma adımları kayıt ekranına taşındı. Ticari ileti iznini geri alma kontrolü Ayarlar'da.
4. `tests/browser-flows.py` içinde dar ekran genişliği kontrolü açık randevu ayrıntısı penceresine bağlandı. Önceki seçici hem listeyi hem ayrıntıyı buluyordu.
5. `tests/web-flows.py` ve `tests/preparation-popup.py` güncel “Görüşmeye hazırlık” ve “Finansman ön tercihleri” düğmelerine göre düzenlendi. Web testi müşterinin hazırlık penceresini tekrar açabildiğini kontrol ediyor.
6. `PROJE_ILERLEME.md` sonuna tarihli doğrulama notları eklendi. Bu dosya devir için oluşturuldu.
7. Kullanıcı telefon için çalışan güncel tasarımı seçti. `URUN_KURALLARI.md` içine logosuz üst bant ve yüzen menü kararı eklendi. `tests/phone-layout.py` menü kenar boşluğunu, içerik için ayrılan alanı, klavyede mesaj yazma ve menüye geri dönüşü kontrol ediyor.
8. `tests/appointment-list.py` tarih bloğu, güncel durum etiketi, pencereyi dışına dokunarak kapatma, hesap düğmesinin hizası ve çerçeve içindeki menü ölçülerine uyarlandı. `tests/browser-flows.py` içinde “Tarihi değiştir”, randevuyu listeden açarak iptal etme ve aynı müşterinin numarasını tekrar girerek oturum açma adımları güncellendi.
9. `tests/merkez-akis.py` ilk çağrı kaydıyla dört saniye sonra oluşan teklifi ayrı adımlarda izliyor. Bildirime dokunma, aynı SPY'nin kamera testi, ilçeye göre uygun adaylar ve Saha Canlı'daki on iki işaret için deneme adımları güncellendi.

## Deneme merkezinde doğrulananlar

- Ümraniye örneğinde 5 aday sıralandı, 7 SPY gerekçesiyle elendi. Ölçütlerin toplamı aday puanını verdi ve ilk adaya teklif gitti.
- Dört uzaklık türünde kaydetme ve yeniden hesaplama çalıştı. Önceki çağrının kayıtlı sıralaması ve teklifi korundu. Yeni çağrıda yeni ağırlık ve ilçe şartı kullanıldı.
- Tüm ağırlıklar sıfırken merkez kaydı reddetti. Varsayılana dönüş, telefon genişliğinde panel, Escape ile kapatma, harita filtreleri ve haritada çağrı ekleme moduna giriş/çıkış kontrol edildi.
- Müşteri telefon görünümünde girişten randevu listesine ulaşıldı. Personel girişinde boş seçim, 7 SPY ve Yönetici doğrulandı. Node testleri ve panel senaryosu geçti.

## Yayın durumu

GitHub'a gönderim ve canlı merkezde yeniden başlatma yapılmadı. Genel testler geçmeden yayın yapılmaması gerekiyor. Denemelerde geçici veri ve ayrı merkez kullanıldı.
