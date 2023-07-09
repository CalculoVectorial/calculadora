import pygame_gui as pyg
from .box import Box

class Label(Box):
    def __init__(self, size, pos, text):
        super().__init__(size, pos)
        self.text = text #Texto

    def create_my_box(self, manager): #Override
        self.label = pyg.elements.UILabel(relative_rect=self.true_rect, text=self.text, manager = manager)
    
    def set_text(self, text):
        self.text = text
        self.label.set_text(self.text)