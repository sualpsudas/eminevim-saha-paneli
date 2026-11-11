"""Web başvurusu ve isteğe bağlı bilgilerin uygulamaya aktarımını kontrol eder."""
from pathlib import Path
from urllib.parse import urlparse,parse_qs
import tempfile
from playwright.sync_api import sync_playwright

OUT=Path(tempfile.gettempdir())/'ty-randevu-qa'
OUT.mkdir(exist_ok=True)
with sync_playwright() as p:
    browser=p.chromium.launch(channel='chrome',headless=True)
    for width,height in [(1440,1000),(393,852)]:
        ctx=browser.new_context(viewport={'width':width,'height':height},is_mobile=width<500,has_touch=width<500)
        page=ctx.new_page()
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto('http://127.0.0.1:8799/web-basvuru/index.html',wait_until='domcontentloaded')
        page.wait_for_function("document.querySelector('[data-ty-form] input[name=ad]').value.length>0")
        if width<500:
            page.locator('.tk-mobilFormYeniCover [data-bs-toggle]').click()
            scope=page.locator('.ty-mobil')
        else:
            scope=page.locator('.tk-desktopForm')
        form=scope.locator('[data-ty-form]')
        form.locator('[name=temsilci]').check()
        dialog=page.locator('[data-pen=temsilci].acik')
        dialog.locator('[data-ileri]').click()
        dialog.locator('[data-ileri]').click()
        form.locator('[type=submit]').click()
        result=scope.locator('[data-sonuc]')
        result.locator('.ty-ek summary').click()
        result.locator('[data-ek-calisma]').select_option(label='Ücretli çalışan')
        result.locator('[data-ek-yas]').select_option(label='25–34')
        result.locator('[data-ek-kaydet]').click()
        link=result.locator('a[data-ty-dis]').first.get_attribute('href')
        q=parse_qs(urlparse(link).query)
        assert q['calisma']==['Ücretli çalışan'] and q['yas']==['25–34']
        assert q['rid'] and q['lat'] and q['lng'] and q['tarih']
        assert urlparse(link).hostname=='127.0.0.1'
        result.locator('.ty-ek').scroll_into_view_if_needed()
        page.screenshot(path=str(OUT/f'web-ek-bilgi-{width}.png'))
        box=result.locator('.ty-ek').bounding_box()
        assert box['x']>=0 and box['x']+box['width']<=width+1
        # SMS önizlemesi: 6 haneli giriş kodu + uygulama linki
        kod=result.locator('.ty-sms-balon b').inner_text().strip()
        assert len(kod)==6 and kod.isdigit(), kod
        assert 'randevu takibi, temsilciyle sohbet ve finansman aracı' in result.locator('.ty-sms-balon').inner_text()
        # Aynı tarayıcıda (aynı site deposu) bağlantıyı aç: önce SMS kodu, sonra parola oluşturma; bilgiler randevuyla gelmeli.
        app=ctx.new_page(); app.set_viewport_size({'width':393,'height':852})
        app.goto(link+'&native=1',wait_until='domcontentloaded')
        app.get_by_label('SMS ile gelen 6 haneli kod').fill('000000'); app.get_by_role('button',name='Doğrula').click()
        assert app.get_by_text('Kod eşleşmedi').count()==1
        app.get_by_label('SMS ile gelen 6 haneli kod').fill(kod); app.get_by_role('button',name='Doğrula').click()
        app.get_by_label('Parola',exact=True).fill('abc123'); app.get_by_label('Parola tekrar').fill('abc123')
        app.get_by_role('button',name='Parolayı kaydet ve devam et').click()
        app.wait_for_function("JSON.parse(sessionStorage.getItem('ty-randevu-v1')||'null')?.mTalep")
        saved=app.evaluate("JSON.parse(sessionStorage.getItem('ty-randevu-v1'))")
        assert saved['mTalep']['id']==q['rid'][0]
        assert saved['customerForm']['ekBilgi']['yas']=='25–34'
        app.close()
        assert not errors,errors
        page.close()
    print('Web telefon/bilgisayar, SMS kodu + parola ile uygulamaya randevu+ek bilgi aktarımı: OK')
    browser.close()
