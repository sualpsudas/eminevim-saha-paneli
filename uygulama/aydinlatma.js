/* Tasarruf Yanımda · KVKK Aydınlatma Metni (tek kaynak: uygulama ve web formu aynı metni gösterir).
   KVKK m.10 ve Aydınlatma Yükümlülüğü Tebliği m.5'teki zorunlu başlıklar: veri sorumlusu, amaç, aktarım (alıcı grupları + amaç),
   toplama yöntemi ve hukuki sebep, m.11 hakları; ayrıca başvuru yolu ve saklama süresi. Her amaç kendi hukuki sebebiyle eşleşir.
   Örnek metindir: yayından önce Eminevim uyum/hukuk onayı gerekir (saklama süreleri, yurt dışı aktarım, İYS). */
(function (w) {
  var GUNCEL = "18 Kasım 2026";
  var B = [
    ["Veri sorumlusu",
      "Emin Evim Tasarruf Finansmanı A.Ş. (Eminevim) · Yamanevler Mah. Ahmet Tevfik İleri Cad. No: 20 A Ümraniye / İstanbul · " +
      "Mersis No: 0333072097900104 · KEP: eminevim@hs06.kep.tr. Bu metin, 6698 sayılı Kişisel Verilerin Korunması Kanunu (KVKK) " +
      "m.10 uyarınca Tasarruf Yanımda web formu ve uygulaması için hazırlanmıştır."],
    ["İşlenen kişisel verileriniz", [
      "<b>Kimlik:</b> ad, soyad.",
      "<b>İletişim:</b> cep telefonu numarası.",
      "<b>Görüşme bilgisi:</b> görüşme için haritadan seçtiğiniz yer, gün ve saat; çağrının durumu; temsilcinin görüşme yerine vardığını gösteren doğrulama kaydı.",
      "<b>Müşteri işlem:</b> temsilcinizle yazışmalarınız, görüşme özeti, görüşmeye verdiğiniz puan.",
      "<b>İsteğe bağlı paylaştıklarınız:</b> çalışma durumu, yaş aralığı, temsilcinize notunuz; Finansman Aracı'nda seçtiğiniz finansman türü, tutar, peşinat ve vade.",
      "<b>İşlem güvenliği:</b> SMS doğrulama kodu ve giriş kayıtları, bildirim izni kaydı.",
      "<b>Pazarlama:</b> ticari elektronik ileti izniniz ve tarihi."]],
    ["İşleme amaçları ve hukuki sebepler", [
      "Talebinizi almak, size en uygun temsilciyi yönlendirmek, görüşmeyi planlamak ve yapmak, çağrınızla ilgili SMS ve bildirim göndermek: " +
      "talep ettiğiniz görüşme ve olası finansman sözleşmesinin kurulmasıyla doğrudan ilgili olması (KVKK m.5/2-c).",
      "İsteğe bağlı paylaştığınız hazırlık bilgileri ve finansman tercihlerini temsilcinize iletmek, görüşmeye hazırlıklı gelmesini sağlamak: " +
      "sözleşmenin kurulmasıyla doğrudan ilgili olması (KVKK m.5/2-c). Paylaşmamanız görüşmenizi etkilemez.",
      "Hesabınıza SMS koduyla güvenli giriş yapmanızı sağlamak, kötüye kullanımı önlemek: meşru menfaatimiz (KVKK m.5/2-f).",
      "Hizmet kalitesini ölçmek ve iyileştirmek (görüşme puanı, görüşme süreleri): meşru menfaatimiz (KVKK m.5/2-f).",
      "Mevzuattan doğan saklama, bilgi verme ve denetim yükümlülüklerini yerine getirmek: hukuki yükümlülüğümüz (KVKK m.5/2-ç).",
      "Kampanya ve tanıtım iletisi göndermek: <b>yalnız açık rızanız</b> (KVKK m.5/1) ve 6563 sayılı Kanun kapsamında verdiğiniz ticari elektronik ileti izni. " +
      "İzin vermemeniz hizmeti etkilemez; izninizi Ayarlar'dan veya iletideki ret bağlantısıyla dilediğiniz an geri alabilirsiniz."]],
    ["Toplama yöntemi",
      "Verileriniz, web formuna ve uygulamaya sizin girdiğiniz bilgilerle, kısmen otomatik yollarla (harita üzerinde yer seçimi, SMS doğrulaması) " +
      "elektronik ortamda; görüşme özeti ise görüşmeden sonra temsilciniz tarafından toplanır."],
    ["Kimlere, hangi amaçla aktarılır", [
      "<b>Hizmet sağlayıcılarımıza</b> (SMS gönderimi, uygulama bildirimi, harita ve adres arama, sunucu barındırma): yalnız hizmetin yürütülmesi için, " +
      "verdiğimiz talimatla ve gerekli güvenlik önlemleriyle.",
      "<b>Yurt dışına:</b> bildirim ve harita hizmetlerinin bir kısmının sunucuları yurt dışındadır. Bu aktarımlar KVKK m.9'daki güvencelerle " +
      "(Kurul'a bildirilen standart sözleşme) yapılır.",
      "<b>Yetkili kamu kurum ve kuruluşlarına:</b> yalnız mevzuatın gerektirdiği hallerde ve ölçüde.",
      "<b>Emin Üstün Holding şirketlerine:</b> yalnız ticari elektronik ileti izni verdiyseniz, kampanya iletisi gönderilmesi için; izin kaydınız ayrıca " +
      "İleti Yönetim Sistemi'ne (İYS) bildirilir.",
      "Verileriniz satılmaz ve bu amaçlar dışında kimseyle paylaşılmaz."]],
    ["Saklama süresi",
      "Görüşme bir sözleşmeyle sonuçlanmazsa çağrı ve görüşme kayıtlarınız son görüşme tarihinden itibaren 2 yıl saklanır. Sözleşme kurulursa " +
      "mevzuattaki süre (10 yıl) uygulanır. Ticari elektronik ileti izin kayıtları, izin geri alındıktan sonra 3 yıl saklanır. Süre dolunca " +
      "verileriniz silinir, yok edilir veya anonim hale getirilir (Eminevim Kişisel Veri Saklama ve İmha Politikası)."],
    ["KVKK m.11 kapsamındaki haklarınız", [
      "Kişisel verilerinizin işlenip işlenmediğini öğrenme, işlenmişse buna ilişkin bilgi talep etme,",
      "İşlenme amacını ve amacına uygun kullanılıp kullanılmadığını öğrenme,",
      "Yurt içinde veya yurt dışında aktarıldığı üçüncü kişileri bilme,",
      "Eksik veya yanlış işlenmişse düzeltilmesini isteme,",
      "KVKK m.7'deki şartlar çerçevesinde silinmesini veya yok edilmesini isteme,",
      "Düzeltme, silme ve yok etme işlemlerinin verilerin aktarıldığı üçüncü kişilere bildirilmesini isteme,",
      "Münhasıran otomatik sistemlerle analiz edilmesi sonucu aleyhinize bir sonucun ortaya çıkmasına itiraz etme,",
      "Kanuna aykırı işlenmesi sebebiyle zarara uğramanız halinde zararın giderilmesini talep etme."]],
    ["Başvuru",
      "Taleplerinizi yazılı olarak (Yamanevler Mah. Ahmet Tevfik İleri Cad. No: 20 A Ümraniye / İstanbul adresine imzalı posta veya noter yoluyla), " +
      "güvenli elektronik veya mobil imzalı olarak KEP adresimize (eminevim@hs06.kep.tr) ya da eminevim.com/kvkk adresindeki KVKK Başvuru Formu ile " +
      "iletebilirsiniz. Başvurunuz en geç 30 gün içinde ücretsiz yanıtlanır; işlem ayrıca bir maliyet gerektirirse Kurul'un belirlediği tarife uygulanabilir."]
  ];
  function govde(sinif) {
    sinif = sinif || "";
    var h = '<em>Örnek metindir · yayından önce Eminevim uyum/hukuk onayı gerekir.</em>';
    B.forEach(function (b) {
      var ic = Array.isArray(b[1]) ? '<ul>' + b[1].map(function (x) { return '<li>' + x + '</li>'; }).join("") + '</ul>' : '<p>' + b[1] + '</p>';
      h += '<section class="' + sinif + '"><b class="ayd-b">' + b[0] + '</b>' + ic + '</section>';
    });
    return h + '<small>Son güncelleme: ' + GUNCEL + '</small>';
  }
  w.Aydinlatma = { govde: govde, bolumler: B.map(function (b) { return b[0]; }), guncel: GUNCEL };
})(window);
