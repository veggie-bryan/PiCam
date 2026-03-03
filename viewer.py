from pathlib import Path
from signal import pause
import threading
import time

from display import CameraDisplay

PHOTOS_DIR = Path("/home/bryan/photos")
POLL_SECONDS = 0.5  # how often to check for a new photo


def latest_photo_path(photos_dir: Path) -> Path | None:
    """Return newest image file by mtime, or None if none exist."""
    if not photos_dir.exists():
        return None

    exts = {".jpg", ".jpeg", ".png"}
    candidates = [p for p in photos_dir.iterdir() if p.is_file() and p.suffix.lower() in exts]
    if not candidates:
        return None

    return max(candidates, key=lambda p: p.stat().st_mtime)


def watch_latest(display: CameraDisplay, stop_event: threading.Event):
    """Continuously watch for a newer image and display it."""
    last_shown: Path | None = None
    last_mtime: float = -1.0

    # On boot: show latest if it exists
    p = latest_photo_path(PHOTOS_DIR)
    if p is None:
        display.show_text("No photos yet")
    else:
        last_shown = p
        last_mtime = p.stat().st_mtime
        display.show_image(p)

    # Watch loop
    while not stop_event.is_set():
        try:
            p = latest_photo_path(PHOTOS_DIR)
            if p is not None:
                mtime = p.stat().st_mtime
                # Update if it's a different file OR strictly newer mtime
                if (last_shown is None) or (p != last_shown) or (mtime > last_mtime):
                    last_shown = p
                    last_mtime = mtime
                    display.show_image(p)
        except Exception as e:
            # If something goes wrong (partial write, etc.), don't crash the watcher
            print("Watcher error:", repr(e))

        time.sleep(POLL_SECONDS)


def main():
    display = CameraDisplay()
    display.clear()

    stop_event = threading.Event()
    t = threading.Thread(target=watch_latest, args=(display, stop_event), daemon=True)
    t.start()

    print("Viewer running: showing latest photo and auto-updating on new captures.")
    print("Exit with Ctrl+C")

    try:
        pause()
    except KeyboardInterrupt:
        stop_event.set()


if __name__ == "__main__":
    main()