const assert = require("node:assert/strict");
const OrgData = require("../org-data.js");

assert.equal(OrgData.sahalar.length, 4, "4 saha olmalı");
assert.equal(OrgData.bolgeler.length, 22, "22 bölge olmalı");
assert.equal(OrgData.subeler.length, 220, "220 şube olmalı");
assert.equal(OrgData.personeller.length, 250, "250 personel olmalı");
assert.equal(OrgData.takimLiderleri.length, 45, "45 takım lideri olmalı");

const ids = new Set(OrgData.personeller.map((x) => x.id));
["s1", "s2", "s3"].forEach((id) => assert(ids.has(id), `${id} canlı SPY listesinde ve organizasyonda bulunmalı`));
OrgData.personeller.forEach((p) => {
  assert(OrgData.sahalar.some((x) => x.id === p.sahaId), `${p.id} saha referansı`);
  assert(OrgData.bolgeler.some((x) => x.id === p.bolgeId), `${p.id} bölge referansı`);
  assert(OrgData.subeler.some((x) => x.id === p.subeId), `${p.id} şube referansı`);
  assert(OrgData.takimLiderleri.some((x) => x.id === p.tlId), `${p.id} TL referansı`);
});

for (const period of ["gun", "hafta", "ay", "yil"]) {
  const company = OrgData.getPeriod("ask", "ask-1", period);
  const sahaMetrics = OrgData.sahalar.map((x) => OrgData.getPeriod("saha", x.id, period));
  for (const key of ["ciro", "randevu", "kart", "kayit"]) {
    assert.equal(company[key], sahaMetrics.reduce((sum, x) => sum + x[key], 0), `${period} ${key} saha toplamı`);
  }
  assert(Math.abs(company.hedef - sahaMetrics.reduce((sum, x) => sum + x.hedef, 0)) <= 4, `${period} hedef toplamı`);
  assert(Math.abs(company.hg - (company.hedef ? company.ciro / company.hedef * 100 : 0)) < 1e-9, `${period} H/G toplamlardan hesaplanmalı`);
}

console.log("org-data: 4 saha · 22 bölge · 220 şube · 45 TL · 250 personel — OK");
