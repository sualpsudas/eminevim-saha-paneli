"""Saat onayı sonrası isteğe bağlı hazırlık penceresi; yerel 8799 + Chrome."""
from pathlib import Path
import tempfile
from playwright.sync_api import sync_playwright

OUT=Path(tempfile.gettempdir())/'ty-phone-layout'
OUT.mkdir(exist_ok=True)

def app(page,code):
    return page.evaluate('''code=>{const el=document.getElementById('dc-root');const q=[el[Object.keys(el).find(k=>k.startsWith('__reactContainer$'))]],seen=new Set();while(q.length){const f=q.shift();if(!f||seen.has(f))continue;seen.add(f);if(f.stateNode?.logic){const app=f.stateNode.logic;return eval(code);}q.push(f.child,f.sibling,f.alternate);}throw Error('App missing');}''',code)

with sync_playwright() as p:
    browser=p.chromium.launch(channel='chrome',headless=True)
    for width,height,tab in [(320,568,'Randevularım'),(393,852,'Sohbetler')]:
        page=browser.new_page(viewport={'width':width,'height':height},reduced_motion='reduce')
        page.goto('http://127.0.0.1:8799/Eminevim%20Saha%20Paneli.dc.html?native=1')
        page.get_by_text('Kayıtlı Müşteri',exact=True).click()
        page.get_by_role('button',name='Giriş Yap',exact=True).click()
        app(page,'app.setState({mTalep:{...app.state.mTalep,durum:"atandi"}})')
        dialog=page.get_by_role('dialog',name='Görüşmeye hazırlanmamıza yardımcı olun',exact=True)
        assert dialog.count()==0
        assert page.get_by_role('button',name='Bilgi ekle',exact=True).count()==0
        page.get_by_role('button',name=tab,exact=True).click()
        if tab=='Randevularım': page.locator('.m-randevu-row').first.click()
        else: page.locator('.m-konuşma-row').click()
        page.get_by_role('button',name='Saati onayla',exact=False).click()
        dialog.wait_for()
        assert app(page,'app.state.mTalep.durum')=='netlesti'
        box=dialog.bounding_box()
        assert box['y']>=0 and box['x']>=0 and box['x']+box['width']<=width+1
        dialog.get_by_role('button',name='Şimdi değil',exact=True).scroll_into_view_if_needed()
        page.screenshot(path=str(OUT/f'hazirlik-popup-{width}.png'))
        dialog.get_by_role('button',name='Şimdi değil',exact=True).click()
        assert dialog.count()==0
        assert app(page,'app.state.mTalep.durum')=='netlesti'
        page.get_by_role('button',name='Randevularım',exact=True).click()
        page.locator('.m-randevu-row').first.click()
        page.get_by_role('button',name='İsterseniz bilgi ekleyin',exact=True).click()
        dialog.get_by_label('Çalışma durumu',exact=True).select_option(label='Emekli')
        dialog.get_by_role('button',name='Kaydet',exact=True).click()
        assert app(page,'app.state.customerForm.ekBilgi.calisma')=='Emekli'
        page.get_by_role('button',name='Bilgileri düzenle',exact=True).click()
        assert dialog.get_by_role('button',name='Ön tercihlerimi oluştur',exact=True).count()==0
        dialog.get_by_role('button',name='Şimdi değil',exact=True).click()
        page.get_by_role('button',name='Ön tercihlerimi oluştur',exact=True).click()
        page.locator('.customer-finance').wait_for()
        assert app(page,'app.state.mTalep.durum')=='netlesti'
        page.reload()
        page.get_by_text('Kayıtlı Müşteri',exact=True).click()
        page.get_by_role('button',name='Giriş Yap',exact=True).click()
        page.get_by_role('button',name='Randevularım',exact=True).wait_for()
        assert dialog.count()==0
        page.close()
    browser.close()
    print('Hazırlık penceresi: onay öncesi gizli, onay sonrası açık, atlama/düzenleme/yenileme OK')
