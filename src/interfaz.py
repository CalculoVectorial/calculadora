import pygame as py
import pygame_gui as pyg
import numpy as np
from algebra import Parametro

class Canvas:
    def __init__(self, size, pos, color, manager):
        self.pos = np.array(pos) #Posicion del canvas
        self.size = np.array(size) #Tamaño
        self.color = color #Color
        self.canvas = py.Surface(self.size) #canvas de pygame
        self.manager = manager #Manager para los objetos del canvas
        self.objetos = [] #Objetos que contendrá el canvas
        self.rect = py.Rect(self.pos, self.size)

    def draw(self, screen): #Dibuja al canvas
        screen.blit(self.canvas, self.pos)
        self.canvas.fill(self.color)
        for obj in self.objetos:
            if isinstance(obj, Canvas):
                self.canvas.blit(obj.canvas, obj.pos)
                obj.canvas.fill(obj.color)
            for objeto in obj.objetos:
                if isinstance(objeto, Slider):
                    objeto.draw(obj.canvas)
        self.manager.draw_ui(screen)
    
    def add(self, *obj): #Añade un objeto al canvas
        for objeto in obj:
            if not(isinstance(objeto, Canvas)):
                objeto.set_true_pos(self.pos, self.manager)
        self.objetos += obj
    
    def click_event(self, pressed=None, mouse=None, pos=None): #Recolecta los demás eventos del bucle principal
        
        for obj in self.objetos:
            if isinstance(obj, Boton) and obj.pressed():
                obj.command()
            elif isinstance(obj, Canvas):
                obj.click_event(pressed, mouse, pos)
            elif isinstance(obj, Slider):
                obj.click(pressed, mouse, pos)


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
    
    def clear(self):
        self.input.clear()


class Boton(Label):
    def __init__(self, size, pos, text, command):
        super().__init__(size, pos, text)
        self.command = command #Comando del boton
    
    def create_my_box(self, manager):
        self.boton = pyg.elements.UIButton(relative_rect=self.true_rect, text=self.text, manager = manager)
    
    def pressed(self): #True si el boton es presionado
        return self.boton.check_pressed()
    
    def set_text(self, text):
        self.text = text
        self.boton.set_text(self.text)


class InfoLabel(Box):
    def __init__(self, size, pos, name, obj):
        super().__init__(size, pos)
        self.name = name
        self.obj = obj
    
    def create_my_box(self, manager):
        
        if not isinstance(self.obj, Parametro):
            self.label = pyg.elements.UILabel(relative_rect=self.true_rect, text = f"{self.name} = {self.obj}",manager = manager)
            self.color_label = pyg.elements.UILabel(relative_rect=self.color_rect, text = f"color = {self.obj.color}", manager = manager)
        else:
            self.label = pyg.elements.UILabel(relative_rect=self.true_rect, text = f"{self.name} = {self.obj}",manager = manager)
    
    def set_true_pos(self, canvas_pos, manager): 
        self.true_pos = canvas_pos + self.pos
        self.true_rect = py.Rect(self.true_pos, self.size)
        self.color_rect = py.Rect(self.true_pos + np.array([0, 30]), self.size)
        self.create_my_box(manager)
    
    def set_text(self, text):
        self.label.set_text(text)
    
    def kill(self):
        self.label.kill()
        if not isinstance(self.obj, Parametro):
            self.color_label.kill()

class DeleteBoton(Boton):
    def __init__(self, size, pos, name, command, text='Delete'):
        super().__init__(size, pos, text, command)
        self.name = name
        self.command = lambda : command(self.name)
    
    def kill(self):
        self.boton.kill()

class Slider:
    calculadora = None
    update = None
    def __init__(self, size, pos, inicial=0,name_parametro=None, velocidad=0.02):
        self.size = np.array(size)
        self.pos = np.array(pos)
        self.inicial = inicial
        self.porcentaje = inicial
        self.circle_center = np.array([self.pos[0]+self.porcentaje*self.size[0], self.pos[1]+self.size[1]/2])
        self.circle_inicial = np.array([self.pos[0]+self.porcentaje*self.size[0], self.pos[1]+self.size[1]/2])
        self.name_parametro = name_parametro
        self.run=False
        self.regreso = False
        self.velocidad = velocidad

    def draw(self, canvas):
        py.draw.line(canvas, (50,50,250), [self.pos[0],self.pos[1]+self.size[1]/2], [self.pos[0]+self.size[0], self.pos[1]+self.size[1]/2])
        py.draw.circle(canvas, 'red', self.circle_inicial, 2)
        py.draw.circle(canvas, 'grey', self.circle_center, 5)
        py.draw.circle(canvas, 'black', self.circle_center, 5,1)
    
    def move(self, des):
        if 0<=self.porcentaje<=1:
            self.porcentaje += des
            self.circle_center = np.array([self.pos[0]+self.porcentaje*self.size[0], self.pos[1]+self.size[1]/2])
            if self.porcentaje>1:
                self.porcentaje=1
                self.regreso= not self.regreso
            elif self.porcentaje<0:
                self.porcentaje=0
                self.regreso= not self.regreso
        if self.name_parametro != None:
            Slider.calculadora.get_parametros()[self.name_parametro].set_porcentaje(self.porcentaje)
            Slider.calculadora.constantes[self.name_parametro] = Slider.calculadora.get_parametros()[self.name_parametro].valor
            Slider.calculadora.locals[self.name_parametro] = Slider.calculadora.get_parametros()[self.name_parametro].valor
            Slider.update()

    def click(self, pressed, mouse, pos):
        if self.run:
            if not self.regreso:
                self.move(self.velocidad)
            else:
                self.move(-self.velocidad)
        elif self.true_rect.collidepoint(pos) and pressed[0]:
            if mouse[0] > 0:
                self.move(0.02)
            if mouse[0] < 0:
                self.move(-0.02)
        

    def set_true_pos(self, canvas_pos, manager): 
        self.true_pos = canvas_pos + self.pos
        self.true_rect = py.Rect(self.true_pos, self.size)
    
    def get_porcentaje(self):
        return self.porcentaje
    
    def correr(self):
        self.run = not self.run
    
    def set_velocidad(self):
        parametro = Slider.calculadora.get_parametros()[self.name_parametro]
        long = parametro.rango[1] - parametro.rango[0]
        self.velocidad = parametro.velocidad/long
        
       