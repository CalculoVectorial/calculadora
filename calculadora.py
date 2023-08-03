import numpy as np
from funciones import *
from vector import Vector
from algebra import Parametro
from graficos import *
from funciones import *
from util import *

class Calculadora:
    def __init__(self):
        self.constantes = {'e' : np.e, 'pi' : np.pi}
        self.parametros = {}
        self.funciones = {'cos' : np.cos, 'sen': np.sin, 'tan': np.tan, 'sin' : np.sin, 'arccos': np.arccos, 'arcsen': np.arcsin,
        'arcsen': np.arcsin, 'arcsin': np.arcsin, 'arctan': np.arctan, 'csc': lambda x: 1/np.sin(x), 
        'sec': lambda x: 1/np.cos(x), 'arccsc': lambda x: np.arcsin(2/x), 'arcsec' : lambda x: np.arccos(1/x), 
        'cot' : lambda x: 1/np.tan(x), 'arccot': lambda x: np.pi/2 - np.arctan(x), 'ln' : np.log, 'Diff' : 4}
        self.grafics = {'Vector2D' : {}, 'Point2D' : {}, 'Campo2D' : {}, 'Vector3D' : {}, 
        'Point3D' : {}, 'Campo3D' : {}, 'Curva3D' : {}, 'Superficie3D' : {}, 
        'SuperficieParametrica3D': {}, 'Bola' : {}}
        self.locals = {}
        self.mode = 'Cartesiano'
        self.axis = 1
        self.vector_unitario = False
        self.tipo_campo = 'Flujo'
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
    
    def add_parametro(self, nombre, valor):
        #Agrega parametros
        self.parametros[nombre] = valor
        self.constantes[nombre] = valor.valor
        self.update()
    
    def add_funcion(self, nombre, valor):
        #Agrega funcion
        self.funciones[nombre] = valor
        self.update()
    
    def delete(self, nombre):
        #Elimina constantes o funciones
        if self.constantes.keys().__contains__(nombre):
            del self.constantes[nombre]
            del self.locals[nombre]
        
        if self.funciones.keys().__contains__(nombre):
            del self.funciones[nombre]
            del self.locals[nombre]
        
        if self.parametros.keys().__contains__(nombre):
            del self.parametros[nombre]

        self.delete_grafic(nombre)
        self.update()
   

    def delete_grafic(self, nombre):
        for tipo in self.grafics:
            if self.grafics[tipo].keys().__contains__(nombre):
                del self.grafics[tipo][nombre]

    def get_grafics(self):
        return self.grafics
    
    def get_parametros(self):
        return self.parametros
    
    def set_mode(self, mode):
        self.mode = mode
    
    def set_unitario(self, mode):
        self.vector_unitario = mode
    
    def set_axis(self, axis):
        self.axis = axis

    def gen_grafic(self, tipo, nombre, color, exp, rebanadas, long_vector, rango1, rango2):
            color = detectar_color(color)
            if rango1 != '':
                rango1 = np.array(self.evaluar(rango1))
            if rango2 != '':
                rango2 = np.array(self.evaluar(rango2))
            if tipo == 'Vector':
                obj = Vector(exp)
                if len(obj.coord) == 2:
                    grafic_obj = Vector2D(obj, color=color)
                    self.add_constante(nombre, obj)
                    self.grafics['Vector2D'][nombre] = grafic_obj
                elif len(obj.coord) == 3:
                    grafic_obj = Vector3D(obj, color=color)
                    self.add_constante(nombre, obj)
                    self.grafics['Vector3D'][nombre] = grafic_obj
            
            elif tipo == 'Point':
                obj = np.array(self.evaluar(exp))
                if len(obj) == 2:
                    grafic_obj = Point2D(obj, color=color)
                    self.add_constante(nombre, obj)
                    self.grafics['Point2D'][nombre] = grafic_obj
                elif len(obj) == 3:
                    grafic_obj = Point3D(obj, color=color)
                    self.add_constante(nombre, obj)
                    self.grafics['Point3D'][nombre] = grafic_obj
                
            
            elif tipo == 'Campo':
                exp = exp.split(';')
                if len(exp) == 2:
                    obj = FuncionVectorial(exp)
                    rebanadas = 1 + int(rebanadas*50)
                    grafic_obj = Campo2D(obj,rebanadas, long_vector, self.vector_unitario, color)
                    self.add_funcion(nombre, obj)
                    self.grafics['Campo2D'][nombre] = grafic_obj
                elif len(exp) == 3:
                    obj = FuncionVectorial(exp, ['x', 'y', 'z'])
                    rebanadas = 1 + int(rebanadas*50)
                    grafic_obj = Campo3D(obj,rebanadas, long_vector, self.vector_unitario, color)
                    self.add_funcion(nombre, obj)
                    self.grafics['Campo3D'][nombre] = grafic_obj
                
            
            elif tipo == 'Curva':
                exp = exp.split(';')
                obj = FuncionVectorial(exp, ['t'])
                rebanadas = 2 + int(rebanadas*2000)
                grafic_obj = Curva3D(obj, rebanadas, color)
                self.add_funcion(nombre, obj)
                self.grafics['Curva3D'][nombre] = grafic_obj
            
            elif tipo == 'Superficie':
                rango1, rango2 = ajustar_rango(rango1, rango2, self.mode, self.axis)
                obj = FuncionEscalar(exp)
                rebanadas = 2 + int(rebanadas*75)
                grafic_obj = Superficie3D(obj, rebanadas, rango1, rango2, color, self.mode, axis=self.axis)
                self.add_funcion(nombre, obj)
                self.grafics['Superficie3D'][nombre] = grafic_obj
            
            elif tipo == 'SuperficieParametrica':
                if rango1 == '':
                    rango1 = np.array([-3,3])
                if rango2 != '':
                    rango2 = np.array([-3,3])
                exp = exp.split(';')
                obj = FuncionVectorial(exp, ['u', 'v'])
                rebanadas = 2 + int(rebanadas*75)
                grafic_obj = SuperficieParametrica3D(obj, rebanadas, color)
                self.add_funcion(nombre, obj)
                self.grafics['SuperficieParametrica3D'][nombre] = grafic_obj
            
            elif tipo == 'Special':
                mode = 'Esfera'
                name, info, desplazamiento = info_special_sup(exp)
                if name in ['Esfera', 'Elipse', 'Hiperboloide1', 'Hiperboloide2', 'Cono']:
                    desplazamiento = np.array(self.evaluar(desplazamiento))
                    rebanadas = 2 + int(rebanadas*75)
                    grafic_obj = SuperficieCuadratica(name, rebanadas, info, desplazamiento,color)
                    self.grafics['SuperficieParametrica3D'][nombre] = grafic_obj
                
                elif name == 'Bola':
                    desplazamiento = np.array(self.evaluar(desplazamiento))
                    name_func = info[0]
                    pos = desplazamiento
                    bola = Bola(name_func, pos, color, self.tipo_campo)
                    self.grafics['Bola'][BOLANAME.pop(0)] = bola

                elif name == 'Diff':
                    if rango1 == '':
                        rango1 = np.array([-3,3])
                    if rango2 == '':
                        rango2 = np.array([-3,3])   
                    name_func = info[0]
                    var = desplazamiento
                    rebanadas = 2 + int(rebanadas*75)
                    if var == 'x':
                        obj = self.diff_x(name_func)
                        grafic_obj = Superficie3D(obj, rebanadas, rango1, rango2, color, self.mode, axis=self.axis)
                        self.add_funcion(nombre, obj)
                        self.grafics['Superficie3D'][nombre] = grafic_obj
                    elif var == 'y':
                        obj = self.diff_y(name_func)
                        grafic_obj = Superficie3D(obj, rebanadas, rango1, rango2, color, self.mode, axis=self.axis)
                        self.add_funcion(nombre, obj)
                        self.grafics['Superficie3D'][nombre] = grafic_obj
                    else:
                        var = np.array(self.evaluar(var))
                        obj = self.diff_u(var,name_func)
                        grafic_obj = Superficie3D(obj, rebanadas, rango1, rango2, color, self.mode, axis=self.axis)
                        self.add_funcion(nombre, obj)
                        self.grafics['Superficie3D'][nombre] = grafic_obj

                elif name == 'Grad':
                    if rango1 == '':
                        rango1 = np.array([-3,3])
                    if rango2 == '':
                        rango2 = np.array([-3,3])
                    rebanadas = 1 + int(rebanadas*50)
                    name_func = exp[exp.find('(')+1:-1]
                    dim = self.funciones[name_func].dim_dominio
                    obj = self.gradiente(name_func)
                    if dim==2:
                        self.add_funcion(nombre, obj)
                        grafic_obj = Campo2D(obj,rebanadas, long_vector, self.vector_unitario, color)
                        self.grafics['Campo2D'][nombre] = grafic_obj
                    elif dim==3:
                        self.add_funcion(nombre, obj)
                        grafic_obj = Campo2D(obj,rebanadas, long_vector, self.vector_unitario, color)
                        self.grafics['Campo3D'][nombre] = grafic_obj

                else:
                    desplazamiento = np.array(self.evaluar(desplazamiento))
                    nombre_parametro = info[0]
                    velocidad = float(info[1])
                    rango = desplazamiento.copy()
                    parametro = Parametro(nombre_parametro, rango, velocidad)
                    self.add_parametro(nombre_parametro, parametro)

    
    def diff_x(self, func):
        if isinstance(self.funciones[func], FuncionEscalar):
            dfunc = FuncionEscalar(f'({func}(x+0.000001,y) - {func}(x,y))/0.000001')
            dfunc.name=f'Dx({func})'
            return dfunc
        else:
            dfunc = FuncionVectorial([f'({func}(x+0.000001,y) - {func}(x,y))/0.000001'])
            dfunc.name=f'Dx({func})'
            return dfunc

    def diff_plus(self, func,var):
        if var == 'x':
            dfunc = FuncionVectorial([f'({func}(x+0.000001,y,z) - {func}(x,y,z))/0.000001'], ['x','y','z'])
        elif var == 'y':
            dfunc = FuncionVectorial([f'({func}(x,y+0.000001,z) - {func}(x,y,z))/0.000001'], ['x','y','z'])
        else:
            dfunc = FuncionVectorial([f'({func}(x,y,z+0.000001) - {func}(x,y,z))/0.000001'], ['x','y','z'])
        dfunc.name=f'Dx({func})'
        return dfunc
    
    def diff_y(self,func):
        if isinstance(self.funciones[func], FuncionEscalar):
            dfunc = FuncionEscalar(f'({func}(x,y+0.000001) - {func}(x,y))/0.000001')
            dfunc.name=f'Dy({func})'
            return dfunc
        else:
            dfunc = FuncionVectorial([f'({func}(x,y+0.000001) - {func}(x,y))/0.000001'])
            dfunc.name=f'Dy({func})'
            return dfunc
    
    def diff_z(self,func):
        if isinstance(self.funciones[func], FuncionEscalar):
            dfunc = FuncionEscalar(f'({func}(x,y,z+0.000001) - {func}(x,y,z))/0.000001')
            dfunc.name=f'Dz({func})'
            return dfunc

    
    def gradiente(self, func):
        if isinstance(self.funciones[func], FuncionEscalar):
            dim = self.funciones[func].dim_dominio
            if dim == 2:
                fx = self.diff_x(func)
                fy = self.diff_y(func)
                dfunc = FuncionVectorial([fx.expresion, fy.expresion])
                dfunc.name = f'grad({func})'
                return dfunc
            else:
                fx = self.diff_plus(func,'x')
                fy = self.diff_plus(func,'y')
                fz = self.diff_plus(func,'z')
                dfunc = FuncionVectorial([fx.expresion, fy.expresion,fz.expresion])
                dfunc.name = f'grad({func})'
                return dfunc

    def diff_u(self, v,func):
        u = np.array(v)/np.linalg.norm(v)
        if isinstance(self.funciones[func], FuncionEscalar):
            fx = self.diff_x(func)
            fy = self.diff_y(func)
            dfunc = FuncionEscalar(f'{fx.expresion}*{u[0]}+{fy.expresion}*{u[1]}')
            dfunc.name = f'Du({func}); {v}'
            return dfunc
        else:
            fx = self.diff_x(func)
            fy = self.diff_y(func)
            dfunc = FuncionVectorial([f'{fx.expresion}*{u[0]}+{fy.expresion}*{u[1]}'])
            dfunc.name = f'Du({func}); {v}'
            return dfunc




