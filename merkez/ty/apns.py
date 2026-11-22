"""APNS — iPhone uygulamasına (TestFlight/App Store) Apple bildirimi. Web Push'un yanında çalışır (bildirim.py çağırır).

Anahtar yalnız sunucuda: `apns.p8` (Apple'ın verdiği AuthKey) + `apns.json` {"key_id", "team_id", "topic"}; ikisi yoksa APNs kapalıdır, gerisi çalışır.
Bağımlılık: conda base'de `pyjwt`, `httpx[http2]` (h2). TestFlight/App Store bildirimi üretim sunucusundan, Xcode ile kurulan sandbox'tan gider:
üretimde "BadDeviceToken" gelirse sandbox denenir.
"""
import json
import threading
import time

from .ayarlar import APNS_AYAR, APNS_P8, BILDIRIM_TTL

URETIM, SANDBOX = "https://api.push.apple.com", "https://api.sandbox.push.apple.com"
_jeton = {"zaman": 0, "deger": ""}
_kilit = threading.Lock()


def ayar():
    """apns.json + apns.p8 tamsa ayar sözlüğü, değilse None."""
    try:
        a = json.loads(APNS_AYAR.read_text(encoding="utf-8"))
        if APNS_P8.exists() and all(a.get(k) and "?" not in a[k] for k in ("key_id", "team_id", "topic")):
            return a
    except (OSError, ValueError):
        pass
    return None


def hazir():
    return ayar() is not None


def _bearer(a):
    import jwt
    with _kilit:
        if time.time() - _jeton["zaman"] > 40 * 60:  # Apple: en az 20 dk, en çok 60 dk geçerli
            _jeton["deger"] = jwt.encode({"iss": a["team_id"], "iat": int(time.time())}, APNS_P8.read_text(), algorithm="ES256",
                                         headers={"kid": a["key_id"]})
            _jeton["zaman"] = time.time()
        return _jeton["deger"]


def _istek(c, sunucu, a, token, yuk):
    return c.post(f"{sunucu}/3/device/{token}", content=yuk, headers={
        "authorization": "bearer " + _bearer(a), "apns-topic": a["topic"], "apns-push-type": "alert", "apns-priority": "10",
        "apns-expiration": str(int(time.time()) + BILDIRIM_TTL)})


def gonder(tokenlar, govde):
    """Her token için (token, sonuc) döner: "ok" | "silindi" (telefon bildirimi bırakmış) | "hata <neden>"."""
    a = ayar()
    if not a:
        return []
    import httpx
    yuk = json.dumps({"aps": {"alert": {"title": govde.get("baslik") or "Tasarruf Yanımda", "body": govde.get("govde") or ""},
                              "sound": "default", "thread-id": govde.get("etiket") or "ty"},
                      "rid": govde.get("rid") or ""}, ensure_ascii=False).encode()
    sonuclar = []
    with httpx.Client(http2=True, timeout=10) as c:
        for t in tokenlar:
            try:
                r = _istek(c, URETIM, a, t, yuk)
                neden = (r.json() if r.content else {}).get("reason", "")
                if r.status_code == 400 and neden == "BadDeviceToken":
                    r = _istek(c, SANDBOX, a, t, yuk)
                    neden = (r.json() if r.content else {}).get("reason", "")
                if r.status_code == 200:
                    sonuc = "ok"
                elif r.status_code == 410 or neden in ("BadDeviceToken", "Unregistered", "DeviceTokenNotForTopic"):
                    sonuc = "silindi"
                else:
                    if neden in ("InvalidProviderToken", "ExpiredProviderToken"):
                        _jeton["zaman"] = 0
                    sonuc = f"hata {r.status_code} {neden}"
            except Exception as e:  # ağ hatası vb.: bir sonraki çağrıda yeniden denenir
                sonuc = "hata " + type(e).__name__
            sonuclar.append((t, sonuc))
    return sonuclar
