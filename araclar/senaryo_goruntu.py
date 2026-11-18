"""Panel senaryoları için gerçek ekran görüntüleri (2026-11-18).

Gerçek uygulamayı (gösteri kipi) ve gerçek web formunu açar, her adımı gerçekten yapar ve müşteri (telefon) ile
SPY (tablet) ekranının görüntüsünü alır. Çıktı: senaryo/goruntu/*.jpg + senaryo/adimlar.js (panel.html okur).
Akış veya ekran değişince yeniden çalıştırın; bir adım yapılamazsa betik hata verip durur (eski görüntü sessizce kalmaz).

Çalıştırma (proje klasöründe, yerel sunucu açıkken: python -m http.server 8799; conda scrapling + Playwright Chrome):
    python araclar/senaryo_goruntu.py
"""
import json
import re
import shutil
from datetime import date, datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

KOK = Path(__file__).resolve().parent.parent
CIKTI = KOK / "senaryo" / "goruntu"
ADRES = "http://127.0.0.1:8799/"
UYGULAMA = ADRES + "Eminevim%20Saha%20Paneli.dc.html?native=1"
WEB = ADRES + "web-basvuru/index.html"
TELEFON = {"width": 393, "height": 852}
TABLET = {"width": 1180, "height": 820}
BUGUN = date.today().isoformat()
# SPY yalnız görüşme günü yola çıkabildiği için uygulama senaryosunda gün "Bugün"; geçmemiş bir saat seçilir
SAAT = "%02d:00" % max(12, min(20, datetime.now().hour + 2))

BUL = "const el=document.getElementById('dc-root');const root=el[Object.keys(el).find(k=>k.startsWith('__reactContainer$'))];const queue=[root],seen=new Set();while(queue.length){const f=queue.shift();if(!f||seen.has(f))continue;seen.add(f);if(f.stateNode?.logic){const app=f.stateNode.logic;return eval(code);}queue.push(f.child,f.sibling,f.alternate);}"


def app(page, code):
    return page.evaluate("(code)=>{" + BUL + "throw Error('Mounted app missing');}", code)


def bekle(page, kosul, sure=8000):
    page.wait_for_function("(code)=>{try{" + BUL + "}catch(e){}return false;}", arg="!!(" + kosul + ")", timeout=sure)


class Senaryo:
    def __init__(self, kod):
        self.kod, self.adimlar, self.sayac = kod, [], 0
        self.son = {"m": "", "p": ""}

    def goruntu(self, page, yan, boyut):
        """Ekranı verilen boyutta çeker; dosya adını döner."""
        self.sayac += 1
        ad = f"{self.kod}-{self.sayac:02d}-{yan}.jpg"
        page.set_viewport_size(boyut)
        page.wait_for_timeout(700)
        page.screenshot(path=str(CIKTI / ad), type="jpeg", quality=82, animations="disabled")
        self.son[yan] = ad
        return ad

    def adim(self, kim, baslik, metin, m="", p=""):
        """kim: m (müşteri), p (SPY), y (ikisi). m/p verilmezse o yanın son görüntüsü kalır."""
        m, p = m or self.son["m"], p or self.son["p"]
        assert m and p, (self.kod, baslik)
        self.adimlar.append({"kim": kim, "baslik": baslik, "metin": metin, "m": m, "p": p})


def musteri_ekrani(page):
    app(page, 'clearTimeout(app._bildirimHide);app.setState({panel:"musteri",customerNav:"basvurum",bildirim:null})')


def spy_ekrani(page, secim=None):
    app(page, 'clearTimeout(app._bildirimHide);app.loginRole("spy");app.setState({tpSecim:%s,bildirim:null})' % json.dumps(secim))


def spy_bos(ctx, s):
    """SPY'nin çağrı gelmeden önceki ekranı (ayrı sekmede; müşteri girişini bozmasın)."""
    spy = ctx.new_page()
    spy.goto(UYGULAMA)
    spy.get_by_role("button", name="Devam et", exact=True).wait_for()
    app(spy, 'app.loginRole("spy","s1")')
    s.goruntu(spy, "p", TABLET)
    spy.close()


def kapida_ve_ozet(page, s, tid):
    """Ortak son: SPY yola çıkar → kapıda QR → görüşme → özet (iki senaryoda aynı)."""
    spy_ekrani(page, tid)
    page.get_by_role("button", name="Yola çık · müşteriye bildir", exact=True).wait_for()
    s.goruntu(page, "p", TABLET)
    s.adim("p", "Görüşme günü", "SPY'nin listesinde randevu ve müşterinin paylaştığı bilgiler. Görüşme günü \"Yola çık\"a basar.")

    page.get_by_role("button", name="Yola çık · müşteriye bildir", exact=True).click()
    bekle(page, 'app.state.mTalep.durum==="yolda"')
    s.goruntu(page, "p", TABLET)
    musteri_ekrani(page)
    page.get_by_text("Temsilciniz yolda", exact=True).first.wait_for()
    s.goruntu(page, "m", TELEFON)
    s.adim("y", "SPY yolda", "Müşteri temsilcinin yolda olduğunu ve tahmini varışı görür; SPY haritada rotayı izler.")

    page.get_by_role("button", name="Kapıda kimliğini doğrula", exact=True).click()
    kod = app(page, "app.state.mTalep.dogrulama.kod")
    s.goruntu(page, "m", TELEFON)
    app(page, "app.setState({mQrAcik:false})")
    spy_ekrani(page, tid)
    page.get_by_role("button", name="Vardım: müşterinin QR'ını okut", exact=True).click()
    s.goruntu(page, "p", TABLET)
    s.adim("y", "Kapıda kimlik doğrulama", "Müşteri telefonunda QR'ı açar, SPY tabletiyle okutur (okunmazsa 4 haneli kod).")

    app(page, "app.setState({qrKodGirdi:%s});app.dogrula(true)" % json.dumps(kod))
    bekle(page, 'app.state.mTalep.durum==="gorusmede"')
    app(page, 'app.setState({qrTarama:"",tpOzetNot:"Konut finansmanı ve aylık ödeme seçenekleri konuşuldu."})')
    s.goruntu(page, "p", TABLET)
    musteri_ekrani(page)
    page.get_by_text("Temsilciniz yanınızda", exact=True).first.wait_for()
    s.goruntu(page, "m", TELEFON)
    s.adim("y", "Görüşme", "Kimlik doğrulandı, görüşme başladı. SPY görüşme notunu yazar.")

    spy_ekrani(page, tid)
    page.get_by_role("button", name="Görüşmeyi bitir · özeti gönder", exact=True).click()
    bekle(page, 'app.state.mTalep.durum==="tamamlandi"')
    s.goruntu(page, "p", TABLET)
    musteri_ekrani(page)
    page.get_by_role("heading", name="Görüşme özeti", exact=True).wait_for()
    s.goruntu(page, "m", TELEFON)
    s.adim("p", "Görüşme özeti", "SPY görüşmeyi bitirir; özet müşterinin uygulamasına gelir, müşteri isterse puan verir.")


def senaryo_web(browser, hatalar):
    s = Senaryo("s1")
    ctx = browser.new_context(viewport=TELEFON, device_scale_factor=2)
    spy_bos(ctx, s)
    web = ctx.new_page()
    web.on("pageerror", lambda e: hatalar.append("s1 web: " + str(e)))
    web.goto(WEB, wait_until="domcontentloaded")
    web.wait_for_function("document.querySelector('[data-ty-form] input[name=ad]').value.length>0")
    web.locator(".tk-mobilFormYeniCover [data-bs-toggle]").click()
    kap = web.locator(".ty-mobil")
    form = kap.locator("[data-ty-form]")
    form.locator("[name=ad]").fill("Can")
    form.locator("[name=soyad]").fill("Aydın")
    web.wait_for_timeout(600)
    s.goruntu(web, "m", TELEFON)
    s.adim("m", "Müşteri web formunu doldurur", "Eminevim sitesindeki başvuru formu: ad, soyad, telefon. E-posta istenmez.")

    form.locator("[name=temsilci]").check()
    pen = web.locator("[data-pen=temsilci].acik")
    pen.wait_for()
    web.wait_for_timeout(1500)  # harita döşemeleri
    s.goruntu(web, "m", TELEFON)
    s.adim("m", "Temsilci çağırma (isteğe bağlı)", "Müşteri temsilci gelsin isterse harita açılır; görüşme yerini seçer.")

    pen.locator("[data-ileri]").click()
    pen.locator("[data-adim='2']").wait_for()
    s.goruntu(web, "m", TELEFON)
    s.adim("m", "Gün ve saat", "Uygun gün ve saati seçer.")

    pen.locator("[data-ileri]").click()
    form.locator("[type=submit]").click()
    sonuc = kap.locator("[data-sonuc]")
    sms = sonuc.locator("[data-sms-pencere]")
    sms.locator("[data-sms-kod]").wait_for()
    web.wait_for_timeout(500)
    m_sms = s.goruntu(web, "m", TELEFON)
    kod = sms.locator("[data-sms-kod]").inner_text().strip()
    sms.locator("[data-sms-kapat]").click()
    link = sonuc.locator("a[data-ty-dis]").first.get_attribute("href")
    assert len(kod) == 6 and link, (kod, link)

    page = ctx.new_page()
    page.on("pageerror", lambda e: hatalar.append("s1 uygulama: " + str(e)))
    page.goto(link + "&native=1", wait_until="domcontentloaded")
    page.get_by_label("SMS ile gelen 6 haneli kod").wait_for()
    page.get_by_label("SMS ile gelen 6 haneli kod").fill(kod)
    m_kod = s.goruntu(page, "m", TELEFON)
    page.get_by_role("button", name="Doğrula", exact=True).click()
    bekle(page, "app.state.mTalep")
    # Web çağrısı SPY'ye kabul bekleyen yeni çağrı olarak düşer (canlı merkezdeki gibi); gösteri kipi bunu hemen atadığı için geri alınır
    app(page, 'app.mKayitYaz({...app.state.mTalep,durum:"alindi",repId:null,kaynak:"web"});app.setState({chatMessages:[]})')
    tid = app(page, "app.state.mTalep.id")
    spy_ekrani(page, tid)
    page.get_by_role("button", name="Kabul et", exact=True).wait_for()
    p_yeni = s.goruntu(page, "p", TABLET)
    s.adim("y", "Çağrı alındı, SMS gider", "Müşteri teşekkür ekranını ve SMS'i görür (uygulama bağlantısı ve giriş kodu). Çağrı SPY'nin tabletine düşer.", m=m_sms, p=p_yeni)

    page.get_by_role("button", name="Kabul et", exact=True).click()
    bekle(page, 'app.state.mTalep.durum==="atandi"')
    app(page, 'app.setState({chatMessages:[atamaMesaji("Can",app.state.mTalep.repId,app.state.mTalep)]})')
    s.goruntu(page, "p", TABLET)
    s.adim("p", "SPY çağrıyı kabul eder", "Çağrı SPY'nin listesinde \"Bekleyen\" olur; müşteriye temsilcinin adı ve mesajı gider.", m=m_sms)

    s.adim("m", "Müşteri SMS'teki bağlantıyı açar", "Uygulama SMS koduyla açılır; ad, soyad ve randevu formdan gelir, yeniden sorulmaz.", m=m_kod)

    musteri_ekrani(page)
    page.get_by_role("button", name="Atla", exact=True).wait_for()
    s.goruntu(page, "m", TELEFON)
    s.adim("m", "Hoş geldiniz", "Kısa tanıtım açılır; müşteri geçebilir.")

    page.get_by_role("button", name="Atla", exact=True).click()
    page.get_by_role("dialog", name="Görüşmeye hazırlanmamıza yardımcı olun", exact=True).wait_for()
    page.get_by_label("Çalışma durumu", exact=True).select_option(index=1)
    page.get_by_label("Yaş aralığı", exact=True).select_option(index=2)
    s.goruntu(page, "m", TELEFON)
    s.adim("m", "Görüşmeye hazırlık", "İsteğe bağlı birkaç soru; müşteri \"Şimdi değil\" de diyebilir.")

    page.get_by_role("button", name="Kaydet", exact=True).click()
    page.locator(".m-randevu-row").first.click()
    onay = page.get_by_role("button", name=re.compile("^Saati onayla"))
    onay.wait_for()
    s.goruntu(page, "m", TELEFON)
    s.adim("m", "Randevularım", "Temsilcinin adı ve mesajı gelmiştir. Müşteri saati onaylar.")

    onay.click()
    bekle(page, 'app.state.mTalep.durum==="netlesti"')
    page.wait_for_timeout(400)
    s.goruntu(page, "m", TELEFON)
    s.adim("m", "Randevu kesinleşti", "Müşterinin paylaştığı bilgiler temsilciye gider.")

    # Görüşme günü geldi (SPY yalnız o gün yola çıkabilir)
    app(page, 'app.mKayitYaz({...app.state.mTalep,tarih:%s,gunYazi:"Bugün"})' % json.dumps(BUGUN))
    kapida_ve_ozet(page, s, tid)
    ctx.close()
    return s


def senaryo_uygulama(browser, hatalar):
    s = Senaryo("s2")
    ctx = browser.new_context(viewport=TELEFON, device_scale_factor=2)
    spy_bos(ctx, s)
    page = ctx.new_page()
    page.on("pageerror", lambda e: hatalar.append("s2: " + str(e)))
    page.goto(UYGULAMA)
    page.get_by_role("button", name="Devam et", exact=True).wait_for()
    page.get_by_label("Telefon numaranız", exact=True).fill("0532 001 02 03")
    s.goruntu(page, "m", TELEFON)
    s.adim("m", "Müşteri uygulamayı açar", "Yalnız telefon numarasını yazar. Parola yok.")

    page.get_by_role("button", name="Devam et", exact=True).click()
    page.get_by_label("SMS ile gelen 6 haneli kod").wait_for()
    s.goruntu(page, "m", TELEFON)
    s.adim("m", "SMS kodu", "Telefonuna gelen 6 haneli kodu girer (gösteride kod kendiliğinden dolar).")

    page.get_by_role("button", name="Doğrula", exact=True).click()
    page.get_by_label("Soyad", exact=True).wait_for()
    page.get_by_label("Ad", exact=True).fill("Zeynep")
    page.get_by_label("Soyad", exact=True).fill("Arslan")
    s.goruntu(page, "m", TELEFON)
    s.adim("m", "İlk kez gelen müşteri: ad ve soyad", "Kayıtlı değilse yalnız adı ve soyadı sorulur. Aydınlatma metni gösterilir; ticari ileti izni isteğe bağlıdır.")

    page.get_by_role("button", name="Hesabımı oluştur", exact=True).click()
    page.get_by_role("button", name="Atla", exact=True).wait_for()
    s.goruntu(page, "m", TELEFON)
    s.adim("m", "Hoş geldiniz", "Kısa tanıtım açılır; müşteri geçebilir.")

    page.get_by_role("button", name="Atla", exact=True).click()
    page.get_by_role("button", name="Temsilci iste", exact=True).wait_for()
    s.goruntu(page, "m", TELEFON)
    s.adim("m", "Randevularım", "Henüz randevu yok. Müşteri \"Temsilci iste\"ye basar.")

    page.get_by_role("button", name="Temsilci iste", exact=True).click()
    bekle(page, "app.state.yaOpen")
    page.wait_for_timeout(1500)  # harita döşemeleri
    # Haritada nokta seçimi (harita çerçevesi içindeki dokunuşun sonucu)
    app(page, 'app.setState({yaKonum:{lat:40.9923,lng:29.1244,adres:"Atatürk Mah., Ataşehir",bolge:"Ataşehir"}})')
    s.goruntu(page, "m", TELEFON)
    s.adim("m", "Görüşme yeri", "Haritadan görüşmek istediği yeri seçer.")

    app(page, "app.yaKonumDevam()")
    page.locator("button", has_text="Bugün").first.click()
    page.get_by_role("button", name=SAAT, exact=True).click()
    s.goruntu(page, "m", TELEFON)
    s.adim("m", "Gün ve saat", "Uygun gün ve saati seçer.")

    page.get_by_role("button", name="Onayla", exact=True).click()
    bekle(page, 'app.state.mTalep && app.state.mTalep.durum==="alindi"')
    app(page, "clearTimeout(app._yaTimer)")  # gösteri kipi 2 sn sonra kendisi atıyor; SPY kabulü canlı akıştaki gibi elle
    app(page, 'app.setState({yaOpen:false,yaKaynak:""})')
    s.goruntu(page, "m", TELEFON)
    tid = app(page, "app.state.mTalep.id")
    spy_ekrani(page, tid)
    page.get_by_role("button", name="Kabul et", exact=True).wait_for()
    s.goruntu(page, "p", TABLET)
    s.adim("y", "Çağrı SPY'ye düşer", "Müşterinin ekranında \"Randevu bekliyor\". SPY'nin tabletinde yeni çağrı: yer, gün, saat.")

    page.get_by_role("button", name="Kabul et", exact=True).click()
    bekle(page, 'app.state.mTalep.durum==="atandi"')
    app(page, 'app.setState({chatMessages:[atamaMesaji("Zeynep",app.state.mTalep.repId,app.state.mTalep)]})')
    s.goruntu(page, "p", TABLET)
    musteri_ekrani(page)
    page.locator(".m-randevu-row").first.click()
    onay = page.get_by_role("button", name="Saati onayla · " + SAAT, exact=True)
    onay.wait_for()
    s.goruntu(page, "m", TELEFON)
    s.adim("p", "SPY çağrıyı kabul eder", "Müşteriye temsilcinin adı ve mesajı gider; müşteri saati onaylayabilir.")

    onay.click()
    page.get_by_role("dialog", name="Görüşmeye hazırlanmamıza yardımcı olun", exact=True).wait_for()
    page.get_by_label("Çalışma durumu", exact=True).select_option(label="Emekli")
    page.get_by_label("Yaş aralığı", exact=True).select_option(label="65 ve üzeri")
    s.goruntu(page, "m", TELEFON)
    s.adim("m", "Müşteri saati onaylar", "Görüşmeye hazırlık için birkaç isteğe bağlı soru açılır.")

    page.get_by_role("button", name="Kaydet", exact=True).click()
    page.wait_for_timeout(500)
    s.goruntu(page, "m", TELEFON)
    s.adim("m", "Randevu kesinleşti", "Müşterinin paylaştığı bilgiler temsilciye gider.")
    kapida_ve_ozet(page, s, tid)
    ctx.close()
    return s


def main():
    if CIKTI.exists():
        shutil.rmtree(CIKTI)
    CIKTI.mkdir(parents=True)
    hatalar = []
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        senaryolar = {"web": senaryo_web(browser, hatalar), "uygulama": senaryo_uygulama(browser, hatalar)}
        browser.close()
    assert not hatalar, hatalar
    veri = {k: v.adimlar for k, v in senaryolar.items()}
    (KOK / "senaryo" / "adimlar.js").write_text(
        "// araclar/senaryo_goruntu.py üretir; elle düzenlenmez\nwindow.SENARYO_SURUM = \"" + datetime.now().strftime("%Y%m%d%H%M")
        + "\";\nwindow.SENARYO = " + json.dumps(veri, ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8")
    # Panel yeni adım dosyasını önbellekten değil yeniden alsın
    panel = KOK / "panel.html"
    panel.write_text(re.sub(r"senaryo/adimlar\.js\?v=\w+", "senaryo/adimlar.js?v=" + datetime.now().strftime("%Y%m%d%H%M"),
                            panel.read_text(encoding="utf-8")), encoding="utf-8")
    for k, v in veri.items():
        print(k, len(v), "adım")


if __name__ == "__main__":
    main()
