import numpy as np
import pygame as py
from util import *
from vector import Vector
from funciones import *
from comandos import update, cargar_curva

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
                self.escala += self.escala/20  
            elif event.y == -1 and self.escala > 2:
                self.escala -= self.escala/20     

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
        py.draw.circle(self.canvas.canvas, color, info, 5)
        py.draw.circle(self.canvas.canvas, 'white', info, 5, 1)
    
    def draw_campo(self, campo):
        color = campo.color
        info = campo.get_info()
        for vector in info:
            self.draw_vector(vector)
    
    def interpolacion_lineal(self, points, color):
        py.draw.lines(self.canvas.canvas, color, False, points)
    
    def draw_bola(self, bola):
        bola.move()
        info = bola.get_info().transpose()
        info = self.transformacion(info).transpose()
        color = bola.color
        self.interpolacion_lineal(info, color)
        py.draw.circle(self.canvas.canvas, "blue", info[-1],5)
        py.draw.circle(self.canvas.canvas, "white", info[-1],5,1)
    
class Graficador2D(Graficador):
    def __init__(self, canvas, escala=50):
        super().__init__(2, canvas, escala)
        self.prueba_curva = False
    
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
        borde_x = int(self.canvas.size[0]//(2*self.escala) + 2)
        borde_y = borde_x
        for i in range(1, borde_x):
            py.draw.line(self.canvas.canvas, (50,50,50), self.transformacion([i,-borde_y]), self.transformacion([i,borde_y]))
            py.draw.line(self.canvas.canvas, (50,50,50), self.transformacion([-i,-borde_y]), self.transformacion([-i,borde_y]))

        for j in range(1, borde_y):
            py.draw.line(self.canvas.canvas, (50,50,50), self.transformacion([-borde_x, j]), self.transformacion([borde_x, j]))
            py.draw.line(self.canvas.canvas, (50,50,50), self.transformacion([-borde_x, -j]), self.transformacion([borde_x, -j]))

    def draw(self, grafics):
        try:
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

                for bola in grafics['Bola']:
                    bola = grafics['Bola'][bola]
                    if bola.dim == 2:
                        self.draw_bola(bola)
                if self.prueba_curva:
                    datos = cargar_curva()
                    datos = self.transformacion(datos.transpose()).transpose()
                    self.interpolacion_lineal(datos,"orange")
        except:
            pass


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
                if self.theta>2*np.pi:
                    self.theta = 0
                
            if mouse[0] > 0 and self.get_visible():
                self.set_theta(-np.pi/50)
                if self.theta<0:
                    self.theta = 2*np.pi

        
        if pressed[2] and self.canvas.rect.collidepoint(pos):
            if mouse[1] < 0 and self.get_visible():
                self.set_phi(np.pi/50)
                if self.phi>2*np.pi:
                    self.phi = 0

            if mouse[1] > 0 and self.get_visible():
                self.set_phi(-np.pi/50)
                if self.phi<0:
                    self.phi = 2*np.pi

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
        if np.pi/2<self.theta<3*np.pi/2 and superficie.mode == 'Cartesiano':
            info = info[::-1] 
        if (0<self.phi<np.pi/2 or 3*np.pi/2<self.phi<2*np.pi) and superficie.mode == 'Esfera':
            info = info[::-1]  
        for vertice in info:
            vertice = self.transformacion(np.array(vertice).transpose()).transpose()
            py.draw.polygon(self.canvas.canvas, color, vertice)
            py.draw.polygon(self.canvas.canvas, 'black', vertice, 1)

    def draw(self, grafics):
        try:
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
                
                for bola in grafics['Bola']:
                    bola = grafics['Bola'][bola]
                    if bola.dim == 3:
                        self.draw_bola(bola)
        except:
            pass

class Vector2D:
    def __init__(self, vector, origen = (0,0), color = 'red', visible=True):
        self.str_vector = vector
        self.vector = Vector(self.str_vector)
        self.color=color
        self.origen = np.array(origen, dtype=float)
        self._coord_ = self.origen + self.vector.coord
        self.visible = visible
        self.info = self.load_info()


    def load_info(self):
        self.vector = Vector(self.str_vector)
        self._coord_ = self.origen + self.vector.coord
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
        self.str_coord = coord
        self.coord = np.array(Funcion.calculadora.evaluar(self.str_coord), dtype=float)
        self.color = color
        self.visible = visible
        self.info = self.load_info()
 
    def load_info(self):
        self.coord = np.array(Funcion.calculadora.evaluar(self.str_coord), dtype=float)
        return self.coord
    
    def get_info(self):
        return self.info
    
    def __str__(self):
        return str(tuple(self.coord.round(2)))

class Campo2D:
    def __init__(self, func, rebanadas, long_vector, unitario=False,color='orange', visible=True):
        self.func = func
        self.color = color
        self.visible = visible
        self.rebanadas = rebanadas
        self.long = long_vector
        self.unitario = unitario
        self.p = 0.3
        self.info = self.load_info()
    
    def load_info(self):
        self.func.update()
        dom = cartesiano((-10, 10), (-10, 10), self.rebanadas)
        result = []
        for i in range(len(dom)):
            v = dom[i]
            if self.unitario:
                vector = self.func(v[0], v[1]).unitario()
            else:
                vector = self.func(v[0], v[1])
            
            vector *= self.long
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
    def __init__(self, func, rebanadas, long_vector, unitario,color='orange'):
        super().__init__(func, rebanadas, long_vector, unitario,color)
    
    def load_info(self):
        self.func.update()
        dom = cartesiano3D((-5, 5), (-5, 5), (-5, 5), self.rebanadas//2)
        result = []
        for i in range(len(dom)):
            v = dom[i]
            if self.unitario:
                vector = self.func(v[0], v[1], v[2]).unitario()
            else:
                vector = self.func(v[0], v[1], v[2])
            vector *= self.long
            result.append(Vector3D(vector, v, self.color))
        return result

class Curva3D:
    def __init__(self, func, rebanadas, color='yellow', visible=True):
        self.func = func
        self.color = color
        self.visible = visible
        self.rebanadas = rebanadas
        self.p = 0.3
        self.info = self.load_info()
    
    def load_info(self):
        self.func.update()
        dom = np.linspace(-50, 50, self.rebanadas)
        result = self.func(dom)
        mask = np.all((np.array(result, dtype=str)) != 'nan', axis=0)
        result = result[:, mask]
        mask = np.all((np.array(result, dtype=str)) != 'inf', axis=0)
        result = result[:, mask]
        return result
    def get_info(self):
        return self.info
    
    def __str__(self):
        return str(self.func)

class Superficie3D:
    def __init__(self, func, rebanadas, rango1, rango2, color='pink', mode='Cartesiano', visible=True, axis=1):
        self.func = func
        self.color = color
        self.mode = mode
        self.visible = visible
        self.axis = axis
        self.rebanadas = rebanadas
        self.rango1 = rango1
        self.rango2 = rango2
        self.p = 0.3
        self.info = self.load_info()
        
    def load_info(self):
        self.func.update()
        dom = cartesiano(self.rango1, self.rango2, self.rebanadas)
        if self.mode == 'Esfera':
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
        particiones = np.array(np.split(points, self.rebanadas))
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
    def __init__(self, func, rebanadas, rango1, rango2,color='cyan'):
        super().__init__(func, rebanadas, rango1, rango2,color)
    
    def load_info(self):
        self.func.update()
        dom = cartesiano(self.rango1, self.rango2, self.rebanadas)
        points = []

        for i in range(len(dom)):
            v = dom[i]
            vector = self.func(v[0], v[1])
            points.append(vector.coord)
        particiones = np.array(np.split(np.array(points), self.rebanadas))
        vertices = []
        for i in range(len(particiones)-1):
            for j in range(len(particiones[0])-1):
                vertice = [particiones[i,j], particiones[i,j+1], particiones[i+1,j+1], particiones[i+1,j]]
                if not (np.array(vertice, dtype=str) == 'nan').any() and (abs(np.array(vertice)).max()<1000).all():
                    vertices.append(vertice)
        return vertices

class SuperficieCuadratica(Superficie3D):
    def load_info(self):
            return super().load_info() + self.desplazamiento

    def __init__(self, name, rebanadas, info, desplazamiento,color='pink', visible=True):
        self.desplazamiento = desplazamiento
        if len(info) == 1:
            r = Funcion.calculadora.evaluar(info[0])
            lbda = f"(abs({r**2})*sen(y)*cos(x))"
            alpha = f"(abs({r**2})*sen(y)*sen(x))"
            beta = f"(abs({r**2})*cos(y))"
            num = f'abs({r**3})'
        else:
            a,b,c=Funcion.calculadora.evaluar(",".join(info))
            lbda = f"(abs({b*c})*sen(y)*cos(x))"
            alpha = f"(abs({a*c})*sen(y)*sen(x))"
            beta = f"(abs({a*b})*cos(y))"
            num = f'abs({a*b*c})'

        if name == 'Esfera':
            func = FuncionEscalar(f'abs({r})')
            super().__init__(func, rebanadas, (0, 2*np.pi), (0, np.pi), color, 'Esfera', visible,1)
        
        elif name == 'Elipsoide':
            den = f'({lbda}**2 + {alpha}**2 + {beta}**2)'
            func = FuncionEscalar(f'{num}/{den}**0.5')
            super().__init__(func, rebanadas, (0, 2*np.pi), (0, np.pi), color, 'Esfera', visible,1)
        
        elif name == 'Hiperboloide1':
            den = f'({lbda}**2 + {alpha}**2 - {beta}**2)'
            func = FuncionEscalar(f'{num}/{den}**0.5')
            super().__init__(func, rebanadas, (0, 2*np.pi), (0, np.pi), color, 'Esfera', visible,1)
        
        elif name == 'Hiperboloide2':
            den = f'(-{lbda}**2 - {alpha}**2 + {beta}**2)'
            func = FuncionEscalar(f'{num}/{den}**0.5')
            super().__init__(func, rebanadas, (0, 2*np.pi), (0, np.pi), color, 'Esfera', visible,1)
        
        elif name == 'Cono':
            func = FuncionEscalar(str(r))
            super().__init__(func, rebanadas, (0, 2*np.pi), (-5, 5), color, 'Esfera', visible,2)
        self.info = self.load_info()
        self.func.name= f'{name}({",".join(info)},{tuple(desplazamiento)})'
        
        

    
class Bola:
    def __init__(self, func, pos, color, tipo, masa=None):
        self.func = Funcion.calculadora.funciones[func]
        self.pos = np.array(pos, dtype=float)
        self.dim = len(self.pos)
        self.registro_pos = [pos]
        self.registro_vel = [np.array([0,0])]
        self.h=0.00005
        self.color = color
        self.tipo=tipo
      
        self.w = 0
        
        self.info = self.get_info()

    def move(self):
        if self.tipo=='Flujo':
            for x in range(500):
                vi = self.func(*self.pos).coord
                dr =  self.h*vi
                self.pos += dr
            self.registro_pos.append(self.pos.copy())
            vi = self.func(*self.registro_pos[-1]).coord
            v0 = self.func(*self.registro_pos[0]).coord
            self.w=0.5*(np.linalg.norm(vi)**2 - np.linalg.norm(v0)**2)

        elif self.tipo == 'Fuerza':
            for x in range(500):
                a = self.func(*self.pos).coord
                vi = self.registro_vel[-1] + self.h*a
                self.registro_vel.append(vi)
                dr = self.h*vi
                self.pos += dr
            self.registro_pos.append(self.pos.copy())
            self.w=0.5*(np.linalg.norm(vi)**2 - np.linalg.norm(self.registro_vel[0])**2)
        update()
    
    def load_info(self):
        self.get_info()
        
    def get_info(self):
        return np.array(self.registro_pos)
    
    def get_trabajo(self):
        return round(self.w,2)

    def __str__(self):
        return str(self.get_trabajo())
    

    
