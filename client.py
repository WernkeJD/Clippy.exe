import requests
import pyperclip
import time
from pynput import keyboard
import platform

url = "http://172.16.2.241:5000"

def run_mac_client():
    # Key mappings for Cmd/Ctrl and punctuation keys
    cmd_key = keyboard.Key.cmd
    semicolon_key = keyboard.KeyCode(char=';')
    apostrophe_key = keyboard.KeyCode(char="'")

    # Set of currently pressed keys
    pressed_keys = set()

    # Define the actions for each key combination
    key_combinations = {
        frozenset([cmd_key, semicolon_key]): "copy",     # Cmd/Ctrl + ;
        frozenset([cmd_key, apostrophe_key]): "paste"    # Cmd/Ctrl + '
    }

    def receive_shared_clipboard():
        clipboard_content = requests.get(f"{url}/clipboard").json()["data"]
        pyperclip.copy(clipboard_content)
        print("Received shared clipboard content.")

    def send_shared_clipboard():
        clipboard_content = pyperclip.paste()
        requests.post(f"{url}/clipboard", json={"data": clipboard_content})
        print("Sent shared clipboard content.")

    def check_combination():
        """Check if any key combination is active and call the corresponding action."""
        for combo, action in key_combinations.items():
            if combo <= pressed_keys:  # Check if all keys in combo are pressed
                if action == "copy":
                    send_shared_clipboard()
                elif action == "paste":
                    receive_shared_clipboard()

    def on_press(key):
        pressed_keys.add(key)
        check_combination()

    def on_release(key):
        pressed_keys.discard(key)

    # Set up the listener
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
        
def run_win_client():
    # Virtual key codes for Windows/Linux
    cmd_key_code = 162  # VK code for Ctrl key
    semicolon_key_code = 186  # VK code for ';' key
    apostrophe_key_code = 222  # VK code for "'" key

    # Set of currently pressed key codes
    pressed_keys = set()

    # Define the actions for each key combination
    key_combinations = {
        frozenset([cmd_key_code, semicolon_key_code]): "copy",     # Ctrl + ;
        frozenset([cmd_key_code, apostrophe_key_code]): "paste"    # Ctrl + '
    }

    def receive_shared_clipboard():
        clipboard_content = requests.get(f"{url}/clipboard").json()["data"]
        pyperclip.copy(clipboard_content)
        print("Received shared clipboard content.")

    def send_shared_clipboard():
        clipboard_content = pyperclip.paste()
        requests.post(f"{url}/clipboard", json={"data": clipboard_content})
        print("Sent shared clipboard content.")

    def check_combination():
        """Check if any key combination is active and call the corresponding action."""
        for combo, action in key_combinations.items():
            if combo <= pressed_keys:  # Check if all keys in combo are pressed
                if action == "copy":
                    send_shared_clipboard()
                elif action == "paste":
                    receive_shared_clipboard()


    def on_press(key):
        try:
            key_code = key.vk if hasattr(key, 'vk') else key.value.vk
            pressed_keys.add(key_code)
            print(f"Pressed keys: {pressed_keys}")
            check_combination()
        except AttributeError:
            pass  # Skip if the key doesn't have vk or value attributes

    def on_release(key):
        try:
            key_code = key.vk if hasattr(key, 'vk') else key.value.vk
            pressed_keys.discard(key_code)
        except AttributeError:
            pass

    # Set up the listener
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def run_client():
    if platform.system() == 'Darwin':  # macOS
        run_mac_client()
    else:
        run_win_client()

if __name__ == "__main__":
    run_client()