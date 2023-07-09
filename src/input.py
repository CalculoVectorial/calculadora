import pygame_gui as pyg
from .box import Box

class Input(Box):
    def __init__(self, size, pos):
        super().__init__(size, pos)
    
    def create_my_box(self, manager):
        self.input = pyg.elements.UITextEntryLine(relative_rect=self.true_rect, manager = manager)
    
    def get_text(self): #Devuelve el texto del input
        return self.input.get_text()
