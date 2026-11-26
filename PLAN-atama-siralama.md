# PLAN — Atama seçenekleri: kompakt çağrı sıralaması (2026-11-26)

Kullanıcı kararı: takip sayfasındaki **Atama seçenekleri → çağrı sıralaması** her SPY için **tek satır** olsun,
satıra dokununca ayrıntı açılsın; ayrıntıda kriterlerin **puan katkısı yerine gerçek değeri** görünsün.
Önce `AGENTS.md` ve `CLAUDE.md`'yi oku. Yanıtlar ve belgeler Türkçe.

## Şu anki durum
- Çizim: `merkez/takip.html` → `apSiraHtml(s, baslik, deneme)` (yaklaşık satır 636).
  Bunu `apSiraCiz()` çağırıyor (iki blok çiziliyor: "Atama anında" ve isteğe bağlı "Şimdiki seçeneklerle").
- Her SPY dört satır tutuyor:
  1. Ad, rozetler ve puan
  2. Renkli çubuk
  3. "Yakınlık 24 · Çağrı sayısı 22,5 · …" (puan katkıları)
  4. Mesafe, süre ve o günkü çağrı
- Veri: `merkez/ty/atama.py` → `adaylar()` her aday için `ayrinti` sözlüğü üretiyor.
  `siralama_ozet()` bunu `adaylar` listesine koyuyor.
- `ayrinti` içinde şunlar var: `parca` (kriter puanları), `km`, `dk`, `carpan`, `trafik` ("canlı"/"tipik"/""), `rotaSayisi`,
  `kaynak` ("yol"/"kus"/"yok"), `cagri` (o günkü çağrı sayısı), `nereden`, `oncelik`, `ayniIlce`, `subeIlce`.
- **Eksik:** ciro H/G ve randevu H/G yüzdeleri yalnız `gerekce` metninde geçiyor, ayrı alan yok.

## 1. Merkez (veri) — `merkez/ty/atama.py`
1. `adaylar()` içindeki `ayrinti` sözlüğüne şu alanları ekle:
   - `"ciroHG": s.get("ciroHG")`
   - `"randevuHG": s.get("randevuHG")`
   - `"gunlukSinir": sinir`
   Puan hesabı DEĞİŞMEZ.
2. Başka dosya değişmez. Eski kayıtlarda bu alanlar yoksa sayfa "—" göstersin.

## 2. Görünüm — `merkez/takip.html`, `apSiraHtml`
**Kapalı satır (tek satır, varsayılan):**
```
1. Ece Yalçın  [aynı ilçe] [2 km altı]   4,2 km · 9 dk   ▓▓▓▓▓░░░  72
```
- Satırda şunlar olsun:
  - sıra numarası
  - ad (ilk sıradaysa yeşil kalın)
  - rozetler (`.ap-onc`, mevcut)
  - yakınlık özeti: `km` · `~dk` (kuş uçuşuysa "kuş uçuşu")
  - ince, kısa renkli çubuk (mevcut `.ap-bar`, satır içinde yaklaşık 60–80 px)
  - toplam puan (sağda, kalın)
- "· teklif edilen" / "· ilk sırada" yazısı kalksın; ilk satırın vurgusu yeterli.
- Telefonda (390 px) tek satıra sığmalı. Sığmazsa ad kısalsın (`text-overflow: ellipsis`); çubuk ve puan her zaman görünsün.

**Açık satır (dokununca altında):** kriter başına **gerçek değer**, yanında küçük gri puan katkısı:
```
Yakınlık      9 dk (anlık trafik ×1,9 · 2 rotadan en hızlısı) · şu anki yerinden · şube: Ümraniye   24 p
Çağrı sayısı  o gün 1 / 4                                                                          22,5 p
Ciro H/G      %115                                                                                 10 p
Randevu H/G   %130                                                                                 10 p
```
- Yakınlık değeri uzaklık türüne göre değişir (`s.uzaklik`):
  - "trafikli" ve "yol" → dk
  - "yolkm" ve "kus" → km
  - Parantez içi mevcut metinden gelir: `carpan`, `trafik`, `rotaSayisi`, `kaynak`, `nereden`, `subeIlce`.
- Kriter adının önünde çubuktaki renk küçük kare olarak dursun (`OLCUT` renkleri). Böylece ayrı lejant satırı (`.ap-lejant`) kaldırılabilir.
- Puan katkısı küçük ve gri ("24 p"). Asıl vurgu gerçek değerde.

**Davranış:**
- Satır bir `<button>` (ya da `role="button"`, `tabindex=0`) olsun. `aria-expanded` doğru güncellensin; klavyede Enter/Boşluk ile açılsın.
- Aynı anda birden fazla satır açık olabilir.
- `apSiraCiz` yeniden çizdiğinde açık satırlar kapanmasın. Açık aday id'lerini bir kümede tut, çizimden sonra geri uygula.
  `apAnahtar` ile gereksiz yeniden çizim zaten engelleniyor; bu kontrol bozulmasın.
- "Elenen N SPY" (`details`) aynı kalsın.

**Silinecekler:** her SPY'deki 3. satır (puan katkıları listesi) ve 4. satır (yol metni). İkisi de açık satıra taşınır.

## 3. Kurallar
- İç ekran olduğu için "SPY" ve "çağrı" kullanılır. "ASK" yazılmaz.
- Gereksiz açıklama metni eklenmez (kullanıcı 2026-11-26'da bu bölümdeki açıklamaları kaldırttı).
- Görünüm: yeşil #00724c, turuncu #ea803f, mevcut `.ap-*` stilleri. Yeni CSS de `.ap-` önekiyle olsun.
- GitHub Pages kopyası etkilenmez: bu bölüm yalnız merkezde görünür, `?demo=1` modunu bozma. `video/`, `backup/` değişmez.

## 4. Deneme ve test
1. Deneme kopyası:
   - `merkez/` içinde `TY_PORT=8795 TY_YOL=deneme TY_VERI=<geçici>\deneme.json` ile `python sunucu.py` (conda base).
   - Aç: `http://127.0.0.1:8795/deneme/takip`
   - Haritada "+ Çağrı ekle" ile 2–3 çağrı ekle, "Atama seçenekleri"ni aç.
   - Tek satır görünümünü, açıp kapamayı, telefon genişliğini (390 px) ve "Yeniden hesapla" sonrası açık satırların korunmasını dene.
2. Testler (conda `scrapling` Python, `PYTHONIOENCODING=utf-8`):
   - `tests/merkez-akis.py` (deneme kopyası 8795 açıkken)
   - `tests/phone-layout.py`
   - `tests/browser-flows.py`
3. Bitince deneme kopyasını `python sunucu.py --durdur` ile durdur (aynı TY_* değişkenleriyle). taskkill KULLANMA.

## 5. Bitirme
1. Belgeleri güncelle:
   - `rapor/tasarruf-yanimda-proje-calismasi/10-atama-ve-rota.md`, "Atama seçenekleri" bölümüne sıralamanın tek satır + ayrıntı ve gerçek değer gösterdiğini yaz.
   - `TEKNIK.md`'ye yeni `ayrinti` alanlarını (`ciroHG`, `randevuHG`, `gunlukSinir`) ekle.
   - `PROJE_ILERLEME.md` sonuna tarihli kısa bir not ekle.
2. Commit + push (`master`).
3. Canlı merkezi yeniden başlat:
   1. `merkez/` içinde `python sunucu.py --durdur`
   2. Başlangıç klasöründeki "Tasarruf Yanimda Merkezi" kısayolunu çalıştır.
   3. Takip sayfası 200 dönmeli; sayfada yeni kod görünmeli.
4. Kullanıcıya kanıt göster: ekran görüntüsü (kapalı + açık satır, bilgisayar + telefon) ve test çıktılarının son satırları.

## Kapsam dışı (ayrı karar)
- Ciro/Randevu H/G'de %100'ün altındaki herkes 0 puan alıyor (%95 ile %40 aynı). Kullanıcıya soruldu, karar verilmedi; puan hesabına dokunma.
