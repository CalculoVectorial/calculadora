import pygame as py
import numpy as np

class Box:
    #Clase abstracta, una caja vacía con posiciones relativas. Será uno de los objetos que contiene un canvas.
    def __init__(self, size, pos):
        self.size = size  #Tamaño
        self.pos = np.array(pos) #Posicion de la caja

    def create_my_box(self, manager): #Se asigna el manager y se crea la caja (label, input, boton, etc)
        pass

    def set_true_pos(self, canvas_pos, manager): #Se asignan las posiciones con respecto al screen.
        self.true_pos = canvas_pos + self.pos
        self.true_rect = py.Rect(self.true_pos, self.size)
        self.create_my_box(manager)