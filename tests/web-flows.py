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
        page=browser.new_page(viewport={'width':width,'height':height},is_mobile=width<500,has_touch=width<500)
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
        link=result.locator('a[data-ty-dis]').get_attribute('href')
        q=parse_qs(urlparse(link).query)
        assert q['calisma']==['Ücretli çalışan'] and q['yas']==['25–34']
        assert q['rid'] and q['lat'] and q['lng'] and q['tarih']
        assert urlparse(link).hostname=='127.0.0.1'
        result.locator('.ty-ek').scroll_into_view_if_needed()
        page.screenshot(path=str(OUT/f'web-ek-bilgi-{width}.png'))
        box=result.locator('.ty-ek').bounding_box()
        assert box['x']>=0 and box['x']+box['width']<=width+1
        # Aynı bağlantıyı yeni sayfada aç; bilgiler randevuyla birlikte gelmeli.
        app=browser.new_page(viewport={'width':393,'height':852})
        app.goto(link+'&native=1',wait_until='domcontentloaded')
        app.wait_for_function("JSON.parse(sessionStorage.getItem('ty-randevu-v1')||'null')?.mTalep")
        saved=app.evaluate("JSON.parse(sessionStorage.getItem('ty-randevu-v1'))")
        assert saved['mTalep']['id']==q['rid'][0]
        assert saved['customerForm']['ekBilgi']['yas']=='25–34'
        app.close()
        assert not errors,errors
        page.close()
    print('Web telefon/bilgisayar ve uygulamaya randevu+ek bilgi aktarımı: OK')
    browser.close()
