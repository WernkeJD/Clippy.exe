import requests
import pyperclip
import time
from pynput import keyboard
import platform

url = "http://172.16.2.241:5000"

# Determine which key to use for the copy command based on OS
if platform.system() == 'Darwin':  # macOS
    copy_key = keyboard.Key.cmd
    c_key = keyboard.KeyCode(char='ç')
    v_key = keyboard.KeyCode(char='√')
    paste_keys = [keyboard.Key.cmd, keyboard.KeyCode(char='v')]

else:  # Windows or Linux
    copy_key = keyboard.Key.ctrl
    paste_keys = [keyboard.Key.ctrl, keyboard.KeyCode(char='v')]

# Set to store currently pressed keys
pressed_keys = set()

controller = keyboard.Controller()

def run_client():
    def copy_shared_clipboard():
        clipboard_content = requests.get(f"{url}/clipboard").json()["data"]
        pyperclip.copy(clipboard_content)
        print("Copied shared clipboard content.")

        # Automatically paste the content
        for key in paste_keys:
            controller.press(key)
        for key in reversed(paste_keys):
            controller.release(key)

    def paste_shared_clipboard():
        clipboard_content = pyperclip.paste()
        requests.post(f"{url}/clipboard", json={"data": clipboard_content})
        print("Pasted shared clipboard content.")

    # Wait for the server to start
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("Server started.")
                break
        except requests.ConnectionError:
            print("Waiting for server to start...")
        time.sleep(1)

    # Define the key combinations
    copy_combination = {copy_key, keyboard.Key.alt, c_key}
    paste_combination = {copy_key, keyboard.Key.alt, v_key}

    def on_press(key):
        # Add the key to the pressed keys set
        pressed_keys.add(key)

        # Check for copy combination
        if all(k in pressed_keys for k in copy_combination):
            paste_shared_clipboard()

        # Check for paste combination
        if all(k in pressed_keys for k in paste_combination):
            copy_shared_clipboard()

    def on_release(key):
        # Remove the key from the pressed keys set
        if key in pressed_keys:
            pressed_keys.remove(key)

    # Set up the listener
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    run_client()