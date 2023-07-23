import numpy as np

class Algebraico:
        
    def nuevo_objeto(self):
        #Retorna un nuevo objeto de la propia clase
        pass

    def __str__(self):
        #Retorna una version str del objeto
        pass

    def suma(self, obj):
        #Se define la suma
        pass
    
    def mul(self, obj):
        #Se define la multiplicacion
        pass
    
    #-----Operaciones entre objetos algebráicos-----

    def __add__(self, obj): #Suma derecha-izquierda
        return self.suma(obj)
    
    def __radd__(self, obj): #Suma izquierda-derecha
        return self + obj
    
    def __sub__(self, obj): #Resta derehca-izquierda
        return self + (-1*obj) #La resta es la suma con el inverso de otro objeto
    
    def __rsub__(self, obj): #Resta izquierda-derecha
        return obj + (-1*self)
    
    def __mul__(self, obj): #Multiplicación derehca-izquierda
        pass

    def __rmul__(self, obj): #Multiplicación izquierda-derecha
        return self.__mul__(obj)

class Vector(Algebraico):
    calculadora = None
    def __init__(self, coord): #Inizializacion del vector
        if type(coord) == str:
            coord = Vector.calculadora.evaluar(coord)
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

class Parametro:
    def __init__(self, name, rango, velocidad, porcentaje=0.5):
        self.name = name
        self.rango = rango
        self.velocidad = velocidad
        self.set_porcentaje(porcentaje)
    
    def set_porcentaje(self,porcentaje):
        self.porcentaje = porcentaje
        self.valor = self.rango[0] + porcentaje*(self.rango[1] - self.rango[0])
        
    def __str__(self):
        return str(round(self.valor,2))