"""Yerel sunucu: python -m http.server 8799. Playwright + Chrome gerektirir."""
from pathlib import Path
import tempfile
from playwright.sync_api import sync_playwright

URL='http://127.0.0.1:8799/Eminevim%20Saha%20Paneli.dc.html?native=1'
OUT=Path(tempfile.gettempdir())/'ty-randevu-qa'
OUT.mkdir(exist_ok=True)

def app(page,code):
    return page.evaluate('''(code)=>{const el=document.getElementById('dc-root');const root=el[Object.keys(el).find(k=>k.startsWith('__reactContainer$'))];const queue=[root],seen=new Set();while(queue.length){const f=queue.shift();if(!f||seen.has(f))continue;seen.add(f);if(f.stateNode?.logic){const app=f.stateNode.logic;return eval(code);}queue.push(f.child,f.sibling,f.alternate);}throw Error('Mounted app missing');}''',code)

with sync_playwright() as p:
    browser=p.chromium.launch(channel='chrome',headless=True)
    page=browser.new_page(viewport={'width':393,'height':852})
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(URL)
    page.get_by_text('Kayıtlı Müşteri',exact=True).wait_for()
    page.get_by_text('Kayıtlı Müşteri',exact=True).click()
    page.get_by_role('button',name='Giriş Yap',exact=True).click()
    page.locator('.m-randevu-row').first.click()
    page.get_by_text('Temsilciniz yolda',exact=True).first.wait_for()
    page.wait_for_timeout(400)
    page.screenshot(path=str(OUT/'musteri-telefon.png'),animations='disabled')
    page.get_by_role('button',name='Kapıda kimliğini doğrula',exact=True).click()
    code=app(page,'app.state.mTalep.dogrulama.kod')
    assert len(code)==4
    page.screenshot(path=str(OUT/'qr-telefon.png'))
    app(page,'app.setState({mQrAcik:false});app.loginRole("spy");app.setState({tpSecim:"ayse"})')
    page.set_viewport_size({'width':1180,'height':820})
    page.get_by_role('button',name="Vardım: müşterinin QR'ını okut",exact=True).click()
    # Var olan demo tarayıcının kod girişi; gerçek kamera taklit edilmez.
    app(page,'app.setState({qrKodGirdi:'+repr(code)+'});app.dogrula(true)')
    assert app(page,'app.state.mTalep.durum')=='gorusmede'
    app(page,'app.setState({qrTarama:"",tpOzetNot:"Plan seçenekleri görüşüldü."})')
    page.get_by_role('button',name='Görüşmeyi bitir · özeti gönder',exact=True).click()
    assert app(page,'app.state.mTalep.durum')=='tamamlandi'
    page.screenshot(path=str(OUT/'personel-tablet.png'))
    app(page,'app.setState({panel:"musteri",customerNav:"basvurum"})')
    page.set_viewport_size({'width':393,'height':852})
    page.get_by_role('heading',name='Görüşme özeti',exact=True).wait_for()
    assert page.get_by_role('button',name='Yeni randevu iste',exact=True).count()==1
    page.get_by_role('button',name='Düzeltme iste',exact=True).click()
    page.get_by_placeholder('Düzeltilmesini istediğiniz bilgiyi veya sorununuzu yazın.').fill('Görüşme konusu eksik.')
    page.get_by_role('button',name='Bildirimi gönder',exact=True).click()
    assert app(page,'app.state.mTalep.sorun.durum')=='Alındı'
    app(page,'app.loginRole("ask");app.setState({destekYaniti:"Kaydınız incelendi, temsilciniz düzeltilmiş özeti paylaşacak."})')
    page.set_viewport_size({'width':1180,'height':820})
    page.get_by_role('button',name='İncelemeye al',exact=True).click()
    page.get_by_role('button',name='Yanıtı müşteriye gönder',exact=True).click()
    assert app(page,'app.state.mTalep.sorun.durum')=='Yanıtlandı'
    app(page,'app.setState({panel:"musteri",customerNav:"basvurum"})')
    page.set_viewport_size({'width':320,'height':740})
    page.screenshot(path=str(OUT/'ozet-dar-telefon.png'))
    assert page.locator('.m-akis').evaluate('(e)=>e.scrollWidth<=e.clientWidth+1')
    page.get_by_role('button',name='Yeni randevu iste',exact=True).click()
    # Haritadan gelen seçimi kullanarak yeni başvuru davranışını test et.
    app(page,'app.setState({yaKonum:{lat:41.02,lng:29.02,adres:"Üsküdar, uzun bir adres ve görüşme noktası",bolge:"Üsküdar"},yaGun:"Bugün",yaGunISO:new Date().toLocaleDateString("en-CA"),yaSaat:"18:00"});app.yaGonder();app.setState({yaOpen:false,yaKaynak:""})')
    page.locator('.m-randevu-row').first.click()
    page.get_by_role('button',name='Saati onayla · 18:00',exact=True).click()
    assert app(page,'app.state.mTalep.repId')=='s2'
    assert app(page,'app.state.mGecmis.length')==1
    page.get_by_role('dialog',name='Görüşmeye hazırlanmamıza yardımcı olun',exact=True).wait_for()
    page.get_by_label('Çalışma durumu',exact=True).select_option(label='Emekli')
    page.get_by_label('Yaş aralığı',exact=True).select_option(label='65 ve üzeri')
    page.get_by_role('button',name='Kaydet',exact=True).click()
    assert app(page,'app.state.customerForm.ekBilgi.calisma')=='Emekli'
    page.get_by_role('button',name='Gün / saati değiştir',exact=True).click()
    app(page,'app.setState({yaSaat:"19:00"});app.yaGonder()')
    assert app(page,'app.state.mTalep.saat')=='18:00'
    assert app(page,'app.state.mTalep.degisiklik.saat')=='19:00'
    app(page,'app.loginRole("spy");app.setState({tpSecim:app.state.mTalep.id})')
    page.set_viewport_size({'width':1180,'height':820})
    page.get_by_role('button',name='Yeni zamanı onayla',exact=True).click()
    assert app(page,'app.state.mTalep.saat')=='19:00'
    page.get_by_role('button',name='Yola çık · müşteriye bildir',exact=True).click()
    assert app(page,'app.state.mTalep.durum')=='yolda'
    app(page,'app.setState({panel:"musteri",customerNav:"basvurum"})')
    page.set_viewport_size({'width':393,'height':852})
    page.get_by_role('button',name='İptal et',exact=True).click()
    page.get_by_role('button',name='Randevuyu iptal et',exact=True).click()
    assert app(page,'app.state.mTalep.durum')=='iptal'
    page.reload()
    page.get_by_text('Kayıtlı Müşteri',exact=True).wait_for()
    assert app(page,'app.state.mTalep.durum')=='iptal','Yenilemede iptal kaydı korunmalı'
    assert not errors,errors
    print('Müşteri/personel/QR/özet/destek akışı: OK')
    print('Görseller:',OUT)
    browser.close()
