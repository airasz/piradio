from pynput.keyboard import Listener


def on_press(key):
    if str(key) == '<179>':
        # play pause media key was pressed
    if str(key) == '<176>':
        # next key was pressed
    if str(key) == '<177>':
        # previous key was pressed


def on_release(key):
    pass
    
    
listener_thread = Listener(on_press=on_press, on_release=None)
# This is a daemon=True thread, use .join() to prevent code from exiting  
listener_thread.start()