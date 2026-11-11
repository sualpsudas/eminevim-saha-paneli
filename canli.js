/* Tasarruf Yanımda merkez bağlantısı (test sürümü).
   Yalnız merkez sunucusundan açılan sayfada window.TY_CANLI tanımlıdır (merkez/sunucu.py ekler);
   GitHub Pages kopyasında Canli.aktif=false kalır ve uygulama gösteri modunda çalışır. */
(function (global) {
  "use strict";
  var ayar = global.TY_CANLI || null;
  var api = ayar ? new URL(ayar.api || "api/", global.location.href).href : "";  // sayfanın <base> etiketinden bağımsız

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

  // Uygulama kapalıyken bildirim (Web Push). Bir telefon tek SPY'ye bağlıdır; aynı SPY birden çok telefonda açılabilir,
  // yeni çağrı o SPY'yi seçmiş tüm telefonlara gider. Döner: "acik" | "kapali" | "reddedildi" | "ana-ekran" | "destek-yok" | "native"
  function iosTarayici() {
    var ios = /iPhone|iPad|iPod/.test(navigator.userAgent) || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
    var anaEkran = navigator.standalone === true || (global.matchMedia && matchMedia("(display-mode: standalone)").matches);
    return ios && !anaEkran;
  }
  function b64(s) {
    var p = "=".repeat((4 - s.length % 4) % 4), h = atob((s + p).replace(/-/g, "+").replace(/_/g, "/")), d = new Uint8Array(h.length);
    for (var i = 0; i < h.length; i++) d[i] = h.charCodeAt(i);
    return d;
  }
  function pushDestek() {
    if (global.EMINEVIM_NATIVE) return "native";  // iPhone uygulaması (TestFlight): Apple bildirimi ayrı adım
    if (!ayar) return "destek-yok";
    if (iosTarayici() && !global.PushManager) return "ana-ekran";
    if (!("serviceWorker" in navigator) || !global.PushManager || !global.Notification) return "destek-yok";
    return "";
  }
  function pushBagla(spy, sor) {
    // spy: SPY kimliği ya da müşteri için { musteri: tel, jeton } (girişte merkezin verdiği jeton)
    // sor=true yalnız bir dokunuşla çağrılır (iPhone izni ancak dokunuşla sorar)
    var engel = pushDestek();
    if (engel) return Promise.resolve(engel);
    var izin = Notification.permission === "default" && sor ? Notification.requestPermission() : Promise.resolve(Notification.permission);
    return izin.then(function (p) {
      if (p === "denied") return "reddedildi";
      if (p !== "granted") return "kapali";
      var hazir = navigator.serviceWorker.register("sw.js").then(function () { return navigator.serviceWorker.ready; });  // sayfanın tam yüklenmesini beklemeden
      return Promise.all([hazir, istek("anahtar")]).then(function (x) {
        var reg = x[0], anahtar = x[1].anahtar;
        if (!anahtar) return "destek-yok";
        return reg.pushManager.getSubscription().then(function (ab) {
          return ab || reg.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: b64(anahtar) });
        }).then(function (ab) {
          yaz("ty-push-uc", ab.endpoint);
          var kim = typeof spy === "object" ? { musteri: spy.musteri, jeton: spy.jeton } : { spy: spy };
          kim.abonelik = ab.toJSON(); kim.cihaz = navigator.userAgent.slice(0, 80);
          return gonder("api/abone", kim).then(function () { return "acik"; });
        });
      });
    }).catch(function (e) { try { console.warn("Bildirim açılamadı:", e); } catch (_) {} return "kapali"; });
  }
  function pushBirak() {
    // Çıkışta bu telefon artık o SPY'nin / müşterinin bildirimini almaz
    var uc = oku("ty-push-uc");
    if (!ayar || !uc) return Promise.resolve();
    return gonder("api/abone-sil", { endpoint: uc }).catch(function () {});
  }

  function oku(ad) { try { return localStorage.getItem(ad); } catch (e) { return null; } }
  function yaz(ad, deger) { try { if (deger == null) localStorage.removeItem(ad); else localStorage.setItem(ad, deger); } catch (e) {} }

  global.Canli = { aktif: !!ayar, durum: durum, gonder: gonder, mid: mid, uyar: uyar, bildirimIzni: bildirimIzni, oku: oku, yaz: yaz,
                   pushBagla: pushBagla, pushBirak: pushBirak };
})(window);
