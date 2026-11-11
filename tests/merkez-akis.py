"""Merkez (canlı) akışı: müşteri, SPY'ler ve yönetici ayrı tarayıcılarda.
Aynı gün çağrısı uygulaması açık en uygun SPY'ye düşer; ileri tarih puanla atanır; 3 ret yöneticiye düşer;
yönetici atar; web formu çağrısı merkeze gider ve giriş koduyla uygulamada açılır.
Deneme sunucusu (kullanıcının baktığı kopya değil):
  set TY_PORT=8795 & set TY_YOL=deneme & set TY_VERI=<geçici>\\deneme.json & python merkez\\sunucu.py
Playwright + Chrome gerektirir."""
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import datetime, json, re, tempfile, urllib.error, urllib.request
from playwright.sync_api import sync_playwright

KOK = 'http://127.0.0.1:8795/deneme/'
URL = KOK + 'Eminevim%20Saha%20Paneli.dc.html'
OUT = Path(tempfile.gettempdir()) / 'ty-merkez'
OUT.mkdir(exist_ok=True)
SPYLER = json.loads(re.search(r'window\.TY_SPYLER = (\[.*\]);', (Path(__file__).parent.parent / 'spyler.js').read_text(encoding='utf-8'), re.S).group(1))
AKTIF = {s['id'] for s in SPYLER if s['randevuHG'] >= 100 and s['ciroHG'] >= 100}
YARIN = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()


def app(page, code):
    return page.evaluate('''(code)=>{const el=document.getElementById('dc-root');const root=el[Object.keys(el).find(k=>k.startsWith('__reactContainer$'))];const queue=[root],seen=new Set();while(queue.length){const f=queue.shift();if(!f||seen.has(f))continue;seen.add(f);if(f.stateNode?.logic){const app=f.stateNode.logic;return eval(code);}queue.push(f.child,f.sibling,f.alternate);}throw Error('Mounted app missing');}''', code)


def merkez(yol, govde=None):
    istek = urllib.request.Request(KOK + yol, data=json.dumps(govde).encode() if govde is not None else None,
                                   headers={'Content-Type': 'application/json'})
    return json.loads(urllib.request.urlopen(istek).read())


def bekle(page, kosul, sure=8000):
    page.wait_for_function('''(code)=>{const el=document.getElementById('dc-root');const root=el[Object.keys(el).find(k=>k.startsWith('__reactContainer$'))];const queue=[root],seen=new Set();while(queue.length){const f=queue.shift();if(!f||seen.has(f))continue;seen.add(f);if(f.stateNode?.logic){const app=f.stateNode.logic;return !!eval(code);}queue.push(f.child,f.sibling,f.alternate);}return false;}''', arg=kosul, timeout=sure)


def personel(pg, sid=None):
    pg.get_by_role('button', name='Personel Girişi', exact=True).click()
    if sid is None:
        pg.get_by_role('button', name='Yönetici', exact=True).click()
        return bekle(pg, 'app.state.panel==="ask"')
    pg.get_by_label('SPY seçin').select_option(sid)
    ad = next(s['ad'] for s in SPYLER if s['id'] == sid)
    pg.get_by_role('button', name=ad + ' olarak giriş yap', exact=True).click()
    bekle(pg, 'app.state.panel==="spy" && app.state.personelRepId===' + repr(sid))


assert len(SPYLER) == 30 and len(AKTIF) == 22, (len(SPYLER), len(AKTIF))
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

    # Personel girişi: açılır listede 30 SPY; Derya (tablet) ve Onur (telefon) girer → uygulamaları açık
    spy.get_by_role('button', name='Personel Girişi', exact=True).click()
    assert spy.get_by_label('SPY seçin').locator('option').count() == 31
    spy.get_by_role('button', name='Geri', exact=True).click()
    personel(spy, 's2'); personel(spy_diger, 's1')
    spy.screenshot(path=str(OUT / '1-spy-giris.png'))

    # Yeni müşteri: telefon → SMS kodu (testte ekranda dolu) → ad + parola → onaylar
    app(musteri, 'app.setState({girisMod:"kod",kodAdim:1,kodTel:"0555 111 22 33",kodAd:"Deniz Test",kodParola:"test123",kodParola2:"test123"})')
    app(musteri, 'app.kodIleri()'); app(musteri, 'app.kodIleri()')
    bekle(musteri, 'app.state.kodAdim===3')  # merkezde kod yok → uygulamanın kodu
    app(musteri, 'app.kodIleri()')
    app(musteri, 'app.setState({kvkk1:true,kvkk2:true,kvkk3:true})'); app(musteri, 'app.kvkkOnayla()')
    assert app(musteri, 'app.state.customerForm.name') == 'Deniz Test'
    # Aynı gün: Üsküdar sahiline yakın nokta → uygulaması açık en yakın aktif SPY Derya (s2)
    app(musteri, 'app.mTemsilciIste()')
    app(musteri, 'app.setState({yaKonum:{lat:41.0230,lng:29.0200,adres:"Mimar Sinan Mah., Üsküdar",bolge:"Üsküdar"},yaAdim:2,yaGun:"Bugün",yaGunISO:new Date().toLocaleDateString("en-CA"),yaSaat:"23:00"})')
    app(musteri, 'app.yaGonder()')
    bekle(musteri, 'app._canliBilinen && app.state.mTalep && app._canliBilinen[app.state.mTalep.id]')
    kayit = merkez('api/durum?hepsi=1')['kayitlar'][0]
    assert kayit['repId'] == 's2' and kayit['musteri']['ad'] == 'Deniz Test', kayit
    assert kayit['teklif']['bitis'] > 0 and kayit['puan'] and 'km' in kayit['gerekce'], kayit
    assert app(musteri, 'app.state.mTalep.repId') is None, 'Müşteri kabulden önce SPY görmez'
    assert 'SPY' not in musteri.locator('body').inner_text(), 'Müşteri ekranında SPY yazmamalı'

    # Derya'ya bildirim + 2 dk geri sayım + gerekçe; Onur'da görünmez
    bekle(spy, 'Object.values(app.state.tpKayitlar).some(k=>k.musteri&&k.musteri.ad==="Deniz Test")')
    spy.get_by_text('Yeni çağrı: Deniz Test', exact=True).wait_for()
    spy.get_by_text('Kabul için kalan süre', exact=False).wait_for()
    spy.get_by_text('Neden size geldi', exact=True).wait_for()
    spy.screenshot(path=str(OUT / '2-spy-yeni-cagri.png'))
    spy_diger.wait_for_timeout(3000)
    assert app(spy_diger, 'Object.keys(app.state.tpKayitlar).length') == 0, 'Başka SPY çağrıyı görmemeli'

    spy.get_by_role('button', name='Kabul et', exact=True).click()
    bekle(musteri, 'app.state.mTalep.durum==="atandi" && app.state.chatMessages.length>=1')
    assert app(musteri, 'app.state.mTalep.repId') == 's2'
    assert 'Derya Aksoy' in app(musteri, 'app.state.chatMessages[0].text')
    assert merkez('api/durum?hepsi=1')['kayitlar'][0]['teklif']['bitis'] == 0, 'Kabulde süre durmalı'

    # Müşteri saati onaylar ve yazar; SPY görür ve yanıtlar
    app(musteri, 'app.mSaatOnayla()')
    app(musteri, 'app.setState({sohbetTaslak:"Kapı kodu 12, bekliyorum."});app.mSohbetGonder()')
    bekle(spy, 'Object.values(app.state.tpKayitlar)[0].durum==="netlesti" && Object.values(app.state.tpKayitlar)[0].mesajlar.length>=3')
    spy.get_by_placeholder('Müşteriye mesaj yazın', exact=True).fill('Tamam, 23:00 gibi oradayım.')
    spy.get_by_role('button', name='Gönder', exact=True).click()
    bekle(musteri, 'app.state.chatMessages.some(m=>m.text==="Tamam, 23:00 gibi oradayım.")')
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

    # Molada olan SPY'ye çağrı gitmez: Derya molada → aynı gün, uygulaması açık tek aktif SPY Onur (s1)
    app(spy, 'app.tpDurumSec("molada")')
    musteri.wait_for_timeout(500)
    sonuc = merkez('api/cagri', {'kayit': {'id': 'deneme-2', 'tip': 'ziyaret', 'konum': {'lat': 41.0230, 'lng': 29.0200}, 'yer': 'Üsküdar', 'saat': '23:00'},
                                 'musteri': {'ad': 'İkinci Test'}})['sonuc']
    assert sonuc['repId'] == 's1', sonuc['repId']

    # İleri tarih: uygulaması kapalı SPY'ler de aday; yalnız aktif (iki H/G ≥ %100) SPY seçilir.
    # 3 kez devret → yöneticiye düşer; eski SPY artık kabul edemez; yönetici atar (süre işlemez)
    k = merkez('api/cagri', {'kayit': {'id': 'deneme-3', 'tip': 'ziyaret', 'tarih': YARIN, 'saat': '14:00', 'konum': {'lat': 41.0300, 'lng': 29.1500}, 'yer': 'Esenşehir, Ümraniye'},
                             'musteri': {'ad': 'Yarın Test'}})['sonuc']
    ilk = k['repId']
    assert ilk in AKTIF and ilk != 's2', k
    denenen = [ilk]
    for _ in range(3):
        k = merkez('api/aktar', {'id': 'deneme-3', 'repId': ''})['sonuc']
        if k['repId']:
            assert k['repId'] in AKTIF and k['repId'] not in denenen, k
            denenen.append(k['repId'])
    assert k['repId'] is None and k['yonetici'] is True, k
    try:
        merkez('api/kayit', {'kayit': {'id': 'deneme-3', 'durum': 'atandi', 'repId': ilk}})
        raise AssertionError('Devredilen çağrıyı eski SPY kabul edememeli')
    except urllib.error.HTTPError as e:
        assert e.code == 400
    k = merkez('api/aktar', {'id': 'deneme-3', 'repId': 's3'})['sonuc']
    assert k['repId'] == 's3' and not k['yonetici'] and k['gerekce'] == 'Yönetici atadı' and k['teklif']['bitis'] == 0, k

    # Yönetici: tek giriş, Saha Canlı sekmesinde merkezin takip sayfası; yöneticiye düşen bölümü ve 30 SPY
    yonetici = browser.new_context(viewport={'width': 1024, 'height': 1366}).new_page()
    yonetici.on('pageerror', lambda e: errors.append(str(e)))
    yonetici.goto(URL); yonetici.get_by_text('Giriş Yap', exact=True).first.wait_for()
    personel(yonetici)
    cerceve = yonetici.frame_locator('iframe[src^="takip"]')
    cerceve.get_by_text('Yarın Test', exact=True).first.wait_for(timeout=10000)
    cerceve.get_by_text('22 / 30', exact=True).wait_for()
    yonetici.screenshot(path=str(OUT / '5-yonetici-canli.png'))
    yonetici.get_by_role('button', name='Performans').first.click()
    yonetici.get_by_text('Aktif değil', exact=True).first.wait_for()

    # Web formu (merkezdeki kopya): çağrı merkeze gider, giriş kodunu merkez verir; uygulamada kodla açılır
    web_ctx = browser.new_context(viewport={'width': 1440, 'height': 1000})
    web = web_ctx.new_page(); web.on('pageerror', lambda e: errors.append('web: ' + str(e)))
    web.goto(KOK + 'web-basvuru/index.html', wait_until='domcontentloaded')
    web.wait_for_function("document.querySelector('[data-ty-form] input[name=ad]').value.length>0")
    form = web.locator('.tk-desktopForm [data-ty-form]')
    form.locator('[name=temsilci]').check()
    pencere = web.locator('[data-pen=temsilci].acik')
    pencere.locator('[data-ileri]').click(); pencere.locator('[data-ileri]').click()
    form.locator('[type=submit]').click()
    sonuc = web.locator('.tk-desktopForm [data-sonuc]')
    web.wait_for_function("/^\\d{6}$/.test((document.querySelector('.tk-desktopForm [data-sms-kod]')||{}).textContent||'')")
    kod = sonuc.locator('[data-sms-kod]').inner_text().strip()
    link = sonuc.locator('a[data-ty-dis]').first.get_attribute('href')
    rid = parse_qs(urlparse(link).query)['rid'][0]
    wk = next(x for x in merkez('api/durum?hepsi=1')['kayitlar'] if x['id'] == rid)
    assert wk['girisKodu'] == kod and wk['kaynak'] == 'web' and wk['musteri']['ad'] == 'Mehmet Demir', wk
    uyg = web_ctx.new_page(); uyg.set_viewport_size({'width': 393, 'height': 852})
    uyg.on('pageerror', lambda e: errors.append('uyg: ' + str(e)))
    uyg.goto(link + '&native=1', wait_until='domcontentloaded')
    uyg.get_by_label('SMS ile gelen 6 haneli kod').fill(kod); uyg.get_by_role('button', name='Doğrula').click()
    uyg.get_by_label('Parola', exact=True).fill('abc123'); uyg.get_by_label('Parola tekrar').fill('abc123')
    uyg.get_by_role('button', name='Parolayı kaydet ve devam et').click()
    bekle(uyg, 'app.state.mTalep && app.state.mTalep.id===' + repr(rid))
    assert app(uyg, 'app.state.customerForm.name') == 'Mehmet Demir'
    uyg.screenshot(path=str(OUT / '6-web-uygulama.png'))
    assert not errors, errors
    print('Merkez akışı: OK (30 SPY, aynı gün açık SPY, geri sayım + gerekçe, kabul, mesaj, yola çıkış, QR, özet, molada,'
          ' ileri tarih puanı, 3 ret → yönetici, yönetici ataması, yönetici ekranı, web formu → merkez kodu → uygulama)')
    print('Görseller:', OUT)
    browser.close()
