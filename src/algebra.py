
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
    
