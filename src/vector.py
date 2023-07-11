import numpy as np
from algebra import Algebraico

class Vector(Algebraico):
    calculadora = None
    def __init__(self, coord): #Inizializacion del vector
        if isinstance(coord, Vector):
            self.coord = Vector.calculadora.evaluar(coord.coord)
        else:
            self.coord = np.array(coord, dtype=float)

    def nuevo_objeto(self, coord): #Override
        return Vector(coord)

    def suma(self, vector): #Override
        new_coord = self.coord + vector.coord
        return self.nuevo_objeto(new_coord)

    def mul(self, escalar): #Override
        new_coord = self.coord * escalar
        return self.nuevo_objeto(new_coord)

    def magnitud(self): #Magnitud del vector
        return np.linalg.norm(self.coord)

    def unitario(self): #Vector unitario
        magnitud = self.magnitud()
        if magnitud != 0:
            new_coord = self.coord / magnitud
        else:
             new_coord = self.coord
        return self.nuevo_objeto(new_coord)
    
    def punto(self, vector): #Producto punto
        return sum(self.coord * vector.coord)
    
    def __str__(self): #Override
        return str(self.coord)
    
    def __add__(self, vector): #Override
        return self.suma(vector)
    
    def __mul__(self, obj): #Override
        if isinstance(obj, Vector):
            return self.punto(obj)
        else:
            return self.mul(obj)
    
    def __truediv__(self, escalar): #Division para un escalar
        if escalar != 0:
            return self.mul(1/escalar)



    