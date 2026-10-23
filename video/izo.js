/* İzometrik (2,5B) mahalle sahnesi. izoSahne(svg, {cagri: bool}) → { ciz(lt, d) }
   Eksenler: x = dükkân sırası boyunca (sağa, hafif aşağı), y = derinlik (sola-aşağı = bize doğru), z = yukarı. */
function izoSahne(svg, sec) {
  sec = sec || {};
  var NS = "http://www.w3.org/2000/svg";
  function E(ad, oz, ust) { var e = document.createElementNS(NS, ad); for (var k in oz) e.setAttribute(k, oz[k]); (ust || svg).appendChild(e); return e; }
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
  var KAT = E("g", {}), ON = E("g", {});
  /* ---- zemin, yollar ---- */
  poly([[-6, -12, 0], [26, -12, 0], [26, 9, 0], [-6, 9, 0]], { fill: "#e4ece7" }, KAT);
  poly([[-6, 0, 0], [26, 0, 0], [26, .8, 0], [-6, .8, 0]], { fill: "#f1f4f2" }, KAT);            /* kaldırım */
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
  var W = 2.1, D = 2.3, ZK = 1.2, ZU = .78, dukkan = [];
  DK.forEach(function (d, i) {
    var x = i * 2.15, h = ZK + ZU * KATS[i], g = E("g", {}, KAT), ren = DUVAR[i];
    kutu(x, -D, W, D, h, ren, g);
    yuz(x - .02, x + W + .02, 0.001, h - .12, h, { fill: "#d8e0db" }, g);                                         /* korkuluk bandı */
    poly([[x + .12, -D + .12, h], [x + W - .12, -D + .12, h], [x + W - .12, -.12, h], [x + .12, -.12, h]], { fill: ren[2], opacity: .45 }, g);
    if (i % 2 === 0) kutu(x + .4, -D + .5, .55, .5, .28, ["#eef2f0", "#d9e1dc", "#c6d0ca"], g); else kutu(x + 1.1, -D + .4, .7, .7, .45, ["#e9eeeb", "#d4ddd8", "#c0cbc5"], g);
    for (var f = 0; f < KATS[i]; f++) for (var w = 0; w < 3; w++) {
      var wx = x + .22 + w * .62, wz = ZK + .18 + f * ZU;
      yuz(wx, wx + .4, .002, wz, wz + .42, { fill: "#cfe1da" }, g);
      poly([[wx + .06, .003, wz + .05], [wx + .16, .003, wz + .05], [wx + .3, .003, wz + .37], [wx + .2, .003, wz + .37]], { fill: "#fff", opacity: .6 }, g);
      yuz(wx - .04, wx + .44, .004, wz - .04, wz, { fill: "#dfe6e2" }, g);
    }
    yuz(x, x + W, .002, 0, ZK, { fill: ren[1] }, g);
    yuz(x + .12, x + 1.32, .004, .1, .9, { fill: "#cde2db" }, g);                                                 /* vitrin */
    poly([[x + .25, .006, .12], [x + .45, .006, .12], [x + .8, .006, .88], [x + .6, .006, .88]], { fill: "#fff", opacity: .55 }, g);
    poly([[x + .7, .006, .12], [x + .8, .006, .12], [x + 1.15, .006, .88], [x + 1.05, .006, .88]], { fill: "#fff", opacity: .4 }, g);
    var kapi = yuz(x + 1.48, x + 1.92, .004, 0, .9, { fill: "#8fa39b" }, g);
    var aralik = poly([[x + 1.48, .004, 0], [x + 1.48, .3, 0], [x + 1.48, .3, .88], [x + 1.48, .004, .9]], { fill: "#a9bbb3", opacity: 0 }, g);
    /* tente: cepheden dışarı eğik */
    for (var s = 0; s < 6; s++) { var sx = x + .02 + s * (W - .04) / 6; poly([[sx, .004, 1.1], [sx + (W - .04) / 6, .004, 1.1], [sx + (W - .04) / 6, .42, .92], [sx, .42, .92]], { fill: s % 2 ? "#ffffff" : d[1] }, g); }
    poly([[x + .02, .42, .92], [x + W - .02, .42, .92], [x + W - .02, .42, .86], [x + .02, .42, .86]], { fill: d[1], opacity: .85 }, g);
    /* tabela */
    var p = P(x + W / 2, .004, 1.33);
    var tg = E("g", { transform: "matrix(" + XV[0].toFixed(4) + "," + XV[1].toFixed(4) + ",0,1," + p[0].toFixed(1) + "," + p[1].toFixed(1) + ")" }, g);
    E("rect", { x: -98, y: -20, width: 196, height: 36, rx: 6, fill: "#fff", stroke: "#cfd6d2", "stroke-width": 1.5 }, tg);
    T(tg, 0, 6, d[0], { "font-size": 22, fill: d[1] });
    dukkan.push({ x: x, h: h, kapi: kapi, aralik: aralik, kapiX: x + 1.7 });
  });
  /* ---- sokak eşyası ---- */
  function agac(x, y, ol, ust) {
    var a = P(x, y, 0), g = E("g", {}, ust || ON); g.z = y;
    E("ellipse", { cx: a[0] + 14 * ol, cy: a[1] + 4, rx: 34 * ol, ry: 12 * ol, fill: "rgba(40,60,50,.16)" }, g);
    E("rect", { x: a[0] - 4 * ol, y: a[1] - 52 * ol, width: 8 * ol, height: 52 * ol, rx: 3, fill: "#80664c" }, g);
    var t = E("g", {}, g);
    E("circle", { cx: a[0], cy: a[1] - 78 * ol, r: 38 * ol, fill: "#78a98c" }, t);
    E("circle", { cx: a[0] - 16 * ol, cy: a[1] - 88 * ol, r: 22 * ol, fill: "#8fbfa2" }, t);
    E("circle", { cx: a[0] + 14 * ol, cy: a[1] - 66 * ol, r: 20 * ol, fill: "#6a9c7f" }, t);
    g.tepe = t; g.ax = a[0]; g.ay = a[1];
    return g;
  }
  function lamba(x, y) { var a = P(x, y, 0), b = P(x, y, 1.9), g = E("g", {}, ON); E("line", { x1: a[0], y1: a[1], x2: b[0], y2: b[1], stroke: "#6f7b76", "stroke-width": 5 }, g); E("path", { d: "M" + b[0] + " " + b[1] + "q16 -6 26 4", fill: "none", stroke: "#6f7b76", "stroke-width": 4 }, g); E("ellipse", { cx: b[0] + 28, cy: b[1] + 7, rx: 10, ry: 5, fill: "#fff3cc", stroke: "#6f7b76", "stroke-width": 2 }, g); }
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
  function kisi(renk, etiket, ol) {
    var k = { g: E("g", {}, ON), ol: ol || 1 };
    E("ellipse", { cx: 6, cy: 3, rx: 26, ry: 8, fill: "rgba(40,50,45,.18)" }, k.g);
    k.a = E("path", { stroke: "#2f3b48", "stroke-width": 9, "stroke-linecap": "round" }, k.g);
    k.b = E("path", { stroke: "#3a4653", "stroke-width": 9, "stroke-linecap": "round" }, k.g);
    E("path", { d: "M-16 -38c0-24 6-36 16-36s16 12 16 36z", fill: renk }, k.g);
    k.kol = E("path", { stroke: renk, "stroke-width": 8, "stroke-linecap": "round" }, k.g);
    E("rect", { x: 8, y: -62, width: 15, height: 21, rx: 2, fill: "#1E3856", stroke: "#fff", "stroke-width": 1.5 }, k.g);
    E("circle", { cx: 0, cy: -86, r: 12, fill: "#f1c9a5" }, k.g);
    E("path", { d: "M-12 -89a12 12 0 0 1 24 0c-5-5-19-5-24 0z", fill: "#3b2a20" }, k.g);
    if (etiket) { k.etk = E("g", {}, k.g); E("rect", { x: -28, y: -126, width: 56, height: 26, rx: 13, fill: "#fff", stroke: renk, "stroke-width": 3 }, k.etk); T(k.etk, 0, -107, etiket, { "font-size": 16, fill: renk === "#00724c" ? "#00724c" : "#B25E30" }); }
    k.ciz = function (x, y, faz, yuruyor, ters) {
      var a = P(x, y, 0), s = yuruyor ? Math.sin(faz * 10) * 10 : 0, z = yuruyor ? Math.abs(Math.cos(faz * 10)) * 2.5 : 0;
      k.a.setAttribute("d", "M-5 -36L" + (-5 - s) + " 0"); k.b.setAttribute("d", "M5 -36L" + (5 + s) + " 0");
      k.kol.setAttribute("d", "M-14 -64L" + (-18 + s * .7) + " -40");
      k.g.setAttribute("transform", "translate(" + a[0].toFixed(1) + "," + (a[1] - z).toFixed(1) + ") scale(" + (ters ? -k.ol : k.ol) + "," + k.ol + ")");
      if (k.etk) k.etk.setAttribute("transform", "scale(" + (ters ? -1 : 1) + ",1)");
    };
    return k;
  }
  var yaya1 = kisi("#a3aea9", null, .75), yaya2 = kisi("#c2b3a3", null, .75), yaya3 = kisi("#9fb1c2", null, .72);
  var spy = kisi("#ea803f", "SPY", 1), spy2 = sec.cagri ? kisi("#00724c", "SPY", 1) : null;
  /* ---- rota çizgileri ---- */
  var rotaT = E("polyline", { fill: "none", stroke: "#ea803f", "stroke-width": 5, "stroke-dasharray": "2 11", "stroke-linecap": "round", opacity: .9 }, ON);
  var rotaY = E("polyline", { fill: "none", stroke: "#00724c", "stroke-width": 5, "stroke-dasharray": "2 11", "stroke-linecap": "round", opacity: .9 }, ON);
  /* ---- onay işaretleri ve çağrı simgeleri ---- */
  var tik = dukkan.map(function (d) {
    var g = E("g", {}, ON); E("circle", { r: 20, fill: "#00724c", stroke: "#fff", "stroke-width": 4 }, g);
    E("path", { d: "M-8 0l6 6 11-12", fill: "none", stroke: "#fff", "stroke-width": 4.5, "stroke-linecap": "round", "stroke-linejoin": "round" }, g);
    var a = P(d.x + 1.78, .02, 1.78); g.xy = a; return g;
  });
  var cagriPin = dukkan.map(function (d) {
    var a = P(d.x + 1.05, -1.15, d.h + .55), g = E("g", { transform: "translate(" + a[0].toFixed(1) + "," + a[1].toFixed(1) + ")", opacity: 0 }, ON);
    E("path", { d: "M0 52v-18", stroke: "#00724c", "stroke-width": 4 }, g);
    g.halka = E("circle", { r: 36, fill: "none", stroke: "#00724c", "stroke-width": 4 }, g);
    E("circle", { r: 34, fill: "#00724c", stroke: "#fff", "stroke-width": 4 }, g);
    E("path", { d: "M-13 -12c0 14 12 26 26 26l5-7-8-6-4 4c-5-2-9-6-11-11l4-4-6-8z", fill: "#fff" }, g);
    return g;
  });
  function kapiAc(i, acik) { dukkan[i].kapi.setAttribute("fill", acik ? "#3e5a50" : "#8fa39b"); dukkan[i].aralik.style.opacity = acik ? 1 : 0; }
  function tikGoster(i, v) { var p = Math.max(0, Math.min(1, v / .25)); p = 1 - Math.pow(1 - p, 3); tik[i].style.opacity = v > 0 ? 1 : 0; tik[i].setAttribute("transform", "translate(" + tik[i].xy[0].toFixed(1) + "," + tik[i].xy[1].toFixed(1) + ") scale(" + (v > 0 ? .6 + .4 * p : 0) + ")"); }
  function yum(x) { x = Math.max(0, Math.min(1, x)); return x < .5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2; }
  var YT = .42;   /* kaldırımda yürüme çizgisi */
  /* kapı kapı gezinti: duraklar, başlangıç, aralık → konum + rota noktaları */
  function gezinti(duraklar, lt, bas, aralik, x0) {
    var x = x0, yuruyor = false, ters = false, nokta = [[x0, YT]];
    duraklar.forEach(function (dk, k) {
      var b = bas + k * aralik, once = k === 0 ? x0 : dukkan[duraklar[k - 1]].kapiX, sure = aralik * .6, hedef = dukkan[dk].kapiX;
      if (lt >= b) { var p = Math.max(0, Math.min(1, (lt - b) / sure)); x = once + (hedef - once) * yum(p); yuruyor = p > 0 && p < 1; ters = hedef < once; nokta.push([x, YT]); }
      var varis = b + sure, ayrilis = k < duraklar.length - 1 ? b + aralik : 1e9;
      kapiAc(dk, lt > varis && lt < ayrilis - .05); tikGoster(dk, lt - varis - .15);
    });
    return { x: x, yuruyor: yuruyor, ters: ters, nokta: nokta };
  }
  function cizgi(el, nokta) { el.setAttribute("points", nokta.map(function (n) { var a = P(n[0], n[1], 0); return a[0].toFixed(1) + "," + a[1].toFixed(1); }).join(" ")); }
  return {
    ciz: function (lt, d) {
      /* arka plan hareketi */
      ar1.ciz(-3 + ((lt * 1.6) % 26), 1.05); ar2.ciz(23 - ((lt * 1.3 + 8) % 28), 2.3);
      yaya1.ciz(19 - ((lt * .55) % 24), 3.45, lt, true, true);
      yaya2.ciz(-4 + ((lt * .5 + 6) % 24), 3.55, lt + 1, true);
      yaya3.ciz(14.4, 6 - ((lt * .5) % 10), lt + 2, true);
      if (!sec.cagri) {
        var g = gezinti([0, 1, 2, 3, 4, 5], lt, .2, (d - .9) / 6, -1.2);
        spy.ciz(g.x, YT, lt, g.yuruyor, g.ters); cizgi(rotaT, g.nokta); rotaY.setAttribute("points", "");
        cagriPin.forEach(function (c) { c.style.opacity = 0; });
      } else {
        var g2 = gezinti([0, 2, 4], lt, .3, (d - 1) / 3, -1.2);
        spy.ciz(g2.x, YT, lt, g2.yuruyor, g2.ters); cizgi(rotaT, g2.nokta);
        var CG = [1, 3, 5], ARA = 2.3, bx = 14.4, by = 7, nok = [[14.4, 7]], yur = false, ters = false, ax = 14.4, ay = 7;
        CG.forEach(function (dk, k) {
          var b = .6 + k * ARA, varis = b + 1.5, pin = cagriPin[dk], gor = lt >= b + .1 && lt < varis + .25;
          pin.style.opacity = gor ? Math.min(1, (lt - b - .1) / .25) : 0;
          var r = (Math.max(0, lt - b) % .9) / .9; pin.halka.setAttribute("r", 34 + 24 * r); pin.halka.style.opacity = gor ? 1 - r : 0;
          if (lt >= b + .3) {
            var p = Math.max(0, Math.min(1, (lt - b - .3) / 1.2)), e = yum(p);
            if (k === 0) {   /* ara sokaktan gelir, köşeden döner */
              var seg1 = 6.58, seg2 = 14.4 - dukkan[dk].kapiX, top = seg1 + seg2, m = e * top;
              if (m < seg1) { ax = 14.4; ay = 7 - m; nok = [[14.4, 7], [ax, ay]]; } else { ax = 14.4 - (m - seg1); ay = YT; nok = [[14.4, 7], [14.4, YT], [ax, YT]]; }
            } else { var on = dukkan[CG[k - 1]].kapiX; ax = on + (dukkan[dk].kapiX - on) * e; ay = YT; nok = [[on, YT], [ax, YT]]; }
            yur = p > 0 && p < 1; ters = k === 0 && ay === YT;
          }
          var ayrilis = k < CG.length - 1 ? .6 + (k + 1) * ARA + .3 : 1e9;
          kapiAc(dk, lt > varis && lt < ayrilis); tikGoster(dk, lt - varis - .15);
        });
        spy2.ciz(ax, ay + .12, lt, yur, ters); cizgi(rotaY, nok);
      }
    }
  };
}
