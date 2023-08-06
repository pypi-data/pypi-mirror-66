from ..pin import DIGPin
from ..device import Relay


class SingleRelay(Relay):

    def __init__(self):
        super().__init__()
        self.pin: DIGPin = None

    def on_attached(self):
        self.pin = self.pins[0]
        assert self.pin, 'Invalid Pin'

    def set_state(self, on: int):
        self.pin.output(on)
