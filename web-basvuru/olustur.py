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
    bilesen = (KLASOR / "form_bolumu.html").read_text(encoding="utf-8")
    css, form, takip, js = (parca(bilesen, a) for a in ("TY_CSS", "TY_FORM", "TY_TAKIP", "TY_JS"))

    # İzleme kodları, Messenger sohbeti ve reCAPTCHA (önizlemede gereksiz, ziyaretleri saymasın)
    html = re.sub(r"<script>\(function\(w,d,s,l,i\).*?</script>", "", html, count=1, flags=re.S)
    html = re.sub(r"<noscript><iframe src=\"https://www.googletagmanager.com.*?</noscript>", "", html, flags=re.S)
    html = re.sub(r"<!-- Messenger Sohbet Eklentisi Code -->.*?facebook-jssdk'\)\);\s*</script>", "", html, flags=re.S)
    html = re.sub(r"<script[^>]*recaptcha/api\.js[^>]*></script>", "", html)

    html = html.replace(
        "<head>",
        '<head>\n<base href="https://www.eminevim.com/">\n<meta name="robots" content="noindex,nofollow">',
        1,
    )
    html = re.sub(r"<title>.*?</title>", "<title>Tasarruf Yanımda · Form Önizlemesi</title>", html, count=1, flags=re.S)
    html = html.replace("</head>", css + "\n</head>", 1)

    # Masaüstü form: aç/kapa düğmesi kalır, form yenilenir
    masaustu = (
        '<div class="tk-desktopForm ty-genis d-none d-xl-block">\n'
        '    <div class="tk-formGizleAc" onclick="homeFormGizleAcToogle(this);"><i class="bi bi-arrow-right-short"></i></div>\n'
        '    <div class="tk-iletişimYazisi" id="kapaliBaslik">HIZLI BAŞVURU</div>\n'
        + form
        + '\n    <div style="display:none !important" id="desktopBilgilendirmeFormTesekkur"></div>\n</div>\n'
    )
    html = degistir(html, '<div class="tk-desktopForm d-none d-xl-block">', "<!-- Tablet ve Mobil Form -->", masaustu + "\n        ")

    # Tablet/mobil: açılır pencerenin içi yenilenir
    mobil = form + '\n<div style="display:none !important" id="tabletBilgilendirmeFormTesekkur"></div>\n'
    html = degistir(html, "<!-- Form Başladı-->", "<!-- Form Bitti-->", mobil)

    # Bağlantılar tıklanır ama hiçbir yere gitmez (eminevim.com'a yönlendirmesin)
    def etkisiz(m):
        etiket = re.sub(r'\s(?:href|target|data-fancybox|data-type|onclick)="[^"]*"', "", m.group(0))
        return etiket.replace("<a", '<a href="javascript:void(0)"', 1)

    html = re.sub(r"<a\b[^>]*>", etkisiz, html)
    bekci = """
<script>
/* Önizleme: sonradan eklenen bağlantılar da dahil hiçbir link sayfadan çıkarmaz */
document.addEventListener('click', function (e) {
  var a = e.target.closest && e.target.closest('a');
  if (a && !a.hasAttribute('data-bs-toggle')) e.preventDefault();
}, true);
document.addEventListener('submit', function (e) {
  if (!e.target.hasAttribute('data-ty-adim')) e.preventDefault();
}, true);
window.open = function () { return null; };
</script>
"""

    son = html.rindex("</body>")
    html = html[:son] + takip + js + bekci + html[son:]
    CIKTI.write_text(html, encoding="utf-8")
    print("Yazıldı:", CIKTI)


if __name__ == "__main__":
    main()
