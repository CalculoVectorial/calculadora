import numpy as np
import pygame as py, sys
from interfaz import *
from graficos import *
from vector import *
from calculadora import Calculadora
from funciones import *


def main():
    py.init()
    calculadora = Calculadora()
    Funcion.calculadora = calculadora
    Vector.calculadora = calculadora
    calculadora.add_constante('t', 5)
    
    size = (width, height) = (1300, 500)
    screen = py.display.set_mode(size)
    fps = 60
    clock = py.time.Clock()

    canvas = Canvas(size, (0,0), 'black') 
    g = Graficador2D()
    g.origen_pantalla = np.array(canvas.size//2)

    
    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit()
            
            canvas.py_event(event) #Detecta eventos del for event, esta línea es OBLIGATORIA

        canvas.click_event() #Detecta eventos de clicks para botones, esta línea es OBLIGATORIA
        
        screen.fill('black')
        canvas.draw(screen) #Se dibuja el canvas en el screen

        k = {'tipo':'Vector', 'nombre': 'v1', 'color': 'blue', 'exp': '[e,pi]', 'dim' : 2}
        calculadora.gen_grafic(**k)

        k2 = {'tipo':'Point', 'nombre': 'v2', 'color': 'red', 'exp': '(1,-1)', 'dim' : 2}
        calculadora.gen_grafic(**k2)
        
        k3 = {'tipo':'Campo', 'nombre': 'v3', 'color': 'orange', 'exp': 'y, -x', 'dim' : 2}
        calculadora.gen_grafic(**k3)
        
        g.draw(canvas, calculadora.get_grafics())
       
        
        py.display.flip()
        canvas.update(clock.tick(fps)) #Se actualiza el manager, esta línea es OBLIGATORIA

main()


