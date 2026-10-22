"""Telefon sekmeleri, finansman adımları ve önizleme çerçevesi yerleşim kontrolü.

Yerel 8799 sunucusu ve Playwright + Chrome gerektirir.
"""
from pathlib import Path
import tempfile
from playwright.sync_api import sync_playwright

BASE='http://127.0.0.1:8799/'
OUT=Path(tempfile.gettempdir())/'ty-phone-layout'
OUT.mkdir(exist_ok=True)

def app(page,code):
    return page.evaluate('''(code)=>{const el=document.getElementById('dc-root');const root=el[Object.keys(el).find(k=>k.startsWith('__reactContainer$'))];const q=[root],seen=new Set();while(q.length){const f=q.shift();if(!f||seen.has(f))continue;seen.add(f);if(f.stateNode?.logic){const app=f.stateNode.logic;return eval(code);}q.push(f.child,f.sibling,f.alternate);}throw Error('App missing');}''',code)

def aligned(page):
    geometry=page.locator('.customer-screen').evaluate('''e=>{const s=e.getBoundingClientRect(),n=e.querySelector('.customer-nav').getBoundingClientRect(),p=e.querySelector('.customer-panel').getBoundingClientRect();return {screen:s.toJSON(),nav:n.toJSON(),panel:p.toJSON(),height:innerHeight,overflow:e.scrollWidth>e.clientWidth+1};}''')
    assert abs(geometry['nav']['bottom']-geometry['height'])<2,geometry
    assert abs(geometry['screen']['height']-geometry['height'])<2,geometry
    assert geometry['panel']['bottom']<=geometry['nav']['top']+1,geometry
    assert not geometry['overflow'],geometry

def login(page):
    page.goto(BASE+'Eminevim%20Saha%20Paneli.dc.html?native=1')
    page.get_by_text('Kayıtlı Müşteri',exact=True).click()
    page.get_by_role('button',name='Giriş Yap',exact=True).click()
    page.get_by_role('button',name='Randevularım',exact=True).wait_for()

with sync_playwright() as p:
    browser=p.chromium.launch(channel='chrome',headless=True)
    page=browser.new_page(viewport={'width':393,'height':852})
    page.emulate_media(reduced_motion='reduce')
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    login(page)
    for width,height in [(393,852),(320,568),(390,659),(430,932)]:
        page.set_viewport_size({'width':width,'height':height})
        for tab in ['Randevularım','Sohbetler','Finansman','Ayarlar']:
            page.get_by_role('button',name=tab,exact=True).click()
            page.wait_for_timeout(350)
            aligned(page)
            if tab=='Sohbetler':
                page.locator('.m-konuşma-row').click()
                composer=page.locator('.customer-chat form').bounding_box()
                nav=page.locator('.customer-nav').bounding_box()
                assert abs(composer['y']+composer['height']-nav['y'])<2
            if width in (320,393):
                page.screenshot(path=str(OUT/f'fixed-{width}-{tab}.png'),animations='disabled')
        page.get_by_role('button',name='Finansman',exact=True).click()
        page.get_by_role('button',name='+ Yeni',exact=True).click()
        for step in [1,2,3]:
            aligned(page)
            actions=page.locator('.customer-finance-actions').bounding_box()
            nav=page.locator('.customer-nav').bounding_box()
            assert actions['y']+actions['height']<=nav['y']+1
            if step==1:
                page.get_by_role('button',name='Konut',exact=True).click()
                page.get_by_role('button',name='Devam ›',exact=True).click()
            elif step==2:
                page.get_by_role('button',name='Bireysel',exact=False).click()
                page.get_by_role('button',name='Devam ›',exact=True).click()
            else:
                page.screenshot(path=str(OUT/f'fixed-{width}-finansman-hesap.png'),animations='disabled')
        assert page.locator('.customer-finance-actions').get_by_role('button',name='Geri',exact=False).count()==0
        page.locator('.customer-header').get_by_role('button',name='Geri',exact=True).click()
        assert app(page,'app.state.basvuruAdim')==2
        page.locator('.customer-header').get_by_role('button',name='Geri',exact=True).click()
        assert app(page,'app.state.basvuruAdim')==1
        page.locator('.customer-header').get_by_role('button',name='Geri',exact=True).click()
        assert app(page,'app.state.basvuruDuzenle') is False
        app(page,'app.setState({basvuruDuzenle:false})')
    # Klavye açıldığında daralan görünür alan: mesaj alanı ve menü görünür kalır.
    page.set_viewport_size({'width':393,'height':440})
    page.get_by_role('button',name='Sohbetler',exact=True).click()
    page.locator('.m-konuşma-row').click()
    page.get_by_placeholder('Mesajınızı yazın',exact=True).focus()
    aligned(page)
    composer=page.locator('.customer-chat form').bounding_box()
    assert composer['y']>=0 and composer['y']+composer['height']<440
    # Kısa telefonda alt pencerenin son düğmesine kaydırarak erişilebilmeli.
    page.set_viewport_size({'width':320,'height':568})
    page.get_by_role('button',name='Randevularım',exact=True).click()
    page.locator('.m-randevu-row').first.click()
    page.get_by_role('button',name='Kapıda kimliğini doğrula',exact=True).click()
    sheet=page.get_by_role('dialog',name='Temsilcinizi doğrulayın',exact=True)
    sheet.get_by_role('button',name='Örnek: temsilci okuttu',exact=True).scroll_into_view_if_needed()
    bounds=sheet.bounding_box()
    assert bounds['y']>=0 and bounds['y']+bounds['height']<=568
    page.screenshot(path=str(OUT/'fixed-320-qr.png'),animations='disabled')
    app(page,'app.setState({mQrAcik:false})')
    # Personel sekmeleri de telefon genişliğinde taşmamalı.
    for role,tabs in [('spy',['Görüşmeler','Performans','Profil']),('tl',['Görüşmeler','Performans','Saha Canlı','Profil']),('ask',['Performans','Saha Canlı','Profil'])]:
        app(page,'app.loginRole('+repr(role)+')')
        for tab in tabs:
            page.locator('.tp-alt').get_by_role('button',name=tab,exact=True).click()
            assert page.locator('.tp').evaluate('(e)=>e.scrollWidth<=e.clientWidth+1'),(role,tab)
            nav=page.locator('.tp-alt').bounding_box()
            assert nav['y']+nav['height']<=568
            page.screenshot(path=str(OUT/f'personel-{role}-{tab}.png'),animations='disabled')
    # Kullanıcının açtığı linkler.html içindeki 393x852 telefon çerçevesi.
    preview=browser.new_page(viewport={'width':1440,'height':1000})
    preview.emulate_media(reduced_motion='reduce')
    preview.goto(BASE+'linkler.html#uygulama-telefon')
    frame=preview.frame_locator('#cerceve')
    frame.get_by_text('Kayıtlı Müşteri',exact=True).click()
    frame.get_by_role('button',name='Giriş Yap',exact=True).click()
    for tab in ['Randevularım','Sohbetler','Finansman','Ayarlar']:
        frame.get_by_role('button',name=tab,exact=True).click()
        preview.wait_for_timeout(350)
        aligned(frame)
    preview.screenshot(path=str(OUT/'fixed-onizleme-cerceve.png'),animations='disabled')
    assert not errors,errors
    browser.close()
    print('Telefon sekmeleri, finansman adımları, kısa ekran, pencereler ve önizleme: OK')
    print('Görseller:',OUT)
