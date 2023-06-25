import pygame as py

class LabelText:   
    def __init__(self, text, color, size, pos):
        self.text = text # texto 
        self.color = color # color del fondo del rectangulo
        self.size = size # tamaño del rectangulo (ancho, alto)
        self.pos = pos # posicion del rectangulo (x, y)
        self.rect = py.Rect(self.pos, self.size)

    def draw(self, canvas, font):
        py.draw.rect(canvas, self.color, self.rect) # dibujar el rectangulo
        text = font.render(self.text, True, 'white') # renderizar el texto
        text_rect = text.get_rect(center=self.rect.center) # centrar el texto
        canvas.blit(text, text_rect) # dibujar el texto en el canvas