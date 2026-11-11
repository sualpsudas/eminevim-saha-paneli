"""Merkez (canlı) akışı: müşteri, SPY'ler ve yönetici ayrı tarayıcılarda.
Hemen çağrı (bugün, 2 saat içinde) boşta en yüksek puanlı SPY'ye düşer (uygulaması kapalı da olabilir: bildirim gider);
bildirim o SPY'yi seçmiş tüm telefonlara gider (sahte bildirim sunucusuyla); ileri tarih puanla atanır;
devredildikçe sıradakine geçer, kimse kalmayınca "kimse almadı" (haritada kırmızı); yönetici Saha Canlı haritasını ve
kompakt performans listesini görür; web formu çağrısı merkeze gider, SMS penceresi açılır, giriş koduyla uygulamada açılır
ve görüşmeye hazırlık penceresi çıkar.
Deneme sunucusu (kullanıcının baktığı kopya değil):
  set TY_PORT=8795 & set TY_YOL=deneme & set TY_VERI=<geçici>\\deneme.json & python merkez\\sunucu.py
Playwright + Chrome gerektirir."""
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import base64, datetime, json, os, re, tempfile, threading, time, urllib.error, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
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


# Sahte bildirim servisi (Google/Apple yerine): merkezin gönderdiği şifreli bildirimleri yakalar; /gone → 410 (telefon aboneliği bırakmış)
GELEN = []
class SahtePush(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass
    def do_POST(self):
        govde = self.rfile.read(int(self.headers.get('Content-Length') or 0))
        GELEN.append({'yol': self.path, 'basliklar': {k.lower(): v for k, v in self.headers.items()}, 'boy': len(govde)})
        self.send_response(410 if self.path == '/gone' else 201); self.end_headers()
push_sunucu = ThreadingHTTPServer(('127.0.0.1', 0), SahtePush)
threading.Thread(target=push_sunucu.serve_forever, daemon=True).start()
PUSH = f'http://127.0.0.1:{push_sunucu.server_address[1]}'


def abonelik(yol):
    acik = ec.generate_private_key(ec.SECP256R1()).public_key().public_bytes(serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint)
    b = lambda x: base64.urlsafe_b64encode(x).decode().rstrip('=')
    return {'endpoint': PUSH + yol, 'keys': {'p256dh': b(acik), 'auth': b(os.urandom(16))}}


def gelen_bekle(yollar, sure=8):
    son = time.time() + sure
    while time.time() < son and not set(yollar) <= {g['yol'] for g in GELEN}:
        time.sleep(0.2)
    return {g['yol'] for g in GELEN}


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
(Path(tempfile.gettempdir()) / 'deneme_abonelik.json').unlink(missing_ok=True)  # bildirim abonelikleri sıfırlamada silinmez; testte temiz başla
with sync_playwright() as p:
    browser = p.chromium.launch(channel='chrome', headless=True)
    errors = []
    musteri = browser.new_context(viewport={'width': 393, 'height': 852}).new_page()
    spy = browser.new_context(viewport={'width': 1180, 'height': 820}).new_page()
    spy_diger = browser.new_context(viewport={'width': 393, 'height': 852}).new_page()
    for pg in (musteri, spy, spy_diger):
        pg.on('pageerror', lambda e: errors.append(str(e)))
        pg.goto(URL)
        pg.get_by_role('button', name='Devam et', exact=True).wait_for()
    assert musteri.evaluate('window.Canli.aktif') is True

    # Personel girişi: açılır listede 7 SPY; Derya (tablet) ve Onur (telefon) girer → uygulamaları açık
    spy.get_by_role('button', name='Personel Girişi', exact=True).click()
    assert spy.get_by_label('SPY seçin').locator('option').count() == 8
    spy.get_by_role('button', name='Geri', exact=True).click()
    personel(spy, 's2'); personel(spy_diger, 's1')
    spy.screenshot(path=str(OUT / '1-spy-giris.png'))
    # Bildirim abonelikleri: Derya iki telefonda (t1, t2), Selin bir telefonda (t3) + aboneliği bırakmış bir telefon (/gone)
    assert merkez('api/anahtar')['anahtar'], 'Merkez bildirim anahtarı yok (pywebpush kurulu mu?)'
    ab = {y: abonelik(y) for y in ('/t1', '/t2', '/t3', '/gone')}
    for y, sid in (('/t1', 's2'), ('/t2', 's2'), ('/t3', 's4'), ('/gone', 's4')):
        merkez('api/abone', {'spy': sid, 'abonelik': ab[y], 'cihaz': 'test'})
    try:
        merkez('api/abone', {'spy': 's2', 'abonelik': {**ab['/t1'], 'endpoint': 'http://ornek.com/x'}})
        raise AssertionError('Yalnız https bildirim adresi kabul edilmeli')
    except urllib.error.HTTPError as e:
        assert e.code == 400

    # Yeni müşteri: gerçek ekran adımlarıyla kod, ad/parola ve KVKK.
    musteri.get_by_label('Telefon numaranız',exact=True).fill('0555 111 22 33')
    musteri.get_by_role('button',name='Devam et',exact=True).click()
    musteri.get_by_label('SMS ile gelen 6 haneli kod').wait_for()
    musteri.get_by_role('button',name='Doğrula',exact=True).click()
    musteri.get_by_label('Ad Soyad',exact=True).fill('Deniz Test')
    musteri.get_by_label('Parola',exact=True).fill('test123')
    musteri.get_by_label('Parola tekrar',exact=True).fill('test123')
    musteri.get_by_role('button',name='Parolayı kaydet ve devam et',exact=True).click()
    musteri.get_by_role('checkbox',name='Aydınlatma Metni',exact=False).check()
    musteri.get_by_role('button',name='Onaylıyorum',exact=True).click()
    bekle(musteri, 'app.state.girisYapildi')
    assert app(musteri, 'app.state.customerForm.name') == 'Deniz Test'
    # Müşteri bildirimi: girişten sonra Randevularım'da "Bildirimleri açın" kartı; abonelik yalnız girişte verilen jetonla
    musteri.get_by_text('Bildirimleri açın', exact=True).wait_for()
    ab['/m1'] = abonelik('/m1')
    try:
        merkez('api/abone', {'musteri': '5551112233', 'jeton': 'uydurma', 'abonelik': ab['/m1']})
        raise AssertionError('Jetonsuz müşteri aboneliği kabul edilmemeli')
    except urllib.error.HTTPError as e:
        assert e.code == 400
    merkez('api/abone', {'musteri': '5551112233', 'jeton': app(musteri, 'app._musteriBildirim.jeton'), 'abonelik': ab['/m1'], 'cihaz': 'test'})
    def musteriye(n):
        son = time.time() + 8
        while time.time() < son and sum(g['yol'] == '/m1' for g in GELEN) < n:
            time.sleep(0.2)
        return sum(g['yol'] == '/m1' for g in GELEN)
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
    # Bildirim Derya'nın iki telefonuna gitti, Selin'inkine gitmedi; Web Push biçiminde (VAPID imzalı, şifreli)
    gelen = gelen_bekle(['/t1', '/t2'])
    assert {'/t1', '/t2'} <= gelen and '/t3' not in gelen, gelen
    b = next(g for g in GELEN if g['yol'] == '/t1')
    assert b['basliklar'].get('authorization', '').startswith('vapid t=') and b['basliklar'].get('content-encoding') == 'aes128gcm' and b['boy'] > 0, b
    assert b['basliklar'].get('ttl') == '120' and b['basliklar'].get('urgency') == 'high', b

    # Derya'ya bildirim + 2 dk geri sayım; Onur'da görünmez
    bekle(spy, 'Object.values(app.state.tpKayitlar).some(k=>k.musteri&&k.musteri.ad==="Deniz Test")')
    spy.get_by_text('Yeni çağrı: Deniz Test', exact=True).wait_for()
    spy.get_by_text('Kabul için kalan süre', exact=False).wait_for()
    assert spy.get_by_text('Neden size geldi', exact=True).count() == 0, 'Gerekçe satırı kaldırıldı'
    spy.screenshot(path=str(OUT / '2-spy-yeni-cagri.png'))
    spy_diger.wait_for_timeout(3000)
    assert app(spy_diger, 'Object.keys(app.state.tpKayitlar).length') == 0, 'Başka SPY çağrıyı görmemeli'

    spy.get_by_role('button', name='Kabul et', exact=True).click()
    bekle(musteri, 'app.state.mTalep.durum==="atandi" && app.state.chatMessages.length>=1')
    assert app(musteri, 'app.state.mTalep.repId') == 's2'
    assert 'Derya Aksoy' in app(musteri, 'app.state.chatMessages[0].text')
    assert merkez('api/durum?hepsi=1')['kayitlar'][0]['teklif']['bitis'] == 0, 'Kabulde süre durmalı'
    assert musteriye(1) == 1, 'Kabulde tek müşteri bildirimi (temsilciniz belli oldu; hazır mesaj ayrı bildirim üretmez)'

    # Müşteri saati onaylar ve yazar; SPY görür ve yanıtlar
    app(musteri, 'app.mSaatOnayla()')
    app(musteri, 'app.setState({sohbetTaslak:"Kapı kodu 12, bekliyorum."});app.mSohbetGonder()')
    bekle(spy, 'Object.values(app.state.tpKayitlar)[0].durum==="netlesti" && Object.values(app.state.tpKayitlar)[0].mesajlar.length>=3')
    spy.get_by_placeholder('Müşteriye mesaj yazın', exact=True).fill('Tamam, birazdan oradayım.')
    spy.get_by_role('button', name='Gönder', exact=True).click()
    bekle(musteri, 'app.state.chatMessages.some(m=>m.text==="Tamam, birazdan oradayım.")')
    spy.screenshot(path=str(OUT / '3-spy-sohbet.png'))
    assert musteriye(2) == 2, 'SPY mesajında müşteriye bildirim (müşterinin kendi mesajında değil)'

    # Yola çık → müşteri "yolda"; QR kodu müşteri ekranında, SPY kodu girer → görüşmede → bitir
    spy.get_by_role('button', name='Yola çık · müşteriye bildir', exact=True).click()
    bekle(musteri, 'app.state.mTalep.durum==="yolda"')
    assert musteriye(3) == 3, 'Yola çıkışta müşteriye bildirim'
    # Bildirime dokunma: ilgili randevu açılır; Ayarlar'da Bildirimler kartı
    app(musteri, 'app.setState({customerNav:"ayarlar"})')
    musteri.get_by_role('region', name='Bildirimler').wait_for()
    app(musteri, 'app.randevuAc(app.state.mTalep.id)')
    assert app(musteri, 'app.state.customerNav') == 'basvurum' and app(musteri, 'app.state.mSeciliRandevuId') == app(musteri, 'app.state.mTalep.id')
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

    # Molada olan SPY'ye hemen çağrı gitmez: Derya molada → en yakın boştaki Selin (s4); uygulaması kapalı ama bildirim gider.
    # t2 telefonu Selin'i seçti (aynı telefon tek SPY'ye bağlı), t1 çıkış yaptı.
    merkez('api/abone', {'spy': 's4', 'abonelik': ab['/t2'], 'cihaz': 'test'})
    merkez('api/abone-sil', {'endpoint': ab['/t1']['endpoint']})
    GELEN.clear()
    app(spy, 'app.tpDurumSec("molada")')
    musteri.wait_for_timeout(500)
    sonuc = merkez('api/cagri', {'kayit': {'id': 'deneme-2', 'tip': 'ziyaret', 'konum': {'lat': 41.0230, 'lng': 29.0200}, 'yer': 'Üsküdar', 'saat': SIMDI},
                                 'musteri': {'ad': 'İkinci Test'}})['sonuc']
    assert sonuc['repId'] == 's4', sonuc['repId']
    gelen = gelen_bekle(['/t2', '/t3', '/gone'])
    assert {'/t2', '/t3', '/gone'} <= gelen and '/t1' not in gelen, gelen
    time.sleep(0.5)
    bil = {s['id']: s['bildirim'] for s in merkez('api/durum?hepsi=1')['spyler']}
    assert bil['s2'] == 0 and bil['s4'] == 2, bil  # /gone (410) silindi

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
    assert len(hal) == 7 and hal['s2'] == 'molada' and hal['s4'] == 'bosta', hal

    # Yönetici: Saha Canlı = takip haritası (Gelen Çağrı, Görüşme Sayısı, süzgeçler, kimse almadı); performans kompakt liste
    yonetici = browser.new_context(viewport={'width': 1024, 'height': 1366}).new_page()
    yonetici.on('pageerror', lambda e: errors.append(str(e)))
    yonetici.goto(URL); yonetici.get_by_role('button', name='Devam et', exact=True).wait_for()
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
    # Merkez de web çağrısını onaysız kabul etmez.
    try:
        merkez('api/cagri', {'kaynak':'web', 'kayit':{'id':'onaysiz-web','kaynak':'web','konum':{'lat':41.02,'lng':29.02}}})
        raise AssertionError('Onaysız web çağrısı kabul edildi')
    except urllib.error.HTTPError as err:
        assert err.code == 400 and 'konum onayı' in json.loads(err.read())['hata']
    form.locator('[name=temsilci]').check()
    assert web.locator('[data-pen=temsilci].acik').count() == 0
    form.locator('[data-konum-riza] label').click()
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
    assert wk['konumRizaTarih'] == wk['olusma'] and wk['konumRizaTarih'] > 0
    assert wk['girisKodu'] == kod and wk['kaynak'] == 'web' and wk['musteri']['ad'] == 'Mehmet Demir', wk
    uyg = web_ctx.new_page(); uyg.set_viewport_size({'width': 393, 'height': 852})
    uyg.on('pageerror', lambda e: errors.append('uyg: ' + str(e)))
    uyg.goto(link + '&native=1', wait_until='domcontentloaded')
    bekle(uyg, 'app.state.kodAdim===2')
    uyg.get_by_label('SMS ile gelen 6 haneli kod').fill('000000')
    uyg.get_by_role('button', name='Doğrula', exact=True).click()
    uyg.get_by_role('alert').get_by_text('Kod eşleşmedi', exact=False).wait_for()
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

    # Hesap merkezde: A telefonunda açılan hesapla B telefonunda yalnız parolayla girilir; çağrılar da gelir
    def telefon_b():
        pg = browser.new_context(viewport={'width': 393, 'height': 852}).new_page()
        pg.on('pageerror', lambda e: errors.append('b: ' + str(e)))
        pg.goto(URL); pg.get_by_role('button', name='Devam et', exact=True).wait_for()
        return pg
    def numara(pg, tel):
        pg.get_by_label('Telefon numaranız', exact=True).fill(tel)
        pg.get_by_role('button', name='Devam et', exact=True).click()
    b = telefon_b()
    numara(b, '0555 111 22 33')
    b.get_by_text('Parolanızı girin', exact=True).wait_for()
    b.get_by_label('Parola', exact=True).fill('yanlis1')
    b.get_by_role('button', name='Giriş Yap', exact=True).click()
    b.get_by_role('alert').get_by_text('Parola eşleşmedi', exact=False).wait_for()
    b.get_by_label('Parola', exact=True).fill('test123')
    b.get_by_role('button', name='Giriş Yap', exact=True).click()
    bekle(b, 'app.state.girisYapildi && app.state.mTalep')
    assert app(b, 'app.state.customerForm.name') == 'Deniz Test' and app(b, 'app.state.kvkkAsama') is False
    assert app(b, 'app.state.mTalep.durum') == 'tamamlandi' and app(b, 'app.state.chatMessages.length') >= 3
    b.screenshot(path=str(OUT / '9-baska-telefon-giris.png'))
    # Uygulama kapanıp açılınca müşteri girişli kalır (parola sorulmaz), randevular merkezden gelir
    b.reload()
    bekle(b, 'app.state.girisYapildi && app.state.customerForm.name==="Deniz Test" && app.state.mTalep', 10000)
    assert 'test123' not in b.evaluate('JSON.stringify(localStorage)'), 'Parola telefonda saklanmamalı'
    # Web'den gelen müşteri (Mehmet Demir) de başka telefonda parolayla girer, web çağrısı Randevularım'da
    b2 = telefon_b()
    numara(b2, parse_qs(urlparse(link).query)['tel'][0])
    b2.get_by_label('Parola', exact=True).fill('abc123')
    b2.get_by_role('button', name='Giriş Yap', exact=True).click()
    bekle(b2, 'app.state.mTalep && app.state.mTalep.id===' + repr(rid))
    # Çıkış yap → oturum telefonda ve merkezde kapanır; yeniden açınca giriş ekranı
    o = json.loads(b2.evaluate('localStorage.getItem("ty-musteri-oturum")'))
    app(b2, 'app.cikisYap()')
    b2.reload(); b2.get_by_role('button', name='Devam et', exact=True).wait_for()
    b2.wait_for_timeout(1500)
    assert app(b2, 'app.state.girisYapildi') is False and b2.evaluate('localStorage.getItem("ty-musteri-oturum")') is None
    try:
        merkez('api/musteri', {'islem': 'oturum', **o})
        raise AssertionError('Çıkıştan sonra eski oturum geçerli olmamalı')
    except urllib.error.HTTPError as e:
        assert e.code == 400
    # Kayıtlı olmayan numara: parola sorulmaz, SMS kodu → ad/parola → KVKK
    b3 = telefon_b()
    numara(b3, '0555 999 88 77')
    b3.get_by_label('SMS ile gelen 6 haneli kod').wait_for()
    b3.get_by_role('button', name='Doğrula', exact=True).click()
    b3.get_by_label('Ad Soyad', exact=True).wait_for()
    assert merkez('api/musteri', {'islem': 'sorgu', 'tel': '5559998877'})['sonuc']['kayitli'] is False
    # 5 yanlış parola → kısa süreli kilit (doğru parola da geçmez)
    for _ in range(5):
        try:
            merkez('api/musteri', {'islem': 'giris', 'tel': '5551112233', 'parola': 'yanlis'})
        except urllib.error.HTTPError as e:
            assert e.code == 400
    try:
        merkez('api/musteri', {'islem': 'giris', 'tel': '5551112233', 'parola': 'test123'})
        raise AssertionError('Kilitliyken giriş olmamalı')
    except urllib.error.HTTPError as e:
        assert 'Çok fazla hatalı deneme' in json.loads(e.read())['hata']
    assert '"tuz"' not in json.dumps(merkez('api/durum?hepsi=1')), 'Parola özeti dışarı çıkmamalı'

    # Yeni sürüm yayınlanınca açık uygulamada "Yeni sürüm hazır · Yenile" şeridi
    app(b, 'app._uygulamaSurum="eski"')
    b.get_by_role('button', name='Yeni sürüm hazır · Yenile', exact=True).wait_for()

    # Test verisi sıfırlanınca: açık telefonlarda eski kayıtlar silinir, müşteri girişe döner;
    # o sırada kapalı olan telefon da açılınca temizlenir; müşteri bildirim abonelikleri silinir (SPY'ninkiler kalır)
    b2_ctx = b2.context
    assert b2.evaluate('localStorage.getItem("ty-randevu-v1")')
    b2.close()
    merkez('api/sifirla', {'onay': 'evet'})
    bekle(b, '!app.state.girisYapildi && !app.state.mTalep', 10000)
    b.get_by_role('alert').get_by_text('Test verisi sıfırlandı', exact=False).wait_for()
    bekle(spy, 'Object.keys(app.state.tpKayitlar).length===0', 10000)
    b2 = b2_ctx.new_page(); b2.goto(URL); b2.get_by_role('button', name='Devam et', exact=True).wait_for()
    b2.wait_for_function('localStorage.getItem("ty-randevu-v1")===null', timeout=10000)
    abone = json.loads((Path(tempfile.gettempdir()) / 'deneme_abonelik.json').read_text(encoding='utf-8'))
    assert abone and not any(x.get('musteri') for x in abone.values()), abone
    assert merkez('api/musteri', {'islem': 'sorgu', 'tel': '5551112233'})['sonuc']['kayitli'] is False
    assert not errors, errors
    print('Merkez akışı: OK (7 SPY, hemen çağrı, bildirim tüm telefonlara + telefon değişimi + 410 temizliği, geri sayım + gerekçe, kabul, mesaj, yola çıkış, QR, özet, molada,'
          ' ileri tarih puanı, devret → kimse almadı, Saha Canlı haritası + süzgeç, kompakt performans,'
          ' web formu → SMS penceresi → merkez kodu → uygulama → görüşmeye hazırlık,'
          ' merkezdeki hesapla başka telefonda parola girişi + yanlış parola + kilit, kayıtsız numara → SMS kodu,'
          ' müşteri bildirimi: kabul + SPY mesajı + yola çıkış, jetonsuz abonelik reddi, dokununca randevu)')
    print('Görseller:', OUT)
    browser.close()
