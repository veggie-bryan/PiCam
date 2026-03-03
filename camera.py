from pathlib import Path
from datetime import datetime
import time

from picamera2 import Picamera2

PHOTOS_DIR = Path.home() / "photos"

# Persistent camera instance
_picam2: Picamera2 | None = None


def ensure_photos_dir():
    PHOTOS_DIR.mkdir(parents=True, exist_ok=True)


def new_photo_path() -> Path:
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    milliseconds = int(now.microsecond / 1000)
    filename = f"{timestamp}_{milliseconds:03d}.jpg"
    return PHOTOS_DIR / filename


def init_camera(
    still_size: tuple[int, int] = (1640, 1232),
    warmup_seconds: float = 0.2,
):
    """
    Initialize and start Picamera2 once.
    still_size: choose smaller than full-res for speed (4:3 aspect recommended).
    """
    global _picam2
    if _picam2 is not None:
        return _picam2

    ensure_photos_dir()

    picam2 = Picamera2()

    # Still configuration; smaller size = much faster capture/encode on Pi Zero 2 W
    config = picam2.create_still_configuration(
        main={"size": still_size},
        buffer_count=2,
    )

    picam2.configure(config)
    picam2.start()

    # Short warm-up so first capture doesn't pay extra latency
    if warmup_seconds > 0:
        time.sleep(warmup_seconds)

    _picam2 = picam2
    return _picam2


def capture_photo() -> Path:
    """
    Capture a still to a file using the already-started camera.
    """
    ensure_photos_dir()
    picam2 = init_camera()

    output_path = new_photo_path()

    # This is the fast path (no process spawn)
    picam2.capture_file(str(output_path))

    return output_path


def list_photos(limit: int = 100):
    if not PHOTOS_DIR.exists():
        return []

    photos = [
        p for p in PHOTOS_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in (".jpg", ".jpeg", ".png")
    ]
    photos.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return photos[:limit]


def latest_photo():
    photos = list_photos(1)
    return photos[0] if photos else None