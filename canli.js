/* Tasarruf Yanımda merkez bağlantısı (test sürümü).
   Yalnız merkez sunucusundan açılan sayfada window.TY_CANLI tanımlıdır (merkez/sunucu.py ekler);
   GitHub Pages kopyasında Canli.aktif=false kalır ve uygulama gösteri modunda çalışır. */
(function (global) {
  "use strict";
  var ayar = global.TY_CANLI || null;
  var api = ayar ? ayar.api || "api/" : "";

  function istek(yol, govde) {
    return fetch(api + yol, {
      method: govde ? "POST" : "GET",
      headers: govde ? { "Content-Type": "application/json" } : { Accept: "application/json" },
      body: govde ? JSON.stringify(govde) : undefined,
      cache: "no-store",
    }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (v) {
        if (!r.ok) throw new Error(v.hata || "Merkez yanıt vermedi (" + r.status + ")");
        return v;
      });
    });
  }

  function durum(surum, secenek) {
    var q = ["surum=" + (surum || 0)];
    if (secenek && secenek.spy) q.push("spy=" + encodeURIComponent(secenek.spy));
    if (secenek && secenek.ids && secenek.ids.length) q.push("ids=" + secenek.ids.map(encodeURIComponent).join(","));
    if (secenek && secenek.hepsi) q.push("hepsi=1");
    return istek("durum?" + q.join("&"));
  }

  function gonder(yol, govde) { return istek(String(yol).replace(/^api\//, ""), govde || {}); }

  function mid() { return Date.now().toString(36) + Math.random().toString(36).slice(2, 8); }

  // Yeni çağrı uyarısı: ses + titreşim + (izin verildiyse) sistem bildirimi
  var ses = null;
  function cal() {
    try {
      ses = ses || new (global.AudioContext || global.webkitAudioContext)();
      if (ses.state === "suspended") ses.resume();
      [0, 0.28, 0.56].forEach(function (bas) {
        var o = ses.createOscillator(), g = ses.createGain();
        o.type = "sine"; o.frequency.value = bas === 0.28 ? 1175 : 880;
        g.gain.setValueAtTime(0.0001, ses.currentTime + bas);
        g.gain.exponentialRampToValueAtTime(0.35, ses.currentTime + bas + 0.02);
        g.gain.exponentialRampToValueAtTime(0.0001, ses.currentTime + bas + 0.24);
        o.connect(g); g.connect(ses.destination);
        o.start(ses.currentTime + bas); o.stop(ses.currentTime + bas + 0.26);
      });
    } catch (e) {}
  }
  // iOS sesi ancak bir dokunuştan sonra açar: ilk dokunuşta ses bağlamını hazırla
  if (ayar) global.addEventListener("pointerdown", function hazirla() {
    try { ses = ses || new (global.AudioContext || global.webkitAudioContext)(); ses.resume(); } catch (e) {}
    global.removeEventListener("pointerdown", hazirla);
  });

  function uyar(baslik, metin) {
    cal();
    try { if (navigator.vibrate) navigator.vibrate([200, 100, 200]); } catch (e) {}
    var cap = global.Capacitor, p = cap && cap.Plugins;
    try { if (p && p.Haptics) p.Haptics.notification({ type: "WARNING" }); } catch (e) {}
    try {
      if (p && p.LocalNotifications) {
        p.LocalNotifications.schedule({ notifications: [{ id: Math.floor(Date.now() % 2000000000), title: baslik, body: metin }] });
      } else if (global.Notification && Notification.permission === "granted" && document.hidden) {
        new Notification(baslik, { body: metin, icon: "assets/icon-192.png" });
      }
    } catch (e) {}
  }

  function bildirimIzni() {
    var cap = global.Capacitor, p = cap && cap.Plugins;
    try {
      if (p && p.LocalNotifications) return p.LocalNotifications.requestPermissions();
      if (global.Notification && Notification.permission === "default") return Notification.requestPermission();
    } catch (e) {}
    return Promise.resolve();
  }

  function oku(ad) { try { return localStorage.getItem(ad); } catch (e) { return null; } }
  function yaz(ad, deger) { try { if (deger == null) localStorage.removeItem(ad); else localStorage.setItem(ad, deger); } catch (e) {} }

  global.Canli = { aktif: !!ayar, durum: durum, gonder: gonder, mid: mid, uyar: uyar, bildirimIzni: bildirimIzni, oku: oku, yaz: yaz };
})(window);
