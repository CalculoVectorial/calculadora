import pygame_gui as pyg
from .label import Label

class Boton(Label):
    def __init__(self, size, pos, text, command):
        super().__init__(size, pos, text)
        self.command = command #Comando del boton
    
    def create_my_box(self, manager):
        self.boton = pyg.elements.UIButton(relative_rect=self.true_rect, text=self.text, manager = manager)
    
    def pressed(self): #True si el boton es presionado
        return self.boton.check_pressed()