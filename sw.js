const CACHE = 'eminevim-v102';
const ASSETS = [
  './',
  './index.html',
  './Eminevim Saha Paneli.dc.html',
  './uygulama/assignment.js',
  './uygulama/appointment.js',
  './uygulama/servisler.js',
  './uygulama/ayarlar.js',
  './uygulama/bicim.js',
  './uygulama/finansman.js',
  './uygulama/personel.js',
  './uygulama/hesap.js',
  './uygulama/aydinlatma.js',
  './uygulama/ornek-veri.js',
  './uygulama/support.js',
  './harita/konum-sec.html',
  './harita/rota.html',
  './harita/map.html',
  './vendor/qrcode.min.js',
  './vendor/jsQR.js',
  './veri/spyler.js?v=2',
  './veri/org-data.js?v=7',
  './vendor/react.production.min.js',
  './vendor/react-dom.production.min.js',
  './manifest.json',
  './assets/logo-green.png',
  './assets/logo-white.png',
  './assets/tasarruf-yanimda-logo.png',
  './assets/ty-isaret.png','./assets/fonts/jakarta-400.ttf','./assets/fonts/jakarta-500.ttf','./assets/fonts/jakarta-600.ttf','./assets/fonts/jakarta-700.ttf','./assets/fonts/jakarta-800.ttf','./assets/ty/giris-sahne.webp',
  './assets/ty/acilis-foto.webp','./assets/ty/acilis-el-sikisma.webp','./assets/ty/acilis.mp4','./assets/ty/hero-randevu.webp','./assets/ty/hero-sohbet.webp','./assets/ty/hero-finans.webp','./assets/ty/hero-ayar.webp','./assets/ty/hero-profil.webp','./assets/ty/kart-konut.webp','./assets/ty/kart-tasit.webp','./assets/ty/kart-isyeri.webp','./assets/eminevim/header_araba_yan.svg',
  './assets/icon-180.png',
  './assets/icon-192.png',
  './assets/icon-512.png'
];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(ASSETS).catch(() => {})));
  self.skipWaiting();
});
self.addEventListener('message', (e) => { if (e.data === 'skipWaiting') self.skipWaiting(); });

self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))));
  self.clients.claim();
});

// Network-first for HTML/JS/JSON (kod güncellemeleri anında ulaşsın);
// cache-first for statik varlıklar (görseller, ikonlar).
function isAppShell(url) {
  return /\.(html|js|json)$/i.test(url.pathname) || url.pathname === '/' || url.pathname.endsWith('/');
}

// iPhone (WebKit) video için 'Range' isteği ister; önbellekten tam dosya (200) dönerse video oynamaz → 206 parça yanıtı
async function videoYanit(req) {
  const c = await caches.open(CACHE);
  let hit = await c.match(req.url);
  if (!hit) {
    const res = await fetch(req.url);
    if (res.ok) c.put(req.url, res.clone()).catch(() => {});
    hit = res;
  }
  const aralik = req.headers.get('range');
  if (!aralik || !hit.ok) return hit;
  const buf = await hit.arrayBuffer();
  const m = /bytes=(\d*)-(\d*)/.exec(aralik) || [];
  let bas = m[1] ? parseInt(m[1], 10) : 0, son = m[2] ? parseInt(m[2], 10) : buf.byteLength - 1;
  if (son >= buf.byteLength) son = buf.byteLength - 1;
  return new Response(buf.slice(bas, son + 1), { status: 206, headers: {
    'Content-Type': 'video/mp4', 'Accept-Ranges': 'bytes', 'Content-Length': String(son - bas + 1),
    'Content-Range': 'bytes ' + bas + '-' + son + '/' + buf.byteLength } });
}

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== location.origin) {
    e.respondWith(fetch(req).catch(() => caches.match(req)));
    return;
  }
  if (/\.mp4$/i.test(url.pathname)) { e.respondWith(videoYanit(req)); return; }
  if (isAppShell(url)) {
    e.respondWith(
      fetch(req).then((res) => {
        const copy = res.clone();
        caches.open(CACHE).then((c) => c.put(req, copy).catch(() => {}));
        return res;
      }).catch(() => caches.match(req).then((hit) => hit || caches.match('./index.html')))
    );
    return;
  }
  e.respondWith(
    caches.match(req).then((hit) => hit || fetch(req).then((res) => {
      const copy = res.clone();
      caches.open(CACHE).then((c) => c.put(req, copy).catch(() => {}));
      return res;
    }))
  );
});
