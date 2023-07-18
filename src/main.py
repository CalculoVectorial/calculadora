import numpy as np
import pygame as py, sys
from interfaz import *
from graficos import *
from vector import *
from calculadora import Calculadora
from funciones import *
from util import *

def mostrar_info():
    i=0
    for obj in info_canvas.objetos:
        if isinstance(obj, InfoLabel) or isinstance(obj, DeleteBoton):
            obj.kill()
    info_canvas.objetos.clear()
    for tipo_grafico in calculadora.get_grafics():
        for name_grafic in calculadora.get_grafics()[tipo_grafico]:
            grafic = calculadora.get_grafics()[tipo_grafico][name_grafic]
            info = InfoLabel((400, 60), (0,i*120), name_grafic, grafic)
            delete_boton = DeleteBoton((100, 30), (150, 90+120*i), name_grafic, command=delete)
            info_canvas.add(info, delete_boton)
            i+=1
    
def apply():
    try:
        text = input_text.get_text().replace(" ", "")
        color = input_color.get_text().replace(" ", "")
        input_text.clear()
        input_color.clear()
        if text != "":
            if '=' in text:
                name, exp = text.split('=')
                tipo = identificar_tipo_entrada(exp)
            else:
                exp = text
                tipo = identificar_tipo_entrada(exp)
                name = nombre_default(tipo)
            
            if color == '':
                color = 'orange'
            calculadora.gen_grafic(tipo, name, color, exp)
            mostrar_info()
    except:
        pass
    

def delete(name):
    calculadora.delete(name)
    for obj in info_canvas.objetos:
        if isinstance(obj, InfoLabel) or isinstance(obj, DeleteBoton):
            if obj.name == name:
                obj.kill()
                mostrar_info()

def axis():
    if axis_button.text == 'Axis 1':
        axis_button.set_text('Axis 2')
        calculadora.set_axis(2)
    
    elif axis_button.text == 'Axis 2':
        axis_button.set_text('Axis 3')
        calculadora.set_axis(3)
    else:
        axis_button.set_text('Axis 1')
        calculadora.set_axis(1)

def coord():
    if coord_button.text == 'Cartesiano':
        coord_button.set_text('Esfera')
        calculadora.set_mode('Esfera')

    elif coord_button.text == 'Esfera':
        coord_button.set_text('Cilindro')
        calculadora.set_mode('Cilindro')
    
    else:
        coord_button.set_text('Cartesiano')
        calculadora.set_mode('Cartesiano')

def dim():
    if dim_button.text == '2D':
        dim_button.set_text('3D')
        g.set_visible(False)
        g3.set_visible(True)
    else:
        dim_button.set_text('2D')
        g3.set_visible(False)
        g.set_visible(True)



py.init()
calculadora = Calculadora()
Funcion.calculadora = calculadora
Vector.calculadora = calculadora
size = (width, height) = (1300, 700)
screen = py.display.set_mode(size)
fps = 60
clock = py.time.Clock()

manager = pyg.UIManager(size, 'config.json')

contain_canvas = Canvas(size, (0,0), 'pink', manager)

plano = Canvas((900, 600), (400,0), 'black', manager) 
input_canvas = Canvas((1300, 100), (0, 600), 'pink', manager)
info_canvas = Canvas((400, 550), (0, 50), 'cyan', manager)
config_canvas = Canvas((400, 50), (0, 0), 'pink', manager)

input_text = Input((500, 30), (250, 35))
input_color = Input((100, 30), (850, 35))
slider = Slider((100, 30), (10,10), 0, 10)

apply_button = Boton((100,30), (250, 0), 'Apply', apply)
coord_button = Boton((120,30), (100, 0), 'Cartesiano', coord)
axis_button = Boton((100,30), (240, 0), 'Axis 1', axis)
dim_button = Boton((50,30), (30, 0), '3D', dim)



input_canvas.add(input_text, input_color, apply_button, slider)
config_canvas.add(coord_button, dim_button, axis_button)


contain_canvas.add(plano, input_canvas, info_canvas, config_canvas)
g = Graficador2D(plano)
g.origen_pantalla = np.array(plano.size//2)

g3 = Graficador3D(plano)
g3.origen_pantalla = np.array(plano.size//2)

g3.escala = 50
g.escala = 50
g.set_visible(False)



while True:
    pressed = py.mouse.get_pressed()
    mouse = py.mouse.get_rel()
    pos = py.mouse.get_pos()
    for event in py.event.get():
        if event.type == py.QUIT:
            sys.exit()
        
        if event.type == py.MOUSEWHEEL:
            g.zoom(event, pos)
            g3.zoom(event, pos)
        g.mouse_event(pressed, mouse, pos)
        g3.mouse_event(pressed, mouse, pos)
        manager.process_events(event) #Detecta eventos del for event, esta línea es OBLIGATORIA
                
    contain_canvas.click_event(pressed, mouse, pos)  #Detecta eventos de clicks para botones, esta línea es OBLIGATORIA
        
    screen.fill('black')
    contain_canvas.draw(screen) #Se dibuja el canvas en el screen
   
    g3.draw(calculadora.get_grafics())
    g.draw(calculadora.get_grafics())
    py.display.flip()
    manager.update(clock.tick(fps)/600) #Se actualiza el manager, esta línea es OBLIGATORIA
        



