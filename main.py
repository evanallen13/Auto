import time
import webbrowser
import platform
import pyautogui
import pyperclip
from screeninfo import get_monitors
import mss
import mss.tools
from PIL import Image
from io import BytesIO

def get_monitor_with_mouse():
    mouse_x, mouse_y = pyautogui.position()

    for monitor in get_monitors():
        if (
            monitor.x <= mouse_x < monitor.x + monitor.width
            and monitor.y <= mouse_y < monitor.y + monitor.height
        ):
            return monitor

    raise RuntimeError("Could not determine which monitor the mouse is on")

def screenshot_mouse_monitor_to_clipboard():
    monitor = get_monitor_with_mouse()

    with mss.mss() as sct:
        region = {
            "left": monitor.x,
            "top": monitor.y,
            "width": monitor.width,
            "height": monitor.height,
        }

        sct_img = sct.grab(region)

        img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)

        output = BytesIO()
        img.save(output, format="PNG")
        image_data = output.getvalue()

    # Copy image to clipboard (platform-specific handling)
    system = platform.system()

    if system == "Windows":
        import win32clipboard
        import win32con

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(
            win32con.CF_DIB,
            img.convert("RGB").tobytes()
        )
        win32clipboard.CloseClipboard()

    else:
        # macOS / Linux: copy PNG bytes
        pyperclip.copy(image_data)

    print("Screenshot copied to clipboard")

def open_chatgpt_and_paste():
    webbrowser.open("https://chat.openai.com")
    time.sleep(6)  # wait for browser + page to load

    system = platform.system()

    if system == "Darwin":  # macOS
        pyautogui.hotkey("command", "v")
    else:  # Windows / Linux
        pyautogui.hotkey("ctrl", "v")

    print("Pasted screenshot into ChatGPT")

if __name__ == "__main__":
    print("Move your mouse to the target screen...")
    time.sleep(2)

    screenshot_mouse_monitor_to_clipboard()
    open_chatgpt_and_paste()
