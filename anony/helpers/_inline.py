# __init__.py 
from .start import StartPanel
from .play import PlayPanel

class Inline(StartPanel, PlayPanel):
    def __init__(self):
        super().__init__()
