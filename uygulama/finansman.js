/* FİNANSMAN KAPISI — bütçe/ödeme planı hesabı. Şu an KABA ÖRNEK hesap (ekranda 'Örnek hesaplamadır').
   Gerçek yayında senaryoHesapla() şirketin onaylı hesabına bağlanır (uyum/hukuk onayı şart); ekranlar değişmez.
   Ürün türleri, vade ve peşinat seçenekleri de buradan gelir. */
const EV_IKON_TASIT = "assets/eminevim/header_araba_yan.svg";
const EV_IKON_KONUT = "assets/eminevim/header_ev.svg";
const EV_IKON_ISYERI = "assets/eminevim/header_isYeri.svg";
/* eminevim.com/finansal-cozumler sayfalarından: her üründe Bireysel (kendi tahsisat tarihini belirle) ve Çekilişli (grup çekilişi) plan var. */
const FINANSMAN_TURLERI = {
  "Konut Finansmanı": { ikon: EV_IKON_KONUT, alt: "", nesne: "ev", ciper: [2000000, 3500000, 5000000, 8000000], aciklama: "Konut için bütçenize uygun ödeme planı. Temsilciniz aylık ödeme seçeneklerini sizinle netleştirir.", grup: "40–240 kişi" },
  "Taşıt Finansmanı": { ikon: EV_IKON_TASIT, alt: "", nesne: "araba", ciper: [500000, 1000000, 1500000, 2500000], aciklama: "Sıfır veya ikinci el araç için bütçenize uygun ödeme planı. Temsilciniz seçenekleri yanınızda getirir.", grup: "18–100 kişi" },
  "İşyeri Finansmanı": { ikon: EV_IKON_ISYERI, alt: "", nesne: "iş yeri", ciper: [1500000, 3000000, 5000000, 10000000], aciklama: "İşyeri için bütçenize uygun ödeme planı. Temsilciniz aylık ödeme seçeneklerini sizinle netleştirir.", grup: "40–240 kişi" },
};
const PLAN_TURLERI = {
  "Bireysel": "Peşinat ve taksitinizle tahsisat tarihinizi siz belirlersiniz.",
  "Çekilişli": "Alım gücünüze uygun bir grupta noter huzurunda çekiliş; daha erken teslim şansı.",
};
function turBilgi(tur) { return FINANSMAN_TURLERI[tur] || FINANSMAN_TURLERI["Konut Finansmanı"]; }
/* Eminevim sitesindeki bireysel finansman örneklerine (200.000 ₺ → 2.500 ₺ × 72 ay, teslim 30. ay, org. 16.800 ₺) ve
   BDDK tasarruf finansmanı kurallarına (teslim için birikim ≈ bedelin yarısı, en erken 6. ay; org. ücreti yarısı başvuruda,
   kalanı 4 taksit) dayanan KABA senaryo. Kesin plan temsilci görüşmesinde netleşir. */
function senaryoHesapla(tur, tutar, pesinatPct, vade) {
  tutar = Number(tutar) || 0; vade = Number(vade) || 0; pesinatPct = Number(pesinatPct) || 0;
  if (!tutar || !vade) return null;
  const pesinat = Math.round(tutar * pesinatPct / 100);
  const kalan = tutar - pesinat;
  const taksit = Math.max(100, Math.round(kalan / vade / 10) * 10);
  const teslimAy = Math.min(vade, Math.max(6, Math.ceil((tutar * 0.5 - pesinat) / taksit)));
  const org = Math.round(tutar * 0.085);
  return { pesinat, kalan, taksit, teslimAy, org, orgPesin: Math.round(org / 2), orgTaksit: Math.round(org / 8), toplam: tutar + org };
}
const VADE_SECENEKLERI = { "Taşıt Finansmanı": [12, 18, 24, 30, 36, 48, 60], "Konut Finansmanı": [24, 36, 48, 60, 72, 80, 96, 108, 120], "İşyeri Finansmanı": [24, 36, 48, 60, 72, 80, 96, 108, 120] };
const PESINAT_SECENEKLERI = [0, 10, 20, 30, 40];
