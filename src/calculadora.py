import numpy as np
import sympy as sp
from funciones import *
from vector import Vector
from graficos import *
from funciones import *

class Calculadora:
    def __init__(self):
        self.constantes = {'e' : np.e, 'pi' : np.pi}
        self.funciones = {'cos' : np.cos, 'sen': np.sin, 'tan': np.tan}
        self.grafics = {'Vector2D' : {}, 'Point2D' : {}, 'Campo2D' : {}}
        self.locals = {'Vector' : Vector, 'FuncionVectorial': FuncionVectorial}
        self.update()

    def update(self):
        #Actualiza las variables locales de la calculadora
        self.locals.update(self.constantes)
        self.locals.update(self.funciones)

    def evaluar(self, expresion):
        #Evalua expresiones
        return eval(expresion, self.locals)
    
    def add_constante(self, nombre, valor):
        #Agrega constantes
        self.constantes[nombre] = valor
        self.update()
    
    def add_funcion(self, nombre, valor):
        #Agrega funcion
        self.funciones[nombre] = valor
        self.update()
    
    def delete_constante(self, nombre):
        #Elimina constantes
        del self.constantes[nombre]
        self.delete_grafic(nombre)
        self.update()
    
    def delete_funcion(self, nombre):
        #Elimina constantes
        del self.funciones[nombre]
        self.delete_grafic(nombre)
        self.update()

    def delete_grafic(self, nombre):
        for tipo in self.grafics:
            if self.grafics[tipo].keys().__contains__(nombre):
                del self.grafics[tipo][nombre]

    def get_grafics(self):
        return self.grafics

    def gen_grafic(self, tipo, nombre, color, exp, dim):
        if tipo == 'Vector':
            obj = self.evaluar(f'Vector({exp})')
            if dim == 2:
                grafic_obj = Vector2D(obj, color=color)
                self.add_constante(nombre, obj)
                self.grafics['Vector2D'][nombre] = grafic_obj
        
        if tipo == 'Point':
            if dim == 2:
                obj = np.array(self.evaluar(exp))
                grafic_obj = Point2D(obj, color=color)
                self.add_constante(nombre, obj)
                self.grafics['Point2D'][nombre] = grafic_obj
        
        if tipo == 'Campo':
            if dim == 2:
                exp = exp.split(',')
                obj = self.evaluar(f'FuncionVectorial({exp})')
                grafic_obj = Campo2D(obj, color)
                self.add_funcion(nombre, obj)
                self.grafics['Campo2D'][nombre] = grafic_obj
        
    