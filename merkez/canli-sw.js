/* Tasarruf Yanımda merkezi: servis çalışanı (merkez <gizli>/sw.js adresinden verir).
   Önbellek tutmaz (canlı sürüm her zaman merkezden gelir); yalnız uygulama kapalıyken gelen bildirimi gösterir.
   GitHub Pages'teki gösteri kopyası kökteki sw.js'i kullanır. */
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (e) => {
  e.waitUntil((async () => {
    for (const k of await caches.keys()) await caches.delete(k);  // eski gösteri önbelleği kalmasın
    await self.clients.claim();
  })());
});

self.addEventListener("push", (e) => {
  let v = {};
  try { v = e.data ? e.data.json() : {}; } catch (_) { v = { govde: e.data ? e.data.text() : "" }; }
  e.waitUntil(self.registration.showNotification(v.baslik || "Tasarruf Yanımda", {
    body: v.govde || "",
    tag: v.etiket || "ty",
    renotify: true,
    requireInteraction: true,
    icon: "assets/icon-192.png",
    badge: "assets/icon-192.png",
    data: { url: new URL("Eminevim%20Saha%20Paneli.dc.html", self.registration.scope).href },
  }));
});

self.addEventListener("notificationclick", (e) => {
  e.notification.close();
  e.waitUntil((async () => {
    const acik = await self.clients.matchAll({ type: "window", includeUncontrolled: true });
    for (const c of acik) if ("focus" in c) return c.focus();
    return self.clients.openWindow(e.notification.data.url);
  })());
});
