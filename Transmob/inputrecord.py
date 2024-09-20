from pynput import mouse, keyboard
import time
import json

class InputRecorder:
    def __init__(self):
        self.enter_count = 0
        self.records = []
        self.recorded = False

    def on_press(self, key):
        try:
            event = {
                'type': 'keyboard',
                'action': 'press',
                'key': key.char,
                'time': time.time()
            }
            self.records.append(event)
        except AttributeError:
            # Handle special keys
            event = {
                'type': 'keyboard',
                'action': 'press',
                'key': str(key),
                'time': time.time()
            }
            self.records.append(event)
            if key == keyboard.Key.enter:
                self.enter_count += 1
                if self.enter_count >= 3:
                    return False  # Stop listener after 3 Enter presses

    def on_release(self, key):
        event = {
            'type': 'keyboard',
            'action': 'release',
            'key': str(key),
            'time': time.time()
        }
        self.records.append(event)

    def on_click(self, x, y, button, pressed):
        action = 'click' if pressed else 'release'
        event = {
            'type': 'mouse',
            'action': action,
            'button': str(button),
            'position': (x, y),
            'time': time.time()
        }
        self.records.append(event)

    def start_recording(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as k_listener, \
            mouse.Listener(on_click=self.on_click) as m_listener:
            k_listener.join()
            m_listener.join()

        self.recorded = True


    def replay_events(self):

        # Replay the recorded events
        start_time = self.records[0]['time']
        for event in self.records:
            time.sleep(event['time'] - start_time)  # Wait for the correct duration
            if event['type'] == 'keyboard':
                if event['action'] == 'press':
                    if event['key'].startswith('Key.'):
                        key = getattr(keyboard.Key, event['key'][4:])  # Extract the key name
                        keyboard.Controller().press(key)
                    else:
                        keyboard.Controller().press(event['key'])
                elif event['action'] == 'release':
                    if event['key'].startswith('Key.'):
                        key = getattr(keyboard.Key, event['key'][4:])
                        keyboard.Controller().release(key)
                    else:
                        keyboard.Controller().release(event['key'])
            elif event['type'] == 'mouse':
                if event['action'] == 'click':
                    x, y = event['position']
                    mouse.Controller().position = (x, y)
                    mouse.Controller().click(getattr(mouse.Button, event['button'][5:]))
                # Mouse release not included in this replay for simplicity

# Usage
if __name__ == "__main__":
    recorder = InputRecorder()
    recorder.start_recording()
    recorder.replay_events()
