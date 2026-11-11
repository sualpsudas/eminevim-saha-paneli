"""Merkez (canlı) akışı: müşteri ve SPY ayrı tarayıcılarda; çağrı en yakın SPY'ye düşer, mesajlar iki yöne gider.
Deneme sunucusu (kullanıcının baktığı kopya değil):
  set TY_PORT=8795 & set TY_YOL=deneme & set TY_VERI=<geçici>\\deneme.json & python merkez\\sunucu.py
Playwright + Chrome gerektirir."""
from pathlib import Path
import json, tempfile, urllib.request
from playwright.sync_api import sync_playwright

KOK = 'http://127.0.0.1:8795/deneme/'
URL = KOK + 'Eminevim%20Saha%20Paneli.dc.html'
OUT = Path(tempfile.gettempdir()) / 'ty-merkez'
OUT.mkdir(exist_ok=True)


def app(page, code):
    return page.evaluate('''(code)=>{const el=document.getElementById('dc-root');const root=el[Object.keys(el).find(k=>k.startsWith('__reactContainer$'))];const queue=[root],seen=new Set();while(queue.length){const f=queue.shift();if(!f||seen.has(f))continue;seen.add(f);if(f.stateNode?.logic){const app=f.stateNode.logic;return eval(code);}queue.push(f.child,f.sibling,f.alternate);}throw Error('Mounted app missing');}''', code)


def merkez(yol, govde=None):
    istek = urllib.request.Request(KOK + yol, data=json.dumps(govde).encode() if govde is not None else None,
                                   headers={'Content-Type': 'application/json'})
    return json.loads(urllib.request.urlopen(istek).read())


def bekle(page, kosul, sure=8000):
    page.wait_for_function('''(code)=>{const el=document.getElementById('dc-root');const root=el[Object.keys(el).find(k=>k.startsWith('__reactContainer$'))];const queue=[root],seen=new Set();while(queue.length){const f=queue.shift();if(!f||seen.has(f))continue;seen.add(f);if(f.stateNode?.logic){const app=f.stateNode.logic;return !!eval(code);}queue.push(f.child,f.sibling,f.alternate);}return false;}''', arg=kosul, timeout=sure)


merkez('api/sifirla', {'onay': 'evet'})
with sync_playwright() as p:
    browser = p.chromium.launch(channel='chrome', headless=True)
    errors = []
    musteri = browser.new_context(viewport={'width': 393, 'height': 852}).new_page()
    spy = browser.new_context(viewport={'width': 1180, 'height': 820}).new_page()
    spy_diger = browser.new_context(viewport={'width': 393, 'height': 852}).new_page()
    for pg in (musteri, spy, spy_diger):
        pg.on('pageerror', lambda e: errors.append(str(e)))
        pg.goto(URL)
        pg.get_by_text('Giriş Yap', exact=True).first.wait_for()
    assert musteri.evaluate('window.Canli.aktif') is True

    # SPY'ler personel girişinden kendi adlarıyla girer (biri tablet, biri telefon)
    for pg, ad, sid in ((spy, 'Derya Aksoy', 's2'), (spy_diger, 'Onur Kaya', 's1')):
        pg.get_by_role('button', name='Personel Girişi', exact=True).click()
        pg.get_by_role('button', name=ad + ' olarak giriş yap', exact=True).click()
        bekle(pg, 'app.state.panel==="spy" && app.state.personelRepId===' + repr(sid))
    spy.screenshot(path=str(OUT / '1-spy-giris.png'))

    # Yeni müşteri: telefon → SMS kodu (testte ekranda dolu) → ad + parola → onaylar
    app(musteri, 'app.setState({girisMod:"kod",kodAdim:1,kodTel:"0555 111 22 33",kodAd:"Deniz Test",kodParola:"test123",kodParola2:"test123"})')
    app(musteri, 'app.kodIleri()'); app(musteri, 'app.kodIleri()'); app(musteri, 'app.kodIleri()')
    app(musteri, 'app.setState({kvkk1:true,kvkk2:true,kvkk3:true})'); app(musteri, 'app.kvkkOnayla()')
    assert app(musteri, 'app.state.customerForm.name') == 'Deniz Test'
    # SPY iste: haritada Üsküdar sahiline yakın nokta → en yakın Derya Aksoy (s2)
    app(musteri, 'app.mTemsilciIste()')
    app(musteri, 'app.setState({yaKonum:{lat:41.0230,lng:29.0200,adres:"Mimar Sinan Mah., Üsküdar",bolge:"Üsküdar"},yaAdim:2,yaGun:"Bugün",yaGunISO:new Date().toLocaleDateString("en-CA"),yaSaat:"18:00"})')
    app(musteri, 'app.yaGonder()')
    bekle(musteri, 'app._canliBilinen && app.state.mTalep && app._canliBilinen[app.state.mTalep.id]')
    kayit = merkez('api/durum?hepsi=1')['kayitlar'][0]
    assert kayit['repId'] == 's2' and kayit['musteri']['ad'] == 'Deniz Test', kayit
    assert app(musteri, 'app.state.mTalep.repId') is None, 'Müşteri kabulden önce SPY görmez'

    # Derya'ya bildirim + liste; Onur'da görünmez
    bekle(spy, 'Object.values(app.state.tpKayitlar).some(k=>k.musteri&&k.musteri.ad==="Deniz Test")')
    spy.get_by_text('Yeni çağrı: Deniz Test', exact=True).wait_for()
    spy.screenshot(path=str(OUT / '2-spy-yeni-cagri.png'))
    spy_diger.wait_for_timeout(3000)
    assert app(spy_diger, 'Object.keys(app.state.tpKayitlar).length') == 0, 'Başka SPY çağrıyı görmemeli'

    spy.get_by_role('button', name='Kabul et', exact=True).click()
    bekle(musteri, 'app.state.mTalep.durum==="atandi" && app.state.chatMessages.length>=1')
    assert app(musteri, 'app.state.mTalep.repId') == 's2'
    assert 'Derya Aksoy' in app(musteri, 'app.state.chatMessages[0].text')

    # Müşteri saati onaylar ve yazar; SPY görür ve yanıtlar
    app(musteri, 'app.mSaatOnayla()')
    app(musteri, 'app.setState({sohbetTaslak:"Kapı kodu 12, bekliyorum."});app.mSohbetGonder()')
    bekle(spy, 'Object.values(app.state.tpKayitlar)[0].durum==="netlesti" && Object.values(app.state.tpKayitlar)[0].mesajlar.length>=3')
    spy.get_by_placeholder('Müşteriye mesaj yazın', exact=True).fill('Tamam, 18:00 gibi oradayım.')
    spy.get_by_role('button', name='Gönder', exact=True).click()
    bekle(musteri, 'app.state.chatMessages.some(m=>m.text==="Tamam, 18:00 gibi oradayım.")')
    spy.screenshot(path=str(OUT / '3-spy-sohbet.png'))

    # Yola çık → müşteri "yolda"; QR kodu müşteri ekranında, SPY kodu girer → görüşmede → bitir
    spy.get_by_role('button', name='Yola çık · müşteriye bildir', exact=True).click()
    bekle(musteri, 'app.state.mTalep.durum==="yolda"')
    app(musteri, 'app.setState({customerNav:"basvurum",mSeciliRandevuId:app.state.mTalep.id});app.mQrHazirla(false)')
    bekle(spy, 'Object.values(app.state.tpKayitlar)[0].dogrulama')
    kod = app(musteri, 'app.state.mTalep.dogrulama.kod')
    spy.get_by_role('button', name="Vardım: müşterinin QR'ını okut", exact=True).click()
    app(spy, 'app.setState({qrKodGirdi:' + repr(kod) + '});app.dogrula(true)')
    bekle(musteri, 'app.state.mTalep.durum==="gorusmede"')
    app(spy, 'app.setState({qrTarama:"",tpOzetNot:"Plan seçenekleri görüşüldü."})')
    spy.get_by_role('button', name='Görüşmeyi bitir · özeti gönder', exact=True).click()
    bekle(musteri, 'app.state.mTalep.durum==="tamamlandi"')
    musteri.screenshot(path=str(OUT / '4-musteri-ozet.png'))

    # Molada olan SPY'ye çağrı gitmez: Derya molada → aynı nokta Selin'e (s4)
    app(spy, 'app.tpDurumSec("molada")')
    musteri.wait_for_timeout(500)
    sonuc = merkez('api/cagri', {'kayit': {'id': 'deneme-2', 'tip': 'ziyaret', 'konum': {'lat': 41.0230, 'lng': 29.0200}, 'yer': 'Üsküdar'},
                                 'musteri': {'ad': 'İkinci Test'}})['sonuc']
    assert sonuc['repId'] == 's4', sonuc['repId']
    assert not errors, errors
    print('Merkez akışı: OK (atama, bildirim, kabul, mesaj, yola çıkış, QR, özet, molada)')
    print('Görseller:', OUT)
    browser.close()
