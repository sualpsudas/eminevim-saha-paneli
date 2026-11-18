(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.Appointment = api;
})(typeof window === 'undefined' ? globalThis : window, function () {
  'use strict';
  const terminal = (t) => !!t && ['tamamlandi', 'iptal'].includes(t.durum);
  function id() { return 'ty-' + (globalThis.crypto?.randomUUID?.() || Date.now().toString(36) + Math.random().toString(36).slice(2)); }
  function create(data) { return { ...data, id: data.id || id(), revision: data.revision || 1 }; }
  function propose(t, change) {
    if (!t || terminal(t) || t.durum === 'gorusmede') return t;
    return { ...t, degisiklik: { ...change, oncekiDurum: t.durum, istendi: Date.now() } };
  }
  function approve(t) {
    if (!t?.degisiklik || terminal(t) || t.durum === 'gorusmede') return t;
    return { ...t, ...t.degisiklik, degisiklik: null, durum: 'netlesti', revision: (t.revision || 1) + 1, dogrulama: null, yolaCikis: null, varisZamani: null, gecikme: 0, demoZaman: null };
  }
  function depart(t, minutes, now = Date.now()) {
    if (!t || t.durum !== 'netlesti' || t.degisiklik) return t;
    return { ...t, durum: 'yolda', yolaCikis: now, sonKonum: now, varisZamani: now + Math.max(1, minutes) * 60000, demoZaman: null };
  }
  function challenge(t, now = Date.now()) {
    if (!t || !['yolda', 'gorusme'].includes(t.durum) || !t.repId) return t;
    if (t.dogrulama && t.dogrulama.son > now && t.dogrulama.revision === t.revision) return t;
    const values = new Uint32Array(1);
    if (globalThis.crypto?.getRandomValues) globalThis.crypto.getRandomValues(values);
    else values[0] = Math.floor(Math.random() * 0xffffffff);
    return { ...t, dogrulama: { kod: String(1000 + values[0] % 9000), son: now + 10 * 60000, revision: t.revision } };
  }
  function verify(t, bookingId, repId, code, now = Date.now()) {
    const c = t?.dogrulama;
    if (!t || !['yolda', 'gorusme'].includes(t.durum) || t.id !== bookingId || t.repId !== repId || !c || c.kod !== code || c.son <= now || c.revision !== t.revision) return null;
    return { ...t, durum: 'gorusmede', dogrulama: null, dogrulandi: { bookingId, repId, zaman: now } };
  }
  function cancel(t) { return !t || terminal(t) || t.durum === 'gorusmede' ? t : { ...t, durum: 'iptal', iptalZamani: Date.now(), degisiklik: null, dogrulama: null }; }
  function eta(t, now = Date.now()) {
    if (!t?.varisZamani) return null;
    const clock = t.demoZaman ? t.demoZaman.simdi + now - t.demoZaman.baslangic : now;
    return { dakika: Math.max(0, Math.ceil((t.varisZamani - clock) / 60000)), saat: new Date(t.varisZamani).toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' }), eski: !!t.sonKonum && now - t.sonKonum > 120000 };
  }
  return { create, terminal, propose, approve, depart, challenge, verify, cancel, eta };
});
