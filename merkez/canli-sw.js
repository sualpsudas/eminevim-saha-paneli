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
    data: { rid: v.rid || "", url: new URL("Eminevim%20Saha%20Paneli.dc.html" + (v.rid ? "?ac=" + encodeURIComponent(v.rid) : ""), self.registration.scope).href },
  }));
});

// Dokununca uygulama açılır; müşteri bildiriminde ilgili randevu seçilir (açık uygulamaya mesajla, kapalıysa adresle)
self.addEventListener("notificationclick", (e) => {
  e.notification.close();
  const d = e.notification.data || {};
  e.waitUntil((async () => {
    const acik = await self.clients.matchAll({ type: "window", includeUncontrolled: true });
    for (const c of acik) if ("focus" in c) {
      if (d.rid) c.postMessage({ tip: "ty-randevu-ac", rid: d.rid });
      return c.focus();
    }
    return self.clients.openWindow(d.url);
  })());
});
