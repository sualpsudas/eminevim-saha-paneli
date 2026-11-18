"""Panel: senaryolar iki bölmeli (müşteri telefon + SPY tablet), adım adım ilerler; görüntüler yüklenir; video iki sürüm.
Yerel sunucu: python -m http.server 8799. Görüntüler: python araclar/senaryo_goruntu.py"""
from pathlib import Path
import tempfile
from playwright.sync_api import sync_playwright

URL = 'http://127.0.0.1:8799/panel.html'
OUT = Path(tempfile.gettempdir()) / 'ty-randevu-qa'
OUT.mkdir(exist_ok=True)
with sync_playwright() as p:
    browser = p.chromium.launch(channel='chrome', headless=True)
    for w, h in [(1440, 900), (393, 852)]:
        page = browser.new_page(viewport={'width': w, 'height': h})
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('response', lambda r: errors.append('404 ' + r.url) if r.status >= 400 else None)
        for ad, sayi_en_az in (('senaryo-1', 10), ('senaryo-2', 10)):
            page.goto(URL + '#' + ad)
            kok = page.locator('.bolum.acik [data-senaryo]')
            kok.wait_for()
            toplam = kok.locator('.noktalar button').count()
            assert toplam >= sayi_en_az, (ad, toplam)
            assert kok.locator('[data-geri]').is_disabled()
            for i in range(toplam):
                page.wait_for_function("[...document.querySelectorAll('.bolum.acik .bolme img')].every(i=>i.complete&&i.naturalWidth>0)")
                gorunen = kok.locator('.bolme.gorunur' if w < 900 else '.bolme')
                assert gorunen.count() == (1 if w < 900 else 2), (ad, i)
                assert kok.locator('.bolme.etkin').count() >= 1
                if i in (0, toplam // 2):
                    page.screenshot(path=str(OUT / f'panel-{ad}-{w}-{i + 1}.png'))
                if i < toplam - 1:
                    kok.locator('[data-ileri]').click()
            assert kok.locator('[data-ileri]').is_disabled()
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'), 'yatay kaydırma olmamalı'
            if w < 900:  # dar ekranda diğer tarafa geçiş
                kok.locator('[data-yan=p]').click(); assert kok.locator('[data-bolme=p].gorunur').count() == 1
            page.keyboard.press('ArrowLeft')
            assert kok.locator('.sira').inner_text().startswith(f'{toplam - 1} /')
        page.goto(URL + '#video')
        page.get_by_role('button', name='Kadın sesli', exact=True).click()
        assert 'kadin' in page.locator('#b-video video').get_attribute('src')
        assert not errors, errors
        page.close()
    print('Panel senaryoları (iki bölme, adım adım, görüntüler yüklü, dar ekranda tek taraf) ve video sürümleri: OK')
    browser.close()
