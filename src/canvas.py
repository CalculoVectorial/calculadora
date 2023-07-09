import pygame as py
import pygame_gui as pyg
import numpy as np

from .boton import Boton

py.init()

class Canvas:
    def __init__(self, size, pos, color):
        self.pos = np.array(pos) #Posicion del canvas
        self.size = np.array(size) #Tamaño
        self.color = color #Color
        self.canvas = py.Surface(self.size) #canvas de pygame
        self.manager = pyg.UIManager(self.size, 'config.json') #Manager para los objetos del canvas
        self.objetos = [] #Objetos que contendrá el canvas
    
    def draw(self, screen): #Dibuja al canvas junto a todos los objetos que contiene
        screen.blit(self.canvas, self.pos)
        self.canvas.fill(self.color)
        self.manager.draw_ui(screen)
    
    def add(self, *obj): #Añade un objeto al canvas
        self.objetos += obj
        for obj in self.objetos:
            obj.set_true_pos(self.pos, self.manager)

    def py_event(self, event): #Recolecta los eventos del for each del main
        self.manager.process_events(event)
    
    def click_event(self): #Recolecta los demás eventos del bucle principal
        for obj in self.objetos:
            if isinstance(obj, Boton) and obj.pressed():
                obj.command()
    
    def update(self, clock): #Realiza un update del manager
        self.manager.update(clock/600)