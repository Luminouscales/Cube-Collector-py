import keyboard

global pressedkey
pressedkey = "a"

def on_key(event):
    global pressedkey
    print(event.name)
    pressedkey = event.name

keyboard.on_press(on_key)
print(pressedkey)