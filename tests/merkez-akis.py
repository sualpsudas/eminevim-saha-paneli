"""Merkez (canlı) akışı: müşteri, SPY'ler ve yönetici ayrı tarayıcılarda.
Hemen çağrı (bugün, 2 saat içinde) uygulaması açık, boşta en yüksek puanlı SPY'ye düşer; ileri tarih puanla atanır;
devredildikçe sıradakine geçer, kimse kalmayınca "kimse almadı" (haritada kırmızı); yönetici Saha Canlı haritasını ve
kompakt performans listesini görür; web formu çağrısı merkeze gider, SMS penceresi açılır, giriş koduyla uygulamada açılır
ve görüşmeye hazırlık penceresi çıkar.
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
IDLER = {s['id'] for s in SPYLER}
SIMDI = datetime.datetime.now().strftime('%H:%M')  # hemen çağrı
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


assert len(SPYLER) == 7 and all(s['randevuHG'] >= 100 and s['ciroHG'] >= 100 for s in SPYLER), len(SPYLER)
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

    # Personel girişi: açılır listede 7 SPY; Derya (tablet) ve Onur (telefon) girer → uygulamaları açık
    spy.get_by_role('button', name='Personel Girişi', exact=True).click()
    assert spy.get_by_label('SPY seçin').locator('option').count() == 8
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
    # Hemen: Üsküdar sahiline yakın nokta → uygulaması açık, en yakın SPY Derya (s2)
    app(musteri, 'app.mTemsilciIste()')
    app(musteri, 'app.setState({yaKonum:{lat:41.0230,lng:29.0200,adres:"Mimar Sinan Mah., Üsküdar",bolge:"Üsküdar"},yaAdim:2,yaGun:"Bugün",yaGunISO:new Date().toLocaleDateString("en-CA"),yaSaat:"' + SIMDI + '"})')
    app(musteri, 'app.yaGonder()')
    bekle(musteri, 'app._canliBilinen && app.state.mTalep && app._canliBilinen[app.state.mTalep.id]')
    kayit = merkez('api/durum?hepsi=1')['kayitlar'][0]
    assert kayit['repId'] == 's2' and kayit['musteri']['ad'] == 'Deniz Test', kayit
    assert kayit['teklif']['bitis'] > 0 and kayit['atamaPuan'] and 'km' in kayit['gerekce'], kayit
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
    spy.get_by_placeholder('Müşteriye mesaj yazın', exact=True).fill('Tamam, birazdan oradayım.')
    spy.get_by_role('button', name='Gönder', exact=True).click()
    bekle(musteri, 'app.state.chatMessages.some(m=>m.text==="Tamam, birazdan oradayım.")')
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

    # Molada olan SPY'ye hemen çağrı gitmez: Derya molada → uygulaması açık tek SPY Onur (s1)
    app(spy, 'app.tpDurumSec("molada")')
    musteri.wait_for_timeout(500)
    sonuc = merkez('api/cagri', {'kayit': {'id': 'deneme-2', 'tip': 'ziyaret', 'konum': {'lat': 41.0230, 'lng': 29.0200}, 'yer': 'Üsküdar', 'saat': SIMDI},
                                 'musteri': {'ad': 'İkinci Test'}})['sonuc']
    assert sonuc['repId'] == 's1', sonuc['repId']

    # İleri tarih: uygulaması kapalı SPY'ler de aday. Devret → sıradaki; 7 SPY de denenince "kimse almadı".
    # Eski SPY artık kabul edemez; Ata/Aktar yok.
    k = merkez('api/cagri', {'kayit': {'id': 'deneme-3', 'tip': 'ziyaret', 'tarih': YARIN, 'saat': '14:00', 'konum': {'lat': 41.0300, 'lng': 29.1500}, 'yer': 'Esenşehir, Ümraniye'},
                             'musteri': {'ad': 'Yarın Test'}})['sonuc']
    ilk = k['repId']
    assert ilk in IDLER and k['atamaPuan'] and 'km' in k['gerekce'] and not k['sahipsiz'], k
    denenen = [ilk]
    for _ in range(10):
        k = merkez('api/aktar', {'id': 'deneme-3', 'repId': ''})['sonuc']
        if not k['repId']:
            break
        assert k['repId'] in IDLER and k['repId'] not in denenen, k
        denenen.append(k['repId'])
    assert k['repId'] is None and k['sahipsiz'] is True and len(denenen) == 7, (k, denenen)
    assert 'yonetici' not in k
    try:
        merkez('api/kayit', {'kayit': {'id': 'deneme-3', 'durum': 'atandi', 'repId': ilk}})
        raise AssertionError('Devredilen çağrıyı eski SPY kabul edememeli')
    except urllib.error.HTTPError as e:
        assert e.code == 400
    durum = merkez('api/durum?hepsi=1')
    assert durum['bugun']['gelen'] == 3 and durum['bugun']['gorusme'] == 1, durum['bugun']
    hal = {s['id']: s['hal'] for s in durum['spyler']}
    assert len(hal) == 7 and hal['s2'] == 'molada' and hal['s1'] == 'bosta', hal

    # Yönetici: Saha Canlı = takip haritası (Gelen Çağrı, Görüşme Sayısı, süzgeçler, kimse almadı); performans kompakt liste
    yonetici = browser.new_context(viewport={'width': 1024, 'height': 1366}).new_page()
    yonetici.on('pageerror', lambda e: errors.append(str(e)))
    yonetici.goto(URL); yonetici.get_by_text('Giriş Yap', exact=True).first.wait_for()
    personel(yonetici)
    cerceve = yonetici.frame_locator('iframe[src^="takip"]')
    cerceve.get_by_text('Gelen Çağrı · bugün', exact=True).wait_for(timeout=10000)
    cerceve.get_by_text('Görüşme Sayısı · bugün', exact=True).wait_for()
    cerceve.get_by_role('button', name='Molada (1)').wait_for()
    cerceve.locator('.cagri-ik').first.wait_for()
    assert cerceve.locator('.spy-ik').count() == 7
    cerceve.get_by_role('button', name='Molada (1)').click()
    yonetici.wait_for_timeout(400)
    assert cerceve.locator('.spy-ik').count() == 1
    assert yonetici.get_by_text('Destek', exact=True).count() == 0
    yonetici.screenshot(path=str(OUT / '5-yonetici-canli.png'))
    yonetici.get_by_role('button', name='Performans').first.click()
    yonetici.get_by_text('Ort. randevu H/G', exact=True).first.wait_for()
    assert yonetici.locator('.py-sat:not(.py-bas)').count() >= 7
    assert yonetici.get_by_text('Aktif değil', exact=True).count() == 0
    yonetici.screenshot(path=str(OUT / '6-yonetici-performans.png'))

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
    smsp = web.locator('.tk-desktopForm [data-sms-pencere]')
    assert 'acik' in smsp.get_attribute('class'), 'SMS penceresi kendiliğinden açılmalı'
    sonuc.get_by_text('Sayın Mehmet Demir, temsilci çağrınız alındı!', exact=True).wait_for()
    assert sonuc.get_by_text('Yeni başvuru').count() == 0 and sonuc.get_by_text('Başarılı!').count() == 0
    web.screenshot(path=str(OUT / '7-web-sms.png'))
    kod = sonuc.locator('[data-sms-kod]').inner_text().strip()
    smsp.locator('[data-sms-kapat]').click()
    assert 'acik' not in smsp.get_attribute('class')
    sonuc.locator('[data-sms-ac]').click()
    assert 'acik' in smsp.get_attribute('class')
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
    # Web'den gelen müşteri: tanıtım geçilince görüşmeye hazırlık penceresi; kaydedilen bilgi merkeze gider
    bekle(uyg, 'app.state.ekBilgiAcik || app.state.hosgeldinAdim>0')
    if app(uyg, 'app.state.hosgeldinAdim') > 0:
        uyg.get_by_role('button', name='Atla', exact=True).click()
    uyg.get_by_text('Görüşmeye hazırlanmamıza yardımcı olun', exact=True).wait_for()
    uyg.screenshot(path=str(OUT / '8-hazirlik.png'))
    uyg.get_by_label('Ne için düşünüyorsunuz').select_option('Konut')
    uyg.get_by_role('button', name='Kaydet', exact=True).click()
    for _ in range(20):
        wk = next(x for x in merkez('api/durum?hepsi=1')['kayitlar'] if x['id'] == rid)
        if (wk.get('ekBilgi') or {}).get('neIcin') == 'Konut':
            break
        uyg.wait_for_timeout(300)
    assert (wk.get('ekBilgi') or {}).get('neIcin') == 'Konut', wk.get('ekBilgi')
    assert not errors, errors
    print('Merkez akışı: OK (7 SPY, hemen çağrı açık SPY, geri sayım + gerekçe, kabul, mesaj, yola çıkış, QR, özet, molada,'
          ' ileri tarih puanı, devret → kimse almadı, Saha Canlı haritası + süzgeç, kompakt performans,'
          ' web formu → SMS penceresi → merkez kodu → uygulama → görüşmeye hazırlık)')
    print('Görseller:', OUT)
    browser.close()
