/* DIŞ SERVİSLER — uygulamanın kullandığı dış adresler tek yerde. Harita sayfaları (harita/*.html) ve uygulama bu dosyayı okur.
   Şu an ücretsiz genel servisler (yalnız test için; yoğun ticari kullanıma izin vermezler). Gerçek yayında yalnız buradaki
   adresler şirketin anlaşmalı/kendi servisleriyle değiştirilir:
   - haritaAltlik: harita görüntüsü (OpenStreetMap) → ör. Apple MapKit JS, Mapbox, şirket harita sunucusu
   - rota:        araçla yol rotası ve süre (OSRM genel sunucusu) → ücretli ya da kendi yönlendirme servisi
   - adresArama:  adres ↔ konum çevirisi (Nominatim) → ücretli adres servisi */
window.TY_SERVISLER = Object.assign({
  haritaAltlik: {
    url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    subdomains: "abc",
    maxZoom: 19
  },
  rota: "https://router.project-osrm.org/route/v1/driving/",
  adresArama: "https://nominatim.openstreetmap.org/"
}, window.TY_SERVISLER || {});
