from .markup.start import StartMarkup
from .markup.play import PlayMarkup

class Inline(StartMarkup, PlayMarkup):
    def __init__(self):
        # Dono classes ke functions ab 'Inline' ke andar aa gaye hain
        super().__init__()
