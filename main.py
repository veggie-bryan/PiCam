from camera import init_camera
from buttons import CameraButtons
from display import CameraDisplay
from signal import pause
import time
import threading

display = CameraDisplay()

_capture_lock = threading.Lock()
_capture_busy = False

def on_capture():
    global _capture_busy

    with _capture_lock:
        if _capture_busy:
            print("CAPTURE: ignored (busy)")
            return
        _capture_busy = True

    def worker():
        global _capture_busy
        try:
            t0 = time.time()
            print("CAPTURE: start")
            path = capture_photo()
            print(f"CAPTURE: done in {time.time()-t0:.2f}s -> {path.name}")
            # optional immediate display
            # display.show_image(path)
        finally:
            with _capture_lock:
                _capture_busy = False

    threading.Thread(target=worker, daemon=True).start()

def on_menu():
    p = latest_photo()
    if p:
        print("LATEST:", p.name)
    else:
        print("No photos yet")

def on_up():
    print("UP")

def on_down():
    print("DOWN")

def on_left():
    print("LEFT")

def on_right():
    print("RIGHT")

def main():
    init_camera()
    print("PiCam controller running...")
    print("Test buttons or exit (ctrl + C)")

    buttons = CameraButtons()
    buttons.bind(
        on_capture,
        on_menu,
        on_left,
        on_right,
        on_up,
        on_down
    )
    pause()

if __name__ == "__main__":
    main()