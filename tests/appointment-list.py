"""Randevu listesi/okunma/gezinme ve iPhone önizleme güvenli alan kontrolü."""
from pathlib import Path
import tempfile
from playwright.sync_api import sync_playwright

OUT=Path(tempfile.gettempdir())/'ty-phone-layout'
OUT.mkdir(exist_ok=True)

def app(page,code):
    return page.evaluate('''code=>{const el=document.getElementById('dc-root');const q=[el[Object.keys(el).find(k=>k.startsWith('__reactContainer$'))]],seen=new Set();while(q.length){const f=q.shift();if(!f||seen.has(f))continue;seen.add(f);if(f.stateNode?.logic){const app=f.stateNode.logic;return eval(code);}q.push(f.child,f.sibling,f.alternate);}throw Error('App missing');}''',code)

with sync_playwright() as p:
    browser=p.chromium.launch(channel='chrome',headless=True)
    page=browser.new_page(viewport={'width':1440,'height':1040},reduced_motion='reduce')
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto('http://127.0.0.1:8799/linkler.html#uygulama-telefon')
    frame=page.frames[1]
    frame.on('pageerror',lambda e:errors.append(str(e)))
    frame.get_by_text('Giriş Yap',exact=True).click()
    frame.get_by_role('button',name='Giriş Yap',exact=True).click()
    rows=frame.locator('.m-randevu-row')
    rows.first.wait_for()
    assert frame.evaluate('window.EMINEVIM_NATIVE') is True
    assert frame.locator('.customer-header img').count()==0
    assert frame.locator('.customer-header').get_by_text('AK',exact=True).count()==0
    assert frame.locator('.customer-screen .login-return-button').count()==0
    assert frame.locator('.m-yeni').count()==1
    # Geçmiş kayıtlar gerçek randevu yapısını kullanır; aktif kayıt en üstte kalır.
    app(frame,'app.setState({mGecmis:[{id:"old-a",repId:"s2",tarih:"2026-09-01",gunYazi:"1 Eylül",saat:"11:00",durum:"tamamlandi",yer:"Üsküdar",ozet:[{k:"Konu",v:"Konut"}]},{id:"old-b",repId:"s1",tarih:"2026-10-01",gunYazi:"1 Ekim",saat:"12:00",durum:"iptal",yer:"Ataşehir"}]})')
    assert rows.count()==3
    assert '1 Eki' in rows.nth(1).inner_text()
    assert '1 Eyl' in rows.nth(2).inner_text()
    status=frame.locator('.customer-statusbar').bounding_box()
    header=frame.locator('.customer-header').bounding_box()
    assert abs(status['height']-59)<1 and header['y']>=59
    nav=frame.locator('.customer-nav').bounding_box()
    assert nav['height']>=80
    page.screenshot(path=str(OUT/'iphone-randevular-listesi.png'))
    rows.first.click()
    frame.get_by_role('button',name='Geri',exact=True).wait_for()
    assert frame.locator('.m-header-back').inner_text()=='Geri'
    assert frame.get_by_text('Tüm randevular',exact=True).count()==0
    assert frame.get_by_role('button',name='Temsilciye yaz',exact=True).count()==0
    assert frame.locator('.m-durum').inner_text().find('Temsilciniz: Onur Kaya')>=0
    assert frame.get_by_role('button',name='Ön tercihler',exact=True).count()==1
    page.screenshot(path=str(OUT/'iphone-randevu-detayi.png'))
    frame.get_by_role('button',name='Geri',exact=True).click()
    rows.nth(1).click()
    frame.get_by_role('heading',name='İptal edildi',exact=True).wait_for()
    frame.get_by_role('button',name='Geri',exact=True).click()
    rows.nth(2).click()
    frame.get_by_role('heading',name='Görüşme özeti',exact=True).wait_for()
    frame.get_by_role('button',name='Geri',exact=True).click()
    assert frame.locator('.m-yeni').count()==0
    frame.goto(frame.url)
    frame.get_by_text('Giriş Yap',exact=True).click()
    frame.get_by_role('button',name='Giriş Yap',exact=True).click()
    rows.first.wait_for()
    assert frame.locator('.m-yeni').count()==0
    app(frame,'app.setState({mTalep:{...app.state.mTalep,revision:2}})')
    assert frame.locator('.m-yeni').count()==1
    rows.first.click()
    app(frame,'app.setState({mTalep:{...app.state.mTalep,durum:"atandi"}})')
    frame.get_by_role('button',name='Geri',exact=True).click()
    assert frame.locator('.m-yeni').count()==1,'Bekleyen randevu okunsa bile ünlem kalır'
    assert 'Kesinleşmesi bekleniyor' in rows.first.inner_text()
    rows.first.click()
    app(frame,'app.setState({mTalep:{...app.state.mTalep,durum:"netlesti"}})')
    assert 'Temsilciniz yola çıktığında sizi bilgilendireceğiz.' not in frame.locator('.m-durum').inner_text()
    frame.get_by_role('button',name='Geri',exact=True).click()
    assert frame.locator('.m-yeni').count()==0
    frame.get_by_role('button',name='Sohbetler',exact=True).click()
    frame.get_by_role('heading',name='Konuşmalar',exact=True).wait_for()
    assert frame.get_by_placeholder('Mesajınızı yazın',exact=True).count()==0
    page.screenshot(path=str(OUT/'iphone-sohbetler.png'))
    frame.get_by_role('button',name='Konuşmayı aç: Onur Kaya',exact=True).click()
    frame.get_by_placeholder('Mesajınızı yazın',exact=True).fill('Görüşmek üzere.')
    frame.get_by_role('button',name='Gönder',exact=True).click()
    assert app(frame,'app.state.chatMessages.at(-1).text')=='Görüşmek üzere.'
    page.screenshot(path=str(OUT/'iphone-konusma.png'))
    frame.get_by_role('button',name='Geri',exact=True).click()
    frame.get_by_role('heading',name='Konuşmalar',exact=True).wait_for()
    # Gerçek telefon genişliğinde sahte kamera/sistem çubuğu çizilmez.
    mobile=browser.new_page(viewport={'width':320,'height':568},reduced_motion='reduce')
    mobile.goto('http://127.0.0.1:8799/linkler.html#uygulama-telefon')
    mf=mobile.frame_locator('#cerceve')
    mf.get_by_text('Giriş Yap',exact=True).click()
    mf.get_by_role('button',name='Giriş Yap',exact=True).click()
    mf.locator('.m-randevu-row').first.wait_for()
    assert 'preview-iphone' not in (mf.locator('html').get_attribute('class') or '')
    assert mf.locator('.m-randevu-row').evaluate('(e)=>e.scrollWidth<=e.clientWidth+1')
    mobile.screenshot(path=str(OUT/'randevular-mobil-320.png'))
    assert not errors,errors
    browser.close()
    print('Randevu listesi, okunma, geçmiş detayları, gezinme, iPhone güvenli alanı: OK')
