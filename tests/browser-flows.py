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
    page.get_by_role('button',name='Devam et',exact=True).wait_for()
    # Kayıtlı müşteri (Ayşe): telefon → SMS kodu → içeri; parola yok, ad sorulmaz (2026-11-18)
    page.get_by_role('button',name='Devam et',exact=True).click()
    kod=page.get_by_label('SMS ile gelen 6 haneli kod')
    kod.wait_for(); assert len(kod.input_value())==6
    assert page.get_by_label('Parola',exact=True).count()==0
    page.get_by_role('button',name='Doğrula',exact=True).click()
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
    assert page.get_by_role('button',name='Düzeltme iste').count()==0 and page.get_by_text('Destek',exact=True).count()==0  # destek kalktı (2026-11-11)
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
    page.get_by_role('button',name='Devam et',exact=True).wait_for()
    assert app(page,'app.state.mTalep.durum')=='iptal','Yenilemede iptal kaydı korunmalı'
    # Yeni numara: kod hatası → Ad + Soyad (aydınlatma gösterilir, onay kutusu yok; ticari ileti izni isteğe bağlı)
    yeni=browser.new_page(viewport={'width':393,'height':852})
    yeni.on('pageerror',lambda e:errors.append(str(e)))
    yeni.goto(URL)
    def buton(ad): return yeni.get_by_role('button',name=ad,exact=True)
    yeni.get_by_label('Telefon numaranız',exact=True).fill('0532 001 02 03')
    buton('Devam et').click()
    kod=yeni.get_by_label('SMS ile gelen 6 haneli kod')
    gecerli=kod.input_value()
    assert len(gecerli)==6
    kod.fill('000000'); buton('Doğrula').click()
    yeni.get_by_role('alert').get_by_text('Kod eşleşmedi',exact=False).wait_for()
    kod.fill(gecerli); buton('Doğrula').click()
    ad=yeni.get_by_label('Ad',exact=True); soyad=yeni.get_by_label('Soyad',exact=True)
    ad.wait_for()
    assert ad.input_value() and soyad.input_value(), 'Test: ad ve soyad örnek dolu gelmeli'
    assert yeni.get_by_label('Parola',exact=True).count()==0 and yeni.get_by_text('Onaylıyorum',exact=True).count()==0
    izin=yeni.get_by_role('checkbox',name='Ticari elektronik ileti izni (isteğe bağlı)',exact=True)
    assert not izin.is_checked(), 'Ticari ileti izni kendiliğinden işaretli olmamalı'
    buton('Aydınlatma Metni').click()
    yeni.get_by_role('dialog',name='Aydınlatma Metni',exact=True).get_by_text('hukuk onayı',exact=False).wait_for()
    assert yeni.get_by_text('üçüncü kişilerle paylaşılmaz',exact=False).count()==0
    yeni.get_by_role('dialog',name='Aydınlatma Metni',exact=True).get_by_role('button',name='Kapat',exact=True).click()
    # KVKK onayı (2026-11-18): "okudum, bilgilendirildim" kutusu zorunlu; metin bağlantısı kutuyu işaretlemez
    onay=yeni.get_by_role('checkbox',name="Aydınlatma Metni'ni okudum, bilgilendirildim",exact=True)
    assert not onay.is_checked()
    buton('Hesabımı oluştur').click()
    yeni.get_by_role('alert').get_by_text('Devam etmek için Aydınlatma Metni',exact=False).wait_for()
    assert not app(yeni,'app.state.girisYapildi')
    onay.check()
    soyad.fill(''); buton('Hesabımı oluştur').click()
    yeni.get_by_role('alert').get_by_text('Soyadınızı yazın.',exact=True).wait_for()
    assert not app(yeni,'app.state.girisYapildi')
    ad.fill('Deneme'); soyad.fill('Müşteri')
    buton('Hesabımı oluştur').click()
    buton('Atla').click()
    assert app(yeni,'app.state.customerForm.adi')=='Deneme' and app(yeni,'app.state.customerForm.soyadi')=='Müşteri'
    assert app(yeni,'app.state.kampanyaIzni') is False
    buton('Ayarlar').click()
    assert yeni.get_by_text('Deneme Müşteri',exact=True).is_visible()
    buton('Çıkış yap').click()
    # Yeniden giriş: aynı numara + SMS kodu → ad sorulmadan hesap açılır
    buton('Devam et').click()
    yeni.get_by_label('SMS ile gelen 6 haneli kod').wait_for()
    buton('Doğrula').click()
    buton('Randevularım').wait_for()
    assert yeni.get_by_label('Soyad',exact=True).count()==0
    assert app(yeni,'app.state.customerForm.name')=='Deneme Müşteri'
    print('Tek giriş: kayıtlı müşteri SMS koduyla, yeni müşteri Ad + Soyad, aydınlatma metni, isteğe bağlı izin, yeniden giriş: OK')

    # Kapıda da üst başlıktaki aynı metin Randevularım'a döner.
    kapi=browser.new_page(viewport={'width':393,'height':852})
    kapi.goto(URL)
    kapi.get_by_role('button',name='Devam et',exact=True).click()
    kapi.get_by_role('button',name='Doğrula',exact=True).click()
    kapi.get_by_role('button',name='Ayarlar',exact=True).click()
    app(kapi,'app.setState({mTalep:{...app.state.mTalep,durum:"gorusme"}})')
    kapi.locator('.m-header-status-link').get_by_text('Temsilciniz yolda',exact=True).click()
    kapi.get_by_role('heading',name='Randevularım',exact=True).wait_for()
    print('Kapıda görünen başlık Randevularım’a dönüyor: OK')
    assert not errors,errors
    print('Müşteri/personel/QR/özet akışı: OK (destek yok)')
    print('Görseller:',OUT)
    browser.close()
