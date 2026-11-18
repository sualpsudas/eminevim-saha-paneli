/* MÜŞTERİ HESABI KAPISI — giriş, parola, SMS kodu.
   Merkez sürümünde (CANLI) hesaplar merkezde (api/musteri); GitHub Pages gösterisinde bu tarayıcıda.
   Gerçek yayında Eminevim üye sistemi + SMS servisi; yalnız bu dosya ve merkez/ty/musteri.py değişir. */
/* SMS giriş kodu (demo): gerçek SMS yerine aynı sitedeki tarayıcı deposunda tutulur. Web başvurusu 24 saat geçerli kod yazar,
   uygulama "Kodu gönder" ile 10 dakika geçerli yeni kod üretir. Gerçek yayında kod sunucuda üretilir ve SMS ile gider. */
function smsKodOku(tel) { try { const k = JSON.parse(localStorage.getItem("ty-sms-kod") || "null"); return k && k.tel === telAnahtar(tel) && k.son > Date.now() ? k : null; } catch (e) { return null; } }
function smsKodUret(tel) { const v = new Uint32Array(1); (window.crypto && crypto.getRandomValues) ? crypto.getRandomValues(v) : (v[0] = Math.floor(Math.random() * 1e9)); const k = { tel: telAnahtar(tel), kod: String(100000 + v[0] % 900000), son: Date.now() + 10 * 60000 }; try { localStorage.setItem("ty-sms-kod", JSON.stringify(k)); } catch (e) {} return k; }
function smsKodSil() { try { localStorage.removeItem("ty-sms-kod"); } catch (e) {} }
function KAYIT_DEPO() { return CANLI ? localStorage : sessionStorage; }
function parolaKaydi(tel) {
  try { return JSON.parse(KAYIT_DEPO().getItem("ty-demo-parola:" + tel) || "null"); } catch (_) { return null; }
}
function parolaKaydet(tel, kayit) { KAYIT_DEPO().setItem("ty-demo-parola:" + tel, JSON.stringify(kayit)); }
async function parolaOzeti(parola, tuz = Array.from(crypto.getRandomValues(new Uint8Array(16)))) {
  const anahtar = await crypto.subtle.importKey("raw", new TextEncoder().encode(parola), "PBKDF2", false, ["deriveBits"]);
  const sonuc = await crypto.subtle.deriveBits({name:"PBKDF2",hash:"SHA-256",salt:new Uint8Array(tuz),iterations:100000}, anahtar, 256);
  return {tuz, ozet:Array.from(new Uint8Array(sonuc), b => b.toString(16).padStart(2,"0")).join("")};
}
// Merkez sürümünde müşteri hesabı merkezde: aynı telefon + parola her telefonda çalışır (parolayı merkez özetler)
function musteriMerkez(islem, govde) {
  return Canli.gonder("api/musteri", { islem, ...govde }).then((v) => v.sonuc,
    (e) => { throw e instanceof TypeError ? Error("Merkeze ulaşılamadı. İnternet bağlantınızı kontrol edip yeniden deneyin.") : e; });
}
function smsKodYaz(tel, kod) { const k = { tel: telAnahtar(tel), kod, son: Date.now() + 10 * 60000 }; try { localStorage.setItem("ty-sms-kod", JSON.stringify(k)); } catch (e) {} return k; }
