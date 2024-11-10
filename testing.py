import keyboard

def print_key(event):
    # Print the name of the key that was pressed
    print(f"Key pressed: {event.name}")

# Set up a listener for all key presses
keyboard.on_press(print_key)

print("Press keys to see them printed here. Press Esc to exit.")
# Wait until 'esc' is pressed to stop the script
keyboard.wait('esc')