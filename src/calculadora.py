import numpy as np

class Calculadora:
    def __init__(self):
        self.constantes = {'e' : np.e, 'pi' : np.pi}

    def evaluar(self, expresion):
        #Evalua expresiones
        return eval(expresion, self.constantes)
    
    def add_constante(self, nombre, valor):
        #Agrega constantes
        self.constantes[nombre] = valor
    
    def delete_constante(self, nombre):
        #Elimina constantes
        del self.constantes[nombre]