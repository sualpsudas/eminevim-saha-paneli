/* Ortak biçim ve renk yardımcıları (tarih, saat, tutar, yüzde, mesafe, telefon). İş kuralı içermez. */
function qrResim(metin) {
  // vendor/qrcode.min.js ile QR görüntüsü (internet gerekmez); kütüphane yoksa boş
  try { const q = window.qrcode(0, "M"); q.addData(metin); q.make(); return q.createDataURL(6, 2); } catch (e) { return ""; }
}
function telYaz(t) { t = telAnahtar(t); return t.length === 10 ? "0" + t.slice(0, 3) + " " + t.slice(3, 6) + " " + t.slice(6, 8) + " " + t.slice(8) : t; }
function telAnahtar(t) { return String(t || "").replace(/\D/g, "").replace(/^0/, ""); }
function bugunYazi() {
  const gunler = ["Pazar", "Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi"], aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"];
  const d = new Date();
  return d.getDate() + " " + aylar[d.getMonth()] + " " + gunler[d.getDay()];
}
function yarinYazi() {
  const gunler = ["Pazar", "Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi"], aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"];
  const d = new Date(); d.setDate(d.getDate() + 1); if (d.getDay() === 0) d.setDate(d.getDate() + 1);
  return d.getDate() + " " + aylar[d.getMonth()] + " " + gunler[d.getDay()];
}
const NAVY = "#273755";
const GREEN = "#00724C";
const GOLD = "#EA803F";
const CORAL = "#EA803F";
const GOLD_TEXT = "#B25E30";
const CORAL_TEXT = "#B25E30";
const LINE = "#E4E1D8";
const INK = "#666666";
const PALETTE = [GREEN, GOLD, NAVY];

function fmtSure(sn) {
  const m = Math.floor(sn / 60);
  const s = sn % 60;
  return m + ":" + String(s).padStart(2, "0");
}
function readableSure(sn) {
  const m = Math.floor(sn / 60);
  const s = sn % 60;
  if (m <= 0) return s + " sn";
  if (s === 0) return m + " dk";
  return m + " dk " + s + " sn";
}
function ringColor(kalan) {
  if (kalan <= 60) return CORAL;
  if (kalan <= 300) return GOLD;
  return GREEN;
}
function ringTextColor(kalan, dark) {
  if (kalan <= 60) return dark ? CORAL : CORAL_TEXT;
  if (kalan <= 300) return dark ? GOLD : GOLD_TEXT;
  return GREEN;
}
function fmtSaat(t) {
  if (!t) return "";
  const d = new Date(t);
  return String(d.getHours()).padStart(2, "0") + ":" + String(d.getMinutes()).padStart(2, "0");
}
function fmtKm(km) {
  return Number(km || 0).toFixed(1).replace(".", ",");
}
function fmtCompact(value, currency) {
  // Intl "B" (bin) kısaltması finansta milyar sanılabildiği için açıkça "bin" yazılır.
  const text = new Intl.NumberFormat("tr-TR", { notation: "compact", maximumFractionDigits: 1 }).format(Number(value || 0)).replace(/\s?B$/, " bin");
  return text + (currency ? " ₺" : "");
}
function fmtPct(value) { return "%" + Math.round(Number(value || 0)).toLocaleString("tr-TR"); }
function hgColor(value) { return value >= 100 ? "#00724C" : value >= 80 ? "#B25E30" : "#B25E30"; }
function hgBg(value) { return value >= 100 ? "var(--tintGreen)" : value >= 80 ? "var(--tintGold)" : "var(--tintRed)"; }
function haversineKm(a, b) {
  if (!a || !b || !Number.isFinite(a.lat) || !Number.isFinite(a.lng) || !Number.isFinite(b.lat) || !Number.isFinite(b.lng)) return null;
  const rad = (v) => v * Math.PI / 180;
  const dLat = rad(b.lat - a.lat), dLng = rad(b.lng - a.lng);
  const h = Math.sin(dLat / 2) ** 2 + Math.cos(rad(a.lat)) * Math.cos(rad(b.lat)) * Math.sin(dLng / 2) ** 2;
  return 6371 * 2 * Math.atan2(Math.sqrt(h), Math.sqrt(1 - h));
}
function lerp(a, b, t) { return a + (b - a) * t; }
function ilkIlce(bolge) { return bolge.split("/")[0].trim(); }
