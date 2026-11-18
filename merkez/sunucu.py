"""Tasarruf Yanımda merkezi: uygulamanın test sürümü için ortak veri (çağrılar, mesajlar, SPY durumları).

Çalıştır:  python sunucu.py          (127.0.0.1:8794/<gizli_yol.txt>/)
Durdur:    python sunucu.py --durdur
Ek kütüphane: pywebpush (uygulaması kapalı SPY'ye bildirim; yoksa bildirim gitmez, gerisi çalışır).
Kod merkez/ty/ paketinde, parçalara ayrılmış (liste: ty/__init__.py; IT için: IT_DEVIR.md). Bu dosya yalnız başlatır.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ty.api import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
