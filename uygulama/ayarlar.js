/* Uygulama ayarları (tek yer). İş kuralları (H/G, randevu hedefi) veri/ayarlar.json'da; atama kuralları merkez/ty/ayarlar.py'de.
   Yükleme sırası: veri/spyler.js → uygulama/servisler.js → bu dosya → bicim → finansman → personel → hesap → ornek-veri → uygulama sayfası. */
const HIZMET_ILCELERI = ["Ümraniye", "Ataşehir", "Üsküdar"];
const LIVE_CONFIG = window.EMINEVIM_CONFIG || {};
// Merkez (merkez/sunucu.py) sürümü: çağrı, mesaj ve durumlar sunucudan; GitHub Pages kopyasında Canli.aktif=false (gösteri)
const CANLI = !!(window.Canli && window.Canli.aktif);
// TEST/DEVELOPMENT ONLY: production build must set this to false.
const TEST_MODE_SKIP_FORM = true;
const LOCATION_API = LIVE_CONFIG.locationEndpoint || "/api/live-locations";
const LOCATION_POLL_MS = Math.max(5000, LIVE_CONFIG.locationPollMs || 10000);
