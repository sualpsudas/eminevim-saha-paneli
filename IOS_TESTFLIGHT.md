# Tasarruf Yanımda — iOS TestFlight Kurulumu

Bu proje Capacitor 8 ile native iOS kabuğuna alınır ve Windows bilgisayardan Codemagic macOS derleyicisi üzerinden TestFlight'a gönderilir. Apple sırları repoya yazılmaz.

## 1. İlk yüklemeden önce kesinleştirilecek bilgiler

- Apple Developer Program üyeliği bulunan hesap
- Kalıcı Bundle ID (geçici değer: `com.sualpsudas.tasarrufyanimda`)
- App Store Connect uygulama adı: `Tasarruf Yanımda`
- SKU (örnek: `tasarruf-yanimda-ios`)

Bundle ID ilk yüklemeden sonra değiştirilemeyeceği için Codemagic çalıştırılmadan önce `capacitor.config.json` ve `codemagic.yaml` içindeki iki değer birlikte güncellenmelidir.

## 2. App Store Connect kaydı

1. Apple Developer hesabında Bundle ID'yi kaydedin.
2. App Store Connect → Apps → `+` → New App ile uygulama kaydı açın.
3. Oluşan sayfadaki sayısal Apple ID değerini not edin.
4. Users and Access → Integrations → App Store Connect API bölümünde `App Manager` yetkili bir anahtar üretin.
5. `.p8` özel anahtarını indirin. Apple bu dosyayı yalnızca bir kez indirmeye izin verir.

## 3. Codemagic değişkenleri

Codemagic uygulamasında Environment variables bölümünde şu iki grubu oluşturun.

### `appstore_credentials` — tamamı Secret

- `APP_STORE_CONNECT_PRIVATE_KEY`: indirilen `.p8` dosyasının tam içeriği
- `APP_STORE_CONNECT_KEY_IDENTIFIER`: Key ID
- `APP_STORE_CONNECT_ISSUER_ID`: Issuer ID
- `CERTIFICATE_PRIVATE_KEY`: Codemagic'in dağıtım sertifikası oluştururken kullanacağı RSA private key

`CERTIFICATE_PRIVATE_KEY` üretmek için güvenli bir bilgisayarda:

```sh
ssh-keygen -t rsa -b 2048 -m PEM -f codemagic_certificate_key -q -N ""
```

Codemagic'e yalnızca `codemagic_certificate_key` dosyasının içeriğini Secret olarak girin. Bu dosyayı ve `.p8` anahtarını repoya eklemeyin.

### `ios_config`

- `APP_APPLE_ID`: `6819198783`

## 4. Codemagic bağlantısı ve ilk derleme

1. Codemagic'te GitHub hesabını bağlayın.
2. `sualpsudas/eminevim-saha-paneli` reposunu ekleyin.
3. Yapılandırma türü olarak `codemagic.yaml` seçin.
4. Apple Developer Portal/App Store Connect erişimini ayarlayın veya yukarıdaki ortam değişkenlerini ekleyin.
5. `Tasarruf Yanımda - TestFlight` akışını manuel başlatın.

Akış; web dosyalarını `www/` içine toplar, iOS projesini SPM ile üretir, dağıtım sertifikası/profilini getirir, imzalı IPA oluşturur ve TestFlight'a yükler.

## 5. TestFlight

Apple build'i işledikten sonra App Store Connect → TestFlight bölümünde görünür. Önce iç test kullanıcıları eklenebilir. Dış test kullanıcıları için beta test bilgileri doldurulur ve ilk build Beta App Review'a gönderilir.

Her TestFlight build'i 90 gün kullanılabilir. Yeni yüklemelerde build numarası otomatik artırılır.

## Yerel komutlar

Windows'ta web paketini doğrulamak:

```sh
npm ci
npm run web:sync
npm test
```

Mac üzerinde yerel iOS projesi oluşturmak:

```sh
npm ci
npm run ios:add
npm run ios:open
```
