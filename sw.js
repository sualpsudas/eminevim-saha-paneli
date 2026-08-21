const CACHE = 'eminevim-v3';
const ASSETS = [
  './',
  './index.html',
  './Eminevim Saha Paneli.dc.html',
  './assignment.js',
  './support.js',
  './map.html',
  './manifest.json',
  './assets/logo-green.png',
  './assets/logo-white.png',
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

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== location.origin) {
    e.respondWith(fetch(req).catch(() => caches.match(req)));
    return;
  }
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
