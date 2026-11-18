"""Kozmetik öneri taslakları (2026-11-18): gerçek uygulama ekranı → "Şimdi" görüntüsü; aynı ekrana öneriler yalnız taslak için
giydirilir (CSS + küçük DOM ekleri, uygulama kodu DEĞİŞMEZ) → "Öneri" görüntüsü. Çıktı: taslak/kozmetik/*.jpg (yan yana).
Çalıştırma: yerel 8799 açıkken  python araclar/kozmetik_taslak.py"""
import importlib.util
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

_spec = importlib.util.spec_from_file_location("sg", str(Path(__file__).with_name("senaryo_goruntu.py")))
sg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sg)
app, bekle, TELEFON, TABLET = sg.app, sg.bekle, sg.TELEFON, sg.TABLET
CIKTI = sg.KOK / "taslak" / "kozmetik"
GECICI = CIKTI / "_ham"

# Taslak yardımcıları: her değişiklik geri alınabilir (React'in yönettiği düğümler bozulmasın)
YARDIMCI = r"""
window.T = {geri: [],
  css(c){ const s=document.createElement('style'); s.textContent=c; document.head.appendChild(s); this.geri.push(()=>s.remove()); },
  ekle(sec, yer, html){ const e=document.querySelector(sec); if(!e) throw Error('yok: '+sec); const k=document.createElement('div'); k.innerHTML=html;
    const n=[...k.childNodes]; n.forEach(x=>{ if(yer==='once') e.before(x); else if(yer==='sonra') e.after(x); else if(yer==='bas') e.prepend(x); else e.append(x); });
    this.geri.push(()=>n.forEach(x=>x.remove())); },
  gizle(sec){ document.querySelectorAll(sec).forEach(e=>{ const d=e.style.display; e.style.display='none'; this.geri.push(()=>{ e.style.display=d; }); }); },
  yazi(eski, yeni){ const w=document.createTreeWalker(document.getElementById('dc-root'), NodeFilter.SHOW_TEXT); let n, say=0;
    while((n=w.nextNode())){ if(n.nodeValue.includes(eski)){ const o=n.nodeValue; n.nodeValue=o.replace(eski,yeni); const m=n; this.geri.push(()=>{ m.nodeValue=o; }); say++; } }
    if(!say) throw Error('metin yok: '+eski); },
  bul(metin, sec){ return [...document.querySelectorAll(sec||'*')].find(e=>e.children.length===0&&e.textContent.trim()===metin) },
  sinif(el, s){ el.classList.add(s); this.geri.push(()=>el.classList.remove(s)); },
  temizle(){ this.geri.reverse().forEach(f=>f()); this.geri=[]; }
};
"""

# 4. Okunur yazı: müşteri ekranında en küçük yazı ~15 px, gri koyulaşır
MUSTERI_YAZI = """
.customer-screen{--dim:#4d5852 !important}
.customer-screen .m-akis p,.customer-screen .m-akis small,.customer-screen .m-kart p{font-size:15px !important;line-height:1.45 !important}
.customer-screen .m-kart h2{font-size:22px !important}
.customer-screen .m-kart h3{font-size:17px !important}
.customer-screen .m-btn{font-size:16px !important;min-height:50px !important}
.customer-nav span{font-size:12.5px !important}
.customer-durum{display:none !important}
.customer-screen .m-actions .m-btn{font-size:15px !important;white-space:nowrap}
"""

ILERLEME = """<div class="m-kart" style="padding:14px 14px 12px">
 <div style="display:flex;justify-content:space-between;position:relative">
  <div style="position:absolute;left:9%;right:9%;top:13px;height:3px;background:#dfe5e2"></div>
  <div style="position:absolute;left:9%;width:{dolu}%;top:13px;height:3px;background:#00724c"></div>
  {adimlar}
 </div></div>"""


def ilerleme(etkin):
    adlar = ["Çağrı alındı", "Temsilci belli", "Onaylandı", "Yolda", "Görüşme"]
    h = ""
    for i, ad in enumerate(adlar):
        renk = "#00724c" if i < etkin else "#ea803f" if i == etkin else "#c9d1cd"
        ic = "✓" if i < etkin else str(i + 1)
        h += (f'<div style="position:relative;z-index:1;width:20%;text-align:center"><div style="width:28px;height:28px;margin:0 auto;border-radius:50%;'
              f'background:{renk};color:#fff;font:700 13px/28px Century Gothic,sans-serif">{ic}</div>'
              f'<div style="font-size:12.5px;line-height:1.2;margin-top:5px;color:{"#1d2a24" if i <= etkin else "#7a8580"};font-weight:{700 if i == etkin else 400}">{ad}</div></div>')
    return ILERLEME.replace("{adimlar}", h).replace("{dolu}", str(round(82 * min(etkin, 4) / 4)))


TEMSILCI = """<div style="display:flex;align-items:center;gap:12px;margin:10px 0 4px;padding:10px;border-radius:14px;background:rgba(255,255,255,.12)">
 <img src="assets/temsilci/onur-kaya.jpg" alt="" style="width:52px;height:52px;border-radius:50%;object-fit:cover;border:2px solid #fff">
 <div style="line-height:1.3"><b style="font-size:17px">Onur Kaya</b><br><span style="font-size:14px;opacity:.9">Eminevim temsilcisi · Sicil 48213</span></div></div>"""


def kaydet(page, ad, boyut):
    page.set_viewport_size(boyut)
    page.wait_for_timeout(600)
    yol = GECICI / f"{ad}.png"
    page.screenshot(path=str(yol), animations="disabled")
    return yol


def cift(page, ad, boyut, uygula):
    """Şimdi → öneriyi uygula → Öneri → geri al."""
    once = kaydet(page, ad + "-simdi", boyut)
    page.evaluate(YARDIMCI)
    try:
        page.evaluate(uygula)
        sonra = kaydet(page, ad + "-oneri", boyut)
    finally:
        page.evaluate("window.T && T.temizle()")
    return once, sonra


def birlestir(ad, baslik, maddeler, once, sonra):
    a, b = Image.open(once).convert("RGB"), Image.open(sonra).convert("RGB")
    olcek = 560 / a.height if a.width < a.height else 900 / a.width
    a = a.resize((round(a.width * olcek), round(a.height * olcek)))
    b = b.resize(a.size)
    try:
        f_b = ImageFont.truetype("C:/Windows/Fonts/GOTHICB.TTF", 30)
        f = ImageFont.truetype("C:/Windows/Fonts/GOTHIC.TTF", 21)
    except OSError:
        f_b = f = ImageFont.load_default()
    import textwrap
    maddeler = [s for m in maddeler for s in textwrap.wrap(m, 46, subsequent_indent="   ")]
    pay, ust = 28, 110 + 30 * len(maddeler)
    W = a.width * 2 + pay * 3
    H = ust + 44 + a.height + pay
    c = Image.new("RGB", (W, H), "#f4f6f5")
    d = ImageDraw.Draw(c)
    d.text((pay, 22), baslik, font=f_b, fill="#00724c")
    for i, m in enumerate(maddeler):
        d.text((pay, 74 + 30 * i), m, font=f, fill="#2b3530")
    for x, etiket, renk, im in ((pay, "ŞİMDİ", "#6b7570", a), (pay * 2 + a.width, "ÖNERİ", "#ea803f", b)):
        d.text((x, ust + 6), etiket, font=f_b, fill=renk)
        c.paste(im, (x, ust + 44))
        d.rounded_rectangle((x - 2, ust + 42, x + im.width + 1, ust + 45 + im.height), radius=6, outline="#c9d1cd", width=2)
    yol = CIKTI / f"{ad}.jpg"
    c.save(yol, quality=88)
    return yol


def main():
    if CIKTI.exists():
        shutil.rmtree(CIKTI)
    GECICI.mkdir(parents=True)
    hatalar, sonuc = [], []
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        ctx = browser.new_context(viewport=TELEFON, device_scale_factor=2)
        page = ctx.new_page()
        page.on("pageerror", lambda e: hatalar.append(str(e)))
        page.goto(sg.UYGULAMA)
        page.get_by_role("button", name="Devam et", exact=True).wait_for()

        # 1) Giriş ekranı
        sonuc.append(birlestir("1-giris", "1 · Giriş ekranı", [
            "• Boş kalan alta: uygulamanın ne işe yaradığını anlatan bir cümle ve görsel"],
            *cift(page, "giris", TELEFON, """
              T.ekle('#dc-root .app-root', 'son', `<div style="position:fixed;z-index:5;left:20px;right:20px;bottom:46px;text-align:center">
                <div style="width:96px;height:96px;margin:0 auto 14px;border-radius:24px;background:#e9f0ed;display:flex;align-items:center;justify-content:center">
                <svg width="56" height="56" viewBox="0 0 24 24"><path d="M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z" fill="#00724c"/><circle cx="19" cy="5" r="3" fill="#ea803f"/></svg></div>
                <b style="display:block;font-size:19px;color:#00724c;margin-bottom:6px">Temsilcimiz size gelsin</b>
                <span style="font-size:15px;color:#4d5852;line-height:1.45">Dilediğiniz yerde ve saatte görüşelim. Randevunuzu buradan takip edin, temsilcinizle yazışın.</span></div>`);
            """)))

        # Zeynep: yeni müşteri, randevu iste, SPY kabul eder (senaryo betiğindeki adımlar)
        page.get_by_label("Telefon numaranız", exact=True).fill("0532 001 02 03")
        page.get_by_role("button", name="Devam et", exact=True).click()
        page.get_by_role("button", name="Doğrula", exact=True).click()
        page.get_by_label("Ad", exact=True).fill("Zeynep")
        page.get_by_label("Soyad", exact=True).fill("Arslan")
        page.get_by_role("button", name="Hesabımı oluştur", exact=True).click()
        page.get_by_role("button", name="Atla", exact=True).click()
        page.get_by_role("button", name="Temsilci iste", exact=True).click()
        bekle(page, "app.state.yaOpen")
        app(page, 'app.setState({yaKonum:{lat:40.9923,lng:29.1244,adres:"Atatürk Mah., Ataşehir",bolge:"Ataşehir"}})')
        app(page, "app.yaKonumDevam()")
        page.locator("button", has_text="Bugün").first.click()
        page.get_by_role("button", name=sg.SAAT, exact=True).click()
        page.get_by_role("button", name="Onayla", exact=True).click()
        bekle(page, 'app.state.mTalep && app.state.mTalep.durum==="alindi"')
        app(page, 'clearTimeout(app._yaTimer);app.setState({yaOpen:false,yaKaynak:""})')
        tid = app(page, "app.state.mTalep.id")

        # 6) SPY: yeni çağrı (harita, okunur satırlar, açık ifade)
        sg.spy_ekrani(page, tid)
        page.get_by_role("button", name="Kabul et", exact=True).wait_for()
        sonuc.append(birlestir("6-spy-yeni-cagri", "6 · SPY tableti: yeni çağrı", [
            "• Kabul etmeden önce yer haritada ve uzaklık görünür",
            "• Gün, saat, yer büyük ve koyu; etiketler okunur gri"],
            *cift(page, "spy", TABLET, """
              T.css('.tp-satirlar > div{font-size:16.5px !important;padding:8px 0 !important} .tp-satirlar > div > span{color:#4d5852 !important} .tp-satirlar b{font-size:17px !important} .tp-detay-baslik{font-size:21px !important}');
              const z=15,lat=40.9923,lng=29.1244,n=2**z,X=(lng+180)/360*n,r=lat*Math.PI/180,Y=(1-Math.log(Math.tan(r)+1/Math.cos(r))/Math.PI)/2*n;
              const x0=Math.floor(X)-2,y0=Math.floor(Y)-1;let t='';
              for(let i=0;i<5;i++)for(let j=0;j<3;j++)t+=`<img src="https://tile.openstreetmap.org/${z}/${x0+i}/${y0+j}.png" style="position:absolute;width:256px;height:256px;left:${i*256}px;top:${j*256}px">`;
              const px=(X-x0)*256,py=(Y-y0)*256;
              T.ekle('.tp-iki > .tp-sutun:last-child .tp-satirlar','sonra',`<div style="position:relative;height:190px;border-radius:14px;overflow:hidden;margin:12px 0 4px;border:1px solid var(--line)">
                <div style="position:absolute;left:calc(50% - ${px}px);top:${95-py}px;width:1280px;height:768px">${t}</div>
                <div style="position:absolute;left:50%;top:95px;transform:translate(-50%,-100%);width:26px;height:26px;border-radius:50% 50% 50% 0;rotate:-45deg;background:#ea803f;border:3px solid #fff;box-shadow:0 2px 6px rgba(0,0,0,.3)"></div>
                <div style="position:absolute;left:10px;bottom:10px;background:#fff;border-radius:10px;padding:6px 10px;font-size:14px;font-weight:700;box-shadow:0 1px 4px rgba(0,0,0,.2)">Size 4,2 km · yaklaşık 12 dk</div></div>`);
            """)))

        page.get_by_role("button", name="Kabul et", exact=True).click()
        bekle(page, 'app.state.mTalep.durum==="atandi"')
        app(page, 'app.setState({chatMessages:[atamaMesaji("Zeynep",app.state.mTalep.repId,app.state.mTalep)]})')

        # 2) Randevularım listesi
        sg.musteri_ekrani(page)
        app(page, "app.setState({mSeciliRandevuId:null})")
        page.locator(".m-randevu-row").first.wait_for()
        sonuc.append(birlestir("2-randevularim", "2 · Randevularım listesi", [
            "• Tablo yerine kart: büyük gün ve saat, temsilci fotoğrafı, renkli durum",
            "• Küçük yazılar büyüdü; üstteki küçük durum yazısı kalktı"],
            *cift(page, "liste", TELEFON, ("T.css(" + json.dumps(MUSTERI_YAZI) + ");" + """
              T.gizle('.m-randevu-tablo');
              const sa="SAAT_YER";
              T.ekle('.m-akis','bas',`<div class="m-kart" style="display:flex !important;flex-direction:row !important;gap:14px;align-items:center;text-align:left;border:1px solid var(--line);border-left:6px solid #ea803f;padding:14px">
                <div style="flex:0 0 64px;text-align:center;border-radius:12px;background:#e9f0ed;padding:8px 0;color:#00724c"><b style="display:block;font-size:24px;line-height:1">${new Date().getDate()}</b><span style="font-size:13px">${new Date().toLocaleDateString('tr-TR',{month:'short'})}</span></div>
                <div style="flex:1;min-width:0"><b style="display:block;font-size:19px">${sa}</b>
                <span style="display:flex;align-items:center;gap:7px;margin:4px 0;font-size:15px"><img src="assets/temsilci/onur-kaya.jpg" style="width:24px;height:24px;border-radius:50%;object-fit:cover">Onur Kaya</span>
                <span style="display:inline-block;font-size:13.5px;font-weight:700;color:#a8541f;background:#fdf0e7;border-radius:20px;padding:3px 10px">Saat onayınız bekleniyor</span></div>
                <span style="font-size:26px;color:#9aa5a0">›</span></div>`);
            """).replace("SAAT_YER", "Bugün · " + sg.SAAT))))

        # 3) Randevu detayı
        page.locator(".m-randevu-row").first.click()
        page.get_by_role("button", name="Saati onayla · " + sg.SAAT, exact=True).wait_for()
        sonuc.append(birlestir("3-randevu-detay", "3 · Randevu detayı", [
            "• Üstte 5 adımlı ilerleme çizgisi: müşteri nerede olduğunu görür",
            "• Temsilcinin fotoğrafı ve sicili (kapıya gelecek kişiye güven)",
            "• \"İptal et\" geri planda (yanlışlıkla basılmasın)"],
            *cift(page, "detay", TELEFON, "T.css(" + json.dumps(MUSTERI_YAZI) + ");" + """
              T.css(`.m-actions .m-btn:last-child{background:none !important;border:0 !important;color:#b23b2e !important;text-decoration:underline;box-shadow:none !important}`);
              T.ekle('.m-akis > .m-kart','once',""" + json.dumps(ilerleme(2)) + """);
              const p=[...document.querySelectorAll('.m-durum p')].find(x=>x.textContent.startsWith('Temsilciniz:'));
              T.sinif(p,'tsl-gz'); T.gizle('.tsl-gz');
              T.ekle('.m-durum .m-btn','once',""" + json.dumps(TEMSILCI) + """);
            """)))

        # 4) Görüşmeye hazırlık
        page.get_by_role("button", name="Saati onayla · " + sg.SAAT, exact=True).click()
        page.get_by_role("dialog", name="Görüşmeye hazırlanmamıza yardımcı olun", exact=True).wait_for()
        sonuc.append(birlestir("4-hazirlik", "4 · Görüşmeye hazırlık", [
            "• Açılır listeler yerine dokunulan seçenekler (tek dokunuş, hepsi görünür)",
            "• \"Paylaşmak istemiyorum\" en sonda, ayrı renk"],
            *cift(page, "hazirlik", TELEFON, """
              const dlg=document.querySelector('[role=dialog][aria-label="Görüşmeye hazırlanmamıza yardımcı olun"]');
              dlg.querySelectorAll('select').forEach((s,i)=>{
                const id='tsl-sel-'+i; T.sinif(s,id); T.gizle('.'+id);
                const ops=[...s.options].map(o=>o.text); const pay=ops.filter(t=>!/istemiyorum/i.test(t)), hayir=ops.find(t=>/istemiyorum/i.test(t));
                const sec=i===1?pay[1]:i===2?pay[3]:'';
                const c=t=>`<span style="display:inline-block;margin:0 6px 7px 0;padding:8px 13px;border-radius:20px;font-size:14.5px;border:1.5px solid ${t===sec?'#00724c':'#cfd6d2'};background:${t===sec?'#00724c':'#fff'};color:${t===sec?'#fff':'#26312c'}">${t}</span>`;
                T.ekle('.'+id,'sonra',`<div style="margin:6px 0 4px">${pay.map(c).join('')}${hayir?`<span style="display:inline-block;margin:0 6px 7px 0;padding:8px 13px;border-radius:20px;font-size:14px;color:#6b7570;border:1.5px dashed #cfd6d2">Belirtmek istemiyorum</span>`:''}</div>`);
              });
            """)))
        page.get_by_role("button", name="Kaydet", exact=True).click()

        # SPY yola çıkar → QR → görüşme → özet
        sg.spy_ekrani(page, tid)
        page.get_by_role("button", name="Yola çık · müşteriye bildir", exact=True).click()
        sg.musteri_ekrani(page)
        page.get_by_role("button", name="Kapıda kimliğini doğrula", exact=True).click()
        kod = app(page, "app.state.mTalep.dogrulama.kod")
        app(page, "app.setState({mQrAcik:false})")
        sg.spy_ekrani(page, tid)
        page.get_by_role("button", name="Vardım: müşterinin QR'ını okut", exact=True).click()
        app(page, "app.setState({qrKodGirdi:%s});app.dogrula(true)" % json.dumps(kod))
        bekle(page, 'app.state.mTalep.durum==="gorusmede"')
        app(page, 'app.setState({qrTarama:"",tpOzetNot:"Konut finansmanı ve aylık ödeme seçenekleri konuşuldu."})')
        page.get_by_role("button", name="Görüşmeyi bitir · özeti gönder", exact=True).click()
        bekle(page, 'app.state.mTalep.durum==="tamamlandi"')

        # 7) SPY: boş sağ taraf (seçim yok)
        sg.spy_ekrani(page, None)
        page.wait_for_timeout(300)
        sonuc.append(birlestir("7-spy-bos", "7 · SPY tableti: görüşme seçili değilken", [
            "• Boş sağ taraf yerine sıradaki görüşme ve yola çıkma saati",
            "• Durum etiketleri biraz büyük"],
            *cift(page, "spybos", TABLET, """
              T.css('.tp-hap{font-size:13px !important;padding:4px 10px !important}');
              const bos=T.bul('Ayrıntı için soldan bir görüşme seçin.');
              if(!bos) throw Error('boş metin yok');
              T.gizle('#dc-root .tp-iki > .tp-sutun:last-child > *');
              T.ekle('#dc-root .tp-iki > .tp-sutun:last-child','bas',`<div class="tp-kart" style="padding:18px">
                <div style="font-size:13px;font-weight:700;color:#6b7570;letter-spacing:.04em">SIRADAKİ GÖRÜŞME</div>
                <div style="display:flex;align-items:center;gap:14px;margin:10px 0 12px"><div style="font-size:34px;font-weight:700;color:#00724c">18:00</div>
                <div><b style="font-size:19px">Ayşe K.</b><br><span style="font-size:15px;color:#4d5852">Barbaros Mah., Ataşehir · 12 dk yol</span></div></div>
                <div style="padding:10px 12px;border-radius:12px;background:#fdf0e7;color:#8a4318;font-size:15px">17:45'te yola çıkmanız önerilir</div>
                <div style="display:flex;gap:10px;margin-top:14px"><span class="tp-btn" style="flex:1;text-align:center">Ayrıntıyı aç</span><span class="tp-btn o" style="flex:1;text-align:center">Bugünkü rota</span></div></div>
                <div class="tp-kart" style="padding:16px;margin-top:12px"><div style="font-size:13px;font-weight:700;color:#6b7570;letter-spacing:.04em">BUGÜN</div>
                <div style="display:flex;gap:26px;margin-top:8px;font-size:15px"><span><b style="font-size:26px;color:#00724c">3</b> görüşme</span><span><b style="font-size:26px;color:#ea803f">1</b> kabul bekleyen çağrı</span><span><b style="font-size:26px">2</b> gerçekleşti</span></div></div>`);
            """)))

        # 5) Görüşme özeti
        sg.musteri_ekrani(page)
        page.get_by_role("heading", name="Görüşme özeti", exact=True).wait_for()
        sonuc.append(birlestir("5-gorusme-ozeti", "5 · Görüşme özeti (tutarsızlık düzeltmesi)", [
            "• \"Düzeltme isteyebilirsiniz\" kalktı (düğmesi 11 Kasım'da kaldırılmıştı)",
            "• Personel dili \"Müşterinin değerlendirmesi bekleniyor\" yerine müşteriye yazılmış cümle"],
            *cift(page, "ozet", TELEFON, "T.css(" + json.dumps(MUSTERI_YAZI) + ");" + """
              T.yazi('Özeti inceleyebilir, düzeltme isteyebilirsiniz.','Görüşmenizin özeti aşağıda. Sorunuz olursa temsilcinize Sohbetler\\'den yazabilirsiniz.');
              T.yazi('Müşterinin değerlendirmesi bekleniyor','Değerlendirmenizi bekliyoruz; temsilciniz gerekirse sizi arayacak.');
              T.ekle('.m-akis > .m-kart','once',""" + json.dumps(ilerleme(5)) + """);
            """)))
        browser.close()
    assert not hatalar, hatalar
    shutil.rmtree(GECICI)
    for y in sorted(sonuc):
        print(y.name)


if __name__ == "__main__":
    main()
