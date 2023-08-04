import evdev
from evdev import ecodes
import threading
from kivy.event import EventDispatcher
from kivy.clock import Clock
from functools import partial
from kivy.app import App
import zmq


class Remote:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Remote, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.remote_base = RemoteBase()

    def bind(self, **kwargs):
        self.remote_base.bind(**kwargs)

    def get_remote_base(self):
        return self.remote_base


class RemoteBase(EventDispatcher):
    def __init__(self, **kwargs):
        self.register_event_type("on_keypress")
        super(RemoteBase, self).__init__(**kwargs)

        self.device = find_remote()
        self.locked = False

        if not self.device:
            raise RuntimeError
        
        self.thread = threading.Thread(target=self.listen, daemon=True)
        self.thread.start()

    def on_keypress(self, keycode, *args):
        if keycode == "reset": return True

        # Handle shutdown key
        if keycode == "KEY_SLEEP":
            # Stop the App
            App.get_running_app().stop()

            # Shutdown the system
            context = zmq.Context()
            socket = context.socket(zmq.REQ)
            socket.connect("tcp://127.0.0.1:5555")

            socket.send(b"shutdown")
            return True

    def set_keypress(self, keycode, *args):
        self.keypress = keycode
        self.keypress = "reset"
     
    def listen(self):
        for event in self.device.read_loop():
            if ecodes.EV[event.type] != "EV_KEY":
                continue

            state = ("up", "down", "hold")[event.value]

            if state == "up":
                self.locked = False
                continue

            if state != "down" or self.locked:
                continue
            
            code = ecodes.KEY[event.code]
            Clock.schedule_once(partial(self.dispatch, "on_keypress", code))

            self.locked = True


def find_remote():
    for device_code in evdev.list_devices():
        try:
            device = evdev.InputDevice(device_code)
            if device.name == "gpio_ir_recv":
                return device
        except Exception:
            pass
    return None
