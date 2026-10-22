"""eminevim.com ana sayfasının kopyasına Tasarruf Yanımda form önizlemesini yerleştirir.

Çalıştırma:  python olustur.py      -> index.html
Görseller/CSS canlı siteden yüklenir (<base>), izleme kodları ve gerçek form gönderimi çıkarılır.
"""
import re
import urllib.request
from pathlib import Path

KLASOR = Path(__file__).parent
KAYNAK = "https://www.eminevim.com/"
CIKTI = KLASOR / "index.html"


def parca(metin, ad):
    return re.search(rf"<!-- {ad} -->(.*?)<!-- /{ad} -->", metin, re.S).group(1)


def degistir(metin, bas, son, yeni):
    a = metin.index(bas)
    b = metin.index(son, a)
    return metin[:a] + yeni + metin[b:]


def main():
    istek = urllib.request.Request(KAYNAK, headers={"User-Agent": "Mozilla/5.0"})
    html = urllib.request.urlopen(istek, timeout=30).read().decode("utf-8")
    html = html.replace("\r\n", "\n").replace("\r", "")
    bilesen = (KLASOR / "form_bolumu.html").read_text(encoding="utf-8")
    css, form, takip, js = (parca(bilesen, a) for a in ("TY_CSS", "TY_FORM", "TY_TAKIP", "TY_JS"))

    # İzleme kodları, Messenger sohbeti ve reCAPTCHA (önizlemede gereksiz, ziyaretleri saymasın)
    html = re.sub(r"<script>\(function\(w,d,s,l,i\).*?</script>", "", html, count=1, flags=re.S)
    html = re.sub(r"<noscript><iframe src=\"https://www.googletagmanager.com.*?</noscript>", "", html, flags=re.S)
    html = re.sub(r"<!-- Messenger Sohbet Eklentisi Code -->.*?facebook-jssdk'\)\);\s*</script>", "", html, flags=re.S)
    html = re.sub(r"<script[^>]*recaptcha/api\.js[^>]*></script>", "", html)
    # Canlı sitedeki Citrix performans ölçümünü önizlemeye taşımayın.
    html = re.sub(r"<script[^>]*>\s*NS_CSM_td=.*?</script>\s*<script[^>]*>.*?sendTimingInfo.*?</script>", "", html, flags=re.S)

    html = html.replace(
        "<head>",
        '<head>\n<base href="https://www.eminevim.com/">\n<meta name="robots" content="noindex,nofollow">',
        1,
    )
    html = html.replace("</head>", css + "\n</head>", 1)

    # Masaüstü form: aç/kapa düğmesi kalır, form yenilenir
    masaustu = (
        '<div class="tk-desktopForm ty-panel d-none d-xl-block">\n'
        '    <div class="tk-formGizleAc" onclick="tyPanelAcKapa(this);" role="button" tabindex="0" aria-label="Formu gizle / göster"><i class="bi bi-arrow-right-short"></i></div>\n'
        '    <div class="tk-iletişimYazisi" id="kapaliBaslik">HIZLI BAŞVURU</div>\n'
        + form
        + '\n    <div style="display:none !important" id="desktopBilgilendirmeFormTesekkur"></div>\n</div>\n'
    )
    html = degistir(html, '<div class="tk-desktopForm d-none d-xl-block">', "<!-- Tablet ve Mobil Form -->", masaustu + "\n        ")

    # Tablet/mobil: açılır pencerenin içi yenilenir
    # Mobilde sitenin mobil sınıfları; logo gizli, başlık yalnız tablette (sitedeki gibi)
    form_m = (form.replace("tk-inputGriLabel", "tk-inputGriLabelMobil").replace('"tk-inputGri"', '"tk-inputMobilGri"')
              .replace("tk-bayrakDropdown ", "tk-bayrakDropdownMobil ")
              .replace('ty-sadece-masaustu"', 'ty-sadece-masaustu d-none"')
              .replace('ty-baslik-satir"', 'ty-baslik-satir formBaslik d-none d-lg-block"')
              .replace('class="tk-turuncuButon"', 'class="tk-turuncuButon" style="padding: 15px !important;"'))
    mobil = '<div class="ty-mobil">' + form_m + '</div>\n<div style="display:none !important" id="tabletBilgilendirmeFormTesekkur"></div>\n'
    html = degistir(html, "<!-- Form Başladı-->", "<!-- Form Bitti-->", mobil)

    # Bağlantılar tıklanır ama hiçbir yere gitmez (eminevim.com'a yönlendirmesin)
    def etkisiz(m):
        if "data-ty-dis" in m.group(0):  # kendi uygulama linkimiz çalışır
            return m.group(0)
        etiket = re.sub(r'\s(?:href|target|data-fancybox|data-type|onclick)="[^"]*"', "", m.group(0))
        return etiket.replace("<a", '<a href="javascript:void(0)"', 1)

    html = re.sub(r"<a\b[^>]*>", etkisiz, html)
    bekci = """
<script>
/* Önizleme: sonradan eklenen bağlantılar da dahil hiçbir link sayfadan çıkarmaz */
document.addEventListener('click', function (e) {
  var a = e.target.closest && e.target.closest('a');
  if (a && !a.hasAttribute('data-bs-toggle') && !a.hasAttribute('data-ty-dis')) e.preventDefault();
}, true);
document.addEventListener('submit', function (e) {
  if (!e.target.hasAttribute('data-ty-adim')) e.preventDefault();
}, true);
window.open = function () { return null; };
/* Masaüstü formu yana gizle / göster (geniş panele göre) */
function tyPanelAcKapa(btn) {
  var panel = btn.closest('.tk-desktopForm'), kapali = panel.getAttribute('data-kapali') === '1';
  panel.style.right = kapali ? '0' : -(panel.offsetWidth - 38) + 'px';
  panel.setAttribute('data-kapali', kapali ? '0' : '1');
  btn.innerHTML = kapali ? '<i class="bi bi-arrow-right-short"></i>' : '<i class="bi bi-arrow-left-short"></i>';
  var bas = document.getElementById('kapaliBaslik'); if (bas) bas.style.opacity = kapali ? 0 : 1;
}
document.addEventListener('keydown', function (e) {
  if ((e.key === 'Enter' || e.key === ' ') && e.target.classList && e.target.classList.contains('tk-formGizleAc')) { e.preventDefault(); tyPanelAcKapa(e.target); }
});
</script>
"""

    son = html.rindex("</body>")
    html = html[:son] + takip + js + bekci + html[son:]
    # Windows'ta tekrar üretim çift CR eklemesin; çıktı satır sonları kararlı olsun.
    html = "\n".join(line.rstrip() for line in html.splitlines()) + "\n"
    CIKTI.write_text(html, encoding="utf-8", newline="\n")
    print("Yazıldı:", CIKTI)


if __name__ == "__main__":
    main()
