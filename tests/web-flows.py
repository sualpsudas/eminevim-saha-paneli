"""Web başvurusu sonuç ekranı (SMS penceresi) ve uygulamaya geçiş (SMS kodu, parola yok; görüşmeye hazırlık) ve KVKK bilgisi kontrolü."""
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
        # KVKK (2026-11-18): zorunlu "Aydınlatma Metni'ni okudum" kutusu (açık rıza değil); konum için ayrı rıza kutusu yok; ticari ileti isteğe bağlı
        assert form.locator('[name=kanun]').count()==0 and form.locator('[name=konumRiza]').count()==0
        assert not form.locator('[name=kampanya]').is_checked()
        form.locator('[data-aydinlatma-ac]').click()
        ayd=page.locator('#ty-aydinlatma.acik')
        ayd.get_by_text('hukuk onayı',exact=False).wait_for()
        # Aydınlatma Yükümlülüğü Tebliği m.5 başlıkları + başvuru yolu; uygulamayla aynı metin (uygulama/aydinlatma.js)
        for bas in ('Veri sorumlusu', 'İşleme amaçları ve hukuki sebepler', 'Toplama yöntemi', 'Kimlere, hangi amaçla aktarılır', 'Saklama süresi', 'KVKK m.11', 'Başvuru'):
            assert bas in ayd.inner_text(), bas
        assert 'üçüncü kişilerle paylaşılmaz' not in ayd.inner_text()
        ayd.get_by_role('button',name='Kapat',exact=True).click()
        assert page.locator('#ty-aydinlatma.acik').count()==0
        assert not form.locator('[data-konum-riza]').is_visible()
        form.locator('[name=kampanya]').evaluate('e=>e.click()'); assert form.locator('[name=kampanya]').is_checked()
        onay=form.locator('[name=aydinlatmaOnay]')
        assert not onay.is_checked()
        form.locator('[type=submit]').click()
        form.get_by_text('Devam etmek için Aydınlatma Metni',exact=False).wait_for()
        assert scope.locator('[data-sonuc]').is_hidden()
        onay.evaluate('e=>e.click()'); assert onay.is_checked()
        assert form.get_by_text('Devam etmek için Aydınlatma Metni',exact=False).count()==0
        form.locator('[name=temsilci]').check()
        dialog=page.locator('[data-pen=temsilci].acik')
        dialog.wait_for()
        dialog.locator('[data-ileri]').click()
        dialog.locator('[data-ileri]').click()
        form.locator('[type=submit]').click()
        result=scope.locator('[data-sonuc]')
        # Sonuç: "Sayın Ad Soyad, temsilci çağrınız alındı!", özet, SMS satırı; SMS önizlemesi Kapat'a kadar duran pencere
        result.get_by_text('Sayın Mehmet Demir, temsilci çağrınız alındı!', exact=True).wait_for()
        for yok in ('Başarılı!', 'Yeni başvuru', 'Görüşmeye hazırlanmamıza'):
            assert result.get_by_text(yok).count() == 0, yok
        sms = result.locator('[data-sms-pencere]')
        assert 'acik' in sms.get_attribute('class')
        page.screenshot(path=str(OUT/f'web-sms-{width}.png'))
        kod=sms.locator('[data-sms-kod]').inner_text().strip()
        assert len(kod)==6 and kod.isdigit(), kod
        assert 'randevu takibi, temsilciyle sohbet ve finansman aracı' in sms.locator('.ty-sms-balon').inner_text()
        box=sms.locator('.ty-sms-kutu').bounding_box()
        assert box['x']>=0 and box['x']+box['width']<=width+1
        page.wait_for_timeout(1500)
        assert 'acik' in sms.get_attribute('class'), 'Kapat denmeden kapanmamalı'
        sms.locator('[data-sms-kapat]').click()
        assert 'acik' not in sms.get_attribute('class')
        result.locator('[data-sms-ac]').click()
        assert 'acik' in sms.get_attribute('class')
        sms.locator('[data-sms-kapat]').click()
        page.screenshot(path=str(OUT/f'web-sonuc-{width}.png'))
        link=result.locator('a[data-ty-dis]').first.get_attribute('href')
        q=parse_qs(urlparse(link).query)
        assert q['rid'] and q['lat'] and q['lng'] and q['tarih']
        assert q['adi']==['Mehmet'] and q['soyad']==['Demir'] and q['kampanya']==['1']
        assert form.locator('[data-konum-riza]').count()==1
        assert urlparse(link).hostname=='127.0.0.1'
        # Aynı tarayıcıda (aynı site deposu) bağlantıyı aç: SMS kodu → doğrudan içeri (ad soyad formdan, parola yok); randevu gelmeli.
        app=ctx.new_page(); app.set_viewport_size({'width':393,'height':852})
        app.goto(link+'&native=1',wait_until='domcontentloaded')
        app.wait_for_function('document.querySelector(".login-box [autocomplete=one-time-code]")?.hasAttribute("data-dc-tpl") || !!document.querySelector("[data-dc-tpl][autocomplete=one-time-code]")')
        app.get_by_label('SMS ile gelen 6 haneli kod').fill('000000'); app.get_by_role('button',name='Doğrula',exact=True).click()
        assert app.get_by_text('Kod eşleşmedi').count()==1
        app.get_by_label('SMS ile gelen 6 haneli kod').fill(kod); app.get_by_role('button',name='Doğrula',exact=True).click()
        app.wait_for_function("JSON.parse(sessionStorage.getItem('ty-randevu-v1')||'null')?.mTalep")
        saved=app.evaluate("JSON.parse(sessionStorage.getItem('ty-randevu-v1'))")
        assert saved['mTalep']['id']==q['rid'][0]
        assert app.get_by_label('Parola',exact=True).count()==0 and app.get_by_label('Soyad',exact=True).count()==0
        # Görüşmeye hazırlık yalnız uygulamada: girişte açılır; "Şimdi değil" → Randevum'da kart kalır
        app.wait_for_timeout(800)
        if app.get_by_role('button', name='Atla', exact=True).count():  # önce tanıtım, sonra hazırlık
            assert app.get_by_text('Görüşmeye hazırlanmamıza yardımcı olun').count() == 0
            app.get_by_role('button', name='Atla', exact=True).click()
        app.get_by_text('Görüşmeye hazırlanmamıza yardımcı olun', exact=True).wait_for()
        app.get_by_role('button', name='Şimdi değil', exact=True).click()
        app.get_by_role('button', name='Randevularım', exact=True).click(); app.locator('.m-randevu-row').first.click()
        app.get_by_text('Görüşmeye hazırlık · isteğe bağlı', exact=True).wait_for()
        app.close()
        # Temsilci penceresi seçim yapmadan kapatılırsa anahtar kapanır; normal başvuru yapılabilir.
        page.reload(wait_until='domcontentloaded')
        page.wait_for_function("document.querySelector('[data-ty-form] input[name=ad]').value.length>0")
        if width<500: page.locator('.tk-mobilFormYeniCover [data-bs-toggle]').click()
        form.locator('[name=temsilci]').check()
        page.locator('[data-pen=temsilci].acik [data-kapat]').first.click()
        assert not form.locator('[name=temsilci]').is_checked()
        assert not form.locator('[data-konum-riza]').is_visible()
        form.locator('[name=aydinlatmaOnay]').evaluate('e=>e.click()')
        form.locator('[type=submit]').click()
        result.get_by_text('Sayın Mehmet Demir, çağrınız alındı!',exact=True).wait_for()
        assert result.locator('[data-sms-pencere]').count()==0
        assert not errors,errors
        page.close()
    print('Web telefon/bilgisayar: sonuç ekranı, SMS penceresi, aydınlatma bilgisi, SMS koduyla (parolasız) uygulamaya randevu, görüşmeye hazırlık: OK')
    browser.close()
