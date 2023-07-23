import numpy as np
from util import *
from vector import Vector

class Funcion:
    calculadora = None

    def __init__(self, expresion, variables):
        self.expresion = expresion
        self.variables = np.array(variables)
        self.dim_dominio = len(variables) 

    def __call__(self, *args): #Al llamar a la funcion f(x) se puede evaluar de 4 maneras distintas
        isnt_arr = np.array(list(map(lambda x: isinstance(x, np.ndarray), args)))
        if isnt_arr.any(): #Nota: los vectores de las matrices deben estar en fila
            if is_desempaquetado(args):
                args = empaquetar(args)
            else:
                args = args[0]
            return self.evaluar_array(args)
        elif isinstance(args[0], Vector):
            return self.evaluar(args[0].coord)
        else:
            return self.evaluar(args)
    
    def __str__(self): #Override
        return str(self.expresion)


class FuncionEscalar(Funcion):
    calculadora = Funcion.calculadora

    def __init__(self, expresion, variables=['x', 'y']):
        super().__init__([expresion], variables)
        self.expresion = expresion
        self.func = Funcion.calculadora.evaluar(f'lambda {",".join(self.variables)}: {self.expresion}')
        #Expresion lambda sigue la estructura lambda: variables: expresion
        
    def evaluar(self, args): #Evalua la funcion con argumentos
        return self.func(*np.array(args))

    def evaluar_array(self, args): #Evalua la funcion con argumentos arrays
        if len(self.variables) > 1:
            result =  self.func(*args)
        else:
            result = self.func(args)
        if not isinstance(result, np.ndarray):
            result = np.full(len(args[0]), result)
        return result

    def update(self):
        self.func = Funcion.calculadora.evaluar(f'lambda {",".join(self.variables)}: {self.expresion}')
    

class FuncionVectorial(Funcion):
    def __init__(self, expresion, variables=['x', 'y']):
        super().__init__(expresion, variables)
        self.funciones_coordenadas = np.array([FuncionEscalar(expresion, self.variables) for expresion in self.expresion])
        if len(self.expresion) == 1:
            self.func = Funcion.calculadora.evaluar(f'lambda {",".join(self.variables)}: {",".join(self.expresion)}')
        else:
            self.func = Funcion.calculadora.evaluar(f'lambda {",".join(self.variables)}: [{",".join(self.expresion)}]')
        
    def nuevo_objeto(self, expresion, variables): #Override
        return FuncionVectorial(expresion, variables)
    
    def evaluar(self, args): #Evalua la funcion con argumentos
        return Vector(self.func(*np.array(args)))
    
    def evaluar_array(self, args): #Evalua la funcion con argumentos arrays
        if len(self.variables) > 1:
            result = self.func(*args)
        else:
            result = self.func(args)

        for i in range(len(result)):
            if np.array(result[i]).size == 1:
                if len(self.variables) >1:
                    result[i] = np.full(len(args[0]), result[i])
                else:
                    result[i] = np.full(len(args), result[i])
        return np.array(result)
    
    def update(self):
        if len(self.expresion) == 1:
            self.func = Funcion.calculadora.evaluar(f'lambda {",".join(self.variables)}: {",".join(self.expresion)}')
        else:
            self.func = Funcion.calculadora.evaluar(f'lambda {",".join(self.variables)}: [{",".join(self.expresion)}]')

