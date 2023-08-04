from kivy.properties import ObjectProperty
from kivy.event import EventDispatcher
import threading
import time

class Test(EventDispatcher):
    a = ObjectProperty(None)

    def __init__(self):
        threading.Thread(target=self.change).start()

    def change(self):
        for i in range(100000):
            self.a = i
            time.sleep(1)

def callback(instance, value):
    print(f"Callback {instance} {value}")

c = Test()
c.bind(a=callback)

c.a = 1
c.a = "Hello"