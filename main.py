from camera import capture_photo, list_photos, latest_photo
from buttons import CameraButtons
from signal import pause

def on_capture():
    path = capture_photo()
    print("CAPTURED:", path.name)

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