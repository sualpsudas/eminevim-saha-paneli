/* İzometrik (2,5B) mahalle sahnesi. izoSahne(svg, {mod, ...}) → { ciz(lt, d) }
   Eksenler: x = dükkân sırası boyunca (sağa, hafif aşağı), y = derinlik (sola-aşağı = bize doğru), z = yukarı.
   mod: "bugun" (SPY kapı kapı) · "sorun" (tek yönlü temas → çağrı kanalı yok → cumartesi; sec.b2, sec.b3 = bölüm başları)
        "cozum" (müşteri telefondan çağırır → turuncu + yeşil SPY; sec.A = giriş süresi) · "ac" (yalnız ortam, açılış arka planı)
   Kamera: sahne grubu ölçeklenip kaydırılır; ağaçlar sallanır, bulut gölgeleri geçer. */
function izoSahne(svg, sec) {
  sec = sec || {};
  var MOD = sec.mod || (sec.cagri ? "cozum" : "bugun");
  var NS = "http://www.w3.org/2000/svg";
  var KAM = document.createElementNS(NS, "g"); svg.appendChild(KAM);
  function E(ad, oz, ust) { var e = document.createElementNS(NS, ad); for (var k in oz) e.setAttribute(k, oz[k]); (ust || KAM).appendChild(e); return e; }
  function T(ust, x, y, t, oz) { var e = E("text", Object.assign({ x: x, y: y, "text-anchor": "middle", "font-size": 22, "font-weight": 700, "font-family": "Century Gothic, Segoe UI, Arial" }, oz || {}), ust); e.textContent = t; return e; }
  var U = 85, CX = 435, CY = 520, AX = 15 * Math.PI / 180, AY = 52 * Math.PI / 180, YK = .8;
  var XV = [Math.cos(AX), Math.sin(AX)], YV = [-Math.cos(AY) * YK, Math.sin(AY) * YK];
  function P(x, y, z) { return [CX + (x * XV[0] + y * YV[0]) * U, CY + (x * XV[1] + y * YV[1]) * U - (z || 0) * U]; }
  function pts(a) { return a.map(function (p) { var q = P(p[0], p[1], p[2]); return q[0].toFixed(1) + "," + q[1].toFixed(1); }).join(" "); }
  function poly(a, oz, ust) { return E("polygon", Object.assign({ points: pts(a) }, oz), ust); }
  function yuz(x1, x2, y, z1, z2, oz, ust) { return poly([[x1, y, z1], [x2, y, z1], [x2, y, z2], [x1, y, z2]], oz, ust); }      /* ön cephe (y sabit) */
  function yan(x, y1, y2, z1, z2, oz, ust) { return poly([[x, y1, z1], [x, y2, z1], [x, y2, z2], [x, y1, z2]], oz, ust); }      /* sağ yüz (x sabit) */
  function kutu(x, y, w, d, h, renk, ust) {
    yan(x + w, y, y + d, 0, h, { fill: renk[2] }, ust);
    yuz(x, x + w, y + d, 0, h, { fill: renk[1] }, ust);
    poly([[x, y, h], [x + w, y, h], [x + w, y + d, h], [x, y + d, h]], { fill: renk[0] }, ust);
  }
  function kis(x) { return Math.max(0, Math.min(1, x)); }
  function yum(x) { x = kis(x); return x < .5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2; }
  function cik(x) { x = kis(x); return 1 - Math.pow(1 - x, 3); }
  function zipla(x) { x = kis(x); var c = 1.70158; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); }   /* hafif taşıp yerine oturur */
  var KAT = E("g", {}), ON = E("g", {}), UST = E("g", {});
  /* ---- zemin, yollar ---- */
  poly([[-6, -12, 0], [26, -12, 0], [26, 9, 0], [-6, 9, 0]], { fill: "#e4ece7" }, KAT);
  poly([[-6, 0, 0], [26, 0, 0], [26, .8, 0], [-6, .8, 0]], { fill: "#f1f4f2" }, KAT);            /* kaldırım */
  for (var kd = -6; kd < 26; kd += .9) poly([[kd, .02, 0], [kd + .02, .02, 0], [kd + .02, .78, 0], [kd, .78, 0]], { fill: "#e3e8e5" }, KAT);   /* kaldırım taşı derzleri */
  poly([[-6, .8, 0], [26, .8, 0], [26, .86, 0], [-6, .86, 0]], { fill: "#c9d1cc" }, KAT);        /* bordür */
  poly([[-6, .86, 0], [26, .86, 0], [26, 3.1, 0], [-6, 3.1, 0]], { fill: "#bfc8c3" }, KAT);      /* yol */
  for (var q = -6; q < 26; q += 1.3) poly([[q, 1.95, 0], [q + .65, 1.95, 0], [q + .65, 2.01, 0], [q, 2.01, 0]], { fill: "#fff", opacity: .85 }, KAT);
  poly([[-6, 3.1, 0], [26, 3.1, 0], [26, 3.9, 0], [-6, 3.9, 0]], { fill: "#f1f4f2" }, KAT);
  poly([[-6, 3.9, 0], [26, 3.9, 0], [26, 9, 0], [-6, 9, 0]], { fill: "#d6e6dc" }, KAT);           /* ön park */
  poly([[13.3, -12, 0], [15.5, -12, 0], [15.5, 9, 0], [13.3, 9, 0]], { fill: "#bfc8c3" }, KAT);  /* ara sokak */
  for (var c = 0; c < 6; c++) poly([[13.4, .95 + c * .36, 0], [15.4, .95 + c * .36, 0], [15.4, 1.13 + c * .36, 0], [13.4, 1.13 + c * .36, 0]], { fill: "#fff", opacity: .9 }, KAT);
  poly([[12.7, -12, 0], [13.3, -12, 0], [13.3, .8, 0], [12.7, .8, 0]], { fill: "#f1f4f2" }, KAT);
  /* ---- arka binalar ---- */
  var ARKA = [[-2.5, -6.2, 2.6, 2.6, 3.9], [0.6, -6, 2.4, 2.6, 4.6], [3.6, -6.4, 2.8, 2.8, 3.6], [6.9, -6, 2.3, 2.6, 4.9], [9.7, -6.4, 2.8, 2.8, 4.1]];
  ARKA.forEach(function (b) {
    var g = E("g", { opacity: .5 }, KAT); kutu(b[0], b[1], b[2], b[3], b[4], ["#f1f5f3", "#e3eae6", "#d3ddd8"], g);
    for (var f = .8; f < b[4] - .4; f += .7) for (var w = 0; w < 3; w++) { var wx = b[0] + .3 + w * .75; yuz(wx, wx + .36, b[1] + b[3] + .002, f, f + .34, { fill: "#dbe6e1" }, g); }
  });
  /* sağ blok */
  [[16.1, -2.6, 2.6, 2.6, 2.4]].forEach(function (b) { var g = E("g", {}, KAT); kutu(b[0], b[1], b[2], b[3], b[4], ["#f3f6f4", "#e6ece8", "#d2dcd6"], g); });
  /* ---- dükkânlar ---- */
  var DK = [["MARKET", "#00724c"], ["ECZANE", "#1E3856"], ["KUAFÖR", "#ea803f"], ["OTO GALERİ", "#5f6b66"], ["EMLAK", "#00724c"], ["BÜRO", "#B25E30"]];
  var KATS = [2, 3, 2, 3, 3, 2], DUVAR = [["#ffffff", "#f6f8f7", "#e3e9e5"], ["#f6f8fb", "#eef2f6", "#dbe2e9"], ["#fff8f3", "#fbefe6", "#ecdcd0"], ["#f7f8f7", "#eff2f0", "#dde3df"], ["#f5faf7", "#ebf3ee", "#d7e4dc"], ["#fcf8f2", "#f6efe4", "#e7dccd"]];
  var W = 2.1, D = 2.3, ZK = 1.2, ZU = .78, dukkan = [], PENCERE = [];
  DK.forEach(function (d, i) {
    var x = i * 2.15, h = ZK + ZU * KATS[i], g = E("g", {}, KAT), ren = DUVAR[i];
    kutu(x, -D, W, D, h, ren, g);
    yuz(x - .02, x + W + .02, 0.001, h - .12, h, { fill: "#d8e0db" }, g);                                         /* korkuluk bandı */
    poly([[x + .12, -D + .12, h], [x + W - .12, -D + .12, h], [x + W - .12, -.12, h], [x + .12, -.12, h]], { fill: ren[2], opacity: .45 }, g);
    if (i % 2 === 0) kutu(x + .4, -D + .5, .55, .5, .28, ["#eef2f0", "#d9e1dc", "#c6d0ca"], g); else kutu(x + 1.1, -D + .4, .7, .7, .45, ["#e9eeeb", "#d4ddd8", "#c0cbc5"], g);
    for (var f = 0; f < KATS[i]; f++) for (var w = 0; w < 3; w++) {
      var wx = x + .22 + w * .62, wz = ZK + .18 + f * ZU;
      PENCERE.push(yuz(wx, wx + .4, .002, wz, wz + .42, { fill: "#cfe1da" }, g));
      poly([[wx + .06, .003, wz + .05], [wx + .16, .003, wz + .05], [wx + .3, .003, wz + .37], [wx + .2, .003, wz + .37]], { fill: "#fff", opacity: .6 }, g);
      yuz(wx - .04, wx + .44, .004, wz - .04, wz, { fill: "#dfe6e2" }, g);
    }
    yuz(x, x + W, .002, 0, ZK, { fill: ren[1] }, g);
    yuz(x + .12, x + 1.32, .004, .1, .9, { fill: "#cde2db" }, g);                                                 /* vitrin */
    /* vitrin içi: raf ve tezgâh silüeti */
    yuz(x + .18, x + 1.26, .005, .5, .54, { fill: "#b9d0c7" }, g); yuz(x + .18, x + 1.26, .005, .28, .32, { fill: "#b9d0c7" }, g);
    poly([[x + .25, .006, .12], [x + .45, .006, .12], [x + .8, .006, .88], [x + .6, .006, .88]], { fill: "#fff", opacity: .55 }, g);
    poly([[x + .7, .006, .12], [x + .8, .006, .12], [x + 1.15, .006, .88], [x + 1.05, .006, .88]], { fill: "#fff", opacity: .4 }, g);
    var kapi = yuz(x + 1.48, x + 1.92, .004, 0, .9, { fill: "#8fa39b" }, g);
    var aralik = poly([[x + 1.48, .004, 0], [x + 1.48, .3, 0], [x + 1.48, .3, .88], [x + 1.48, .004, .9]], { fill: "#a9bbb3", opacity: 0 }, g);
    /* tente: cepheden dışarı eğik */
    for (var s = 0; s < 6; s++) { var sx = x + .02 + s * (W - .04) / 6; poly([[sx, .004, 1.1], [sx + (W - .04) / 6, .004, 1.1], [sx + (W - .04) / 6, .42, .92], [sx, .42, .92]], { fill: s % 2 ? "#ffffff" : d[1] }, g); }
    poly([[x + .02, .42, .92], [x + W - .02, .42, .92], [x + W - .02, .42, .86], [x + .02, .42, .86]], { fill: d[1], opacity: .85 }, g);
    /* tentenin kaldırıma düşen gölgesi */
    poly([[x + .1, .02, 0], [x + W - .1, .02, 0], [x + W - .3, .55, 0], [x - .1, .55, 0]], { fill: "rgba(40,60,50,.07)" }, g);
    /* tabela */
    var p = P(x + W / 2, .004, 1.33);
    var tg = E("g", { transform: "matrix(" + XV[0].toFixed(4) + "," + XV[1].toFixed(4) + ",0,1," + p[0].toFixed(1) + "," + p[1].toFixed(1) + ")" }, g);
    E("rect", { x: -98, y: -20, width: 196, height: 36, rx: 6, fill: "#fff", stroke: "#cfd6d2", "stroke-width": 1.5 }, tg);
    T(tg, 0, 6, d[0], { "font-size": 22, fill: d[1] });
    dukkan.push({ x: x, h: h, kapi: kapi, aralik: aralik, kapiX: x + 1.7 });
  });
  /* ---- sokak eşyası ---- */
  var AGAC = [];
  function agac(x, y, ol, ust) {
    var a = P(x, y, 0), g = E("g", {}, ust || ON); g.z = y;
    E("ellipse", { cx: a[0] + 14 * ol, cy: a[1] + 4, rx: 34 * ol, ry: 12 * ol, fill: "rgba(40,60,50,.16)" }, g);
    E("rect", { x: a[0] - 4 * ol, y: a[1] - 52 * ol, width: 8 * ol, height: 52 * ol, rx: 3, fill: "#80664c" }, g);
    var t = E("g", {}, g);
    E("circle", { cx: a[0], cy: a[1] - 78 * ol, r: 38 * ol, fill: "#78a98c" }, t);
    E("circle", { cx: a[0] - 16 * ol, cy: a[1] - 88 * ol, r: 22 * ol, fill: "#8fbfa2" }, t);
    E("circle", { cx: a[0] + 14 * ol, cy: a[1] - 66 * ol, r: 20 * ol, fill: "#6a9c7f" }, t);
    t.ax = a[0]; t.ay = a[1] - 50 * ol; t.faz = x * 1.7 + y; AGAC.push(t);
    return g;
  }
  [2.12, 6.42, 10.72].forEach(function (x) { agac(x, .66, .85, KAT); });
  [[-1, 5], [2.5, 6.2], [6, 5.2], [9.5, 6.4], [12, 5], [17, 5.6], [19.5, 4.6], [4.2, 7.6], [10.8, 7.8]].forEach(function (t) { agac(t[0], t[1], 1.15, KAT); });
  [[1.5, 4.3], [7.6, 4.3]].forEach(function (b) { var g = E("g", {}, KAT); kutu(b[0], b[1], .9, .25, .16, ["#b39b80", "#9c8469", "#86705a"], g); });
  /* ---- araçlar ---- */
  function araba(renk) {
    var g = E("g", {}, ON);
    g.ciz = function (x, y) {
      while (g.firstChild) g.removeChild(g.firstChild);
      var a = P(x + .6, y + .3, 0); E("ellipse", { cx: a[0] + 8, cy: a[1] + 6, rx: 70, ry: 20, fill: "rgba(40,50,45,.18)" }, g);
      [[x + .25, y + .62], [x + 1.0, y + .62]].forEach(function (w) { var c = P(w[0], w[1], .05); E("ellipse", { cx: c[0], cy: c[1], rx: 9, ry: 11, fill: "#2f3b48" }, g); });
      kutu(x, y, 1.25, .62, .26, [renk[0], renk[1], renk[2]], g);
      kutu(x + .32, y + .07, .6, .48, .48, [renk[0], renk[1], renk[2]], g);
      yuz(x + .37, x + .87, y + .551, .3, .44, { fill: "#d8eaee" }, g);
      yan(x + .921, y + .12, y + .5, .3, .44, { fill: "#c3d9df" }, g);
    };
    return g;
  }
  var ar1 = araba(["#a9bed1", "#93abc0", "#7f97ad"]), ar2 = araba(["#e8c6ae", "#d9ad8f", "#c49779"]), ar3 = araba(["#c9d2d9", "#b5c0c8", "#9faab3"]);
  ar3.ciz(18.5, 1.05);
  /* ---- kişiler ---- */
  /* bir adım çevrimi (iki adım) ≈ 0,75 birim yol; adimGenlik: yumuşak (in-out) ilerlemede hıza göre adım açıklığı */
  var ADIM = 2 * Math.PI / .75;
  function adimGenlik(p) { return p <= 0 || p >= 1 ? 0 : Math.min(1, 4 * Math.min(p, 1 - p)); }
  function kisi(renk, etiket, ol, sec2) {
    sec2 = sec2 || {};
    var k = { g: E("g", {}, ON), ol: ol || 1 };
    E("ellipse", { cx: 6, cy: 3, rx: 26, ry: 8, fill: "rgba(40,50,45,.18)" }, k.g);
    k.a = E("path", { stroke: "#2f3b48", "stroke-width": 9, "stroke-linecap": "round" }, k.g);
    k.b = E("path", { stroke: "#3a4653", "stroke-width": 9, "stroke-linecap": "round" }, k.g);
    k.v = E("g", {}, k.g);   /* gövde: yürürken öne eğilir, adımla iner kalkar (gölge yerde kalır) */
    k.a.remove(); k.b.remove(); k.v.appendChild(k.a); k.v.appendChild(k.b);
    E("path", { d: "M-16 -38c0-24 6-36 16-36s16 12 16 36z", fill: renk }, k.v);
    k.kol = E("path", { stroke: renk, "stroke-width": 8, "stroke-linecap": "round", fill: "none", "stroke-linejoin": "round" }, k.v);
    if (sec2.telefon) {   /* elinde telefon; ekranı yanabilir */
      k.kol2 = E("path", { d: "M12 -62L16 -52L8 -50", fill: "none", stroke: renk, "stroke-width": 8, "stroke-linecap": "round", "stroke-linejoin": "round" }, k.v);
      E("rect", { x: 2, y: -66, width: 12, height: 20, rx: 2.5, fill: "#22302a" }, k.v);
      k.ekran = E("rect", { x: 4, y: -64, width: 8, height: 16, rx: 1.5, fill: "#9aa6a1" }, k.v);
    } else {   /* dosya tutan ön kol: omuzdan hafifçe sallanır */
      k.dosya = E("g", {}, k.v);
      E("rect", { x: 8, y: -62, width: 15, height: 21, rx: 2, fill: "#1E3856", stroke: "#fff", "stroke-width": 1.5 }, k.dosya);
    }
    E("circle", { cx: 0, cy: -86, r: 12, fill: "#f1c9a5" }, k.v);
    E("path", { d: sec2.sac || "M-12 -89a12 12 0 0 1 24 0c-5-5-19-5-24 0z", fill: sec2.sacRenk || "#3b2a20" }, k.v);
    if (etiket) {
      var ew = sec2.etkW || 56, er = sec2.etkRenk || (renk === "#00724c" ? "#00724c" : "#B25E30");
      k.etk = E("g", {}, k.g); E("rect", { x: -ew / 2, y: -126, width: ew, height: 26, rx: 13, fill: "#fff", stroke: renk, "stroke-width": 3 }, k.etk); T(k.etk, 0, -107, etiket, { "font-size": 16, fill: er });
    }
    /* yürüyüş: adım evresi gidilen YOLA bağlı (zamana değil) → ayak yerde kaymaz.
       yuruyor: 0..1 adım genliği (true = 1); kalkışta küçük başlar, duruşta küçülerek biter (bkz. adimGenlik). */
    k.ciz = function (x, y, faz, yuruyor, ters) {
      var a = P(x, y, 0), g = +yuruyor || 0, f = (ters ? y - x : x - y) * ADIM;   /* yüzü dönük yöne ilerledikçe artar */
      function bacak(el, hx, ev) {   /* uyluk + baldır; öne salınırken diz bükülür */
        var u = .42 * g * Math.sin(ev), d = .75 * g * Math.max(0, Math.cos(ev)),
          dx = hx + 18 * Math.sin(u), dy = -36 + 18 * Math.cos(u), ax = dx + 18 * Math.sin(u - d), ay = dy + 18 * Math.cos(u - d);
        el.setAttribute("d", "M" + hx + " -36L" + dx.toFixed(1) + " " + dy.toFixed(1) + "L" + ax.toFixed(1) + " " + ay.toFixed(1));
        return ay;
      }
      var y1 = bacak(k.a, -5, f + Math.PI), y2 = bacak(k.b, 5, f);
      var in_ = -Math.max(y1, y2), egim = 3 * g;   /* yere en yakın ayak tabana basar: iki ayak açıkken gövde biraz iner */
      var kol = -.38 * g * Math.sin(f);   /* arka kol öndeki bacağın tersine */
      k.kol.setAttribute("d", "M-14 -64L" + (-14 + 13 * Math.sin(kol)).toFixed(1) + " " + (-64 + 13 * Math.cos(kol)).toFixed(1) +
        "L" + (-14 + 13 * Math.sin(kol) + 11 * Math.sin(kol * 1.6 + .25 * g)).toFixed(1) + " " + (-64 + 13 * Math.cos(kol) + 11 * Math.cos(kol * 1.6 + .25 * g)).toFixed(1));
      if (k.dosya) k.dosya.setAttribute("transform", "rotate(" + (9 * g * Math.sin(f)).toFixed(2) + " 12 -62)");
      k.v.setAttribute("transform", "translate(0," + in_.toFixed(2) + ") rotate(" + egim.toFixed(2) + ")");
      k.g.setAttribute("transform", "translate(" + a[0].toFixed(1) + "," + a[1].toFixed(1) + ") scale(" + (ters ? -k.ol : k.ol) + "," + k.ol + ")");
      if (k.etk) k.etk.setAttribute("transform", "scale(" + (ters ? -1 : 1) + ",1) translate(0," + in_.toFixed(2) + ")");
      k.x = x; k.y = y;
    };
    return k;
  }
  /* izometrik çizimde uzaklık küçültmez: yayalar da SPY ve müşteriyle aynı boyda */
  var yaya1 = kisi("#a3aea9", null, 1), yaya2 = kisi("#c2b3a3", null, 1), yaya3 = kisi("#9fb1c2", null, 1);
  var spy = kisi("#ea803f", "SPY", 1), spy2 = MOD === "cozum" ? kisi("#00724c", "SPY", 1) : null;
  if (MOD === "ac") spy.g.style.display = "none";
  /* müşteri (Mehmet Bey): lacivert ceket, elinde telefon; kaldırımın önünde durur, SPY'lerden sonra çizilir */
  var MUS = MOD === "sorun" || MOD === "cozum" ? kisi("#1E3856", "Müşteri", 1, { telefon: true, etkW: 84, etkRenk: "#1E3856", sac: "M-12 -88a12 12 0 0 1 24 0v-3c-6-6-18-6-24 0z", sacRenk: "#4a3a30" }) : null;
  /* ---- rota çizgileri ---- */
  var rotaT = E("polyline", { fill: "none", stroke: "#ea803f", "stroke-width": 5, "stroke-dasharray": "2 11", "stroke-linecap": "round", opacity: .9 }, ON);
  var rotaY = E("polyline", { fill: "none", stroke: "#00724c", "stroke-width": 5, "stroke-dasharray": "2 11", "stroke-linecap": "round", opacity: .9 }, ON);
  /* ---- onay işaretleri ve çağrı simgeleri ---- */
  /* ziyaret sonucu: her kapı olumlu (yeşil tik) değil; kapı kapı gezide bazıları olumsuz (kırmızı çarpı).
     Çağrıya giden yeşil SPY'nin kapıları (çözümde 1, 3, 5) hep olumlu. */
  var OLUMLU = { bugun: [1, 0, 0, 1, 0, 1], sorun: [1, 0, 1, 1, 1, 1], cozum: [1, 1, 0, 1, 1, 1] }[MOD] || [1, 1, 1, 1, 1, 1];
  var tik = dukkan.map(function (d, i) {
    var g = E("g", {}, ON), iyi = OLUMLU[i];
    E("circle", { r: 20, fill: iyi ? "#00724c" : "#d64541", stroke: "#fff", "stroke-width": 4 }, g);
    if (iyi) E("path", { d: "M-8 0l6 6 11-12", fill: "none", stroke: "#fff", "stroke-width": 4.5, "stroke-linecap": "round", "stroke-linejoin": "round" }, g);
    else E("path", { d: "M-7 -7L7 7M7 -7L-7 7", stroke: "#fff", "stroke-width": 4.5, "stroke-linecap": "round" }, g);
    var a = P(d.x + 1.78, .02, 1.78); g.xy = a; g.style.opacity = 0; return g;
  });
  var cagriPin = dukkan.map(function (d) {
    var a = P(d.x + 1.05, -1.15, d.h + .55), g = E("g", { transform: "translate(" + a[0].toFixed(1) + "," + a[1].toFixed(1) + ")", opacity: 0 }, ON);
    E("path", { d: "M0 52v-18", stroke: "#00724c", "stroke-width": 4 }, g);
    g.halka = E("circle", { r: 36, fill: "none", stroke: "#00724c", "stroke-width": 4 }, g);
    E("circle", { r: 34, fill: "#00724c", stroke: "#fff", "stroke-width": 4 }, g);
    E("path", { d: "M-13 -12c0 14 12 26 26 26l5-7-8-6-4 4c-5-2-9-6-11-11l4-4-6-8z", fill: "#fff" }, g);
    g.xy = a;
    return g;
  });
  function kapiAc(i, acik) { dukkan[i].kapi.setAttribute("fill", acik ? "#3e5a50" : "#8fa39b"); dukkan[i].aralik.style.opacity = acik ? 1 : 0; }
  function tikGoster(i, v) { var p = Math.max(0, Math.min(1, v / .25)); p = 1 - Math.pow(1 - p, 3); tik[i].style.opacity = v > 0 ? 1 : 0; tik[i].setAttribute("transform", "translate(" + tik[i].xy[0].toFixed(1) + "," + tik[i].xy[1].toFixed(1) + ") scale(" + (v > 0 ? .6 + .4 * p : 0) + ")"); }
  var YT = .42;   /* kaldırımda yürüme çizgisi */
  /* kapı kapı gezinti: duraklar, başlangıç, aralık → konum + rota noktaları */
  function gezinti(duraklar, lt, bas, aralik, x0) {
    var x = x0, yuruyor = false, ters = false, nokta = [[x0, YT]];
    duraklar.forEach(function (dk, k) {
      var b = bas + k * aralik, once = k === 0 ? x0 : dukkan[duraklar[k - 1]].kapiX, sure = aralik * .6, hedef = dukkan[dk].kapiX;
      if (lt >= b) { var p = Math.max(0, Math.min(1, (lt - b) / sure)); x = once + (hedef - once) * yum(p); yuruyor = adimGenlik(p); ters = hedef < once; nokta.push([x, YT]); }
      var varis = b + sure, ayrilis = k < duraklar.length - 1 ? b + aralik : 1e9;
      kapiAc(dk, lt > varis && lt < ayrilis - .05); tikGoster(dk, lt - varis - .15);
    });
    return { x: x, yuruyor: yuruyor, ters: ters, nokta: nokta };
  }
  function cizgi(el, nokta) { el.setAttribute("points", nokta.map(function (n) { var a = P(n[0], n[1], 0); return a[0].toFixed(1) + "," + a[1].toFixed(1); }).join(" ")); }

  /* ---- konuşma balonu (dünyada bir noktanın üstünde) ---- */
  function balon(gen, yuk) {
    var g = E("g", { opacity: 0 }, UST);
    E("path", { d: "M" + (-gen / 2) + " " + (-yuk - 26) + "h" + gen + "a14 14 0 0 1 14 14v" + (yuk - 28) + "a14 14 0 0 1 -14 14h" + (-(gen / 2 - 14)) + "l-14 16l-4 -16h" + (-(gen / 2 - 18)) + "a14 14 0 0 1 -14 -14v" + (-(yuk - 28)) + "a14 14 0 0 1 14 -14z", fill: "#fff", stroke: "#cfd6d2", "stroke-width": 2.5, transform: "translate(0,-2)" }, g);
    g.ic = E("g", { transform: "translate(0," + (-yuk / 2 - 14) + ")" }, g);
    g.goster = function (x, y, z, p) {
      var a = P(x, y, z); g.style.opacity = p > 0 ? 1 : 0;
      g.setAttribute("transform", "translate(" + a[0].toFixed(1) + "," + a[1].toFixed(1) + ") scale(" + (.4 + .6 * zipla(p)) + ")");
    };
    return g;
  }
  function insanSimge(ust, x, renk, ol) {
    var g = E("g", { transform: "translate(" + x + ",0) scale(" + ol + ")" }, ust);
    E("circle", { cx: 0, cy: -12, r: 9, fill: renk }, g); E("path", { d: "M-15 16c0-13 7-20 15-20s15 7 15 20z", fill: renk }, g);
    return g;
  }
  var B = {};
  if (MUS) {
    /* telefon + soru işareti → üstüne turuncu çarpı */
    B.soru = balon(150, 104);
    E("rect", { x: -48, y: -30, width: 36, height: 60, rx: 7, fill: "none", stroke: "#1E3856", "stroke-width": 5 }, B.soru.ic);
    E("line", { x1: -36, y1: 22, x2: -24, y2: 22, stroke: "#1E3856", "stroke-width": 4, "stroke-linecap": "round" }, B.soru.ic);
    T(B.soru.ic, 26, 18, "?", { "font-size": 54, fill: "#1E3856" });
    B.carpi = E("g", { opacity: 0 }, B.soru.ic);
    E("circle", { r: 24, fill: "#ea803f", stroke: "#fff", "stroke-width": 4 }, B.carpi);
    E("path", { d: "M-9 -9L9 9M9 -9L-9 9", stroke: "#fff", "stroke-width": 6, "stroke-linecap": "round" }, B.carpi);
    /* mesai: çanta */
    B.mesai = balon(132, 96);
    E("rect", { x: -30, y: -14, width: 60, height: 40, rx: 7, fill: "none", stroke: "#7d8984", "stroke-width": 5 }, B.mesai.ic);
    E("path", { d: "M-12 -14v-9h24v9", fill: "none", stroke: "#7d8984", "stroke-width": 5 }, B.mesai.ic);
    /* görüşme: iki kişi */
    B.gorusme = balon(150, 100);
    insanSimge(B.gorusme.ic, -22, "#ea803f", 1.25); insanSimge(B.gorusme.ic, 22, "#1E3856", 1.25);
  }
  /* tek yönlü ok (SPY → kapı) */
  var tekYon = E("g", { opacity: 0 }, UST);
  var tekYonC = E("path", { fill: "none", stroke: "#ea803f", "stroke-width": 7, "stroke-linecap": "round" }, tekYon);
  var tekYonU = E("path", { d: "M0 0l-24 -14v28z", fill: "#ea803f" }, tekYon);
  /* telefon dokunuş halkası (müşterinin elinde) */
  var tikla = E("circle", { r: 10, fill: "none", stroke: "#00724c", "stroke-width": 4, opacity: 0 }, UST);

  /* ---- ortam: bulut gölgeleri (sahne koordinatında) ---- */
  var GOLGE = [[-2, 1.8, 0], [9, -2, 9], [18, 4, 18]].map(function (b) { return { g: E("ellipse", { rx: 300, ry: 120, fill: "rgba(30,60,45,.035)" }, UST), x: b[0], y: b[1], k: b[2] }; });
  function ortam(lt) {
    AGAC.forEach(function (t) { t.setAttribute("transform", "rotate(" + (1.6 * Math.sin(lt * 1.4 + t.faz)).toFixed(2) + " " + t.ax.toFixed(1) + " " + t.ay.toFixed(1) + ")"); });
    GOLGE.forEach(function (b) {
      var gx = ((b.x + lt * .35 + 6) % 32) - 6, a = P(gx, b.y + Math.sin(lt * .2 + b.k) * .3, 0);
      b.g.setAttribute("cx", a[0].toFixed(1)); b.g.setAttribute("cy", a[1].toFixed(1)); b.g.setAttribute("transform", "rotate(15 " + a[0].toFixed(1) + " " + a[1].toFixed(1) + ")");
    });
  }
  /* ---- kamera: sahne grubunu ölçekle/kaydır. kam = [x, y, z, ölçek] (dünyadaki odak noktası) ya da null (geniş açı) ---- */
  var GENIS = { cx: 960, cy: 460, s: 1 };
  function kamDeger(k) { if (!k) return GENIS; var a = P(k[0], k[1], k[2]); return { cx: a[0], cy: a[1], s: k[3] }; }
  function kamera(lt, yol) {   /* yol: [[t, kam], ...] art arda; aralarda yumuşak geçiş */
    var a = kamDeger(yol[0][1]), b = a, p = 0;
    for (var i = 0; i < yol.length - 1; i++) {
      if (lt >= yol[i][0] && lt < yol[i + 1][0]) { a = kamDeger(yol[i][1]); b = kamDeger(yol[i + 1][1]); p = yum((lt - yol[i][0]) / (yol[i + 1][0] - yol[i][0])); break; }
      if (lt >= yol[i + 1][0]) { a = b = kamDeger(yol[i + 1][1]); }
    }
    /* yakınlaşma oranla (eşit hızda hissedilir); odak yakınlaşmayla uyumlu kayar */
    var s = a.s * Math.pow(b.s / a.s, p), q = Math.abs(b.s - a.s) < 1e-4 ? p : (1 / a.s - 1 / s) / (1 / a.s - 1 / b.s);
    var cx = a.cx + (b.cx - a.cx) * q, cy = a.cy + (b.cy - a.cy) * q;
    /* odak noktası ekranın görünen ortasına (alt bant hariç) gelir */
    KAM.setAttribute("transform", "translate(960,460) scale(" + s.toFixed(4) + ") translate(" + (-cx).toFixed(1) + "," + (-cy).toFixed(1) + ")");
  }
  function okCiz(x1, y1, x2, y2, p) {
    var a = P(x1, y1, .75), b = P(x2, y2, .55), mx = (a[0] + b[0]) / 2, my = Math.min(a[1], b[1]) - 60;
    tekYon.style.opacity = p > 0 ? 1 : 0;
    var t = cik(p), ex = (1 - t) * (1 - t) * a[0] + 2 * (1 - t) * t * mx + t * t * b[0], ey = (1 - t) * (1 - t) * a[1] + 2 * (1 - t) * t * my + t * t * b[1];
    var qx = a[0] + (mx - a[0]) * t, qy = a[1] + (my - a[1]) * t;
    tekYonC.setAttribute("d", "M" + a[0].toFixed(1) + " " + a[1].toFixed(1) + "Q" + qx.toFixed(1) + " " + qy.toFixed(1) + " " + ex.toFixed(1) + " " + ey.toFixed(1));
    var tx = 2 * (1 - t) * (mx - a[0]) + 2 * t * (b[0] - mx), ty = 2 * (1 - t) * (my - a[1]) + 2 * t * (b[1] - my);
    tekYonU.setAttribute("transform", "translate(" + ex.toFixed(1) + "," + ey.toFixed(1) + ") rotate(" + (Math.atan2(ty, tx) * 180 / Math.PI).toFixed(1) + ")");
  }
  function arkaPlan(lt) {
    ar1.ciz(-3 + ((lt * 1.6) % 26), 1.05); ar2.ciz(23 - ((lt * 1.3 + 8) % 28), 2.3);
    yaya1.ciz(19 - ((lt * .55) % 24), 3.45, lt, true, true);
    yaya2.ciz(-4 + ((lt * .5 + 6) % 24), 3.55, lt + 1, true);
    yaya3.ciz(14.4, 6 - ((lt * .5) % 10), lt + 2, true);
    ortam(lt);
  }
  var BURO = dukkan[5], MX = 11.7, MY = .64;   /* müşterinin yeri: BÜRO önünde, kaldırımın yol tarafı */
  function musteriTelefon(acik) { if (MUS) MUS.ekran.setAttribute("fill", acik ? "#bfe8d6" : "#9aa6a1"); }
  function hepsiniGizle() { cagriPin.forEach(function (c) { c.style.opacity = 0; }); for (var i = 0; i < 6; i++) { kapiAc(i, false); tikGoster(i, -1); } }

  return {
    P: P,
    ciz: function (lt, d) {
      arkaPlan(lt);
      if (MOD === "ac") { kamera(lt, [[0, [6, 0, 1.2, 1.18]], [12, [7.5, 0, 1.2, 1.1]]]); return; }
      if (MOD === "bugun") {
        var g = gezinti([0, 1, 2, 3, 4, 5], lt, .2, (d - .9) / 6, -1.2);
        spy.ciz(g.x, YT, lt, g.yuruyor, g.ters); cizgi(rotaT, g.nokta); rotaY.setAttribute("points", "");
        cagriPin.forEach(function (c) { c.style.opacity = 0; });
        /* kamera SPY'yi hafifçe izler: yakından başlar, sokak boyunca açılır */
        kamera(lt, [[0, [1.6, YT, .8, 1.45]], [d * .45, [5, YT, .8, 1.18]], [d, [6.2, 0, .9, 1.04]]]);
        return;
      }
      if (MOD === "sorun") {
        var b2 = sec.b2, b3 = sec.b3;
        hepsiniGizle(); rotaY.setAttribute("points", "");
        /* 1) Tek yönlü temas: SPY MARKET'ten ECZANE kapısına; ok SPY'den kapıya */
        var s1 = Math.min(lt, b2), x1 = dukkan[0].kapiX + (dukkan[1].kapiX - 1.25 - dukkan[0].kapiX) * yum((s1 - .2) / 1.3);
        var sx = x1, sy = YT, yur = adimGenlik((s1 - .2) / 1.3), ters = false, nokta = [[dukkan[0].kapiX, YT], [x1, YT]];
        tikGoster(0, 1);
        if (lt < b2) okCiz(x1 + .15, YT, dukkan[1].kapiX - .05, .02, (lt - 1.45) / .6); else tekYon.style.opacity = 1 - kis((lt - b2) / .3);
        if (lt > 1.6) kapiAc(1, true);
        /* 3) hafta: SPY sokak boyunca BÜRO'ya yürür (hafta içi kapı kapalı), cumartesi buluşur */
        var cmt = sec.cmt;
        if (lt >= b3) {
          var yp = yum((lt - b3) / (cmt - b3 + .2));
          sx = x1 + (MX - .95 - x1) * yp; yur = adimGenlik((lt - b3) / (cmt - b3 + .2)); nokta = [[dukkan[0].kapiX, YT], [sx, YT]];
          kapiAc(1, false); tikGoster(1, lt - b3);
        }
        spy.ciz(sx, sy, lt, yur, ters); cizgi(rotaT, nokta);
        /* müşteri: 2) telefonuna bakar (kanal yok); 3) hafta içi BÜRO'da mesaide, cumartesi kapıda */
        var mCik = yum((lt - cmt) / .4), mGir = yum((lt - b3) / .4);
        MUS.g.style.opacity = lt < b3 ? 1 : (lt < cmt ? 1 - mGir : mCik);
        var mx = lt < b3 ? MX : (lt < cmt ? MX + (BURO.kapiX - MX) * mGir : BURO.kapiX - (BURO.kapiX - MX) * mCik);
        MUS.ciz(mx, MY, lt, lt < cmt ? adimGenlik((lt - b3) / .4) : adimGenlik((lt - cmt) / .4), true);
        musteriTelefon(lt > b2 && lt < b3);
        kapiAc(5, (lt > b3 && lt < b3 + .5) || (lt > cmt - .1 && lt < cmt + .5));
        var sp = lt >= b2 + .5 && lt < b3 - .1 ? kis((lt - b2 - .5) / .4) : (lt >= b3 - .1 && lt < b3 + .15 ? 1 - kis((lt - b3 + .1) / .25) : 0);
        B.soru.goster(MX + .1, MY, 2.0, sp);
        var cp = kis((lt - sec.yok) / .3); B.carpi.style.opacity = cp > 0 ? 1 : 0; B.carpi.setAttribute("transform", "translate(54,-30) scale(" + (.3 + .7 * zipla(cp)) + ")");
        var mp = lt > b3 + .4 && lt < cmt - .1 ? kis((lt - b3 - .4) / .35) : (lt >= cmt - .1 && lt < cmt + .1 ? 1 - kis((lt - cmt + .1) / .2) : 0);
        B.mesai.goster(BURO.x + 1.05, -.2, BURO.h + .55, mp);
        B.gorusme.goster((MX + sx) / 2, (MY + YT) / 2, 2.2, lt > cmt + .5 ? kis((lt - cmt - .5) / .35) : 0);
        kamera(lt, [[0, [2.4, YT, .7, 1.75]], [1.5, [3, YT, .7, 1.7]], [b2 - .2, [3.2, YT, .7, 1.7]], [b2 + .5, [MX + .2, MY, 1.1, 1.9]],
          [b3 - .15, [MX + .1, MY, 1.1, 1.95]], [b3 + .7, [8.6, 0, 1.2, 1.2]], [cmt + .3, [9.6, 0, 1.2, 1.25]], [cmt + 2.2, [MX - .4, MY, 1.1, 1.6]]]);
        return;
      }
      if (MOD === "cozum") {
        /* giriş: müşteri telefondan temsilci çağırır; sonra geniş açı: turuncu SPY kapı kapı + yeşil SPY çağrılara */
        var A = sec.A, l2 = lt - A;
        var tk = sec.tik;   /* dokunuş anı */
        musteriTelefon(lt > .3);
        MUS.ciz(MX, MY, lt, false, true);
        var tp = (lt - tk) / .6;
        if (tp > 0 && tp < 1) { var ta = P(MX - .02, MY, .75); tikla.setAttribute("cx", ta[0]); tikla.setAttribute("cy", ta[1]); tikla.setAttribute("r", 8 + 30 * cik(tp)); tikla.style.opacity = 1 - tp; } else tikla.style.opacity = 0;
        var g2 = gezinti([0, 2, 4], l2, .3, (d - A - 1) / 3, -1.2);
        if (l2 < 0) { g2 = { x: -1.2, yuruyor: false, ters: false, nokta: [] }; for (var i = 0; i < 6; i++) { kapiAc(i, false); tikGoster(i, -1); } }
        spy.ciz(g2.x, YT, lt, g2.yuruyor, g2.ters); cizgi(rotaT, g2.nokta);
        var CG = [5, 3, 1], ARA = 2.3, nok = [], yur2 = false, ters2 = false, ax = 14.4, ay = 7;
        CG.forEach(function (dk, k) {
          var b = .6 + k * ARA, varis = b + 1.5, pin = cagriPin[dk];
          var bas = k === 0 ? tk + .25 - A : b + .1, gor = l2 >= bas && l2 < varis + .25;
          pin.style.opacity = gor ? 1 : 0;
          var pp = kis((l2 - bas) / .45);
          pin.setAttribute("transform", "translate(" + pin.xy[0].toFixed(1) + "," + (pin.xy[1] + 40 * (1 - zipla(pp))).toFixed(1) + ") scale(" + (.5 + .5 * zipla(pp)) + ")");
          var r = (Math.max(0, l2 - bas) % .9) / .9; pin.halka.setAttribute("r", 34 + 24 * r); pin.halka.style.opacity = gor ? 1 - r : 0;
          if (l2 >= b + .3) {
            var p = Math.max(0, Math.min(1, (l2 - b - .3) / 1.2)), e = yum(p);
            if (k === 0) {   /* ara sokaktan gelir, köşeden döner */
              var seg1 = 6.58, seg2 = 14.4 - dukkan[dk].kapiX - .2, top = seg1 + seg2, m = e * top;
              if (m < seg1) { ax = 14.4; ay = 7 - m; nok = [[14.4, 7], [ax, ay]]; } else { ax = 14.4 - (m - seg1); ay = YT; nok = [[14.4, 7], [14.4, YT], [ax, YT]]; }
            } else { var on = dukkan[CG[k - 1]].kapiX; ax = on + (dukkan[dk].kapiX - on) * e; ay = YT; nok = [[on, YT], [ax, YT]]; }
            yur2 = adimGenlik(p); ters2 = ay === YT;
          }
          var ayrilis = k < CG.length - 1 ? .6 + (k + 1) * ARA + .3 : 1e9;
          if (l2 >= 0) { kapiAc(dk, l2 > varis && l2 < ayrilis); tikGoster(dk, l2 - varis - .15); }
        });
        spy2.ciz(ax, ay + .12, lt, yur2, ters2); cizgi(rotaY, nok);
        kamera(lt, [[0, [MX - .2, MY - .6, 1.7, 1.6]], [A - .35, [MX - .2, MY - .6, 1.75, 1.55]], [A + .9, null], [d, [6.5, 0, 2.3, 1.03]]]);
        return;
      }
    }
  };
}
