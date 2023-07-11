import numpy as np
import pygame as py
from util import *
from vector import Vector

class Graficador:
    def __init__(self, dimension, escala=50):
        self.dimension = dimension
        self.escala = escala
        self.origen_pantalla = np.array([0,0], dtype=float)

    def get_dimension(self):
        return self.dimension
    
    def get_escala(self):
        return self.escala
    
    def rotacion(self, coord):
        pass


    def transformacion(self, coord):
        coord = np.array(coord, dtype=float)
        new_coord = self.escala*self.rotacion(coord)
        punto_x = self.origen_pantalla[0] + new_coord[0]
        punto_y = self.origen_pantalla[1] + new_coord[1]
        return np.array([punto_x, punto_y])
    

    
class Graficador2D(Graficador):
    def __init__(self, escala=50):
        super().__init__(2, escala)
        self.theta = 0
        self.vectores = {}
    
    def rotacion(self, coord):
        fila1 = [np.cos(self.theta), -np.sin(self.theta)]
        fila2 = [-np.sin(self.theta), -np.cos(self.theta)]
        matriz_rotacion = np.array([fila1, fila2])
        return np.matmul(matriz_rotacion, coord)

    def get_theta(self):
        return theta
    
    def set_theta(self, theta):
        self.theta = theta


    def draw_vector(self, canvas, vector):
        color = vector.color
        info = vector.get_info()
        info = self.transformacion(info.transpose()).transpose()
        py.draw.lines(canvas.canvas, color, False, info[:-1])
        py.draw.line(canvas.canvas, color, info[1], info[-1])
    
    def draw_point(self, canvas, point):
        color = point.color
        info = point.get_info()
        info = self.transformacion(info)
        py.draw.circle(canvas.canvas, color, info, self.escala/10)
        py.draw.circle(canvas.canvas, 'white', info, self.escala/10, 1)

    def draw_campo(self, canvas, campo):
        color = campo.color
        info = campo.get_info()
        for vector in info:
            self.draw_vector(canvas, vector)

    def draw(self, canvas, grafics):
        for vector in grafics['Vector2D']:
            self.draw_vector(canvas, grafics['Vector2D'][vector])

        for point in grafics['Point2D']:
            self.draw_point(canvas, grafics['Point2D'][point])
        
        for campo in grafics['Campo2D']:
            self.draw_campo(canvas, grafics['Campo2D'][campo])

    
class Vector2D:
    def __init__(self, vector, origen = (0,0), color = 'red'):
        self.vector = vector
        self.color=color
        self.origen = np.array(origen, dtype=float)
        self._coord_ = self.origen + self.vector.coord
        self.info = self.load_info()

    def load_info(self):
        u = self.vector.unitario()*(-1/5)
        cola1 = true_rotacion2D(u.coord, np.pi/4) + self._coord_
        cola2 = true_rotacion2D(u.coord, -np.pi/4) + self._coord_
        return np.array([self.origen, self._coord_, cola1, cola2])
    
    def get_info(self):
        return self.info

class Point2D:
    def __init__(self, coord, color='blue'):
        self.coord = np.array(coord, dtype=float)
        self.color = color
    
    def get_info(self):
        return self.coord

class Campo2D:
    def __init__(self, func, color='orange'):
        self.func = func
        self.color = color
        self.info = self.load_info()
    
    def load_info(self):
        dom = cartesiano((-10, 10), (-10, 10), 21)
        result = []
        for i in range(len(dom)):
            v = dom[i]
            vector = Vector(self.func(v))
            result.append(Vector2D(vector, v, self.color))

        return result
    
    def get_info(self):
        return self.info
        

        

    
    