/* ÖRNEK (GÖSTERİ) VERİLERİ — örnek müşteriler, hazır randevu, ilçe koordinatları. Gerçek yayında kaldırılır ya da boşaltılır. */
function AYSE_SEED() {
  return {
    yeniMusteri: false, avatarUrl: "", degerlendirmeler: [], appointments: [],
    customerForm: { name: "Ayşe Kaya", phone: "0532 145 67 89", email: "ayse.kaya@ornek.com", address: "Barbaros Mah. Begonya Sk. No:12, Ataşehir / İstanbul", testMode: false },
    customerMeetings: [
      { name: "Ahmet Yılmaz", branch: "Kadıköy Şubesi", date: "12.09.2026" },
      { name: "Buse Demir", branch: "Ataşehir Şubesi", date: "18.09.2026" },
      { name: "Cem Kaya", branch: "Üsküdar Şubesi", date: "24.09.2026" },
    ],
    musteriBasvurulari: [],
    aktifBasvuruId: null,
    talepSebebi: "",
    // Randevusunu sohbette netleştirmiş; bugün görüşme günü, temsilcisi yolda
    mTalep: Appointment.create({ id: "ayse", tip: "ziyaret", kaynak: "Uygulama · kayıtlı müşteri", gunYazi: bugunYazi(), tarih: new Date().toLocaleDateString("en-CA"), saat: "18:00", yer: "Barbaros Mah., Ataşehir", konum: { lat: 40.9905, lng: 29.1050, adres: "Barbaros Mah., Ataşehir", bolge: "Ataşehir" }, durum: "yolda", repId: "s1", gecikme: 10, yolaCikis: Date.now(), sonKonum: Date.now(), demoZaman:{baslangic:Date.now(),simdi:new Date().setHours(17,58,0,0)}, varisZamani: new Date().setHours(18,10,0,0) }),
    chatMessages: [
      { from: "temsilci", t: Date.now() - 86400000, text: "Merhaba Ayşe Hanım, ben Onur Kaya, Eminevim müşteri temsilcinizim. Eminevim çözümlerimiz hakkında sizinle görüşmek isterim." },
      { from: "musteri", t: Date.now() - 86000000, text: "Merhaba Onur Bey, yarın akşam 18:00 uygun olur mu?" },
      { from: "temsilci", t: Date.now() - 85800000, text: "Elbette. Yarın 18:00'de Barbaros Mahallesi'ndeki adresinizde olacağım; ödeme planınızı da yanımda getireceğim." },
      { from: "musteri", t: Date.now() - 85600000, text: "Tamam, bekliyorum. Teşekkürler." },
      { from: "temsilci", t: Date.now() - 900000, text: "İyi akşamlar Ayşe Hanım, yola çıktım. Trafik nedeniyle yaklaşık 10 dakika gecikeceğim, kusura bakmayın; 18:10 gibi yanınızdayım." },
    ],
  };
}
// Örnek müşteriler (2026-11-12): hepsi kayıtlı, parola DEMO_PAROLA; hiçbirinde finansman yok. Ayşe'nin randevusu hazır, diğerleri boş başlar.
const ORNEK_MUSTERILER = [
  { tel: "5321456789", ad: "Ayşe Kaya", adres: "Barbaros Mah. Begonya Sk. No:12, Ataşehir / İstanbul" },
  { tel: "5332103456", ad: "Zeynep Arslan", adres: "Caferağa Mah. Moda Cd. No:48, Kadıköy / İstanbul" },
  { tel: "5353204567", ad: "Can Öztürk", adres: "Altunizade Mah. Kuşbakışı Sk. No:7, Üsküdar / İstanbul" },
  { tel: "5414305678", ad: "Elif Yıldız", adres: "Cevizli Mah. Bağdat Cd. No:215, Maltepe / İstanbul" },
  { tel: "5436507890", ad: "Burak Şahin", adres: "Atatürk Mah. Ihlamur Sk. No:3, Ataşehir / İstanbul" },
];
function ornekMu(tel) { return ORNEK_MUSTERILER.some((m) => m.tel === tel); }
function ornekSeed(tel) {
  if (tel === AYSE_TEL || !ornekMu(tel)) return AYSE_SEED();
  const m = ORNEK_MUSTERILER.find((x) => x.tel === tel);
  return { yeniMusteri: false, avatarUrl: "", degerlendirmeler: [], appointments: [], customerForm: { name: m.ad, phone: telYaz(m.tel), email: "", address: m.adres, testMode: false },
    customerMeetings: [], musteriBasvurulari: [], aktifBasvuruId: null, talepSebebi: "", mTalep: null, mGecmis: [], chatMessages: [] };
}
// Yeni üye kaydı için rastgele örnek bilgi: ad, kayıtlı olmayan telefon ve parola (yazmakla uğraşılmasın)
function rastgeleUye() {
  const ad = ["Selin", "Mert", "Derya", "Kerem", "Naz", "Emre", "Pelin", "Tolga", "Defne", "Barış"], soyad = ["Aydın", "Çelik", "Koç", "Polat", "Güneş", "Erdem", "Aksoy", "Kaplan", "Tekin", "Yavuz"];
  const r = (n) => Math.floor(Math.random() * n), d = (n) => Array.from({ length: n }, () => r(10)).join("");
  let tel; do { tel = ["530", "531", "536", "537", "538", "539"][r(6)] + d(7); } while (ornekMu(tel));
  const parola = "Ty" + d(4) + "k";
  return { ad: ad[r(ad.length)] + " " + soyad[r(soyad.length)], tel: telYaz(tel), parola };
}
const DISTRICT_COORDS = {
  "Beylikdüzü": { lat: 41.0035, lng: 28.6412 }, "Bakırköy": { lat: 40.9829, lng: 28.8770 },
  "Fatih": { lat: 41.0186, lng: 28.9497 }, "Beşiktaş": { lat: 41.0422, lng: 29.0061 },
  "Şişli": { lat: 41.0602, lng: 28.9877 }, "Üsküdar": { lat: 41.0227, lng: 29.0122 },
  "Kadıköy": { lat: 40.9927, lng: 29.0274 }, "Ataşehir": { lat: 40.9923, lng: 29.1244 },
  "Maltepe": { lat: 40.9354, lng: 29.1500 }, "Pendik": { lat: 40.8778, lng: 29.2358 }
};
const INITIAL_BASVURU = [
  { id: 1, ad: "Murat Y.", ilce: "Kadıköy", ...DISTRICT_COORDS["Kadıköy"], kalan: 218, telefonSon: "12" },
  { id: 2, ad: "Elif S.", ilce: "Kadıköy", lat: 40.9991, lng: 29.0418, kalan: 640, telefonSon: "47" },
  { id: 3, ad: "Kerem T.", ilce: "Üsküdar", ...DISTRICT_COORDS["Üsküdar"], kalan: 1180, telefonSon: "83" },
  { id: 4, ad: "Aylin D.", ilce: "Ataşehir", ...DISTRICT_COORDS["Ataşehir"], kalan: 55, telefonSon: "05" },
];

const DISTRICT_NAMES = ["Beylikdüzü", "Bakırköy", "Fatih", "Beşiktaş", "Şişli", "Üsküdar", "Kadıköy", "Ataşehir", "Maltepe", "Pendik"];

const DEMO_BASVURULAR = [
  { ad: "Zeynep K.", ilce: "Şişli" },
  { ad: "Tolga B.", ilce: "Maltepe" },
  { ad: "Sena Y.", ilce: "Beşiktaş" },
];

function coordForDistrict(ilce) { return DISTRICT_COORDS[ilce] || DISTRICT_COORDS["Ataşehir"]; }
// Prototip hesabı yalnız bu tarayıcıda. Parolanın kendisi diske yazılmaz.
const AYSE_TEL = "5321456789";
const DEMO_PAROLA = "test123";
const CUSTOMER_ILCE = "Ataşehir";
