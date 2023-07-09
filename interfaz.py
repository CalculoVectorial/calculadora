import pygame as py
import pygame_gui as pyg
import numpy as np

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

class Label(Box):
    def __init__(self, size, pos, text):
        super().__init__(size, pos)
        self.text = text #Texto

    def create_my_box(self, manager): #Override
        self.label = pyg.elements.UILabel(relative_rect=self.true_rect, text=self.text, manager = manager)
    
    def set_text(self, text):
        self.text = text
        self.label.set_text(self.text)


class Input(Box):
    def __init__(self, size, pos):
        super().__init__(size, pos)
    
    def create_my_box(self, manager):
        self.input = pyg.elements.UITextEntryLine(relative_rect=self.true_rect, manager = manager)
    
    def get_text(self): #Devuelve el texto del input
        return self.input.get_text()


class Boton(Label):
    def __init__(self, size, pos, text, command):
        super().__init__(size, pos, text)
        self.command = command #Comando del boton
    
    def create_my_box(self, manager):
        self.boton = pyg.elements.UIButton(relative_rect=self.true_rect, text=self.text, manager = manager)
    
    def pressed(self): #True si el boton es presionado
        return self.boton.check_pressed()