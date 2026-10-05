(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  root.OrgData = api;
})(typeof window !== "undefined" ? window : globalThis, function () {
  "use strict";

  const METRIK_TANIMLARI = Object.freeze({
    hg: { etiket: "H/G", aciklama: "Hedef / Gerçekleşme", formul: "gerceklesenCiro / ciroHedefi" },
    ciro: { etiket: "Ciro", birim: "₺" },
    randevu: { etiket: "Randevu", birim: "adet" },
    kart: { etiket: "Açılan Kart", birim: "adet" },
    kayit: { etiket: "Kayıt", birim: "adet" },
  });
  // Demo verinin "bugün"ü cihaz saatinden alınır (öğlen 12:00, gün kayması olmasın diye).
  // Sabit tarihle test için window.EMINEVIM_CONFIG.demoToday = "YYYY-AA-GG" verilebilir.
  const DEMO_TODAY = (function () {
    const cfg = typeof window !== "undefined" && window.EMINEVIM_CONFIG && window.EMINEVIM_CONFIG.demoToday;
    if (cfg) return new Date(cfg + "T12:00:00");
    const now = new Date();
    return new Date(now.getFullYear(), now.getMonth(), now.getDate(), 12);
  })();
  const DAY = 86400000;

  function hash(text) {
    let h = 2166136261;
    for (let i = 0; i < String(text).length; i += 1) {
      h ^= String(text).charCodeAt(i);
      h = Math.imul(h, 16777619);
    }
    return h >>> 0;
  }
  function seeded(key) {
    let t = hash(key) + 0x6D2B79F5;
    return function () {
      t += 0x6D2B79F5;
      let x = t;
      x = Math.imul(x ^ (x >>> 15), x | 1);
      x ^= x + Math.imul(x ^ (x >>> 7), x | 61);
      return ((x ^ (x >>> 14)) >>> 0) / 4294967296;
    };
  }
  function iso(d) { return new Date(d).toISOString().slice(0, 10); }
  function addDays(d, n) { return new Date(new Date(d).getTime() + n * DAY); }
  function isWeekday(d) { const day = new Date(d).getDay(); return day !== 0 && day !== 6; }
  function monthKey(d) { return iso(d).slice(0, 7); }

  const sahaPlan = [
    { ad: "Orta", sgl: "Murat Erdem", bolge: ["Ankara", "Konya", "Kayseri", "Eskişehir", "Sivas", "Çorum"] },
    { ad: "Batı", sgl: "Ece Aksoy", bolge: ["İzmir", "Manisa", "Denizli"] },
    { ad: "Doğu", sgl: "Cemal Arslan", bolge: ["Antalya", "Adana", "Gaziantep", "Samsun", "Trabzon", "Ordu", "Diyarbakır", "Şanlıurfa", "Malatya"] },
    { ad: "İstanbul", sgl: "Selin Güneş", bolge: ["İstanbul Anadolu", "İstanbul Avrupa", "Bursa", "Kocaeli"] },
  ];
  const ilceler = {
    "İstanbul Anadolu": ["Kadıköy", "Ataşehir", "Üsküdar", "Maltepe", "Kartal", "Pendik", "Ümraniye", "Beykoz", "Tuzla", "Sancaktepe", "Çekmeköy", "Adalar", "Sultanbeyli", "Şile", "Kozyatağı", "Bostancı", "Acıbadem", "Göztepe"],
    "İstanbul Avrupa": ["Beşiktaş", "Şişli", "Bakırköy", "Beyoğlu", "Sarıyer", "Kağıthane", "Eyüpsultan", "Fatih", "Başakşehir", "Beylikdüzü", "Avcılar", "Bağcılar", "Bahçelievler", "Güngören", "Zeytinburnu", "Esenyurt", "Arnavutköy", "Silivri"],
    Bursa: ["Nilüfer", "Osmangazi", "Yıldırım", "Mudanya", "Gemlik", "İnegöl", "Karacabey", "Kestel", "Gürsu", "Mustafakemalpaşa", "Orhangazi", "İznik", "Yenişehir", "Orhaneli", "Büyükorhan", "Harmancık", "Keles", "Merkez"],
    Kocaeli: ["İzmit", "Gebze", "Darıca", "Körfez", "Gölcük", "Kartepe", "Başiskele", "Çayırova", "Dilovası", "Kandıra", "Derince", "Karamürsel", "Yahya Kaptan", "Sekapark", "Merkez", "Plajyolu", "Umuttepe", "Hereke"],
    Ankara: ["Çankaya", "Keçiören", "Yenimahalle", "Mamak", "Etimesgut", "Sincan", "Gölbaşı", "Pursaklar", "Altındağ", "Polatlı", "Beypazarı", "Eryaman", "Batıkent", "Ümitköy", "Kızılay", "Bahçelievler", "Dikmen", "İncek"],
    Konya: ["Selçuklu", "Meram", "Karatay", "Ereğli", "Akşehir", "Beyşehir", "Seydişehir", "Cihanbeyli", "Ilgın", "Kulu", "Çumra", "Bosna", "Zafer", "Alaaddin", "Merkez", "Nalçacı", "Yazır", "Sille"],
    Kayseri: ["Melikgazi", "Kocasinan", "Talas", "Develi", "Yahyalı", "Bünyan", "İncesu", "Hacılar", "Erciyes", "Hunat", "Forum", "Merkez", "Argıncık", "Belsin", "Gesi", "Mimarsinan", "Sahabiye", "Anayurt"],
    Eskişehir: ["Odunpazarı", "Tepebaşı", "Sivrihisar", "Çifteler", "Alpu", "Mahmudiye", "Batıkent", "Vişnelik", "Bağlar", "Merkez", "Çamlıca", "Emek", "Kurtuluş", "Sazova", "Ihlamurkent", "Hoşnudiye", "Kanlıkavak", "Yenibağlar"],
    Sivas: ["Merkez", "Şarkışla", "Suşehri", "Zara", "Kangal", "Divriği", "Gemerek", "Yıldızeli", "Gürün", "Koyulhisar", "Hafik", "İmranlı", "Ulaş", "Altınyayla", "Akıncılar", "Gölova", "Doğanşar", "Paşabahçe"],
    Çorum: ["Merkez", "Sungurlu", "Osmancık", "İskilip", "Alaca", "Bayat", "Kargı", "Mecitözü", "Ortaköy", "Oğuzlar", "Dodurga", "Boğazkale", "Laçin", "Uğurludağ", "Bahçelievler", "Gülabibey", "Buharaevler", "Hitit"],
    İzmir: ["Konak", "Karşıyaka", "Bornova", "Buca", "Bayraklı", "Çiğli", "Gaziemir", "Balçova", "Narlıdere", "Menemen", "Torbalı", "Aliağa", "Urla", "Çeşme", "Ödemiş", "Kemalpaşa", "Alsancak", "Göztepe"],
    Manisa: ["Şehzadeler", "Yunusemre", "Akhisar", "Salihli", "Turgutlu", "Soma", "Alaşehir", "Kula", "Demirci", "Gördes", "Kırkağaç", "Saruhanlı", "Köprübaşı", "Selendi", "Merkez", "Muradiye", "Laleli", "Horozköy"],
    Denizli: ["Pamukkale", "Merkezefendi", "Çivril", "Acıpayam", "Tavas", "Honaz", "Sarayköy", "Buldan", "Çal", "Çameli", "Kale", "Serinhisar", "Bekilli", "Babadağ", "Kınıklı", "Bayramyeri", "Servergazi", "Üçler"],
    Antalya: ["Muratpaşa", "Kepez", "Konyaaltı", "Alanya", "Manavgat", "Serik", "Kumluca", "Kaş", "Finike", "Kemer", "Döşemealtı", "Aksu", "Gazipaşa", "Korkuteli", "Lara", "Kaleiçi", "Varsak", "Uncalı"],
    Adana: ["Seyhan", "Çukurova", "Yüreğir", "Sarıçam", "Ceyhan", "Kozan", "İmamoğlu", "Karataş", "Pozantı", "Karaisalı", "Tufanbeyli", "Yumurtalık", "Feke", "Saimbeyli", "Ziyapaşa", "Reşatbey", "Barkal", "Merkez"],
    Gaziantep: ["Şahinbey", "Şehitkamil", "Nizip", "İslahiye", "Oğuzeli", "Nurdağı", "Araban", "Yavuzeli", "Karkamış", "Karataş", "İbrahimli", "Binevler", "Alleben", "Merkez", "Gatem", "Gazikent", "Düztepe", "Üniversite"],
    Samsun: ["İlkadım", "Atakum", "Canik", "Tekkeköy", "Bafra", "Çarşamba", "Terme", "Vezirköprü", "Havza", "Alaçam", "Kavak", "Ondokuzmayıs", "Ladik", "Salıpazarı", "Merkez", "Kurupelit", "Denizevleri", "Meydan"],
    Trabzon: ["Ortahisar", "Akçaabat", "Yomra", "Araklı", "Of", "Sürmene", "Vakfıkebir", "Beşikdüzü", "Maçka", "Arsin", "Çarşıbaşı", "Tonya", "Düzköy", "Şalpazarı", "Meydan", "Kaşüstü", "Boztepe", "Değirmendere"],
    Ordu: ["Altınordu", "Ünye", "Fatsa", "Perşembe", "Gölköy", "Korgan", "Kumru", "Aybastı", "Gürgentepe", "Akkuş", "Mesudiye", "Ulubey", "Çamaş", "Kabataş", "Bucak", "Akyazı", "Bahçelievler", "Merkez"],
    Diyarbakır: ["Bağlar", "Kayapınar", "Sur", "Yenişehir", "Bismil", "Ergani", "Silvan", "Çermik", "Çınar", "Kulp", "Dicle", "Lice", "Hani", "Hazro", "Ofis", "Koşuyolu", "Dağkapı", "Merkez"],
    Şanlıurfa: ["Haliliye", "Eyyübiye", "Karaköprü", "Siverek", "Viranşehir", "Birecik", "Akçakale", "Ceylanpınar", "Harran", "Bozova", "Hilvan", "Suruç", "Halfeti", "Göbeklitepe", "Bahçelievler", "Atatürk", "Topçu Meydanı", "Merkez"],
    Malatya: ["Battalgazi", "Yeşilyurt", "Doğanşehir", "Akçadağ", "Darende", "Hekimhan", "Arapgir", "Pütürge", "Yazıhan", "Kuluncak", "Arguvan", "Kale", "Doğanyol", "Merkez", "Çilesiz", "Fahri Kayahan", "Bostanbaşı", "İnönü"],
  };
  const bolgeSubeSayilari = [14, 14, 10, 9, 13, 11, 9, 8, 7, 7, 12, 10, 8, 14, 12, 11, 10, 9, 8, 8, 8, 8];
  const adlar = ["Ahmet", "Ayşe", "Mehmet", "Zeynep", "Mustafa", "Elif", "Ali", "Merve", "Emre", "Ceren", "Burak", "Seda", "Can", "Eylül", "Kerem", "İrem", "Ozan", "Gizem", "Tolga", "Büşra", "Umut", "Pınar", "Serkan", "Dilan", "Barış", "Melis"];
  const soyadlar = ["Yılmaz", "Kaya", "Demir", "Şahin", "Çelik", "Aydın", "Arslan", "Koç", "Kurt", "Özdemir", "Polat", "Güneş", "Erdem", "Aksoy", "Yıldız", "Taş"];
  const renkler = ["#276F4E", "#C99A2E", "#2D4668", "#7A5C91", "#B75D69"];

  const sahalar = [];
  const bolgeler = [];
  const subeler = [];
  const takimLiderleri = [];
  const personeller = [];
  sahaPlan.forEach((s, si) => {
    const sahaId = "saha-" + (si + 1);
    const sglId = "sgl-" + (si + 1);
    sahalar.push({ id: sahaId, ad: s.ad, sglId, bolgeId: null, subeId: null, tlId: null });
    s.bolge.forEach((ad) => bolgeler.push({ id: "bolge-" + (bolgeler.length + 1), ad: ad + " Bölge", sahaId, sglId, subeId: null, tlId: null }));
  });
  bolgeler.forEach((b, i) => {
    const city = b.ad.replace(" Bölge", "");
    const names = ilceler[city];
    for (let j = 0; j < bolgeSubeSayilari[i]; j += 1) {
      subeler.push({ id: "sube-" + (subeler.length + 1), ad: names[j % names.length] + " Şubesi", sahaId: b.sahaId, bolgeId: b.id, sglId: b.sglId, tlId: null });
    }
  });

  const tlSahaSayilari = [12, 8, 15, 10];
  sahalar.forEach((saha, si) => {
    const ilgili = subeler.filter((x) => x.sahaId === saha.id);
    for (let i = 0; i < tlSahaSayilari[si]; i += 1) {
      takimLiderleri.push({ id: "tl-" + (takimLiderleri.length + 1), ad: (i + 1) + ". Takım", liderAd: adlar[(i * 3 + si) % adlar.length] + " " + soyadlar[(i * 5 + si) % soyadlar.length], takimNo: i + 1, sahaId: saha.id, bolgeId: null, subeId: null, tlId: null, sglId: saha.sglId });
    }
    ilgili.forEach((sube, i) => { sube.tlId = takimLiderleri.filter((x) => x.sahaId === saha.id)[i % tlSahaSayilari[si]].id; });
  });

  const ozel = ["Onur K.", "Derya A.", "Berk C."];
  for (let i = 0; i < 250; i += 1) {
    const sube = subeler[(i * 37 + Math.floor(i / 17)) % subeler.length];
    const ad = ozel[i] || (adlar[(i * 7) % adlar.length] + " " + soyadlar[(i * 11) % soyadlar.length]);
    personeller.push({ id: i < 3 ? "s" + (i + 1) : "p-" + (i + 1), ad, sahaId: sube.sahaId, bolgeId: sube.bolgeId, subeId: sube.id, tlId: sube.tlId, sglId: sube.sglId, renk: renkler[i % renkler.length] });
  }

  const aylikHedefler = {};
  const gunlukMetrikler = {};
  personeller.forEach((p, pi) => {
    const perf = 0.68 + seeded("perf:" + p.id)() * 0.55;
    gunlukMetrikler[p.id] = [];
    for (let offset = 399; offset >= 0; offset -= 1) {
      const date = addDays(DEMO_TODAY, -offset);
      const key = monthKey(date);
      if (!aylikHedefler[p.id]) aylikHedefler[p.id] = {};
      if (!aylikHedefler[p.id][key]) aylikHedefler[p.id][key] = Math.round((1500000 + seeded("target:" + p.id + ":" + key)() * 2500000) / 50000) * 50000;
      const rng = seeded("metric:" + p.id + ":" + iso(date));
      const weekend = isWeekday(date) ? 1 : 0.22;
      const monthEnd = date.getDate() >= 25 ? 1.13 : 1;
      const targetDaily = aylikHedefler[p.id][key] / 22;
      const ciro = Math.round(targetDaily * perf * weekend * monthEnd * (0.65 + rng() * 0.75));
      const randevu = Math.max(0, Math.round((2.5 + rng() * 6) * weekend * perf));
      const kart = Math.min(randevu, Math.max(0, Math.round(randevu * (0.48 + rng() * 0.32))));
      const kayit = Math.min(kart, Math.max(0, Math.round(kart * (0.35 + rng() * 0.4))));
      gunlukMetrikler[p.id].push({ tarih: iso(date), ciro, randevu, kart, kayit });
    }
  });

  const idCache = new Map();
  const periodCache = new Map();
  function nodePersonelIds(scope, id) {
    const key = scope + ":" + id;
    if (idCache.has(key)) return idCache.get(key);
    let result;
    if (scope === "ask" || scope === "sirket") result = personeller.map((x) => x.id);
    else if (scope === "sgl") result = personeller.filter((x) => x.sglId === id).map((x) => x.id);
    else if (scope === "saha") result = personeller.filter((x) => x.sahaId === id).map((x) => x.id);
    else if (scope === "bolge") result = personeller.filter((x) => x.bolgeId === id).map((x) => x.id);
    else if (scope === "tl") result = personeller.filter((x) => x.tlId === id).map((x) => x.id);
    else if (scope === "sube") result = personeller.filter((x) => x.subeId === id).map((x) => x.id);
    else result = personeller.filter((x) => x.id === id).map((x) => x.id);
    idCache.set(key, result);
    return result;
  }
  function getRange(periodKey, anchor) {
    const d = new Date(anchor || DEMO_TODAY);
    const start = new Date(d); const end = new Date(d);
    if (periodKey === "gun") { /* same day */ }
    else if (periodKey === "hafta") { const delta = (d.getDay() + 6) % 7; start.setDate(d.getDate() - delta); }
    else if (periodKey === "ay") { start.setDate(1); }
    else { start.setMonth(0, 1); }
    return { start, end };
  }
  function previousRange(periodKey, range) {
    if (periodKey === "ay") {
      // Aylık kıyas: geçen ayın aynı günleri (ör. 1–5 Ekim ↔ 1–5 Eylül).
      const start = new Date(range.start); start.setMonth(range.start.getMonth() - 1, 1);
      const sonGun = new Date(start); sonGun.setMonth(start.getMonth() + 1, 0);
      const end = new Date(start); end.setDate(Math.min(range.end.getDate(), sonGun.getDate()));
      return { start, end };
    }
    const days = Math.round((range.end - range.start) / DAY) + 1;
    return { start: addDays(range.start, -days), end: addDays(range.start, -1) };
  }
  function monthlyWorkdays(key) {
    const start = new Date(key + "-01T12:00:00+03:00");
    const end = new Date(start); end.setMonth(start.getMonth() + 1, 0);
    let n = 0; for (let d = new Date(start); d <= end; d = addDays(d, 1)) if (isWeekday(d)) n += 1;
    return n || 22;
  }
  function aggregate(ids, range) {
    const out = { ciro: 0, hedef: 0, randevu: 0, kart: 0, kayit: 0 };
    ids.forEach((id) => {
      const rows = gunlukMetrikler[id] || [];
      rows.forEach((row) => {
        const d = new Date(row.tarih + "T12:00:00+03:00");
        if (d < range.start || d > range.end) return;
        out.ciro += row.ciro; out.randevu += row.randevu; out.kart += row.kart; out.kayit += row.kayit;
        if (isWeekday(d)) out.hedef += (aylikHedefler[id][monthKey(d)] || 0) / monthlyWorkdays(monthKey(d));
      });
    });
    out.hedef = Math.round(out.hedef);
    out.hg = out.hedef ? out.ciro / out.hedef * 100 : 0;
    out.randevuKart = out.randevu ? out.kart / out.randevu * 100 : 0;
    out.kartKayit = out.kart ? out.kayit / out.kart * 100 : 0;
    out.randevuKayit = out.randevu ? out.kayit / out.randevu * 100 : 0;
    return out;
  }
  function trendFor(ids, periodKey, range) {
    let parts = [];
    if (periodKey === "gun") for (let i = 6; i >= 0; i -= 1) parts.push({ label: iso(addDays(range.end, -i)).slice(5), start: addDays(range.end, -i), end: addDays(range.end, -i) });
    else if (periodKey === "hafta") for (let i = 0; i < 7; i += 1) parts.push({ label: ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"][i], start: addDays(range.start, i), end: addDays(range.start, i) });
    else if (periodKey === "ay") for (let i = 0; i < 4; i += 1) parts.push({ label: (i + 1) + ". hf", start: addDays(range.start, i * 7), end: i === 3 ? range.end : addDays(range.start, i * 7 + 6) });
    else for (let i = 0; i < 12; i += 1) { const start = new Date(range.start); start.setMonth(i, 1); const end = new Date(start); end.setMonth(i + 1, 0); parts.push({ label: (i + 1) + ". ay", start, end }); }
    return parts.map((p) => ({ label: p.label, ...aggregate(ids, p) }));
  }
  function hedefAraligi(ids, start, end) {
    let toplam = 0;
    ids.forEach((id) => {
      for (let d = new Date(start); d <= end; d = addDays(d, 1)) {
        if (isWeekday(d)) toplam += ((aylikHedefler[id] || {})[monthKey(d)] || 0) / monthlyWorkdays(monthKey(d));
      }
    });
    return Math.round(toplam);
  }
  function getPeriod(scope, id, periodKey, anchor) {
    const cacheKey = [scope, id, periodKey || "gun", anchor ? iso(anchor) : iso(DEMO_TODAY)].join(":");
    if (periodCache.has(cacheKey)) return periodCache.get(cacheKey);
    const ids = nodePersonelIds(scope, id);
    const range = getRange(periodKey || "gun", anchor);
    const oncekiAralik = previousRange(periodKey || "gun", range);
    const onceki = aggregate(ids, oncekiAralik);
    const simdi = aggregate(ids, range);
    if ((periodKey || "gun") === "ay") {
      // Aylık H/G ayın TAM hedefine göre: ciro / ay hedefi. Bugüne kadarki hedefe göre oran ay sonu tahminidir.
      const ayBitis = new Date(range.start); ayBitis.setMonth(range.start.getMonth() + 1, 0);
      simdi.hedefBugune = simdi.hedef;
      simdi.tahminHg = simdi.hg;
      simdi.hedef = hedefAraligi(ids, range.start, ayBitis);
      simdi.hg = simdi.hedef ? simdi.ciro / simdi.hedef * 100 : 0;
      simdi.tahminCiro = simdi.hedef * simdi.tahminHg / 100;
    }
    simdi.degisim = onceki.ciro ? (simdi.ciro - onceki.ciro) / onceki.ciro * 100 : 0;
    simdi.onceki = onceki;
    simdi.oncekiAralik = { start: iso(oncekiAralik.start), end: iso(oncekiAralik.end) };
    simdi.trend = trendFor(ids, periodKey || "gun", range);
    simdi.personelSayisi = ids.length;
    periodCache.set(cacheKey, simdi);
    return simdi;
  }
  function kapsamFiltrele(kullanici, veri) {
    const user = kullanici || {};
    if (user.rol === "ask") return veri.slice();
    if (user.rol === "sgl") return veri.filter((x) => x.sglId === user.id || x.sahaId === user.sahaId || x.id === user.sahaId);
    if (user.rol === "tl") return veri.filter((x) => x.tlId === user.id || x.id === user.id || (x.id && user.subeIds && user.subeIds.indexOf(x.id) >= 0));
    return veri.filter((x) => x.id === user.id);
  }
  function children(scope, id) {
    if (scope === "ask" || scope === "sirket") return sahalar.map((x) => ({ ...x, scope: "saha" }));
    if (scope === "sgl" || scope === "saha") return takimLiderleri.filter((x) => x.sglId === id || x.sahaId === id).map((x) => ({ ...x, scope: "tl" }));
    if (scope === "bolge") return subeler.filter((x) => x.bolgeId === id).map((x) => ({ ...x, scope: "sube" }));
    if (scope === "tl") return personeller.filter((x) => x.tlId === id).map((x) => ({ ...x, scope: "personel" }));
    if (scope === "sube") return personeller.filter((x) => x.subeId === id).map((x) => ({ ...x, scope: "personel" }));
    return [];
  }
  function findNode(scope, id) {
    const pools = { saha: sahalar, bolge: bolgeler, sube: subeler, tl: takimLiderleri, personel: personeller, spy: personeller };
    return (pools[scope] || []).find((x) => x.id === id) || null;
  }
  function demoUser(role) {
    if (role === "ask") return { rol: "ask", id: "ask-1", ad: "Deniz Karaca", birimAd: "Şirket Geneli", scope: "ask", scopeId: "ask-1" };
    if (role === "sgl") { const saha = sahalar[1]; return { rol: "sgl", id: saha.sglId, ad: sahaPlan[1].sgl, birimAd: saha.ad, sahaId: saha.id, scope: "saha", scopeId: saha.id }; }
    if (role === "tl") { const tl = takimLiderleri.find((x) => subeler.filter((s) => s.tlId === x.id).length > 1); return { rol: "tl", id: tl.id, ad: tl.liderAd, birimAd: tl.ad, sahaId: tl.sahaId, subeIds: subeler.filter((x) => x.tlId === tl.id).map((x) => x.id), scope: "tl", scopeId: tl.id }; }
    const p = personeller[0]; const tl = takimLiderleri.find((x) => x.id === p.tlId); const saha = sahalar.find((x) => x.id === p.sahaId); return { rol: "spy", id: p.id, ad: p.ad, birimAd: p.ad, takimAd: tl ? tl.ad : "Takım", sahaAd: saha ? saha.ad : "Saha", sahaId: p.sahaId, bolgeId: p.bolgeId, subeId: p.subeId, tlId: p.tlId, scope: "personel", scopeId: p.id };
  }
  function configureRemote() {
    const endpoint = typeof window !== "undefined" && window.EMINEVIM_CONFIG && window.EMINEVIM_CONFIG.orgEndpoint;
    return endpoint ? { endpoint, mode: "remote-ready", fallback: "demo" } : { endpoint: null, mode: "demo" };
  }

  return Object.freeze({ METRIK_TANIMLARI, DEMO_TODAY: iso(DEMO_TODAY), sahalar, bolgeler, subeler, takimLiderleri, personeller, aylikHedefler, gunlukMetrikler, getPeriod, children, findNode, demoUser, kapsamFiltrele, configureRemote, nodePersonelIds });
});
