import numpy as np
import pygame as py
from util import *
from vector import Vector

class Graficador:
    def __init__(self, dimension, canvas, escala=50):
        self.dimension = dimension
        self.escala = escala
        self.origen_pantalla = np.array([0,0], dtype=float)
        self.visible = True
        self.theta = 0
        self.canvas = canvas
    
    def get_theta(self):
        return self.theta
    
    def set_theta(self, theta):
        self.theta += theta

    def get_visible(self):
        return self.visible
    
    def set_visible(self, visible):
        self.visible = visible

    def get_dimension(self):
        return self.dimension
    
    def get_escala(self):
        return self.escala
    
    def rotacion(self, coord):
        pass

    def mouse_event(self, pressed, mouse, pos):
        pass
    
    def zoom(self, event,pos):
        if self.get_visible() and self.canvas.rect.collidepoint(pos):
            if event.y == 1:
                self.escala += 2   
            elif event.y == -1 and self.escala > 2:
                self.escala -= 2   

    def transformacion(self, coord):
        coord = np.array(coord, dtype=float)
        new_coord = self.escala*self.rotacion(coord)
        punto_x = self.origen_pantalla[0] + new_coord[0]
        punto_y = self.origen_pantalla[1] + new_coord[1]
        return np.array([punto_x, punto_y])
    
    def draw_vector(self, vector):
        color = vector.color
        info = vector.get_info()
        info = self.transformacion(info.transpose()).transpose()
        py.draw.lines(self.canvas.canvas, color, False, info[:-1])
        py.draw.line(self.canvas.canvas, color, info[1], info[-1])
    
    def draw_point(self, point):
        color = point.color
        info = point.get_info()
        info = self.transformacion(info)
        py.draw.circle(self.canvas.canvas, color, info, self.escala/10)
        py.draw.circle(self.canvas.canvas, 'white', info, self.escala/10, 1)
    
    def draw_campo(self, campo):
        color = campo.color
        info = campo.get_info()
        for vector in info:
            self.draw_vector(vector)
    
    def interpolacion_lineal(self, points, color):
        py.draw.lines(self.canvas.canvas, color, False, points)
    
    
class Graficador2D(Graficador):
    def __init__(self, canvas, escala=50):
        super().__init__(2, canvas, escala)
    
    def rotacion(self, coord):
        fila1 = [np.cos(self.theta), -np.sin(self.theta)]
        fila2 = [-np.sin(self.theta), -np.cos(self.theta)]
        matriz_rotacion = np.array([fila1, fila2])
        return np.matmul(matriz_rotacion, coord)
    
    def mouse_event(self, pressed, mouse, pos):
        if pressed[0] and self.canvas.rect.collidepoint(pos):
            if mouse[1] < 0 and self.get_visible():
                self.set_theta(np.pi/75)

            if mouse[1] > 0 and self.get_visible():
                self.set_theta(-np.pi/75)

    def draw_ejes(self):
        limit_x = self.canvas.size[0] // (2*self.escala) + 2
        limit_y = limit_x
        py.draw.line(self.canvas.canvas, 'white', self.transformacion([-limit_x, 0]), self.transformacion([limit_x, 0]))
        py.draw.line(self.canvas.canvas, 'white', self.transformacion([0, -limit_y]), self.transformacion([0, limit_y]))

    def draw_malla(self):
        borde_x = self.canvas.size[0]//(2*self.escala) + 2
        borde_y = borde_x
        for i in range(1, borde_x):
            py.draw.line(self.canvas.canvas, (50,50,50), self.transformacion([i,-borde_y]), self.transformacion([i,borde_y]))
            py.draw.line(self.canvas.canvas, (50,50,50), self.transformacion([-i,-borde_y]), self.transformacion([-i,borde_y]))

        for j in range(1, borde_y):
            py.draw.line(self.canvas.canvas, (50,50,50), self.transformacion([-borde_x, j]), self.transformacion([borde_x, j]))
            py.draw.line(self.canvas.canvas, (50,50,50), self.transformacion([-borde_x, -j]), self.transformacion([borde_x, -j]))

    def draw(self, grafics):
        if self.visible:
            if self.escala >= 15:
                self.draw_malla()
            self.draw_ejes()

            for vector in grafics['Vector2D']:
                self.draw_vector(grafics['Vector2D'][vector])

            for point in grafics['Point2D']:
                self.draw_point(grafics['Point2D'][point])
                
            for campo in grafics['Campo2D']:
                self.draw_campo(grafics['Campo2D'][campo])


class Graficador3D(Graficador):
    def __init__(self, canvas, escala=50):
        super().__init__(3, canvas, escala)
        self.theta = np.pi/6
        self.phi = np.pi/3
    
    def rotacion(self, coord):
        fila1 = [np.cos(self.theta), -np.sin(self.theta), 0]
        fila2 = [np.sin(self.theta)*np.cos(self.phi), np.cos(self.theta)*np.cos(self.phi), -np.sin(self.phi)]
        matriz_rotacion = np.array([fila1, fila2])
        return np.matmul(matriz_rotacion, coord)
    
    def get_phi(self):
        return self.phi
    
    def get_mode(self):
        return self.mode

    def set_phi(self, phi):
        self.phi += phi
    
    def set_mode(self, mode):
        self.mode = mode
    
    def mouse_event(self, pressed, mouse, pos):
        if pressed[0] and self.canvas.rect.collidepoint(pos):
            if mouse[0] < 0 and self.get_visible():
                self.set_theta(np.pi/50)

            if mouse[0] > 0 and self.get_visible():
                self.set_theta(-np.pi/50)
        
        if pressed[2] and self.canvas.rect.collidepoint(pos):
            if mouse[1] < 0 and self.get_visible():
                self.set_phi(np.pi/50)

            if mouse[1] > 0 and self.get_visible():
                self.set_phi(-np.pi/50)

    def draw_ejes(self):
        py.draw.line(self.canvas.canvas, 'blue', self.transformacion([-5, 0, 0]), self.transformacion([5, 0, 0]))
        py.draw.line(self.canvas.canvas, 'green', self.transformacion([0, -5, 0]), self.transformacion([0, 5, 0]))
        py.draw.line(self.canvas.canvas, 'white', self.transformacion([0, 0, -5]), self.transformacion([0, 0, 5]))

        py.draw.circle(self.canvas.canvas, 'blue', self.transformacion([5, 0, 0]), self.escala/10)
        py.draw.circle(self.canvas.canvas, 'green', self.transformacion([0, 5, 0]), self.escala/10)
        py.draw.circle(self.canvas.canvas, 'white', self.transformacion([0, 0, 5]), self.escala/10)
    
    def draw_curva(self, curva):
        color = curva.color
        info = curva.get_info()
        info = self.transformacion(info).transpose()
        self.interpolacion_lineal(info, color)

    def draw_superficie(self, superficie):
        color = superficie.color
        info = superficie.get_info()
        for vertice in info:
            vertice = self.transformacion(np.array(vertice).transpose()).transpose()
            py.draw.polygon(self.canvas.canvas, color, vertice)
            py.draw.polygon(self.canvas.canvas, 'black', vertice, 1)

    def draw(self, grafics):
        if self.visible:
            for superficie in grafics['Superficie3D']:
                self.draw_superficie(grafics['Superficie3D'][superficie])
            
            for superficie in grafics['SuperficieParametrica3D']:
                self.draw_superficie(grafics['SuperficieParametrica3D'][superficie])

            self.draw_ejes()
            
            for vector in grafics['Vector3D']:
                self.draw_vector(grafics['Vector3D'][vector])
            
            for point in grafics['Point3D']:
                self.draw_point(grafics['Point3D'][point])
            
            for campo in grafics['Campo3D']:
                self.draw_campo(grafics['Campo3D'][campo])
            
            for curva in grafics['Curva3D']:
                self.draw_curva(grafics['Curva3D'][curva])

class Vector2D:
    def __init__(self, vector, origen = (0,0), color = 'red', visible=True):
        self.vector = vector
        self.color=color
        self.origen = np.array(origen, dtype=float)
        self._coord_ = self.origen + self.vector.coord
        self.visible = visible
        self.info = self.load_info()

    def load_info(self):
        u = self.vector.unitario()*(-1/5)
        cola1 = true_rotacion2D(u.coord, np.pi/4) + self._coord_
        cola2 = true_rotacion2D(u.coord, -np.pi/4) + self._coord_
        return np.array([self.origen, self._coord_, cola1, cola2])
    
    def get_info(self):
        return self.info
    
    def __str__(self):
        return str(self.vector)

class Point2D:
    def __init__(self, coord, color='blue', visible=True):
        self.coord = np.array(coord, dtype=float)
        self.color = color
        self.visible = visible
    
    def get_info(self):
        return self.coord
    
    def __str__(self):
        return str(tuple(self.coord))

class Campo2D:
    def __init__(self, func, color='orange', visible=True):
        self.func = func
        self.color = color
        self.visible = visible
        self.info = self.load_info()
    
    def load_info(self):
        dom = cartesiano((-10, 10), (-10, 10), 21)
        result = []
        for i in range(len(dom)):
            v = dom[i]
            vector = self.func(v[0], v[1])
            
            if not (np.array(vector.coord, dtype=str) == 'nan').any() and (abs(np.array(vector.coord)).max()<1000).all():
                result.append(Vector2D(vector, v, self.color))
        return result
    
    def get_info(self):
        return self.info
    
    def __str__(self):
        return str(self.func)
        

class Vector3D(Vector2D):
    def __init__(self, vector, origen = (0,0,0), color = 'red'):
        super().__init__(vector, origen, color)

    def load_info(self):
        u = self.vector.unitario()*(-1/5)
        cola1 = true_rotacion3D(u.coord, np.pi/4, 0) + self._coord_
        cola2 = true_rotacion3D(u.coord, -np.pi/4, 0) + self._coord_
        return np.array([self.origen, self._coord_, cola1, cola2])

class Point3D(Point2D):
    def __init__(self, coord, color='blue'):
        super().__init__(coord, color)       

    
class Campo3D(Campo2D):
    def __init__(self, func, color='orange'):
        super().__init__(func, color)
    
    def load_info(self):
        dom = cartesiano3D((-5, 5), (-5, 5), (-5, 5), 11)
        result = []
        for i in range(len(dom)):
            v = dom[i]
            vector = self.func(v[0], v[1], v[2]).unitario()
            result.append(Vector3D(vector, v, self.color))
        return result

class Curva3D:
    def __init__(self, func, color='yellow', visible=True):
        self.func = func
        self.color = color
        self.visible = visible
        self.info = self.load_info()
    
    def load_info(self):
        dom = np.linspace(-50, 50, 1000)
        result = self.func(dom)
        mask = np.all((np.array(result, dtype=str)) != 'nan', axis=0)
        result = result[:, mask]
        return result
    
    def get_info(self):
        return self.info
    
    def __str__(self):
        return str(self.func)

class Superficie3D:
    def __init__(self, func, color='pink', mode='Cartesiano', visible=True, axis=1):
        self.func = func
        self.color = color
        self.mode = mode
        self.visible = visible
        self.axis = axis
        self.info = self.load_info()
        
    def load_info(self):
        rebanadas = 20
        rango = 3
        dom = gen_dom(self.mode, rebanadas, rango, self.axis)
        if self.mode == 'Esfera':
            dom = gen_dom(self.mode, rebanadas, rango, self.axis)
            p = self.func(*dom.transpose())
            points = np.column_stack((dom,p))
            move_column(points, self.axis)
            p = points[:, 2]
            theta = points[:, 0]
            phi = points[:, 1]
            z = p*np.cos(phi)
            r = p*np.sin(phi)
            x = r*np.cos(theta)
            y = r*np.sin(theta)
            dom = np.column_stack((x,y))
        elif self.mode == 'Cilindro':
            dom = gen_dom(self.mode, rebanadas, rango, self.axis)
            z = self.func(*dom.transpose())
            points = np.column_stack((dom,z))
            move_column(points, self.axis)
            r = points[:, 0]
            theta = points[:,1]
            z = points[:, 2]
            x = r*np.cos(theta)
            y = r*np.sin(theta)
            dom = np.column_stack((x,y))
        else:
            z = self.func(*dom.transpose())
            points = np.column_stack((dom,z))
            move_column(points, self.axis)
            z = points[:, 2]
            x = points[:, 0]
            y = points[:, 1]
            dom = np.column_stack((x,y))
        
        points = np.column_stack((dom,z))
        particiones = np.array(np.split(points, rebanadas))
        vertices = []
        for i in range(len(particiones)-1):
            for j in range(len(particiones[0])-1):
                vertice = [particiones[i,j], particiones[i,j+1], particiones[i+1,j+1], particiones[i+1,j]]
                if not (np.array(vertice, dtype=str) == 'nan').any() and (abs(np.array(vertice)).max()<1000).all():
                    vertices.append(vertice)
        return vertices
    
    def get_info(self):
        return self.info
    
    def __str__(self):
        return str(self.func)

class SuperficieParametrica3D(Superficie3D):
    def __init__(self, func, color='cyan'):
        super().__init__(func, color)
    
    def load_info(self):
        rebanadas = 30
        rango = (-3,3)
        dom = cartesiano(rango, rango, rebanadas)
        points = []

        for i in range(len(dom)):
            v = dom[i]
            vector = self.func(v[0], v[1])
            points.append(vector.coord)
        particiones = np.array(np.split(np.array(points), rebanadas))
        vertices = []
        for i in range(len(particiones)-1):
            for j in range(len(particiones[0])-1):
                vertice = [particiones[i,j], particiones[i,j+1], particiones[i+1,j+1], particiones[i+1,j]]
                if not (np.array(vertice, dtype=str) == 'nan').any() and (abs(np.array(vertice)).max()<1000).all():
                    vertices.append(vertice)
        return vertices