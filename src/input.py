import pygame as py
from .label import LabelText

class InputText(LabelText):
    def __init__(self, text, color, size, pos, active, color_passive, color_active):
        super().__init__(text, color, size, pos)
        self.active = active
        self.color_passive = color_passive
        self.color_active = color_active

    def setActive(self, active):
        self.active = active
        self.setColor(self.color_active if self.active else self.color_passive)

    def setColor(self, color):
        self.color = color
    
    def draw(self, canvas, font, new_text):
        if self.active:
            rect = py.Rect(self.pos, self.size) # rectangulo
            py.draw.rect(canvas, self.color, rect) # dibujar el rectangulo
            self.text = new_text
            text = font.render(self.text, True, 'white') # renderizar el texto
            text_rect = text.get_rect(center=rect.center) # centrar el texto
            canvas.blit(text, text_rect) # dibujar el texto en el canvas
        else:
            super().draw(canvas, font)

    def clicked(self, event_pos):
        return True if self.rect.collidepoint(event_pos) else False
    
