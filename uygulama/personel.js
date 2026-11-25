/* PERSONEL KAPISI (uygulama tarafı) — SPY bilgileri veri/spyler.js'ten (window.TY_SPYLER).
   veri/spyler.js şirket verisinden üretilir: python araclar/veri_hazirla.py (personel, şube/klasman, hedef, satış, randevu → H/G).
   Gerçek sistemde IT bu listeyi kendi personel servisinden verir; alanlar IT_DEVIR.md → Personel. Kimlik sicil no; id uygulama içi kısa kimlik. */
function atamaMesaji(ilkAd, repId, t) {
  // Temsilci atanınca ilk mesaj: kendini tanıtır ve saati önerir (müşteri Sohbet'te "Saati onayla" ile onaylar)
  return { from: "temsilci", t: Date.now(), text: "Merhaba " + ilkAd + ", ben " + TEMSILCI_DETAY[repId].ad + ", Eminevim müşteri temsilcinizim. " + (t ? "Görüşmemizi " + t.gunYazi + " " + t.saat + ", " + t.yer + " olarak planladım. Uygunsa aşağıdan onaylayabilirsiniz." : "") };
}
/* Müşterinin gördüğü temsilci bilgileri (panelde kısa ad kullanılır) */
// 7 test SPY'si: spyler.js (merkez/sunucu.py da aynı dosyayı okur). foto: sentetik portre, assets/temsilci/OKUBENI.md
// Hareketli örnek SPY'ler (yalnız canlı test merkezi sunar: window.TY_SPYLER_SIM) yalnız müşteri tarafı bilgi kartında kullanılır
const TEMSILCI_DETAY = (window.TY_SPYLER || []).concat(window.TY_SPYLER_SIM || []).reduce((o, x) => { o[x.id] = x; return o; }, {});
