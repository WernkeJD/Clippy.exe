import requests
import pyperclip
import time

def run_client():
    clipboard_content = ""

    # Wait for server to begin
    while True:
        response = requests.get("http://172.16.2.241:5000")
        time.sleep(1)
        print("Waiting for server to start...")
        if response.status_code == 200:
            break

    while True:
        new_clipboard_content = pyperclip.paste()

        if new_clipboard_content != clipboard_content:
            clipboard_content = new_clipboard_content

            # Send clipboard content to server
            requests.post("http://172.16.2.241:5000/clipboard", json={"data": clipboard_content})

        clipboard_content = requests.get("http://172.16.2.241:5000/clipboard").json()["data"]
        print(clipboard_content)
        pyperclip.copy(clipboard_content)

        time.sleep(0.5)

if __name__ == "__main__":
    run_client()