from interfaz import *
from graficos import *
from vector import *
from calculadora import Calculadora
from funciones import *
from util import *
from comandos import *

py.init()
calculadora = Calculadora()
Funcion.calculadora = calculadora
Vector.calculadora = calculadora
Slider.calculadora = calculadora
Slider.update = update

size = (width, height) = (1300, 700)
manager = pyg.UIManager(size, 'config.json')

contain_canvas = Canvas(size, (0,0), 'pink', manager)

plano = Canvas((900, 600), (400,0), 'black', manager) 
input_canvas = Canvas((1300, 100), (0, 600), 'pink', manager)
info_canvas = Canvas((400, 530), (0, 70), 'cyan', manager)
config_canvas = Canvas((400, 70), (0, 0), 'pink', manager)

input_text = Input((500, 30), (150, 35))
input_color = Input((100, 30), (750, 35))
input_rango_var1 = Input((50, 30), (1200, 15))
input_rango_var2 = Input((50, 30), (1200, 55))

apply_button = Boton((100,30), (950, 35), 'Apply', apply)
curva_button = Boton((100,30), (0, 0), 'Curva', cargar_curva)
coord_button = Boton((110,30), (70, 0), 'Cartesiano', coord)
axis_button = Boton((80,30), (190, 0), 'Axis 1', axis)
dim_button = Boton((50,30), (10, 0), '3D', dim)
long_button = Boton((100,30), (280, 0), 'Default', magitud_vector)
flujo_button = Boton((100,30), (10, 35), 'Flujo', flujo)

label1 = Label((100,30),(50,35),"Funciones")
label2 = Label((100,30),(670,35),"Color")
label3 = Label((100,30),(1100,15),"Rango var1")
label4 = Label((100,30),(1100,55),"Rango var2")

input_canvas.add(input_text, input_color, input_rango_var1, input_rango_var2, apply_button, 
label1, label2, label3, label4,curva_button)
config_canvas.add(coord_button, dim_button, axis_button, long_button, flujo_button)


contain_canvas.add(plano, input_canvas, info_canvas, config_canvas)
g = Graficador2D(plano)
g.origen_pantalla = np.array(plano.size//2)

g3 = Graficador3D(plano)
g3.origen_pantalla = np.array(plano.size//2)

g3.escala = 50
g.escala = 50
g.set_visible(False)


ComandosCons.calculadora = calculadora
ComandosCons.info_canvas = info_canvas
ComandosCons.input_text = input_text
ComandosCons.input_color = input_color
ComandosCons.input_rango_var1 = input_rango_var1
ComandosCons.input_rango_var2 = input_rango_var2
ComandosCons.axis_button = axis_button
ComandosCons.coord_button = coord_button
ComandosCons.dim_button = dim_button
ComandosCons.long_button = long_button
ComandosCons.flujo_button = flujo_button
ComandosCons.g = g
ComandosCons.g3 = g3